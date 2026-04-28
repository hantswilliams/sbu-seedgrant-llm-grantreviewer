# Grant Review LLM System

This system uses Large Language Models (LLMs) to automatically review grant applications based on structured criteria. 

## 🎯 What's Been Implemented

### Core Features
- **Multi-LLM Support**: Works with OpenAI GPT, Google Gemini, Anthropic Claude, and GROK
- **Grant Application Processing**: Automatically combines all 4 components (biosketches, budget, coverpage, project)
- **Structured Review**: Uses 6-criteria evaluation system with JSON scoring output
- **Prompt Experiments**: Track and compare different prompt variations for analysis
- **Database Storage**: SQLite database with dedicated grant review tables
- **File Outputs**: JSON files for each review in the `outputs/` directory
- **Flexible Processing**: Can process all applicants or individual ones

### Database Schema
- `grant_reviews`: Main review records with metadata and overall scores
- `grant_review_criteria`: Individual criterion scores and rationales  
- `responses`: Legacy table for backward compatibility

### Review Criteria (from LLM_Grant_Review_Instructions.md)
1. **Innovation and Impact** - Novelty, originality, significance
2. **Methodological Approach and Feasibility** - Quality, rigor, feasibility
3. **Strength of Research Team** - Qualifications, track record
4. **Potential to Attract External Funding** - Future grant potential
5. **Clarity and Efficiency of Budget** - Cost-effectiveness, alignment
6. **Overall Presentation** - Writing quality, organization

## 🚀 Quick Start

### 1. Setup Environment

**Option A: 1Password (recommended for team members)**

Prerequisites:
- [1Password CLI](https://developer.1password.com/docs/cli/get-started/) installed (`brew install --cask 1password-cli`)
- 1Password desktop app unlocked (enables biometric auth for CLI)
- Access to the "Developer Projects" vault

```bash
# Generate .env from 1Password
./scripts/generate-env.sh

# Print to stdout (for piping or inspection)
./scripts/generate-env.sh --stdout

# Diff current .env against 1Password (dry-run)
./scripts/generate-env.sh --check
```

The script pulls all values from the `sbu-seedgrant-llm-grantreviewer-env` secure note in 1Password and writes `.env` with `chmod 600`.

**Option B: Manual setup**

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. 🧪 Prompt Experiments

The system supports **prompt experiments** to test different prompt variations and compare their results.

### Understanding Experiments

Prompts are stored in `llm/prompts/` with a `config.json` file that tracks:
- **Active experiment**: Which prompt is used by default
- **Experiment metadata**: Name, version, description, and file path for each prompt

### Creating a New Prompt Experiment

1. **Create your new prompt file** in `llm/prompts/`:
   ```bash
   # Copy the baseline as a starting point
   cp llm/prompts/baseline_v1.md llm/prompts/with_training_data_v1.md

   # Edit the new prompt file with your changes
   nano llm/prompts/with_training_data_v1.md
   ```

2. **Register the experiment** in `llm/prompts/config.json`:
   ```json
   {
     "active_experiment": "baseline_v1",
     "experiments": {
       "baseline_v1": {
         "file": "baseline_v1.md",
         "version": "1.0",
         "description": "Original prompt without training examples"
       },
       "with_training_data_v1": {
         "file": "with_training_data_v1.md",
         "version": "2.0",
         "description": "Prompt enhanced with training data examples"
       }
     }
   }
   ```

### 3. Process Grant Applications

#### Example Workflow

```bash
# Step 1a: Run baseline experiment prompt with grok and gemeni for baseline 
python scripts/grant_review_processor.py --model grok --experiment baseline_v1 --iterations 3
python scripts/grant_review_processor.py --model gemini --experiment baseline_v1 --iterations 3
python scripts/grant_review_processor.py --model openai --experiment baseline_v1 --iterations 3


# Step 1b: Run with training data experiment prompt with grok and gemeni 
python scripts/grant_review_processor.py --model grok --experiment with_training_data_v1 --iterations 3
python scripts/grant_review_processor.py --model gemini --experiment with_training_data_v1 --iterations 3
python scripts/grant_review_processor.py --model openai --experiment with_training_data_v1 --iterations 3


# Step 1c: Run with training data with multiple examples promptexperiment with grok and gemeni 
python scripts/grant_review_processor.py --model grok --experiment multi_examples_v1 --iterations 3
python scripts/grant_review_processor.py --model gemini --experiment multi_examples_v1 --iterations 3
python scripts/grant_review_processor.py --model openai --experiment multi_examples_v1 --iterations 3


# Step 1d: Run with training data with strict scoring prompt experiment with grok and gemeni 
python scripts/grant_review_processor.py --model grok --experiment strict_scoring_v1 --iterations 3
python scripts/grant_review_processor.py --model gemini --experiment strict_scoring_v1 --iterations 3
python scripts/grant_review_processor.py --model openai --experiment strict_scoring_v1 --iterations 3



```

#### Other examples: 
```bash
# Use specific experiment
python scripts/grant_review_processor.py --model all --experiment with_training_data_v1

# Or set it as active in config.json and run without --experiment flag
python scripts/grant_review_processor.py --model all

# Review Daniel's application with OpenAI
python scripts/grant_review_processor.py --model openai --applicant Daniel

# Review with multiple iterations for reliability
python scripts/grant_review_processor.py --model openai --applicant Daniel --iterations 3

# Review all applications with all available models
python scripts/grant_review_processor.py --model all

# Review all with specific model
python scripts/grant_review_processor.py --model claude --iterations 2
```

### 4. Import Human Reviews and Combine with Newly Created LLMs so assessable via Flask app
```bash
# Import human reviewed grant scores into the database
# This must be done BEFORE running AI comparisons
python combine_reviews.py
```

#### Comparing Experiments

All reviews are tagged with their experiment name and version in the database. You can:

1. **View experiment metadata** in the database:
   ```sql
   SELECT DISTINCT prompt_experiment_name, prompt_version, COUNT(*) as review_count
   FROM grant_reviews
   GROUP BY prompt_experiment_name, prompt_version;
   ```

2. **Compare experiments via API**:
   ```bash
   curl http://localhost:5004/api/experiment_comparison
   ```

3. **Filter by experiment** in the Flask web interface (see `/api/experiments` endpoint)

### Step 5: Compare results in the web interface
python app.py
# Navigate to http://localhost:5004 and use the experiment comparison tools
```

