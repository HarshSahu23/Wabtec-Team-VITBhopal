# Wabtec Hackathon Project

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your configuration values.

## Project Structure
```
main/
├── Include/              # Package includes
├── src/                  # Source code
│   ├── __init__.py
│   ├── data/            # Data processing modules
│   ├── models/          # ML models
│   └── utils/           # Utility functions
├── tests/               # Test files
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore rules
├── README.md           # Project documentation
├── requirements.txt    # Project dependencies
└── setup.py           # Package configuration
```

## Development Guidelines
1. Always work in a virtual environment
2. Format code using black: `black .`
3. Sort imports using isort: `isort .`
4. Run tests before committing: `pytest`

## Contributing
1. Create a new branch for each feature
2. Follow PEP 8 style guide
3. Write tests for new features
4. Update documentation as needed