"""
Database adapter for the AI Ethics Research project.
Supports both SQLite and Supabase PostgreSQL databases.
"""

import os
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables from root .env file
load_dotenv(dotenv_path=Path(__file__).parent.parent / '.env')

logger = logging.getLogger("ai_ethics.db")

class DatabaseAdapter:
    """Base class for database adapters"""
    def __init__(self):
        self.type = None
        
    def get_connection(self):
        """Get a database connection"""
        raise NotImplementedError("Subclasses must implement get_connection()")
        
    def init_db(self):
        """Initialize database tables"""
        raise NotImplementedError("Subclasses must implement init_db()")

    def close_connection(self, conn):
        """Close a database connection"""
        if conn:
            conn.close()
            
    def insert_response(self, conn, case_id, scenario_filename, vendor, model, model_version, 
                        iteration, timestamp, prompt, full_response, recommended_decision, 
                        alternative_decision, least_recommended_decision, processing_time):
        """Insert a response into the database"""
        raise NotImplementedError("Subclasses must implement insert_response()")
    
    def insert_grant_review(self, conn, applicant_name, vendor, model, model_version,
                           iteration, timestamp, prompt, full_response, review_scores_json,
                           overall_recommendation, processing_time, prompt_experiment_name=None,
                           prompt_version=None):
        """Insert a grant review into the database"""
        raise NotImplementedError("Subclasses must implement insert_grant_review()")
    
    def insert_grant_review_criterion(self, conn, grant_review_id, applicant_name, criterion_name, score, rationale):
        """Insert a grant review criterion into the database"""
        raise NotImplementedError("Subclasses must implement insert_grant_review_criterion()")
            
