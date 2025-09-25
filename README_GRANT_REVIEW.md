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

### 2. Import Human Reviews (Required First Step)
```bash
# Import human reviewed grant scores into the database
# This must be done BEFORE running AI comparisons
python combine_reviews.py
```

### 3. Test the System
```bash
# Run the test suite to verify everything works
python test_grant_processor.py
```

### 4. Process Grant Applications

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
   - Orchestrates LLM connectors
   - Response parsing and storage

2. **LLM Connectors** (`scripts/connectors/`)
   - **BaseConnector**: Abstract base class for all providers
   - **OpenAIConnector**: OpenAI GPT models integration
   - **GoogleConnector**: Google Gemini models integration
   - Modular, extensible architecture

3. **Database Adapter** (`shared/db_adapter.py`)
   - SQLite and Supabase support
   - Grant-specific schema
   - Backward compatibility

4. **Review Instructions** (`llm/prompts/LLM_Grant_Review_Instructions.md`)
   - Standardized scoring criteria
   - JSON output format specification

5. **Human-AI Comparison** (`combine_reviews.py`)
   - Imports human reviewer scores from CSV
   - Creates unified comparison database
   - Generates summary statistics

6. **Flask Web Interface** (`app.py`)
   - Web-based result viewing and analysis
   - Real-time charts and comparisons
   - Export functionality

### Key Improvements from Original
- ✅ **Grant-specific data model** instead of ethics case structure
- ✅ **Component combination** - merges all 4 grant parts into single review
- ✅ **JSON score parsing** with fallback to text analysis
- ✅ **Structured database schema** for grant reviews
- ✅ **Modular connector architecture** - separate connectors for each LLM provider
- ✅ **Optional dependencies** - works without all LLM packages installed
- ✅ **Individual applicant processing** option
- ✅ **Comprehensive test suite**
- ✅ **Human-AI comparison workflow** via combine_reviews.py
- ✅ **Flask web interface** for easy access to results
- ✅ **Docker containerization** for deployment

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

## 🌐 Web Interface

A Flask web application provides an easy-to-use interface for viewing grant review results.

### Starting the Web Interface
```bash
# Run the Flask application
python app.py

# Access the interface at http://localhost:5000
```

### Features
- View all grant applications and their reviews
- Compare human vs AI reviewer scores
- Export results in various formats
- Interactive charts and statistics
- Real-time processing status

## 🐳 Docker Deployment

### Build and Run with Docker
```bash
# Build the Docker image
docker build -t grant-reviewer .

# Run the container
docker run -p 5000:5000 -v $(pwd)/data:/app/data grant-reviewer

# Access the web interface at http://localhost:5000
```

### Docker Features
- Self-contained environment with all dependencies
- Persistent data storage via volume mounts
- Easy deployment to cloud platforms
- Consistent runtime across different systems

## 📊 Human-AI Comparison Workflow

### Step 1: Import Human Reviews
```bash
# Place human reviewer scores in inputs/human_scores.csv
# Run the combination script to import into database
python combine_reviews.py
```

### Step 2: Generate AI Reviews
```bash
# Process applications with AI models
python scripts/grant_review_processor.py --model all --iterations 3
```

### Step 3: Compare Results
```bash
# Start web interface to view comparisons
python app.py
# Or query the combined_reviews table directly
```

### Data Flow
1. **Human scores** (CSV) → `inputs/human_scores.csv`
2. **Import script** → `combine_reviews.py`
3. **Database storage** → `data/results.db` (`combined_reviews` table)
4. **AI processing** → `grant_review_processor.py`
5. **Web visualization** → `app.py` Flask interface

## 🛠 Troubleshooting

### Missing Dependencies
The system gracefully handles missing packages:
- **OpenAI**: `pip install openai`
- **Gemini**: `pip install google-generativeai`
- **Claude**: `pip install anthropic`
- **GROK**: Uses standard requests (included)
- **Flask**: `pip install flask` (for web interface)

### API Key Issues
- Check `.env` file exists and has correct keys
- Verify API keys are active and have sufficient credits
- Test with single model first: `--model openai`

### Database Issues
- Database auto-creates on first run
- Located at `data/results.db` by default
- Can switch to Supabase by changing `DB_TYPE` in `.env`

### Human Review Import Issues
- Ensure `inputs/human_scores.csv` exists and has correct format
- Run `combine_reviews.py` before comparing with AI results
- Check column names match expected format in the CSV

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