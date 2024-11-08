import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Set
import torch
from sentence_transformers import SentenceTransformer
import faiss
import logging
import json
import pyodbc
import re
from dataclasses import dataclass
from collections import Counter
import os

@dataclass
class CategoryInfo:
    name: str
    keywords: Set[str]
    patterns: List[str]
    
# Define categories and their related terms
CATEGORIES = {
    'auto': CategoryInfo(
        name='Auto Insurance',
        keywords={
            'vehicle', 'car', 'motor', 'driving', 'comprehensive', 'tpl', 'third party',
            'istimara', 'policy', 'accident', 'claim', 'garage', 'repair', 'agency',
            'damage', 'orange card', 'breakdown', 'roadside', 'assistance', 'plate',
            'license', 'traffic', 'model', 'manufacturing', 'workshop'
        },
        patterns=[
            r'car|vehicle|motor|driving|istimara',
            r'comprehensive|tpl|policy',
            r'garage|repair|agency|workshop',
            r'accident|damage|breakdown',
            r'plate|license|traffic'
        ]
    ),
    'health': CategoryInfo(
        name='Health Insurance',
        keywords={
            'medical', 'health', 'hospital', 'clinic', 'doctor', 'treatment', 'medication',
            'prescription', 'diagnosis', 'patient', 'emergency', 'coverage', 'dental',
            'optical', 'maternity', 'chronic', 'condition', 'disease', 'therapy', 'surgery'
        },
        patterns=[
            r'medical|health|hospital|clinic',
            r'treatment|medication|prescription',
            r'patient|emergency|surgery',
            r'dental|optical|maternity',
            r'disease|condition|chronic'
        ]
    )
}

def detect_category(text: str) -> str:
    """
    Detect the insurance category of a text using multiple methods
    """
    text = text.lower()
    
    # Method 1: Keyword matching
    category_scores = {
        cat: len(set(text.split()) & info.keywords) 
        for cat, info in CATEGORIES.items()
    }
    
    # Method 2: Pattern matching
    for cat, info in CATEGORIES.items():
        for pattern in info.patterns:
            if re.search(pattern, text):
                category_scores[cat] = category_scores.get(cat, 0) + 2
    
    # Get category with highest score
    if any(category_scores.values()):
        return max(category_scores.items(), key=lambda x: x[1])[0]
    
    return 'unknown'

def connect_to_database():
    """Create connection to SQL Server"""
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=192.168.3.120;'
        'DATABASE=agencyDB_Live;'
        'UID=sa;'
        'PWD=P@ssw0rdSQL;'
        'Encrypt=yes;'
        'TrustServerCertificate=yes;'
    )
    
    try:
        connection = pyodbc.connect(conn_str)
        logging.info("Successfully connected to the database!")
        return connection
    except pyodbc.Error as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

def load_qa_data(connection: pyodbc.Connection) -> pd.DataFrame:
    """Load QA pairs from database"""
    try:
        query = """
            SELECT 
                q.QuestionEN,
                a.AnswerEN,
                q.ID as QuestionID,
                c.CategoryNameEN
            FROM tblFAQAnswer a 
            INNER JOIN tblFAQQuestions q ON a.QuestionID = q.ID
            inner join tblFAQCategory c on q.CategoryID = c.id
            WHERE q.QuestionEN IS NOT NULL 
            AND a.AnswerEN IS NOT NULL
            AND LEN(q.QuestionEN) > 0 
            AND LEN(a.AnswerEN) > 0
        """
        
        qa_pairs = pd.read_sql(query, connection)
        
        logging.info(f"Loaded {len(qa_pairs)} QA pairs")
        logging.info("\nDataset Overview:")
        logging.info(qa_pairs.info())
        
        # Add data quality checks
        logging.info("\nData Quality Checks:")
        logging.info(f"Null values:\n{qa_pairs.isnull().sum()}")
        
        return qa_pairs
        
    except Exception as e:
        logging.error(f"Error loading QA data: {e}")
        raise

def preprocess_text(text: str, category: str = None) -> str:
    """
    Preprocess text while considering its category
    """
    # Basic cleaning
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    
    # Category-specific preprocessing
    if category == 'auto':
        # Standardize auto insurance terms
        replacements = {
            'third party liability': 'tpl',
            'third party': 'tpl',
            'comprehensive insurance': 'comprehensive',
            'vehicle registration card': 'istimara',
            'registration card': 'istimara'
        }
    elif category == 'health':
        # Standardize health insurance terms
        replacements = {
            'medical insurance': 'health insurance',
            'health care': 'healthcare',
            'medical condition': 'condition',
            'medical treatment': 'treatment'
        }
    else:
        replacements = {}
        
    # Apply replacements
    for old, new in replacements.items():
        text = re.sub(rf'\b{old}\b', new, text)
    
    return text

