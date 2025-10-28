# LLM Learning Project

A Python project for learning and experimenting with Large Language Models (LLMs).

## Setup

### 1. Run the setup script

```bash
./setup.sh
```

### 2. VSCode/Cursor Setup

1. **Install Python Extension** (if not already installed):
   - Open VSCode/Cursor
   - Go to Extensions (Cmd+Shift+X)
   - Search for "Python" and install the official Python extension by Microsoft

2. **Install Jupyter Extension** (if not already installed):
   - Search for "Jupyter" and install the Jupyter extension by Microsoft

3. **Select Python Interpreter**:
   - Open Command Palette (Cmd+Shift+P)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from your virtual environment: `./venv/bin/python`

4. **Open Notebook**:
   - Navigate to `notebooks/1-transformer.ipynb`
   - Click "Select Kernel" and choose your virtual environment
   - Start coding!

## Usage

Run Jupyter notebook:
```bash
jupyter notebook
```

## Project Structure

```
.
├── requirements.txt  # Project dependencies
├── setup.sh         # Setup script
├── README.md        # Project documentation
├── .gitignore       # Git ignore file
└── notebooks/       # Jupyter notebooks for experiments
    └── 1-transformer.ipynb
```


