# Grant Review LLM System

This system uses Large Language Models (LLMs) to automatically review grant applications based on structured criteria. It has been adapted from your existing AI ethics processor to work specifically with School of Health Professions Research Seed Grant applications.

## 🎯 What's Been Implemented

### Core Features
- **Multi-LLM Support**: Works with OpenAI GPT, Google Gemini, Anthropic Claude, and GROK
- **Grant Application Processing**: Automatically combines all 4 components (biosketches, budget, coverpage, project) 
- **Structured Review**: Uses 6-criteria evaluation system with JSON scoring output
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
```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Test the System
```bash
# Run the test suite to verify everything works
python test_grant_processor.py
```

### 3. Process Grant Applications

#### Review a Single Applicant
```bash
# Review Daniel's application with OpenAI
python scripts/grant_review_processor.py --model openai --applicant Daniel

# Review with multiple iterations for reliability
python scripts/grant_review_processor.py --model openai --applicant Daniel --iterations 3
```

#### Review All Applicants
```bash
# Review all applications with all available models
python scripts/grant_review_processor.py --model all

# Review all with specific model
python scripts/grant_review_processor.py --model claude --iterations 2
```

## 📊 Current Grant Applications

The system found **4 complete grant applications**:
- **Daniel**: Lyme Disease Curricular Trends & Differential Diagnosis in Physical Therapy
- **Christina**: [View in `llm/scenarios/Christina/`]
- **Kelly**: [View in `llm/scenarios/Kelly/`] 
- **Rosie**: [View in `llm/scenarios/Rosie/`]

Each application includes all required components:
- `biosketches.md` - Researcher backgrounds
- `budget.md` - Financial breakdown
- `coverpage.md` - Basic application info
- `project.md` - Detailed research proposal

## 📁 Output Structure

### File Outputs (`outputs/` directory)
```
outputs/
├── Daniel_OpenAI_gpt-4_iter1.json
├── Daniel_OpenAI_gpt-4_iter2.json
├── Christina_Claude_claude-3-opus_iter1.json
└── ...
```

### Database Storage
```sql
-- Main review record
SELECT applicant_name, vendor, model, overall_recommendation, processing_time 
FROM grant_reviews;

-- Individual criterion scores  
SELECT gr.applicant_name, grc.criterion_name, grc.score, grc.rationale
FROM grant_reviews gr
JOIN grant_review_criteria grc ON gr.id = grc.grant_review_id;
```

## 🔧 System Architecture

### Key Components
1. **GrantReviewProcessor** (`scripts/grant_review_processor.py`)
   - Main processing engine
   - LLM API integration
   - Response parsing and storage

2. **Database Adapter** (`shared/db_adapter.py`)
   - SQLite and Supabase support
   - Grant-specific schema
   - Backward compatibility

3. **Review Instructions** (`llm/prompts/LLM_Grant_Review_Instructions.md`)
   - Standardized scoring criteria
   - JSON output format specification

### Key Improvements from Original
- ✅ **Grant-specific data model** instead of ethics case structure
- ✅ **Component combination** - merges all 4 grant parts into single review
- ✅ **JSON score parsing** with fallback to text analysis
- ✅ **Structured database schema** for grant reviews
- ✅ **Optional dependencies** - works without all LLM packages installed
- ✅ **Individual applicant processing** option
- ✅ **Comprehensive test suite**

## 📈 Example Usage Workflow

1. **Initial Setup**
   ```bash
   python test_grant_processor.py  # Verify system works
   ```

2. **Test with One Applicant**
   ```bash
   python scripts/grant_review_processor.py --model openai --applicant Daniel
   ```

3. **Review Output**
   ```bash
   # Check the JSON output
   cat outputs/Daniel_OpenAI_gpt-4_iter1.json
   
   # Check database
   sqlite3 data/results.db "SELECT * FROM grant_reviews WHERE applicant_name='Daniel';"
   ```

4. **Process All Applications**
   ```bash
   python scripts/grant_review_processor.py --model all --iterations 2
   ```

5. **Generate Summary Statistics**
   ```bash
   python scripts/grant_review_processor.py --model all
   # View logs for summary stats at the end
   ```

## 🛠 Troubleshooting

### Missing Dependencies
The system gracefully handles missing packages:
- **OpenAI**: `pip install openai`
- **Gemini**: `pip install google-generativeai` 
- **Claude**: `pip install anthropic`
- **GROK**: Uses standard requests (included)

### API Key Issues
- Check `.env` file exists and has correct keys
- Verify API keys are active and have sufficient credits
- Test with single model first: `--model openai`

### Database Issues
- Database auto-creates on first run
- Located at `data/results.db` by default
- Can switch to Supabase by changing `DB_TYPE` in `.env`

## 📝 Next Steps

1. **Set up API keys** in `.env` file
2. **Run test** to verify installation: `python test_grant_processor.py`
3. **Process a single applicant** first: `--applicant Daniel`
4. **Scale to all applications** when ready: `--model all`
5. **Analyze results** in database and output files

Example:

- To run only `Daniel` with `openAi` 3 times
```sh
python scripts/grant_review_processor.py --model openai --applicant Daniel --iterations 3
```

- To run all people, with `openAi` 5 times 
```sh
python scripts/grant_review_processor.py --model openai --iterations 5
```



The system is ready to use and will save both raw LLM responses and structured review data for analysis!