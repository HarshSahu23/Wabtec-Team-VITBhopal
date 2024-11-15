# error_analyzer_backend.py

import os
from collections import defaultdict
from PyQt5.QtGui import QColor

from ErrorAnalyzer import ErrorAnalyzer

class ErrorAnalyzerBackend:
    def __init__(self):
        self.expected_errors = set()
        self.result_data = []
        self.analyzer = ErrorAnalyzer()
        self.plot_data = []
        self.sort_plot_data_by_expectation()

    def set_expected_errors(self, expected_errors):
        self.expected_errors = expected_errors

    def process_data(self):
        # Process CSV files
        self.analyzer.error_frequencies = defaultdict(int)
        self.analyzer.error_codes = {}
        folder_path = "D:\\Harsh Data\\Coding\\Hackathon\\Wabtec Team VITBhopal\\resources\\csv\\"
        self.analyzer.analyze_folder(folder_path)
        self.categorize_errors()

    def categorize_errors(self):
        expected_seen = []
        expected_not_seen = []
        unexpected_seen = []

        for desc in self.expected_errors:
            if desc in self.analyzer.error_frequencies:
                code = self.analyzer.error_codes.get(desc, 'XXXX')
                freq = self.analyzer.error_frequencies[desc]
                expected_seen.append((code, desc, freq))
            else:
                expected_not_seen.append(('XXXX', desc, 0))

        for desc, freq in self.analyzer.error_frequencies.items():
            if desc not in self.expected_errors:
                code = self.analyzer.error_codes.get(desc, 'XXXX')
                unexpected_seen.append((code, desc, freq))

        self.result_data = []

        # Expected and found - black
        for code, desc, freq in expected_seen:
            self.result_data.append((code, desc, freq, QColor('black')))

        # Expected and not found - blue
        for code, desc, freq in expected_not_seen:
            self.result_data.append((code, desc, freq, QColor('blue')))

        # Not expected and found - red
        for code, desc, freq in unexpected_seen:
            self.result_data.append((code, desc, freq, QColor('red')))

        self.sort_by_expectation()
        self.prepare_plot_data()

    def sort_by_name(self):
        self.result_data.sort(key=lambda x: x[1])

    def sort_by_expectation(self):
        def expectation_sort(item):
            color = item[3]
            if color == QColor('black'):
                return 0
            elif color == QColor('blue'):
                return 1
            else:
                return 2
        self.result_data.sort(key=expectation_sort)

    def sort_by_frequency(self):
        self.result_data.sort(key=lambda x: x[2], reverse=True)

    def get_table_data(self):
        return self.result_data

    def prepare_plot_data(self):
        # Initialize plot data
        self.plot_data = self.result_data.copy()

    def sort_plot_data_by_expectation(self):
        self.sort_by_expectation()
        self.prepare_plot_data()

    def sort_plot_data_by_frequency(self):
        self.result_data.sort(key=lambda x: x[2], reverse=True)
        self.prepare_plot_data()

    def sort_plot_data_alphabetically(self):
        self.result_data.sort(key=lambda x: x[1])
        self.prepare_plot_data()

    def get_plot_data(self):
        error_descs = [desc for _, desc, _, _ in self.plot_data]
        freqs = [freq for _, _, freq, _ in self.plot_data]
        colors = []
        for _, _, _, color in self.plot_data:
            if color == QColor('black'):
                colors.append('black')
            elif color == QColor('blue'):
                colors.append('blue')
            else:
                colors.append('red')
        return error_descs, freqs, colors