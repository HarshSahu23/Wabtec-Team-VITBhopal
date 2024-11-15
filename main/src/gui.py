# gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSplitter, QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ErrorAnalyzerBackend import ErrorAnalyzerBackend

class ErrorAnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = ErrorAnalyzerBackend()
        self.swap_axes = False  # For swapping axes in the plot
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Error Analyzer')
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout(self)
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Enter comma-separated error descriptions')
        input_layout.addWidget(self.input_field)

        self.load_button = QPushButton('Load Errors')
        self.load_button.clicked.connect(self.load_errors)
        input_layout.addWidget(self.load_button)

        # Swap Axes Button
        self.swap_axes_button = QPushButton('Swap Axes')
        self.swap_axes_button.setCheckable(True)
        self.swap_axes_button.clicked.connect(self.toggle_axes)
        input_layout.addWidget(self.swap_axes_button)

        # Sorting ComboBox for Plot
        self.plot_sort_combo = QComboBox()
        self.plot_sort_combo.addItems(['Sort by Expectation', 'Sort by Frequency', 'Sort Alphabetically'])
        self.plot_sort_combo.currentIndexChanged.connect(self.update_plot_sorting)
        input_layout.addWidget(self.plot_sort_combo)

        main_layout.addLayout(input_layout)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left - Table
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(['Sort by Name', 'Sort by Expectation'])
        self.sort_combo.currentIndexChanged.connect(self.sort_table)
        left_layout.addWidget(self.sort_combo)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Error Code', 'Error Description', 'Frequency'])
        left_layout.addWidget(self.table)

        splitter.addWidget(left_widget)

        # Right - Plot
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)

        splitter.addWidget(right_widget)

        self.show()

    def load_errors(self):
        input_text = self.input_field.text()
        expected_errors = set(e.strip().upper() for e in input_text.split(',') if e.strip())
        self.backend.set_expected_errors(expected_errors)
        self.backend.process_data()
        self.update_table()
        self.update_plot()

    def sort_table(self):
        if self.sort_combo.currentText() == 'Sort by Name':
            self.backend.sort_by_name()
        else:
            self.backend.sort_by_expectation()
        self.update_table()

    def update_plot_sorting(self):
        current_sort = self.plot_sort_combo.currentText()
        if current_sort == 'Sort by Expectation':
            self.backend.sort_plot_data_by_expectation()
        elif current_sort == 'Sort by Frequency':
            self.backend.sort_plot_data_by_frequency()
        else:
            self.backend.sort_plot_data_alphabetically()
        self.update_plot()

    def toggle_axes(self):
        self.swap_axes = not self.swap_axes
        self.update_plot()

    def update_table(self):
        data = self.backend.get_table_data()
        self.table.setRowCount(len(data))
        for row, (code, desc, freq, color) in enumerate(data):
            code_item = QTableWidgetItem(code)
            desc_item = QTableWidgetItem(desc)
            freq_item = QTableWidgetItem(str(freq))

            # Set text color based on expectation
            for item in [code_item, desc_item, freq_item]:
                item.setForeground(color)

            self.table.setItem(row, 0, code_item)
            self.table.setItem(row, 1, desc_item)
            self.table.setItem(row, 2, freq_item)
        self.table.resizeColumnsToContents()

    def update_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Data for plotting
        error_descs, freqs, colors = self.backend.get_plot_data()
        positions = range(len(error_descs))

        if self.swap_axes:
            # Swap axes: Error Descriptions on y-axis
            ax.barh(positions, freqs, color=colors)
            ax.set_yticks(positions)
            ax.set_yticklabels(error_descs)
            ax.invert_yaxis()
            ax.set_xlabel('Frequency')
            ax.set_title('Error Frequencies')
        else:
            # Default axes: Error Descriptions on x-axis
            ax.bar(positions, freqs, color=colors)
            ax.set_xticks(positions)
            ax.set_xticklabels(error_descs, rotation=90)
            ax.set_ylabel('Frequency')
            ax.set_title('Error Frequencies')

        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ErrorAnalyzerGUI()
    sys.exit(app.exec_())