# ADK Job Application Advisor 🚀

AI-powered job search assistant built with Google ADK (Agent Development Kit) and Groq LLaMA. Get direct job links from LinkedIn, Indeed, Naukri, Glassdoor plus resume tips and DSA prep.

## Features

- 🔍 **Job Search** - Get direct URLs from LinkedIn, Indeed, Naukri, Glassdoor
- 📄 **Resume Tips** - ATS-friendly resume advice
- 💻 **DSA Roadmap** - Structured coding prep plan
- 🎨 **Portfolio Ideas** - Project suggestions for your tech stack

## Prerequisites

- Python 3.10+
- [Groq API Key](https://console.groq.com/keys) (free tier available)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/padmashri23/adk_job_application_advisor.git
cd adk_job_application_advisor
```

### 2. Create virtual environment

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install "google-adk[extensions]"
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/keys

### 5. Enable models in Groq Console

Go to https://console.groq.com/settings/project/limits and enable `llama-3.1-8b-instant` model.

## Usage

### Start the ADK Web Server

```bash
adk web
```

Open http://127.0.0.1:8000 in your browser.

### Example Prompts

**Job Search:**
- "Find me Python developer jobs in Bangalore"
- "Search for data analyst jobs in Mumbai"

**Resume Help:**
- "Give me resume tips"

**Coding Prep:**
- "Give me a 4-week DSA study plan"

**Portfolio:**
- "What Python projects should I build for my portfolio?"

## Project Structure

```
adk_job_application_advisor/
├── job_application_agent/
│   ├── __init__.py
│   ├── agent.py              # Main agent definition
│   └── tools/
│       ├── __init__.py
│       ├── job_search.py     # Job search tool
│       └── career_tools.py   # DSA, resume, portfolio tools
├── requirements.txt
├── .env                      # Your API keys (not committed)
└── README.md
```

## Tech Stack

- **Google ADK** - Agent Development Kit for building AI agents
- **Groq** - Fast LLM inference (LLaMA 3.1 8B)
- **LiteLLM** - Multi-provider LLM support
- **Python 3.10+**

## Troubleshooting

### Rate Limit Error
If you see "rate limit exceeded", wait 30 seconds and try again. The free tier has limits.

### Model Not Found
Make sure you've enabled the model in Groq Console: https://console.groq.com/settings/project/limits

### Port 8000 in use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

## License

MIT

## Author

Built by [padmashri23](https://github.com/padmashri23)
