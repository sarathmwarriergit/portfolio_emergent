from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import portfolio routes
from routes.portfolio import router as portfolio_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="Sarath M Warrier Portfolio API", version="1.0.0")

# Include portfolio routes
app.include_router(portfolio_router)

# Legacy hello world endpoint for compatibility
@app.get("/api/")
async def root():
    return {"message": "Sarath M Warrier Portfolio API - v1.0.0"}

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    logger.info("🚀 Portfolio API server starting up...")
    logger.info(f"📊 Connected to MongoDB: {os.environ.get('DB_NAME')}")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("📊 Closing MongoDB connection...")
    client.close()