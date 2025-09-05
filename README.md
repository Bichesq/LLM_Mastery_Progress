# LLM Mastery

A Python project demonstrating integration with multiple Large Language Model (LLM) APIs, including Sarvam AI, OpenAI-compatible interfaces, and Ollama for local model inference.

## 🚀 Features

- **Sarvam AI Integration**: Direct integration with Sarvam AI's native Python SDK
- **OpenAI-Compatible Interface**: Use Sarvam AI through OpenAI-compatible API calls
- **Ollama Support**: Local LLM inference using Ollama
- **Rich Console Output**: Beautiful formatted output using Rich library
- **Environment Configuration**: Secure API key management with dotenv

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Sarvam AI API key (get one from [dashboard.sarvam.ai](https://dashboard.sarvam.ai))
- Ollama installed locally (optional, for local model inference)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd llm-mastery
```

### 2. Virtual Environment Setup

**Create a virtual environment:**

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

**Activate the virtual environment:**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**Verify activation:**
You should see `(venv)` at the beginning of your command prompt when the virtual environment is active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install dependencies manually:

```bash
pip install openai sarvamai python-dotenv rich beautifulsoup4 requests ollama
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env  # macOS/Linux
# or create manually on Windows
```

Add your API keys to the `.env` file:

```env
SARVAM_API_KEY=your_sarvam_api_key_here
```

## 📁 Project Structure

```
llm-mastery/
├── venv/                    # Virtual environment (do not commit)
├── sarvam_via_openAI.py    # Sarvam AI via OpenAI-compatible interface
├── testsarvam.py           # Direct Sarvam AI SDK usage
├── test.py                 # Ollama integration examples
├── testsarvamai.py         # Additional Sarvam AI tests (gitignored)
├── .env                    # Environment variables (do not commit)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🎯 Usage Examples

### Sarvam AI via OpenAI Interface

```python
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("SARVAM_API_KEY"),
    base_url="https://api.sarvam.ai/v1"
)

response = client.chat.completions.create(
    model="sarvam-m",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain AI in simple terms."}
    ]
)

print(response.choices[0].message.content)
```

### Direct Sarvam AI SDK

```python
from sarvamai import SarvamAI
import os
from dotenv import load_dotenv

load_dotenv()

client = SarvamAI(
    api_subscription_key=os.getenv("SARVAM_API_KEY")
)

response = client.chat.completions(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ]
)

print(response.choices[0].message.content)
```

### Ollama Local Models

```python
from openai import OpenAI

client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)

response = client.chat.completions.create(
    model="llama3.2:1b",
    messages=[
        {"role": "user", "content": "Explain neural networks"}
    ]
)

print(response.choices[0].message.content)
```

## 🔧 Virtual Environment Management

### Deactivating the Virtual Environment

```bash
deactivate
```

### Reactivating the Virtual Environment

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Updating Dependencies

```bash
# Activate virtual environment first
pip install --upgrade package_name

# Or update all packages
pip list --outdated
pip install --upgrade package_name1 package_name2
```

### Generating Requirements File

```bash
pip freeze > requirements.txt
```

### Removing Virtual Environment

```bash
# Deactivate first
deactivate

# Remove the directory
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows
```

## 🌟 Available Models

### Sarvam AI Models
- `sarvam-m`: General purpose model

### Ollama Models (Local)
- `llama3.2:1b`: Lightweight Llama model
- Other models available through Ollama

## 🔒 Security Notes

- Never commit your `.env` file or API keys to version control
- The `.gitignore` file is configured to exclude sensitive files
- Keep your virtual environment local (already in `.gitignore`)

## 🐛 Troubleshooting

### Virtual Environment Issues

**Problem**: `venv\Scripts\activate` not found
**Solution**: Ensure you created the virtual environment in the correct directory

**Problem**: Permission denied on activation
**Solution**: 
```bash
# Windows PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Problem**: Python not found
**Solution**: Ensure Python is installed and added to PATH

### API Issues

**Problem**: Authentication errors
**Solution**: Verify your API key in the `.env` file

**Problem**: Connection errors
**Solution**: Check your internet connection and API endpoint URLs

## 📚 Dependencies

- `openai`: OpenAI Python client library
- `sarvamai`: Official Sarvam AI Python SDK
- `python-dotenv`: Environment variable management
- `rich`: Rich text and beautiful formatting
- `requests`: HTTP library
- `beautifulsoup4`: HTML parsing
- `ollama`: Ollama Python client

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Useful Links

- [Sarvam AI Documentation](https://docs.sarvam.ai/)
- [Sarvam AI Dashboard](https://dashboard.sarvam.ai)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Ollama Documentation](https://ollama.ai/docs)
- [Rich Library Documentation](https://rich.readthedocs.io/)
