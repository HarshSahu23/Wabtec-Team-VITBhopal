import sys
from PyQt5.QtWidgets import QApplication
from src.frontend.gui import ErrorAnalyzerGUI

def main():
    app = QApplication(sys.argv)
    gui = ErrorAnalyzerGUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()