class QADatabase:
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/all-MiniLM-L12-v2",
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.device = device
        self.embedding_model = SentenceTransformer(embedding_model, trust_remote_code=True).to(device)
        self.data = None
        self.embeddings = None
        self.index = None
        self.categories = None
    
    def add_qa_pairs(self, df: pd.DataFrame):
        """
        Add QA pairs with preprocessing and metadata
        """
        # Add metadata and preprocessing
        self.data = add_metadata(df)
        
        # Store unique categories
        self.categories = self.data['category'].unique()
        
        # Generate embeddings for questions
        questions = self.data['processed_question'].tolist()
        self.embeddings = self._generate_embeddings(questions)
        
        # Create index per category
        self.index = {}
        for cat in self.categories:
            cat_mask = self.data['category'] == cat
            if cat_mask.any():
                cat_embeddings = self.embeddings[cat_mask]
                index = faiss.IndexFlatIP(cat_embeddings.shape[1])
                index.add(cat_embeddings.astype('float32'))
                self.index[cat] = {
                    'index': index,
                    'data_indices': np.where(cat_mask)[0]
                }
        
        logging.info(f"Added {len(self.data)} QA pairs")
        for cat in self.categories:
            if cat in self.index:
                cat_count = len(self.index[cat]['data_indices'])
                logging.info(f"Category '{cat}': {cat_count} questions")
    
    def _generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings with batching"""
        embeddings = []
        batch_size = 32
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embedding_model.encode(
                batch,
                convert_to_tensor=True,
                device=self.device,
                show_progress_bar=False
            )
            embeddings.append(batch_embeddings.cpu().numpy())
            
        return np.vstack(embeddings)
    
    def save(self, path: str):
        """Save the QA database state"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the data
        self.data.to_pickle(f"{path}_data.pkl")
        
        # Save embeddings
        np.save(f"{path}_embeddings.npy", self.embeddings)
        
        # Save indices
        for cat, cat_data in self.index.items():
            faiss.write_index(cat_data['index'], f"{path}_{cat}_index.faiss")
            np.save(f"{path}_{cat}_indices.npy", cat_data['data_indices'])
        
        logging.info(f"Saved database state to {path}")
        
    @classmethod
    def load(cls, path: str):
        """Load a saved QA database state"""
        instance = cls()
        
        # Load the data
        instance.data = pd.read_pickle(f"{path}_data.pkl")
        
        # Load embeddings
        instance.embeddings = np.load(f"{path}_embeddings.npy")
        
        # Get categories from data
        instance.categories = instance.data['category'].unique()
        
        # Load indices
        instance.index = {}
        for cat in instance.categories:
            if os.path.exists(f"{path}_{cat}_index.faiss"):
                instance.index[cat] = {
                    'index': faiss.read_index(f"{path}_{cat}_index.faiss"),
                    'data_indices': np.load(f"{path}_{cat}_indices.npy")
                }
        
        logging.info(f"Loaded database state from {path}")
        return instance
    
    def search(
        self,
        query: str,
        k: int = 5,
        threshold: float = 0.5
    ) -> List[Dict]:
        """
        Search with improved category awareness and scoring
        """
        # Detect query category
        category = detect_category(query)
        
        # Preprocess query
        query = preprocess_text(query, category)
        
        # Get embedding for query
        query_embedding = self._generate_embeddings([query])
        
        results = []
        
        # If category is unknown, search in all categories
        categories_to_search = [category] if category != 'unknown' else self.categories
        
        # Search in appropriate categories
        for cat in categories_to_search:
            if cat in self.index:
                cat_index = self.index[cat]
                
                # Search using dot product
                D, I = cat_index['index'].search(
                    query_embedding.astype('float32'),
                    k
                )
                
                # Convert distances to similarities
                similarities = (D[0] + 1) / 2 
                
                for idx, sim in zip(I[0], similarities):
                    if sim >= threshold:
                        orig_idx = cat_index['data_indices'][idx]
                        row = self.data.iloc[orig_idx]
                        results.append({
                            'question': row['QuestionEN'],
                            'answer': row['AnswerEN'],
                            'category': row['category'],
                            'similarity': float(sim),
                            'question_id': str(row['QuestionID'])
                        })
        
        # Remove duplicates keeping highest similarity score
        seen_answers = {}
        for result in results:
            answer = result['answer']
            if answer not in seen_answers or result['similarity'] > seen_answers[answer]['similarity']:
                seen_answers[answer] = result
                
        unique_results = list(seen_answers.values())
        
        return sorted(unique_results, key=lambda x: x['similarity'], reverse=True)[:k]

