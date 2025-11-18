import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://challenge:challenge_2024@postgres:5432/god-level-challenge")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
