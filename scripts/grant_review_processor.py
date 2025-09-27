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

# Import LLM connectors
try:
    # Try relative import first (when used as a module)
    from .connectors import OpenAIConnector, GoogleConnector, GrokConnector, AnthropicConnector
except ImportError:
    # Fall back to direct import (when run as script)
    from connectors import OpenAIConnector, GoogleConnector, GrokConnector, AnthropicConnector

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
        
        # Load grant review instructions first
        self.review_instructions = self._load_grant_review_instructions()

        # Initialize LLM connectors with the review instructions
        self.openai_connector = OpenAIConnector(openai_api_key, base_path=self.base_path, instructions=self.review_instructions)
        self.google_connector = GoogleConnector(gemini_api_key, base_path=self.base_path, instructions=self.review_instructions)
        self.grok_connector = GrokConnector(grok_api_key, base_path=self.base_path, instructions=self.review_instructions)
        self.anthropic_connector = AnthropicConnector(claude_api_key, base_path=self.base_path, instructions=self.review_instructions)
        
        # Setup database
        self.db_adapter = get_db_adapter()
        self.db_adapter.init_db()
        logger.info(f"Using {self.db_adapter.type} database")
        
        
        # Scan for grant applications
        self.grant_applications = self._scan_grant_applications()
        logger.info(f"Found {len(self.grant_applications)} grant applications")
        
        # Create outputs directory
        self.outputs_dir = self.base_path / "outputs"
        self.outputs_dir.mkdir(exist_ok=True)

    def _init_openai(self, api_key=None):
        """Legacy method - OpenAI is now handled by OpenAIConnector"""
        # This method is kept for compatibility but functionality moved to OpenAIConnector
        self.openai_client = self.openai_connector.client if self.openai_connector.is_available() else None

    def _init_gemini(self, api_key=None):
        """Legacy method - Gemini is now handled by GoogleConnector"""
        # This method is kept for compatibility but functionality moved to GoogleConnector
        self.gemini_model = self.google_connector.client if self.google_connector.is_available() else None


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
        """Build the full prompt with grant content (instructions are handled by connectors)"""
        full_prompt = f"## Grant Application to Review:\n\n{grant_content}"
        return full_prompt

    def query_openai(self, prompt):
        """Query the OpenAI API using the OpenAI connector"""
        if not self.openai_connector.is_available():
            raise ValueError("OpenAI connector not available")

        return self.openai_connector.query(prompt)

    def query_gemini(self, prompt):
        """Query the Google Gemini API using the Google connector"""
        if not self.google_connector.is_available():
            raise ValueError("Google connector not available")

        return self.google_connector.query(prompt)

    def query_grok(self, prompt):
        """Query the Grok API using the Grok connector"""
        if not self.grok_connector.is_available():
            raise ValueError("Grok connector not available")

        return self.grok_connector.query(prompt)

    def query_claude(self, prompt):
        """Query the Anthropic Claude API using the Anthropic connector"""
        if not self.anthropic_connector.is_available():
            raise ValueError("Anthropic connector not available")

        return self.anthropic_connector.query(prompt)


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
        
        if model in ["openai", "all"] and self.openai_connector.is_available():
            for i in range(1, iterations + 1):
                logger.info(f"Running OpenAI iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version, actual_prompt = self.query_openai(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="OpenAI",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=actual_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in OpenAI processing for {applicant_name}: {e}")
        
        if model in ["gemini", "all"] and self.google_connector.is_available():
            for i in range(1, iterations + 1):
                logger.info(f"Running Gemini iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version, actual_prompt = self.query_gemini(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="Google",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=actual_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in Gemini processing for {applicant_name}: {e}")

        if model in ["grok", "all"] and self.grok_connector.is_available():
            for i in range(1, iterations + 1):
                logger.info(f"Running Grok iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version, actual_prompt = self.query_grok(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="xAI",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=actual_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in Grok processing for {applicant_name}: {e}")

        if model in ["claude", "all"] and self.anthropic_connector.is_available():
            for i in range(1, iterations + 1):
                logger.info(f"Running Claude iteration {i}/{iterations} for {applicant_name}")
                try:
                    response, processing_time, model_name, model_version, actual_prompt = self.query_claude(full_prompt)
                    self.save_response(
                        applicant_name=applicant_name,
                        vendor="Anthropic",
                        model=model_name,
                        model_version=model_version,
                        iteration=i,
                        prompt=actual_prompt,
                        response=response,
                        processing_time=processing_time
                    )
                    # Add delay to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error in Claude processing for {applicant_name}: {e}")
                    

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
    parser.add_argument('--model', choices=['openai', 'gemini', 'grok', 'claude', 'all'], default='all',
                        help='Which model provider to use: openai, gemini, grok, claude, or all')
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