import sys
from pathlib import Path
import traceback

# --- HARD-CODED LOG LOCATION (DESKTOP) ---
LOG_FILE = Path(r"C:\Users\TIJU0004\Documents\scheduler_error.log")

try:
    PROJECT_ROOT = Path(__file__).resolve().parent
    sys.path.insert(0, str(PROJECT_ROOT))

    from app.core.reminder_engine import run_reminders
    run_reminders()

except Exception:
    LOG_FILE.write_text(traceback.format_exc())
