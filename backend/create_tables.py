"""Script to create database tables for Phase III chatbot."""
import asyncio
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

# Import models to register them
from src.db.models import ConversationSession, ChatMessage
from src.models.habit import Habit

async def create_tables():
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # Convert to async URL
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    # Remove parameters that asyncpg doesn't support
    # Parse and rebuild URL without sslmode and channel_binding
    from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
    
    parsed = urlparse(DATABASE_URL)
    query_params = parse_qs(parsed.query)
    
    # Remove unsupported params
    query_params.pop('sslmode', None)
    query_params.pop('channel_binding', None)
    
    # Rebuild query string
    new_query = urlencode({k: v[0] for k, v in query_params.items()})
    
    # Rebuild URL
    DATABASE_URL = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    print(f"Connecting to database...")
    
    # Create SSL context for Neon
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    engine = create_async_engine(
        DATABASE_URL, 
        echo=True,
        connect_args={"ssl": ssl_context}
    )
    
    async with engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())
