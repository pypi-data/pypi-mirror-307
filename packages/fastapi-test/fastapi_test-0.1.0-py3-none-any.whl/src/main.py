from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
from contextlib import asynccontextmanager
import os

# Import from our qa_system package
from rag_en import (
    connect_to_database,
    load_qa_data,
    create_qa_system,
    detect_category,
    CATEGORIES
)
from rag_ar import (
    load_qa_data_ar,
    create_qa_system_ar
)

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Pydantic models
class QuestionRequest(BaseModel):
    text: str
    language: str = "en"  # "en" or "ar"
    max_results: Optional[int] = 5
    threshold: Optional[float] = 0.4

class QAResponse(BaseModel):
    answer: str
    confidence: float
    sources: Optional[List[Dict]] = None
    category: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    models_loaded: bool
    database_connected: bool

# Global variables for QA systems
qa_systems = {
    "en": None,
    "ar": None
}

# Create templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(templates_dir, exist_ok=True)

# Create templates
welcome_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Insurance QA API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        .endpoint {
            background-color: #f5f5f5;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .method {
            font-weight: bold;
            color: #0066cc;
        }
        .url {
            color: #666;
            font-family: monospace;
        }
        .description {
            margin-top: 10px;
        }
        .try-it {
            margin-top: 10px;
        }
        code {
            background-color: #eee;
            padding: 2px 5px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <h1>Insurance QA API</h1>
    <p>Welcome to the Multilingual Insurance QA API. This API provides question-answering capabilities for insurance-related queries in both English and Arabic.</p>
    
    <h2>Available Endpoints:</h2>
    
    <div class="endpoint">
        <span class="method">GET</span> 
        <span class="url">/docs</span>
        <div class="description">Interactive API documentation with Swagger UI</div>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> 
        <span class="url">/redoc</span>
        <div class="description">Alternative API documentation with ReDoc</div>
    </div>
    
    <div class="endpoint">
        <span class="method">POST</span> 
        <span class="url">/qa</span>
        <div class="description">Get answers to insurance-related questions</div>
        <div class="try-it">
            Example:
            <pre><code>
curl -X POST "http://localhost:8000/qa" \\
-H "Content-Type: application/json" \\
-d '{
    "text": "How do I submit a car insurance claim?",
    "language": "en"
}'</code></pre>
        </div>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> 
        <span class="url">/categories</span>
        <div class="description">List all available insurance categories</div>
    </div>
    
    <div class="endpoint">
        <span class="method">GET</span> 
        <span class="url">/health</span>
        <div class="description">Check the API's health status</div>
    </div>

    <h2>Getting Started</h2>
    <p>To use the API:</p>
    <ol>
        <li>Visit <a href="/docs">/docs</a> for interactive API documentation</li>
        <li>Try the example endpoints above</li>
        <li>Use the appropriate language code ("en" for English, "ar" for Arabic)</li>
    </ol>
</body>
</html>
"""

# Save welcome.html template
with open(os.path.join(templates_dir, "welcome.html"), "w", encoding="utf-8") as f:
    f.write(welcome_html)

# Initialize templates
templates = Jinja2Templates(directory=templates_dir)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize QA systems on startup
    try:
        # Connect to database
        connection = connect_to_database()
        
        # Load English QA system
        en_qa_pairs = load_qa_data(connection)
        qa_systems["en"] = create_qa_system(en_qa_pairs)
        logging.info("English QA system initialized")
        
        # Load Arabic QA system
        ar_qa_pairs = load_qa_data_ar(connection)
        qa_systems["ar"] = create_qa_system_ar(ar_qa_pairs)
        logging.info("Arabic QA system initialized")
        
        # Close database connection
        connection.close()
        
        # Save initialized systems
        save_dir = "qa_system/models"
        os.makedirs(save_dir, exist_ok=True)
        qa_systems["en"].qa_database.save(os.path.join(save_dir, "english_qa_system"))
        qa_systems["ar"].qa_database.save(os.path.join(save_dir, "arabic_qa_system"))
        
    except Exception as e:
        logging.error(f"Error during initialization: {str(e)}")
        raise
    
    yield
    
    # Cleanup on shutdown
    qa_systems["en"] = None
    qa_systems["ar"] = None
    logging.info("QA systems cleaned up")

# Initialize FastAPI app
app = FastAPI(
    title="Multilingual Insurance QA API",
    description="API for answering insurance-related questions in English and Arabic",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Welcome page with API information"""
    return templates.TemplateResponse("welcome.html", {"request": request})

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health status of the API and its components"""
    return HealthResponse(
        status="healthy",
        models_loaded=all(system is not None for system in qa_systems.values()),
        database_connected=True
    )

@app.post("/qa", response_model=QAResponse)
async def answer_question(request: QuestionRequest):
    """
    Get answer for a question in specified language
    """
    try:
        # Validate language
        if request.language not in qa_systems:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported language: {request.language}"
            )
            
        # Get appropriate QA system
        qa_system = qa_systems[request.language]
        if qa_system is None:
            raise HTTPException(
                status_code=503,
                detail=f"QA system for {request.language} is not initialized"
            )
            
        # Get answer
        result = qa_system.answer_question(request.text)
        
        # Detect category
        category = detect_category(request.text)
        
        return QAResponse(
            answer=result['answer'],
            confidence=result['confidence'],
            sources=result['sources'],
            category=category
        )
        
    except Exception as e:
        logging.error(f"Error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/categories")
async def list_categories():
    """Get available insurance categories"""
    return {
        "categories": [
            {
                "id": cat_id,
                "name_en": info.name,
                "name_ar": CATEGORIES[cat_id].name if cat_id in CATEGORIES else None
            }
            for cat_id, info in CATEGORIES.items()
        ]
    }

@app.post("/debug/search")
async def debug_search(request: QuestionRequest):
    """
    Debug endpoint to see detailed search results
    """
    try:
        qa_system = qa_systems[request.language]
        if qa_system is None:
            raise HTTPException(
                status_code=503,
                detail=f"QA system for {request.language} is not initialized"
            )
            
        return qa_system.qa_database.search(
            request.text,
            k=request.max_results,
            threshold=request.threshold
        )
        
    except Exception as e:
        logging.error(f"Error in debug search: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)