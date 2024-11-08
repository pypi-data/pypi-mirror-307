import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple, Set
import torch
from sentence_transformers import SentenceTransformer
import faiss
import logging
import json
from tqdm import tqdm
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

# Define categories and their related terms in Arabic
CATEGORIES = {
    'auto': CategoryInfo(
        name='تأمين السيارات',
        keywords={
            'سيارة', 'مركبة', 'قيادة', 'شامل', 'ضد الغير', 'طرف ثالث',
            'استمارة', 'وثيقة', 'حادث', 'مطالبة', 'ورشة', 'إصلاح', 'وكالة',
            'ضرر', 'البطاقة البرتقالية', 'تعطل', 'مساعدة', 'لوحة',
            'رخصة', 'مرور', 'موديل', 'تصنيع', 'كراج'
        },
        patterns=[
            r'سيارة|مركبة|قيادة|استمارة',
            r'شامل|ضد الغير|وثيقة',
            r'ورشة|إصلاح|وكالة|كراج',
            r'حادث|ضرر|تعطل',
            r'لوحة|رخصة|مرور'
        ]
    ),
    'health': CategoryInfo(
        name='تأمين صحي',
        keywords={
            'طبي', 'صحي', 'مستشفى', 'عيادة', 'طبيب', 'علاج', 'دواء',
            'وصفة', 'تشخيص', 'مريض', 'طوارئ', 'تغطية', 'أسنان',
            'نظر', 'ولادة', 'مزمن', 'حالة', 'مرض', 'استشارة', 'جراحة'
        },
        patterns=[
            r'طبي|صحي|مستشفى|عيادة',
            r'علاج|دواء|وصفة',
            r'مريض|طوارئ|جراحة',
            r'أسنان|نظر|ولادة',
            r'مرض|حالة|مزمن'
        ]
    )
}

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

def validate_arabic_text(text: str) -> bool:
    """
    Validate if text contains meaningful Arabic content
    """
    if not text or not isinstance(text, str):
        return False
        
    # Check if text contains Arabic characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF]+')
    if not arabic_pattern.search(text):
        return False
    
    # Check minimum length (after removing spaces and special characters)
    clean_text = re.sub(r'[\s\d.,!؟،;]', '', text)
    if len(clean_text) < 5:  # Minimum 5 characters
        return False
    
    return True

