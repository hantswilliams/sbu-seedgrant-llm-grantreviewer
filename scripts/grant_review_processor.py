#!/usr/bin/env python3
"""
Grant Review LLM Processor

This script connects to LLMs (ChatGPT, Google Gemini, Anthropic Claude, and GROK)
to review grant applications and stores the results in a SQLite database.

Usage:
    python grant_review_processor.py [--model MODEL] [--iterations ITERATIONS] [--cleanup]

Options:
    --model MODEL          Specify which model to use: 'openai', 'gemini', 'claude', 'grok', or 'all' (default)
    --iterations ITERATIONS Number of iterations per grant application (default: 1)
    --cleanup              Clean up the database by fixing any incorrect vendor names
"""

import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
import logging
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import database adapter
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.db_adapter import get_db_adapter

# Third-party packages for API access (import as needed)
try:
    import openai
except ImportError:
    openai = None

try:
    from google.generativeai import GenerativeModel, configure
    import google.generativeai as genai
except ImportError:
    GenerativeModel = None
    configure = None
    genai = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("grant_review_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("grant_reviewer")

class GrantReviewProcessor:
    def __init__(self, base_path=None, openai_api_key=None, gemini_api_key=None, claude_api_key=None, grok_api_key=None, db_path=None):
        """
        Initialize the Grant Review Processor
        
        Args:
            base_path: Path to the project root
            openai_api_key: OpenAI API key (if None, will look for OPENAI_API_KEY env var)
            gemini_api_key: Google Gemini API key (if None, will look for GEMINI_API_KEY env var)
            claude_api_key: Anthropic Claude API key (if None, will look for CLAUDE_API_KEY env var)
            grok_api_key: GROK API key (if None, will look for GROK_API_KEY env var)
            db_path: Custom path to database (if None, will use the configured adapter)
        """
        # Set base path
        if base_path is None:
            self.base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        else:
            self.base_path = Path(base_path)
        
        # Initialize API clients
        self._init_openai(openai_api_key)
        self._init_gemini(gemini_api_key)
        self._init_claude(claude_api_key)
        self._init_grok(grok_api_key)
        
        # Setup database
        self.db_adapter = get_db_adapter()
        self.db_adapter.init_db()
        logger.info(f"Using {self.db_adapter.type} database")
        
        # Load grant review instructions
        self.review_instructions = self._load_grant_review_instructions()
        
        # Scan for grant applications
        self.grant_applications = self._scan_grant_applications()
        logger.info(f"Found {len(self.grant_applications)} grant applications")
        
        # Create outputs directory
        self.outputs_dir = self.base_path / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

    def _init_openai(self, api_key=None):
        """Initialize OpenAI client"""
        if openai is None:
            self.openai_client = None
            logger.warning("OpenAI package not installed. OpenAI functionality will be disabled.")
            return
            
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY")
        
        if api_key and api_key != "dummy":
            self.openai_client = openai.OpenAI(api_key=api_key)
            model_name = os.environ.get("OPENAI_MODEL", "gpt-4")
            logger.info(f"OpenAI client initialized with model {model_name}")
        else:
            self.openai_client = None
            logger.warning("OpenAI API key not found. OpenAI functionality will be disabled.")

    def _init_gemini(self, api_key=None):
        """Initialize Google Gemini client"""
        if GenerativeModel is None or configure is None:
            self.gemini_model = None
            logger.warning("Google Gemini package not installed. Gemini functionality will be disabled.")
            return
            
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        
        if api_key and api_key != "dummy":
            configure(api_key=api_key)
            # Get model name from environment variable or use default
            model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
            self.gemini_model = GenerativeModel(model_name)
            logger.info(f"Google Gemini client initialized with model {model_name}")
        else:
            self.gemini_model = None
            logger.warning("Google Gemini API key not found. Gemini functionality will be disabled.")

    def _init_claude(self, api_key=None):
        """Initialize Anthropic Claude client"""
        try:
            import anthropic
            
            if api_key is None:
                api_key = os.environ.get("CLAUDE_API_KEY")
            
            if api_key and api_key != "dummy":
                self.claude_client = anthropic.Anthropic(api_key=api_key)
                # Get model name from environment variable or use default
                model_name = os.environ.get("CLAUDE_MODEL", "claude-3-opus-20240229")
                self.claude_model_name = model_name
                logger.info(f"Anthropic Claude client initialized with model {model_name}")
            else:
                self.claude_client = None
                logger.warning("Claude API key not found. Claude functionality will be disabled.")
        except ImportError:
            logger.error("Anthropic package not installed. Please install with 'pip install anthropic'")
            self.claude_client = None

    def _init_grok(self, api_key=None):
        """Initialize GROK client"""
        try:
            if api_key is None:
                api_key = os.environ.get("GROK_API_KEY")
            
            if api_key and api_key != "dummy":
                self.grok_api_key = api_key
                model_name = os.environ.get("GROK_MODEL", "grok-1")
                self.grok_model_name = model_name
                logger.info(f"GROK client initialized with model {model_name}")
            else:
                self.grok_api_key = None
                logger.warning("GROK API key not found. GROK functionality will be disabled.")
        except Exception as e:
            logger.error(f"Error initializing GROK client: {e}")
            self.grok_api_key = None

    def _load_grant_review_instructions(self):
        """Load the grant review instructions from the prompts directory"""
        instructions_path = self.base_path / "llm" / "prompts" / "LLM_Grant_Review_Instructions.md"
        try:
            with open(instructions_path, 'r') as f:
                instructions = f.read()
                logger.info(f"Loaded grant review instructions from {instructions_path}")
                return instructions
        except Exception as e:
            logger.error(f"Error loading grant review instructions: {e}")
            raise

    def _scan_grant_applications(self):
        """Scan for grant applications in the scenarios directory"""
        scenarios_dir = self.base_path / "llm" / "scenarios"
        grant_applications = []
        
        # Required components for each grant application
        required_components = ["biosketches.md", "budget.md", "coverpage.md", "project.md"]
        
        for applicant_dir in scenarios_dir.iterdir():
            if applicant_dir.is_dir():
                applicant_name = applicant_dir.name
                components = {}
                
                # Check if all required components exist
                all_components_exist = True
                for component in required_components:
                    component_path = applicant_dir / component
                    if component_path.exists():
                        components[component.split('.')[0]] = component_path
                    else:
                        logger.warning(f"Missing component {component} for applicant {applicant_name}")
                        all_components_exist = False
                
                if all_components_exist:
                    grant_applications.append({
                        "applicant_name": applicant_name,
                        "components": components
                    })
                    logger.info(f"Found complete grant application for {applicant_name}")
                else:
                    logger.warning(f"Incomplete grant application for {applicant_name} - skipping")
        
        return sorted(grant_applications, key=lambda x: x["applicant_name"])

    def _load_grant_components(self, grant_application):
        """Load all components of a grant application"""
        applicant_name = grant_application["applicant_name"]
        components = grant_application["components"]
        
        combined_content = f"# Grant Application for {applicant_name}\n\n"
        
        # Load each component in a specific order
        component_order = ["coverpage", "project", "biosketches", "budget"]
        
        for component_name in component_order:
            if component_name in components:
                try:
                    with open(components[component_name], 'r') as f:
                        content = f.read()
                        combined_content += f"## {component_name.title()}\n\n{content}\n\n"
                except Exception as e:
                    logger.error(f"Error loading {component_name} for {applicant_name}: {e}")
                    raise
        
        return combined_content

    def _build_full_prompt(self, grant_content):
        """Build the full prompt by combining the review instructions and grant content"""
        full_prompt = f"{self.review_instructions}\n\n## Grant Application to Review:\n\n{grant_content}"
        return full_prompt

    def query_openai(self, prompt):
        """Query the OpenAI API with the given prompt"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Get model name from environment variable or use default
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4")
        
        start_time = time.time()
        try:
            response = self.openai_client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an expert grant reviewer for the School of Health Professions Research Seed Grant program."},
                    {"role": "user", "content": prompt}
                ],
                                max_completion_tokens=4000
            )
            processing_time = time.time() - start_time
            
            # Extract model version from response if available
            model_version = response.model
            
            return response.choices[0].message.content, processing_time, model_name, model_version
        except Exception as e:
            logger.error(f"Error querying OpenAI: {e}")
            raise

    def query_gemini(self, prompt):
        """Query the Google Gemini API with the given prompt"""
        if not self.gemini_model:
            raise ValueError("Gemini model not initialized")
        
        # Get the model name from environment or use default
        model_name = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
        
        start_time = time.time()
        try:
            response = self.gemini_model.generate_content(prompt)
            processing_time = time.time() - start_time
            
            # Get model version if available, otherwise use the model name
            try:
                model_version = response.candidates[0].safety_ratings[0].model_version if hasattr(response, 'candidates') else model_name
            except (AttributeError, IndexError):
                model_version = model_name
                
            return response.text, processing_time, model_name, model_version
        except Exception as e:
            logger.error(f"Error querying Gemini: {e}")
            raise

    def query_claude(self, prompt):
        """Query the Anthropic Claude API with the given prompt"""
        if not self.claude_client:
            raise ValueError("Claude client not initialized")
        
        model_name = self.claude_model_name
        
        start_time = time.time()
        try:
            response = self.claude_client.messages.create(
                model=model_name,
                max_completion_tokens=4000,
                                messages=[
                    {"role": "user", "content": prompt}
                ],
                system="You are an expert grant reviewer for the School of Health Professions Research Seed Grant program."
            )
            processing_time = time.time() - start_time
            
            # Extract model version
            model_version = response.model
            
            return response.content[0].text, processing_time, model_name, model_version
        except Exception as e:
            logger.error(f"Error querying Claude: {e}")
            raise

    def query_grok(self, prompt):
        """Query the GROK API with the given prompt"""
        if not self.grok_api_key:
            raise ValueError("GROK API key not initialized")
        
        import requests
        
        model_name = self.grok_model_name
        
        # GROK API endpoint
        url = "https://api.x.ai/v1/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.grok_api_key}"
        }
        
        data = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "You are an expert grant reviewer for the School of Health Professions Research Seed Grant program."},
                {"role": "user", "content": prompt}
            ],
                        "max_completion_tokens": 4000
        }
        
        start_time = time.time()
        try:
            response = requests.post(url, headers=headers, json=data, verify=True, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            processing_time = time.time() - start_time
            
            # Extract content and model version
            content = result["choices"][0]["message"]["content"]
            model_version = result.get("model", model_name)
            
            return content, processing_time, model_name, model_version
        except Exception as e:
            logger.error(f"Error querying GROK: {e}")
            raise

    def _extract_review_scores(self, response_text):
        """Extract the review scores and recommendation from the response text"""
        # First try to parse as raw JSON (common with newer models)
        try:
            # Try parsing the entire response as JSON first
            review_data = json.loads(response_text.strip())
            if isinstance(review_data, dict):
                return {
                    "scores": review_data.get("scores", []),
                    "overall_recommendation": review_data.get("OverallRecommendation", "Not specified"),
                    "parsed_successfully": True
                }
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON in markdown code blocks
        json_pattern = r'```json\s*(.*?)\s*```'
        json_match = re.search(json_pattern, response_text, re.DOTALL)
        
        # If no markdown JSON found, try to find JSON at the start of response
        if not json_match:
            # Look for JSON array that starts the response
            array_pattern = r'^\s*(\[.*?\]),?\s*"?OverallRecommendation"?\s*:\s*"([^"]+)"'
            array_match = re.search(array_pattern, response_text, re.DOTALL)
            if array_match:
                try:
                    json_str = array_match.group(1)
                    overall_rec = array_match.group(2)
                    review_data = json.loads(json_str)
                    
                    return {
                        "scores": review_data,
                        "overall_recommendation": overall_rec,
                        "parsed_successfully": True
                    }
                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse array JSON: {e}")
        
        if json_match:
            try:
                json_str = json_match.group(1)
                # Parse the JSON
                review_data = json.loads(json_str)
                
                # Validate the structure
                if isinstance(review_data, list) and len(review_data) >= 1:
                    # Extract scores array and overall recommendation
                    scores = review_data
                    overall_recommendation = "Not specified"
                    
                    # Look for OverallRecommendation in the response
                    recommendation_pattern = r'"OverallRecommendation":\s*"([^"]+)"'
                    rec_match = re.search(recommendation_pattern, response_text)
                    if rec_match:
                        overall_recommendation = rec_match.group(1)
                    
                    return {
                        "scores": scores,
                        "overall_recommendation": overall_recommendation,
                        "parsed_successfully": True
                    }
                elif isinstance(review_data, dict):
                    # Handle case where response is a dict with scores and recommendation
                    return {
                        "scores": review_data.get("scores", []),
                        "overall_recommendation": review_data.get("OverallRecommendation", "Not specified"),
                        "parsed_successfully": True
                    }
                else:
                    logger.warning("JSON structure doesn't match expected format")
                    return self._manual_extract_scores(response_text)
                    
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON from response: {e}")
        
        # If no JSON found or parsing failed, try to extract manually
        logger.info("No valid JSON found, attempting manual extraction")
        return self._manual_extract_scores(response_text)

    def _manual_extract_scores(self, response_text):
        """Manually extract scores if JSON parsing fails"""
        # Look for criterion scores in text format
        criteria_patterns = {
            "Innovation and Impact": r"Innovation and Impact.*?(\d+)",
            "Methodological Approach and Feasibility": r"Methodological Approach.*?(\d+)",
            "Strength of Research Team": r"Strength of Research Team.*?(\d+)",
            "Potential to Attract External Funding": r"Potential.*?External Funding.*?(\d+)",
            "Clarity and Efficiency of Budget": r"Budget.*?(\d+)",
            "Overall Presentation": r"Overall Presentation.*?(\d+)"
        }
        
        extracted_scores = []
        for criterion, pattern in criteria_patterns.items():
            match = re.search(pattern, response_text, re.IGNORECASE | re.DOTALL)
            if match:
                try:
                    score = int(match.group(1))
                    extracted_scores.append({
                        "Criterion": criterion,
                        "Score": score,
                        "Rationale": "Extracted from text analysis"
                    })
                except ValueError:
                    pass
        
        # Look for overall recommendation
        recommendation_patterns = [
            r"Overall Recommendation.*?:\s*([^.\n]+)",
            r"Recommendation.*?:\s*([^.\n]+)",
            r"(Fund|Do Not Fund|Fund with Revisions)"
        ]
        
        overall_recommendation = "Unable to parse"
        for pattern in recommendation_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                overall_recommendation = match.group(1).strip()
                break
        
        return {
            "scores": extracted_scores,
            "overall_recommendation": overall_recommendation,
            "parsed_successfully": False,
            "raw_response": response_text
        }

    def save_response(self, applicant_name, vendor, model, model_version, iteration, prompt, response, processing_time):
        """Save a response to the database and output file"""
        # Extract review scores from response
        review_data = self._extract_review_scores(response)
        
        # Save to database
        conn = self.db_adapter.get_connection()
        
        try:
            # Use the new grant_reviews table if available
            if hasattr(self.db_adapter, 'insert_grant_review'):
                grant_review_id = self.db_adapter.insert_grant_review(
                    conn,
                    applicant_name,
                    vendor,
                    model,
                    model_version,
                    iteration,
                    datetime.now().isoformat(),
                    prompt,
                    response,
                    json.dumps(review_data.get("scores", [])),
                    review_data.get("overall_recommendation", ""),
                    processing_time
                )
                
                # Insert individual criterion scores if available
                if hasattr(self.db_adapter, 'insert_grant_review_criterion'):
                    total_score = 0
                    for score_item in review_data.get("scores", []):
                        if isinstance(score_item, dict) and "Criterion" in score_item:
                            score = score_item.get("Score", 0)
                            total_score += score if score is not None else 0
                            
                            self.db_adapter.insert_grant_review_criterion(
                                conn,
                                grant_review_id,
                                applicant_name,
                                score_item.get("Criterion", ""),
                                score,
                                score_item.get("Rationale", "")
                            )
                    
                    # Insert total score as a special criterion
                    if total_score > 0:
                        self.db_adapter.insert_grant_review_criterion(
                            conn,
                            grant_review_id,
                            applicant_name,
                            "TOTAL_SCORE",
                            total_score,
                            f"Total score across all {len(review_data.get('scores', []))} criteria"
                        )
            else:
                # Fallback to old responses table for backward compatibility
                response_id = self.db_adapter.insert_response(
                    conn,
                    applicant_name,  # Using applicant_name as case_id equivalent
                    f"{applicant_name}_grant_application",  # scenario_filename equivalent
                    vendor,
                    model,
                    model_version,
                    iteration,
                    datetime.now().isoformat(),
                    prompt,
                    response,
                    json.dumps(review_data.get("scores", [])),  # Store scores as JSON string
                    review_data.get("overall_recommendation", ""),
                    "",  # Not using least_recommended for grants
                    processing_time
                )
        
        except Exception as e:
            logger.error(f"Error saving to database: {e}")
            # Continue with file save even if database save fails
        
        finally:
            self.db_adapter.close_connection(conn)
        
        # Save to output file
        self._save_output_file(applicant_name, vendor, model, iteration, review_data, response)
        
        logger.info(f"Saved review for {applicant_name}, {vendor} {model} ({model_version}), iteration {iteration}")

    def _save_output_file(self, applicant_name, vendor, model, iteration, review_data, raw_response):
        """Save review output to a JSON file"""
        output_data = {
            "applicant_name": applicant_name,
            "reviewer_info": {
                "vendor": vendor,
                "model": model,
                "iteration": iteration,
                "timestamp": datetime.now().isoformat()
            },
            "review_data": review_data,
            "raw_response": raw_response
        }
        
        filename = f"{applicant_name}_{vendor}_{model}_iter{iteration}.json"
        output_path = self.outputs_dir / filename
        
        try:
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            logger.info(f"Saved output file: {output_path}")
        except Exception as e:
            logger.error(f"Error saving output file {output_path}: {e}")

    def process_grant_application(self, grant_application, model="all", iterations=1):
        """Process a single grant application through the specified model(s)"""
        applicant_name = grant_application["applicant_name"]
        grant_content = self._load_grant_components(grant_application)
        full_prompt = self._build_full_prompt(grant_content)
        
        # Convert legacy "both" parameter to "all" for backward compatibility
        if model == "both":
            model = "all"
            
        logger.info(f"Processing grant application for {applicant_name} with model(s): {model}")
        
        if model in ["openai", "all"] and self.openai_client:
            for i in range(1, iterations + 1):
                logger.info(f"Running OpenAI iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version = self.query_openai(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="OpenAI",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=full_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in OpenAI processing for {applicant_name}: {e}")
        
        if model in ["gemini", "all"] and self.gemini_model:
            for i in range(1, iterations + 1):
                logger.info(f"Running Gemini iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version = self.query_gemini(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="Google",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=full_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in Gemini processing for {applicant_name}: {e}")
                    
        if model in ["claude", "all"] and self.claude_client:
            for i in range(1, iterations + 1):
                logger.info(f"Running Claude iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version = self.query_claude(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="Anthropic",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=full_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in Claude processing for {applicant_name}: {e}")
                    
        if model in ["grok", "all"] and self.grok_api_key:
            for i in range(1, iterations + 1):
                logger.info(f"Running GROK iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version = self.query_grok(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="GROK",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=full_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in GROK processing for {applicant_name}: {e}")

    def process_all_applications(self, model="all", iterations=1):
        """Process all available grant applications"""
        logger.info(f"Starting processing of {len(self.grant_applications)} grant applications with {model} model(s), {iterations} iteration(s) each")
        for grant_application in self.grant_applications:
            self.process_grant_application(grant_application, model, iterations)
        logger.info("Completed processing all grant applications")

    def generate_summary_stats(self):
        """Generate summary statistics from the database"""
        conn = self.db_adapter.get_connection()
        cursor = conn.cursor()
        
        # Try to use grant_reviews table first, fall back to responses
        try:
            # Count by vendor from grant_reviews
            cursor.execute("SELECT vendor, COUNT(*) FROM grant_reviews GROUP BY vendor")
            vendor_counts = cursor.fetchall()
            
            # Count by specific model from grant_reviews
            cursor.execute("SELECT vendor, model, COUNT(*) FROM grant_reviews GROUP BY vendor, model")
            model_counts = cursor.fetchall()
            
            # Count by applicant from grant_reviews
            cursor.execute("SELECT applicant_name, COUNT(*) FROM grant_reviews GROUP BY applicant_name")
            applicant_counts = cursor.fetchall()
            
            # Average processing time by vendor from grant_reviews
            cursor.execute("SELECT vendor, AVG(processing_time) FROM grant_reviews GROUP BY vendor")
            vendor_avg_times = cursor.fetchall()
            
        except Exception as e:
            logger.warning(f"Error querying grant_reviews table, falling back to responses: {e}")
            # Fallback to responses table
            cursor.execute("SELECT vendor, COUNT(*) FROM responses GROUP BY vendor")
            vendor_counts = cursor.fetchall()
            
            cursor.execute("SELECT vendor, model, COUNT(*) FROM responses GROUP BY vendor, model")
            model_counts = cursor.fetchall()
            
            cursor.execute("SELECT case_id, COUNT(*) FROM responses GROUP BY case_id")
            applicant_counts = cursor.fetchall()
            
            cursor.execute("SELECT vendor, AVG(processing_time) FROM responses GROUP BY vendor")
            vendor_avg_times = cursor.fetchall()
        
        self.db_adapter.close_connection(conn)
        
        # Convert to dictionaries based on adapter type
        if self.db_adapter.type == "sqlite":
            vendor_counts_dict = dict(vendor_counts)
            applicant_counts_dict = dict(applicant_counts)
            vendor_avg_times_dict = dict(vendor_avg_times)
            model_counts_list = model_counts
        else:
            # PostgreSQL returns dictionaries, we need to extract the values
            vendor_counts_dict = {row['vendor']: row['count'] for row in vendor_counts}
            applicant_counts_dict = {row['case_id']: row['count'] for row in applicant_counts}
            vendor_avg_times_dict = {row['vendor']: row['avg'] for row in vendor_avg_times}
            model_counts_list = [(row['vendor'], row['model'], row['count']) for row in model_counts]
        
        # Calculate total count
        total_count = sum(vendor_counts_dict.values())
        
        logger.info("Grant Review Summary Statistics:")
        logger.info(f"Total reviews: {total_count}")
        logger.info(f"By vendor: {vendor_counts_dict}")
        logger.info(f"By model: {model_counts_list}")
        logger.info(f"By applicant: {applicant_counts_dict}")
        logger.info(f"Average processing times by vendor: {vendor_avg_times_dict}")
        
        return {
            "vendor_counts": vendor_counts_dict,
            "model_counts": {f"{vendor}_{model}": count for vendor, model, count in model_counts_list},
            "applicant_counts": applicant_counts_dict,
            "vendor_avg_times": vendor_avg_times_dict
        }


def main():
    parser = argparse.ArgumentParser(description='Process grant applications through AI models for review')
    parser.add_argument('--model', choices=['openai', 'gemini', 'claude', 'grok', 'all'], default='all',
                        help='Which model provider to use: openai, gemini, claude, grok, or all')
    parser.add_argument('--iterations', type=int, default=1,
                        help='Number of iterations per grant application')
    parser.add_argument('--applicant', type=str, default=None,
                        help='Process only a specific applicant (optional)')
    args = parser.parse_args()
    
    try:
        processor = GrantReviewProcessor()
        
        if args.applicant:
            # Process only the specified applicant
            matching_applications = [app for app in processor.grant_applications 
                                   if app["applicant_name"].lower() == args.applicant.lower()]
            if matching_applications:
                processor.process_grant_application(matching_applications[0], model=args.model, iterations=args.iterations)
            else:
                logger.error(f"No grant application found for applicant: {args.applicant}")
                return
        else:
            # Process all applications
            processor.process_all_applications(model=args.model, iterations=args.iterations)
        
        processor.generate_summary_stats()
        logger.info("Grant review processing completed successfully")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()