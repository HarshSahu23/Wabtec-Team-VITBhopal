# gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSplitter, QScrollArea, QCheckBox, QButtonGroup,
    QRadioButton, QGroupBox, QMainWindow, QMenuBar, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.backend.data_handler import DataHandler

class ErrorAnalyzerGUI(QMainWindow):  # Change from QWidget to QMainWindow
    def __init__(self):
        super().__init__()
        self.data_handler = None  # Initialize as None
        self.selected_errors = set()
        self.current_chart_type = 'bar'
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Error Analyzer')
        self.setGeometry(100, 100, 1200, 800)

        # Create menu bar
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        import_action = file_menu.addAction('Import Folder')
        import_action.triggered.connect(self.import_folder)

        # Help menu
        help_menu = menubar.addMenu('Help')
        help_action = help_menu.addAction('Help')
        help_action.triggered.connect(self.show_help)

        # Credits menu
        credits_action = menubar.addAction('Credits')
        credits_action.triggered.connect(self.show_credits)

        # Central widget to hold the main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create the main content widget
        self.main_content_widget = QWidget()
        self.main_content_layout = QHBoxLayout(self.main_content_widget)
        
        # Create placeholder widget
        self.placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout(self.placeholder_widget)
        placeholder_label = QLabel("Please select a folder containing CSV files\nFile → Import Folder")
        placeholder_label.setStyleSheet("font-size: 24px;")
        placeholder_label.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(placeholder_label)
        
        # Add placeholder to main layout initially
        main_layout.addWidget(self.placeholder_widget)
        main_layout.addWidget(self.main_content_widget)
        self.main_content_widget.hide()  # Hide content initially

        # Setup main content
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # Chart type selection
        chart_group = QGroupBox("Chart Type")
        chart_layout = QHBoxLayout()
        self.bar_radio = QRadioButton("Bar Chart")
        self.pie_radio = QRadioButton("Pie Chart")
        self.bar_radio.setChecked(True)
        self.bar_radio.toggled.connect(self.update_chart)
        self.pie_radio.toggled.connect(self.update_chart)
        chart_layout.addWidget(self.bar_radio)
        chart_layout.addWidget(self.pie_radio)
        chart_group.setLayout(chart_layout)
        left_layout.addWidget(chart_group)

        # Scrollable area for checkboxes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.checkbox_layout = QVBoxLayout(scroll_content)

        scroll.setWidget(scroll_content)
        left_layout.addWidget(scroll)

        # Select/Deselect All buttons
        btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        deselect_all_btn = QPushButton("Deselect All")
        select_all_btn.clicked.connect(self.select_all)
        deselect_all_btn.clicked.connect(self.deselect_all)
        btn_layout.addWidget(select_all_btn)
        btn_layout.addWidget(deselect_all_btn)
        left_layout.addLayout(btn_layout)

        # Right side - Plot
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)

        # Add widgets to main content layout
        self.main_content_layout.addWidget(left_widget, stretch=1)
        self.main_content_layout.addWidget(right_widget, stretch=2)

        self.show()

    def import_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            try:
                self.data_handler = DataHandler(folder_path)
                if len(self.data_handler.ecl_freq_summary) == 0:
                    QMessageBox.warning(self, "Warning", "No CSV files found in the selected folder or files are empty!")
                    return
                
                # Switch from placeholder to main content
                self.placeholder_widget.hide()
                self.main_content_widget.show()
                self.refresh_ui()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")

    def refresh_ui(self):
        """Refresh the UI after loading new data"""
        # Clear existing checkboxes
        while self.checkbox_layout.count():
            child = self.checkbox_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.data_handler and len(self.data_handler.ecl_freq_summary) > 0:
            # Add new checkboxes
            for _, row in self.data_handler.ecl_freq_summary.iterrows():
                checkbox = QCheckBox(f"{row['Description']} ({row['Frequency']})")
                checkbox.stateChanged.connect(lambda state, cb=checkbox: self.on_checkbox_change(state, cb))
                self.checkbox_layout.addWidget(checkbox)

        self.selected_errors.clear()
        self.update_chart()

    def show_help(self):
        help_text = """
        Error Analyzer Help:
        
        1. Import Data:
           - Click File -> Import Folder
           - Select a folder containing CSV files
        
        2. Analyze Errors:
           - Use checkboxes to select errors
           - Switch between Bar and Pie charts
           - Use Select All/Deselect All for quick selection
        """
        QMessageBox.information(self, "Help", help_text)

    def show_credits(self):
        credits_text = """
        Error Analyzer
        Version 1.0.0
        
        Developed by:
        Akhand Pratap Tiwari
        Aryan Rana
        Harsh Sahu
        Elson Nag
        
        Under the guidance of:
        Wabtec Corporation 

        © 2024 Wabtec Corporation
        """
        QMessageBox.information(self, "Credits", credits_text)

    def on_checkbox_change(self, state, checkbox=None):
        """Handle individual checkbox changes"""
        if checkbox:  # Single checkbox change
            error_desc = checkbox.text().split(" (")[0]
            if state == Qt.Checked:
                self.selected_errors.add(error_desc)
            else:
                self.selected_errors.discard(error_desc)
            self.update_chart()

    def select_all(self):
        self._set_all_checkboxes(True)

    def deselect_all(self):
        self._set_all_checkboxes(False)

    def _set_all_checkboxes(self, state):
        """Set all checkboxes without triggering individual updates"""
        self.selected_errors.clear()
        # Temporarily disconnect checkbox signals
        for i in range(self.checkbox_layout.count()):
            checkbox = self.checkbox_layout.itemAt(i).widget()
            checkbox.blockSignals(True)
            checkbox.setChecked(state)
            if state:
                error_desc = checkbox.text().split(" (")[0]
                self.selected_errors.add(error_desc)
            checkbox.blockSignals(False)

        # Update chart once after all checkboxes are set
        self.update_chart()

    def update_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if not self.data_handler or len(self.selected_errors) == 0:
            ax.text(0.5, 0.5, 'No data to display\nSelect errors to visualize', 
                   ha='center', va='center')
            self.canvas.draw()
            return

        # Filter data based on selected errors
        filtered_data = self.data_handler.ecl_freq_summary[
            self.data_handler.ecl_freq_summary['Description'].isin(self.selected_errors)
        ]

        if not filtered_data.empty:
            if self.bar_radio.isChecked():
                # Bar chart
                ax.bar(range(len(filtered_data)), filtered_data['Frequency'])
                ax.set_xticks(range(len(filtered_data)))
                ax.set_xticklabels(filtered_data['Description'], rotation=45, ha='right')
                ax.set_ylabel('Frequency')
                self.figure.subplots_adjust(bottom=0.2)
            else:
                # Pie chart
                ax.pie(filtered_data['Frequency'], labels=filtered_data['Description'],
                      autopct='%1.1f%%')

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ErrorAnalyzerGUI()
    sys.exit(app.exec_())