def add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add metadata to enhance matching
    """
    df = df.copy()
    
    # Add categories
    df['category'] = df.apply(
        lambda row: detect_category(f"{row['QuestionEN']} {row['AnswerEN']}"),
        axis=1
    )
    
    # Process text based on category
    df['processed_question'] = df.apply(
        lambda row: preprocess_text(row['QuestionEN'], row['category']),
        axis=1
    )
    
    # Count terms
    df['question_terms'] = df['processed_question'].apply(lambda x: len(set(x.split())))
    
    return df

class QAResult:
    """Class to handle QA results"""
    def __init__(self, answer: str, confidence: float, sources: List[Dict] = None):
        self.answer = answer
        self.confidence = confidence
        self.sources = sources or []
    
    def to_dict(self):
        return {
            'answer': self.answer,
            'confidence': self.confidence,
            'sources': self.sources
        }
    
class RAGQASystem:
    def __init__(
        self,
        qa_database: QADatabase,
        threshold: float = 0.4,
        max_results: int = 5
    ):
        self.qa_database = qa_database
        self.threshold = threshold
        self.max_results = max_results
    
    def answer_question(self, question: str) -> Dict:
        """Answer with better error handling"""
        try:
            results = self.qa_database.search(
                question,
                k=self.max_results,
                threshold=self.threshold
            )
            
            if not results:
                return QAResult(
                    answer="I'm sorry, I couldn't find a relevant answer to your question.",
                    confidence=0.0
                ).to_dict()
            
            best_match = results[0]
            return QAResult(
                answer=best_match['answer'],
                confidence=best_match['similarity'],
                sources=results
            ).to_dict()
            
        except Exception as e:
            logging.error(f"Error answering question: {str(e)}")
            return QAResult(
                answer="I apologize, but I encountered an error processing your question.",
                confidence=0.0
            ).to_dict()

def create_qa_system(qa_pairs: pd.DataFrame) -> RAGQASystem:
    """Create and initialize the RAG QA system"""
    qa_db = QADatabase()
    qa_db.add_qa_pairs(qa_pairs)
    return RAGQASystem(qa_db, threshold=0.4, max_results=5)

def debug_question_search(qa_database: QADatabase, question: str, debug_threshold: float = 0.0):
    """
    Debug search process for a specific question
    """
    print("\n=== Debug Search Process ===")
    
    # Step 1: Preprocessing
    category = detect_category(question)
    processed_query = preprocess_text(question, category)
    print(f"Original question: {question}")
    print(f"Processed question: {processed_query}")
    print(f"Detected category: {category}")
    
    # Step 2: Get query embedding
    query_embedding = qa_database._generate_embeddings([processed_query])
    
    # Step 3: Get all similarities for debugging
    results = []
    
    # Search across all categories for debugging
    for cat, cat_index in qa_database.index.items():
        print(f"\nSearching in category: {cat}")
        
        # Get similarities with all questions in this category
        D, I = cat_index['index'].search(
            query_embedding.astype('float32'),
            len(cat_index['data_indices'])  # Get all matches
        )
        
        # Convert distances to similarities
        similarities = (D[0] + 1) / 2
        
        # Get all matches above debug threshold
        for idx, sim in zip(I[0], similarities):
            if sim >= debug_threshold:
                orig_idx = cat_index['data_indices'][idx]
                row = qa_database.data.iloc[orig_idx]
                results.append({
                    'question': row['QuestionEN'],
                    'processed_question': row['processed_question'],
                    'answer': row['AnswerEN'],
                    'category': row['category'],
                    'similarity': float(sim),
                    'question_id': str(row['QuestionID'])
                })
    
    # Sort by similarity
    results = sorted(results, key=lambda x: x['similarity'], reverse=True)
    
    # Print top 10 most similar questions
    print("\nTop 10 most similar questions:")
    for i, result in enumerate(results[:10], 1):
        print(f"\n{i}. Similarity: {result['similarity']:.4f}")
        print(f"Question: {result['question']}")
        print(f"Processed: {result['processed_question']}")
        print(f"Answer: {result['answer']}")
        print(f"Category: {result['category']}")

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Connect and load data
        connection = connect_to_database()
        qa_pairs = load_qa_data(connection)
        
        # Create and train system
        qa_system = create_qa_system(qa_pairs)

            # Debug specific problematic question
        problem_question = "How can I change my name in my profile?"
        print("\n=== Debugging Specific Question ===")
        debug_question_search(qa_system.qa_database, problem_question)
        
        # Test system
        test_questions = [
            # Auto insurance questions
            "How do I submit a claim?",
            "What are the payment methods?",
            "What is the difference between comprehensive and TPL?",
            
            # Health insurance questions
            "What does the health insurance cover?",
            "How do I get reimbursed for medication?",
            "Is dental treatment covered?",
            
            # Mixed/ambiguous questions
            "What documents do I need?",
            "How much does it cost?",
            "What does the gold coverage covers?"
        ]
        
        print("\nTesting QA System:")
        for question in test_questions:
            result = qa_system.answer_question(question)
            print(f"\nQ: {question}")
            print(f"A: {result['answer']}")
            print(f"Confidence: {result['confidence']:.2f}")
            
            if result['sources']:
                print("\nSimilar Questions:")
                for source in result['sources']:
                    print(f"- Q: {source['question']}")
                    print(f"  Similarity: {source['similarity']:.2f}")
                    print(f"  A: {source['answer']}")
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        raise
    finally:
        if 'connection' in locals():
            connection.close()
            logging.info("Database connection closed")

if __name__ == "__main__":
    main()