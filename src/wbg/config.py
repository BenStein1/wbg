import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

# Paths
ROOT = Path(__file__).parent
DATA = ROOT / "data"
MAX_SENTENCE_LENGTH = 300

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
