import sys
from streamlit_gui import StreamlitGUI
from frontend import cmd_toolset
import ctypes
import streamlit.web.cli as stcli
import sys
import os
from pathlib import Path
# import qdarkstyle
# import os
# def load_stylesheet(file_path):
#     """Load and return the content of a QSS file."""
#     with open(file_path, "r") as file:
#         return file.read()
# [print(i) for i in list(sys.modules.keys())]

def run_cli():
    """Run the CLI version of the application."""
    cmd_toolset.main()

def run_gui():
    """Run the GUI version of the application."""
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

def switch_standard_streams(toSwitch):
    # When we pass --noconsole flag to pyinstaller it sets the standard
    # streams to None and all the libs/functions that try to write on
    # those streams fail. E.g. tqdm fails in this case as it uses stderr
    # to show progress bar. In order to avoid this situation we use these
    # two lines which redirect the standard streams from console to the 
    # files. We need these to work only in case of GUI application and 
    # not in case of CLI application as we need output on console.
    if(toSwitch):
        sys.stdout = open('stdout.log', 'a') # Sets standard ouput 
        sys.stderr = open('stderr.log', 'a') # Sets standard error
    else:                            # Reset standard streams to their defaults
        sys.stdout = sys.__stdout__  # Restore standard output
        sys.stderr = sys.__stderr__  # Restore standard error
    # We are still using the stream switch even if don't pass --noconsole
    # flag as we detach the console in GUI mode and hence switching stream is 
    # required.

def toggle_console(show):
    """Show or hide the console window."""
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    if not show:
        user32.ShowWindow(kernel32.GetConsoleWindow(), 0)  # SW_HIDE
        kernel32.FreeConsole()

def main():
    # If running in CLI mode then don't switch streams and 
    # let the console remain open.
    # Else if running in GUI mode then switch the streams and
    # exit the console.
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        toggle_console(True)
        switch_standard_streams(False)
        run_cli()
    else:
        # temporarily disabled for debug, pls enable later
        # toggle_console(False)
        # switch_standard_streams(True) 
        run_gui()

if __name__ == '__main__':
    main()