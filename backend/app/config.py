"""
Loads settings from the .env file so the rest of the app can use them.

TODO (this one's easy, good warm-up):
1. Import `load_dotenv` from python-dotenv and call it at the top of this file.
2. Read the following from environment variables using os.getenv():
   - ANTHROPIC_API_KEY
   - CHROMA_DB_PATH   (give it a default of "./chroma_store" if not set)
   - NOTES_DIR         (default "../data/notes" if not set)
3. Store them as module-level constants so other files can do:
   from app.config import ANTHROPIC_API_KEY
"""

import os
from dotenv import load_dotenv

# TODO: call load_dotenv() here

# TODO: define ANTHROPIC_API_KEY, CHROMA_DB_PATH, NOTES_DIR as constants below
