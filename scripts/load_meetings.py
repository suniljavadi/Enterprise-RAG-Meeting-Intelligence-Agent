from pathlib import Path
from app.database.session import init_db
from scripts.seed import main
if __name__ == "__main__":
    init_db(); main()
