import sys
from pathlib import Path

# Get the project root directory (app/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Add app/ to sys.path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
