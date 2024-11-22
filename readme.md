# Error Analyzer 📊

<a href="https://www.wabteccorp.com/" target="_blank">
  <img src="https://www.wabteccorp.com/themes/custom/wabtec/images/Wabtec-logo-White.svg" alt="Wabtec" width="200" height="100"/>
</a>
<p></p>

> A Python-based application for analyzing error codes from CSV files with interactive visualizations.

## Features ✨

- Interactive GUI built with PyQt5
- Real-time error code analysis
- Dynamic visualization using matplotlib
- CSV file processing and management
- Comprehensive error frequency reporting

## Installation 🚀

### Prerequisites

- Python 3.8+
- Git

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/HarshSahu23/Wabtec-Team-VITBhopal.git
cd Wabtec-Team-VITBhopal
```

2. Set up virtual environment:
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure 📁

```
ErrorAnalyzer/
├── csv/                  # Error log CSV files
├── exploratory/          # Notebook to analyse csv data
├── src/
│   ├── backend/         # Core analysis logic
│   └── frontend/        # PyQt5 GUI implementation
├── main.py              # Application entry point
├── requirements.txt     # Dependencies
└── guidelines.txt       # Rules to follow while contributing
```

## Usage 💡

1. Launch the application:
```bash
python main.py
```

2. Process error logs:
   - Place CSV files in the `csv/` directory
   - Input expected error descriptions
   - View analysis results and visualizations

OR 

## Use the GUI 💻
  <br/>

  ### A) Import the folder :
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/fd1bf64a8bfb385290acbd3b7e065a4ddd4d6560/assets/SS2.png" alt="Screenshot 1" width="400"/>
  </p>

  ### B) Select the folder containing csv files :
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/fd1bf64a8bfb385290acbd3b7e065a4ddd4d6560/assets/SS3.png" alt="Screenshot 2" width="400"/>
  </p>

  ### C) Wait for the files to be read ... ⌛
  
  ### D) View the Bar Chart and Pie Chart:
  <p align="left">
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/fd1bf64a8bfb385290acbd3b7e065a4ddd4d6560/assets/SS4.png" alt="Screenshot 3" width="400" height="250" style="display: inline-block; margin-right: 10px;"/>
    <img src="https://github.com/HarshSahu23/Wabtec3_BrakesGUI_shared/blob/fd1bf64a8bfb385290acbd3b7e065a4ddd4d6560/assets/SS5.png" alt="Screenshot 4" width="400" height="250" style="display: inline-block;"/>
  </p>


## Development 🛠️

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use descriptive variable and function names
- Include docstrings and comments where appropriate

### Testing

```bash
# Run tests
python -m pytest tests/

# Check code coverage
python -m pytest --cov=src tests/
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes:
```bash
git commit -m 'Add amazing feature'
```

4. Push to your branch:
```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

### Contribution Guidelines

- Write clear commit messages
- Include tests for new features
- Update documentation as needed
- Submit PRs to the `develop` branch

## License 📝

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
Made with ❤️ by Team ^_^ - Exceed 3.0
</div>
