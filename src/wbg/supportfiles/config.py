import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# Paths
ROOT = Path(__file__).parent
DATA = ROOT / "data"


# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
