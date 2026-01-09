import os
import ssl
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get database URL and convert to async if needed
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/dbname")

# Convert postgresql:// to postgresql+asyncpg:// for async support
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Remove parameters that asyncpg doesn't support (sslmode, channel_binding)
parsed = urlparse(DATABASE_URL)
query_params = parse_qs(parsed.query)
query_params.pop('sslmode', None)
query_params.pop('channel_binding', None)
new_query = urlencode({k: v[0] for k, v in query_params.items()})
DATABASE_URL = urlunparse((
    parsed.scheme,
    parsed.netloc,
    parsed.path,
    parsed.params,
    new_query,
    parsed.fragment
))

# Create SSL context for Neon
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    DATABASE_URL, 
    echo=False, 
    future=True,
    connect_args={"ssl": ssl_context},
    pool_pre_ping=True,  # Check connection before using
    pool_size=5,
    max_overflow=10
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