class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter"""
    def __init__(self, db_path):
        super().__init__()
        self.type = "sqlite"
        self.db_path = Path(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        logger.info(f"Using SQLite database at {self.db_path}")
        
    def get_connection(self):
        """Get a SQLite connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
        
    def init_db(self):
        """Initialize SQLite database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create responses table (for backward compatibility with ethics processor)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT,
            scenario_filename TEXT,
            vendor TEXT,
            model TEXT,
            model_version TEXT,
            iteration INTEGER,
            timestamp TEXT,
            prompt TEXT,
            full_response TEXT,
            recommended_decision TEXT,
            alternative_decision TEXT,
            least_recommended_decision TEXT,
            processing_time REAL
        )
        ''')
        
        # Create grant_reviews table (optimized for grant review data)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grant_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_name TEXT NOT NULL,
            vendor TEXT NOT NULL,
            model TEXT NOT NULL,
            model_version TEXT,
            iteration INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            prompt TEXT,
            full_response TEXT,
            review_scores_json TEXT,
            overall_recommendation TEXT,
            processing_time REAL,
            prompt_experiment_name TEXT,
            prompt_version TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create grant_review_criteria table (for individual criterion scores)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grant_review_criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grant_review_id INTEGER NOT NULL,
            applicant_name TEXT NOT NULL,
            criterion_name TEXT NOT NULL,
            score INTEGER,
            rationale TEXT,
            FOREIGN KEY (grant_review_id) REFERENCES grant_reviews (id)
        )
        ''')
        
        # Check if applicant_name column exists in grant_review_criteria, if not add it
        cursor.execute("PRAGMA table_info(grant_review_criteria)")
        criteria_columns = [info[1] for info in cursor.fetchall()]
        if 'applicant_name' not in criteria_columns:
            logger.info("Adding applicant_name column to grant_review_criteria table")
            cursor.execute("ALTER TABLE grant_review_criteria ADD COLUMN applicant_name TEXT")
        
        # Check if scenario_filename column exists in responses table, if not add it
        cursor.execute("PRAGMA table_info(responses)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'scenario_filename' not in columns:
            logger.info("Adding scenario_filename column to responses table")
            cursor.execute("ALTER TABLE responses ADD COLUMN scenario_filename TEXT")
        
        conn.commit()
        self.close_connection(conn)
        logger.info("SQLite database initialized with grant review tables")
        
    def insert_response(self, conn, case_id, scenario_filename, vendor, model, model_version, 
                        iteration, timestamp, prompt, full_response, recommended_decision, 
                        alternative_decision, least_recommended_decision, processing_time):
        """Insert a response into the SQLite database"""
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO responses 
        (case_id, scenario_filename, vendor, model, model_version, iteration, timestamp, prompt, 
        full_response, recommended_decision, alternative_decision, least_recommended_decision, processing_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            case_id, scenario_filename, vendor, model, model_version, iteration, timestamp, prompt,
            full_response, recommended_decision, alternative_decision, least_recommended_decision, processing_time
        ))
        response_id = cursor.lastrowid
        conn.commit()
        return response_id
    
    def insert_grant_review(self, conn, applicant_name, vendor, model, model_version,
                           iteration, timestamp, prompt, full_response, review_scores_json,
                           overall_recommendation, processing_time, prompt_experiment_name=None,
                           prompt_version=None):
        """Insert a grant review into the SQLite database"""
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO grant_reviews
        (applicant_name, vendor, model, model_version, iteration, timestamp, prompt,
        full_response, review_scores_json, overall_recommendation, processing_time,
        prompt_experiment_name, prompt_version)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            applicant_name, vendor, model, model_version, iteration, timestamp, prompt,
            full_response, review_scores_json, overall_recommendation, processing_time,
            prompt_experiment_name, prompt_version
        ))
        grant_review_id = cursor.lastrowid
        conn.commit()
        return grant_review_id
    
    def insert_grant_review_criterion(self, conn, grant_review_id, applicant_name, criterion_name, score, rationale):
        """Insert a grant review criterion into the SQLite database"""
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO grant_review_criteria 
        (grant_review_id, applicant_name, criterion_name, score, rationale)
        VALUES (?, ?, ?, ?, ?)
        ''', (grant_review_id, applicant_name, criterion_name, score, rationale))
        conn.commit()
        return cursor.lastrowid

class SupabaseAdapter(DatabaseAdapter):
    """Supabase PostgreSQL database adapter"""
    def __init__(self):
        super().__init__()
        self.type = "supabase"
        logger.info("Using Supabase PostgreSQL database")
        
    def get_connection(self):
        """Get a Supabase PostgreSQL connection"""
        conn_params = {
            'dbname': os.getenv('SUPABASE_DB_NAME', 'postgres'),
            'user': os.getenv('SUPABASE_USER', 'postgres.eigtivpuaudjkdadajfb'),
            'password': os.getenv('SUPABASE_PASSWORD'),
            'host': os.getenv('SUPABASE_HOST', 'aws-0-us-east-2.pooler.supabase.com'),
            'port': os.getenv('SUPABASE_PORT', '6543'),
            'cursor_factory': RealDictCursor  # Enable dictionary-style access to rows
        }
        
        conn = psycopg2.connect(**conn_params)
        return conn
        
    def init_db(self):
        """Initialize Supabase PostgreSQL database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create responses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            case_id TEXT,
            scenario_filename TEXT,
            vendor TEXT,
            model TEXT,
            model_version TEXT,
            iteration INTEGER,
            timestamp TEXT,
            prompt TEXT,
            full_response TEXT,
            recommended_decision TEXT,
            alternative_decision TEXT,
            least_recommended_decision TEXT,
            processing_time REAL
        )
        ''')
        
        # Create evaluators table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluators (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            created_at TEXT NOT NULL
        )
        ''')
        
        # Create evaluations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id SERIAL PRIMARY KEY,
            evaluator_id INTEGER NOT NULL,
            response_id INTEGER NOT NULL,
            case_id TEXT NOT NULL,
            scenario_filename TEXT NOT NULL,
            iteration INTEGER NOT NULL,
            relevance_score INTEGER NOT NULL,
            correctness_score INTEGER NOT NULL,
            fluency_score INTEGER NOT NULL,
            coherence_score INTEGER NOT NULL,
            comments TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (evaluator_id) REFERENCES evaluators (id),
            FOREIGN KEY (response_id) REFERENCES responses (id)
        )
        ''')
        
        conn.commit()
        self.close_connection(conn)
        logger.info("Supabase PostgreSQL database initialized")
        
    def insert_response(self, conn, case_id, scenario_filename, vendor, model, model_version, 
                       iteration, timestamp, prompt, full_response, recommended_decision, 
                       alternative_decision, least_recommended_decision, processing_time):
        """Insert a response into the Supabase PostgreSQL database"""
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO responses 
        (case_id, scenario_filename, vendor, model, model_version, iteration, timestamp, prompt, 
        full_response, recommended_decision, alternative_decision, least_recommended_decision, processing_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            case_id, scenario_filename, vendor, model, model_version, iteration, timestamp, prompt,
            full_response, recommended_decision, alternative_decision, least_recommended_decision, processing_time
        ))
        conn.commit()

def get_db_adapter():
    """Factory function to get the appropriate database adapter based on configuration"""
    db_type = os.environ.get("DB_TYPE", "sqlite").lower()
    
    if db_type == "sqlite":
        base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.environ.get("DB_PATH", base_path / "data" / "results.db")
        return SQLiteAdapter(db_path)
    elif db_type == "supabase":
        # Check for required Supabase environment variables
        required_vars = ['SUPABASE_PASSWORD', 'SUPABASE_HOST']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            logger.error(f"Missing Supabase configuration. Please set {', '.join(missing_vars)} in .env file")
            raise ValueError("Missing Supabase configuration")
            
        return SupabaseAdapter()
    else:
        logger.error(f"Unknown database type: {db_type}. Using SQLite as fallback.")
        base_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.environ.get("DB_PATH", base_path / "data" / "results.db")
        return SQLiteAdapter(db_path)