def clean_arabic_text(text: str) -> str:
    """
    Clean Arabic text from common issues
    """
    if not isinstance(text, str):
        return ""
        
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Fix common typing issues in Arabic
    text = text.replace('ىى', 'ي')
    text = text.replace('ة ة', 'ة')
    
    # Normalize Arabic characters
    text = re.sub('[إأآا]', 'ا', text)
    text = re.sub('[ىي]', 'ي', text)
    text = re.sub('[ؤئ]', 'ء', text)
    text = text.replace('ة', 'ه')
    
    # Normalize spaces around punctuation
    text = re.sub(r'\s*([،؛؟!.])\s*', r'\1 ', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def load_qa_data_ar(connection: pyodbc.Connection) -> pd.DataFrame:
    """Load Arabic QA pairs from database with validation"""
    try:
        # SQL query for Arabic Q&A pairs with category
        query = """
            SELECT 
                q.QuestionAR,
                a.AnswerAR,
                q.ID as QuestionID,
                c.CategoryNameAR,
                c.ID as CategoryID
            FROM tblFAQAnswer a 
            INNER JOIN tblFAQQuestions q ON a.QuestionID = q.ID
            INNER JOIN tblFAQCategory c on q.CategoryID = c.ID
            WHERE q.QuestionAR IS NOT NULL 
            AND a.AnswerAR IS NOT NULL
            AND LEN(q.QuestionAR) > 0 
            AND LEN(a.AnswerAR) > 0
        """
        
        qa_pairs = pd.read_sql(query, connection)
        initial_count = len(qa_pairs)
        logging.info(f"Initially loaded {initial_count} QA pairs")
        
        # Clean and validate data
        qa_pairs['QuestionAR'] = qa_pairs['QuestionAR'].apply(clean_arabic_text)
        qa_pairs['AnswerAR'] = qa_pairs['AnswerAR'].apply(clean_arabic_text)
        
        # Validate Arabic content
        valid_questions = qa_pairs['QuestionAR'].apply(validate_arabic_text)
        valid_answers = qa_pairs['AnswerAR'].apply(validate_arabic_text)
        
        # Filter valid pairs only
        qa_pairs = qa_pairs[valid_questions & valid_answers].copy()
        
        # Remove duplicates
        qa_pairs = qa_pairs.drop_duplicates(subset=['QuestionAR', 'AnswerAR'])
        final_count = len(qa_pairs)
        
        # Log data quality metrics
        logging.info("\n=== Data Quality Report ===")
        logging.info(f"Initial QA pairs: {initial_count}")
        logging.info(f"Final QA pairs: {final_count}")
        logging.info(f"Removed pairs: {initial_count - final_count}")
        logging.info(f"Categories count: {qa_pairs['CategoryNameAR'].nunique()}")
        
        # Category distribution
        category_dist = qa_pairs['CategoryNameAR'].value_counts()
        logging.info("\nCategory Distribution:")
        for cat, count in category_dist.items():
            logging.info(f"{cat}: {count} pairs")
        
        # Length statistics
        qa_pairs['question_length'] = qa_pairs['QuestionAR'].str.len()
        qa_pairs['answer_length'] = qa_pairs['AnswerAR'].str.len()
        
        logging.info("\nLength Statistics:")
        logging.info(f"Average question length: {qa_pairs['question_length'].mean():.1f} characters")
        logging.info(f"Average answer length: {qa_pairs['answer_length'].mean():.1f} characters")
        
        # Sample validation
        logging.info("\nSample QA Pairs:")
        sample = qa_pairs.sample(min(3, len(qa_pairs)))
        for _, row in sample.iterrows():
            logging.info(f"\nQuestion: {row['QuestionAR']}")
            logging.info(f"Answer: {row['AnswerAR']}")
            logging.info(f"Category: {row['CategoryNameAR']}")
        
        # Return only needed columns
        return qa_pairs[['QuestionAR', 'AnswerAR', 'QuestionID', 'CategoryNameAR']]
        
    except Exception as e:
        logging.error(f"Error loading QA data: {str(e)}")
        raise

def debug_data_loading(connection: pyodbc.Connection) -> None:
    """
    Debug function to analyze Arabic data loading issues
    """
    try:
        # Test raw data loading
        test_query = """
            SELECT TOP 10 
                q.QuestionAR,
                a.AnswerAR,
                q.ID as QuestionID,
                c.CategoryNameAR
            FROM tblFAQAnswer a 
            INNER JOIN tblFAQQuestions q ON a.QuestionID = q.ID
            INNER JOIN tblFAQCategory c on q.CategoryID = c.ID
        """
        
        test_data = pd.read_sql(test_query, connection)
        
        logging.info("\n=== Debug Data Sample ===")
        for _, row in test_data.iterrows():
            logging.info("\nOriginal Question:")
            logging.info(row['QuestionAR'])
            logging.info("Cleaned Question:")
            logging.info(clean_arabic_text(row['QuestionAR']))
            logging.info("Is Valid Arabic:")
            logging.info(validate_arabic_text(row['QuestionAR']))
            
            logging.info("\nOriginal Answer:")
            logging.info(row['AnswerAR'])
            logging.info("Cleaned Answer:")
            logging.info(clean_arabic_text(row['AnswerAR']))
            logging.info("Is Valid Arabic:")
            logging.info(validate_arabic_text(row['AnswerAR']))
            
            logging.info("Category:")
            logging.info(row['CategoryNameAR'])
            logging.info("---")
    
    except Exception as e:
        logging.error(f"Debug Error: {str(e)}")

def preprocess_arabic_text(text: str) -> str:
    """
    Enhanced preprocessing for Arabic text
    """
    if not isinstance(text, str):
        return ""
        
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove diacritics (tashkeel)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # Normalize Arabic characters
    text = re.sub('[إأآا]', 'ا', text)
    text = re.sub('[ىي]', 'ي', text)
    text = re.sub('[ؤئ]', 'ء', text)
    text = text.replace('ة', 'ه')
    
    # Fix common typing issues
    text = text.replace('ىى', 'ي')
    text = text.replace('ة ة', 'ة')
    
    # Normalize spaces around punctuation
    text = re.sub(r'\s*([،؛؟!.])\s*', r'\1 ', text)
    
    # Remove non-Arabic characters except numbers and basic punctuation
    text = re.sub(r'[^\u0600-\u06FF\s0-9،؛؟!.]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()

def detect_category(text: str) -> str:
    """
    Enhanced category detection for Arabic text
    """
    text = preprocess_arabic_text(text)
    
    # Method 1: Keyword matching with stemming
    words = set(text.split())
    category_scores = {cat: 0 for cat in CATEGORIES.keys()}
    
    for cat, info in CATEGORIES.items():
        # Check for exact matches
        exact_matches = len(words & info.keywords)
        category_scores[cat] += exact_matches * 2
        
        # Check for partial matches (substring)
        for word in words:
            for keyword in info.keywords:
                if (word in keyword or keyword in word) and word != keyword:
                    category_scores[cat] += 0.5
    
    # Method 2: Pattern matching with context
    for cat, info in CATEGORIES.items():
        for pattern in info.patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # Give higher score for matches near the beginning of the text
                position_weight = 1.0 - (match.start() / len(text)) * 0.5
                category_scores[cat] += 2 * position_weight
    
    # Get category with highest score
    if any(category_scores.values()):
        return max(category_scores.items(), key=lambda x: x[1])[0]
    
    return 'unknown'

def add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add metadata to enhance matching
    """
    df = df.copy()
    
    # Preprocess questions and answers
    df['processed_question'] = df['QuestionAR'].apply(preprocess_arabic_text)
    df['processed_answer'] = df['AnswerAR'].apply(preprocess_arabic_text)
    
    # Add categories
    df['category'] = df.apply(
        lambda row: detect_category(
            f"{row['processed_question']} {row['processed_answer']}"
        ),
        axis=1
    )
    
    # Count terms
    df['question_terms'] = df['processed_question'].apply(lambda x: len(set(x.split())))
    
    # Add question features
    df['has_question_mark'] = df['QuestionAR'].str.contains('[؟?]')
    
    # Detect question types using common Arabic question starters
    question_starters = ['كيف', 'ما', 'متى', 'اين', 'لماذا', 'هل']
    df['has_question_starter'] = df['processed_question'].apply(
        lambda x: any(x.startswith(w) for w in question_starters)
    )
    
    return df

class QADatabase:
    def __init__(
        self,
        embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        device: str = "cuda" if torch.cuda.is_available() else "cpu"
    ):
        self.device = device
        self.embedding_model = SentenceTransformer(embedding_model).to(device)
        self.data = None
        self.embeddings = None
        self.index = None
        self.categories = None
        
        # Add Arabic-specific configurations
        self.min_question_length = 5
        self.similarity_threshold = 0.4  # Adjusted for Arabic
    
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
        Search with category awareness and scoring
        """
        try:
            # Detect query category
            category = detect_category(query)
            
            # Preprocess query using the imported function
            processed_query = preprocess_arabic_text(query)
            
            # Get embedding for query
            query_embedding = self._generate_embeddings([processed_query])
            
            results = []
            categories_to_search = [category]
            
            # If category is unknown or confidence is low, search all categories
            if category == 'unknown':
                categories_to_search = self.categories
            
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
                                'question': row['QuestionAR'],
                                'answer': row['AnswerAR'],
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
            
            # If no results found in specific category, try all categories
            if not unique_results and category != 'unknown':
                return self.search(query, k, threshold * 0.8)  # Retry with lower threshold
            
            return sorted(unique_results, key=lambda x: x['similarity'], reverse=True)[:k]
            
        except Exception as e:
            logging.error(f"Error in search: {str(e)}")
            return []

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
        """Answer with error handling"""
        try:
            results = self.qa_database.search(
                question,
                k=self.max_results,
                threshold=self.threshold
            )
            
            if not results:
                return QAResult(
                    answer="عذراً، لم أتمكن من العثور على إجابة مناسبة لسؤالك.",
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
                answer="عذراً، حدث خطأ أثناء معالجة سؤالك.",
                confidence=0.0
            ).to_dict()

def create_qa_system_ar(qa_pairs: pd.DataFrame) -> RAGQASystem:
    """Create and initialize the RAG QA system"""
    qa_db = QADatabase()
    qa_db.add_qa_pairs(qa_pairs)
    return RAGQASystem(qa_db, threshold=0.4, max_results=5)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Connect and load data
        connection = connect_to_database()
        qa_pairs = load_qa_data_ar(connection)
        
        # Create and train system
        qa_system = create_qa_system_ar(qa_pairs)
        
        # Test system
        test_questions = [
            # Auto insurance questions
            "كيف يمكنني تقديم مطالبة؟",
            "ما هي طرق الدفع المتاحة؟",
            "ما الفرق بين التأمين الشامل وضد الغير؟",
            
            # Health insurance questions
            "ماذا يغطي التأمين الصحي؟",
            "كيف يمكنني استرداد مصاريف الأدوية؟",
            "هل علاج الأسنان مشمول بالتغطية؟",
            
            # Mixed/ambiguous questions
            "ما هي المستندات المطلوبة؟",
            "كم التكلفة؟",
            "ما هي التغطيات المتوفرة؟"
        ]
        
        print("\nاختبار نظام الأسئلة والأجوبة:")
        for question in test_questions:
            result = qa_system.answer_question(question)
            print(f"\nس: {question}")
            print(f"ج: {result['answer']}")
            print(f"درجة الثقة: {result['confidence']*100:.1f}%")
            
            if result['sources']:
                print("\nأسئلة مشابهة:")
                for source in result['sources']:
                    print(f"- س: {source['question']}")
                    print(f"  نسبة التشابه: {source['similarity']*100:.1f}%")
                    print(f"  ج: {source['answer']}")
        
        # Save the system with proper path
        try:
            save_dir = "models"
            os.makedirs(save_dir, exist_ok=True)
            qa_system.qa_database.save(os.path.join(save_dir, "arabic_qa_system"))
            print("\nتم حفظ النظام بنجاح!")
        except Exception as e:
            logging.error(f"خطأ في حفظ النظام: {str(e)}")
        
    except Exception as e:
        logging.error(f"حدث خطأ: {str(e)}")
        raise
    finally:
        if 'connection' in locals():
            connection.close()
            logging.info("تم إغلاق الاتصال بقاعدة البيانات")

if __name__=='__main__':
    main()