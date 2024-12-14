# main.py

import streamlit.web.cli as stcli
import sys
import os
from pathlib import Path

def main():
    # Get the absolute path to the frontend directory
    current_dir = Path(__file__).parent
    frontend_path = current_dir / "streamlit_gui.py"
    
    if not frontend_path.exists():
        print(f"Error: Could not find {frontend_path}")
        sys.exit(1)
    
    # Add the project root to PYTHONPATH
    root_dir = str(current_dir)
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    
    # Set environment variables if needed
    os.environ['STREAMLIT_THEME'] = "light"
    
    # Launch the Streamlit application
    sys.argv = ["streamlit", "run", str(frontend_path)]
    sys.exit(stcli.main())

if __name__ == "__main__":
    main()