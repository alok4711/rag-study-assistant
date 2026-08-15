"""
Loads settings from the .env file so the rest of the app can use them.

TODO (this one's easy, good warm-up):
1. Import `load_dotenv` from python-dotenv and call it at the top of this file.
2. Read the following from environment variables using os.getenv():
   - GEMINI_API_KEY
   - CHROMA_DB_PATH   (give it a default of "./chroma_store" if not set)
   - NOTES_DIR         (default "../data/notes" if not set)
3. Store them as module-level constants so other files can do:
   from app.config import GEMINI_API_KEY
"""

import os
from dotenv import load_dotenv

# 1. This one line reads your .env file and loads everything in it
load_dotenv()

# 2. Now define constants that pull specific values out
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_store")
NOTES_DIR = os.getenv("NOTES_DIR", "../data/notes")
