# Life Pilot - Your Personal AI Life Assistant

AI-powered personal assistant built with Google ADK (Agent Development Kit) that handles career prep, job search, wellness, daily planning, and finance management. Features a Streamlit chat frontend and 31 integrated tools.

## Features

### Career & Job Search
- **Job Search** - Direct links from LinkedIn, Indeed, Naukri, Glassdoor, Wellfound, Internshala
- **DSA Roadmap** - Dynamic 1-16 week study plans covering 15 topics
- **Resume Tips** - ATS-friendly advice categorized by section
- **Portfolio Ideas** - Stack-specific project suggestions (Python/JS/Java)
- **Interview Prep** - Technical, system design, and behavioral questions with STAR method
- **Skill Gap Analysis** - Readiness scoring for 6+ roles with learning paths
- **Application Tracker** - Track job applications with status updates

### Wellness & Mental Health
- **Mood Tracking** - Log and view mood history with pattern analysis
- **Journaling** - Guided journal entries with prompts
- **Breathing Exercises** - Box breathing, 4-7-8, and energizing techniques
- **Motivation** - Curated quotes and affirmations
- **Weekly Check-in** - Mental health self-assessment

### Daily Planning
- **Task Management** - Add, complete, and list tasks with priorities
- **Habit Tracker** - Track daily habits with streak calculation
- **Weekly Goals** - Set and track weekly goals by category
- **Progress Reports** - Comprehensive weekly progress summaries

### Finance Management
- **Expense Tracking** - Track spending across 10 categories
- **Income Tracking** - Log salary, freelance, and other income
- **Budget Management** - Set budgets with category breakdowns and overspend warnings
- **Savings Goals** - Create and track savings goals with progress bars
- **Financial Summary** - Overview with savings rate and advice

## Prerequisites

- Python 3.10+
- A free LLM API key (see setup options below)

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
```

### 4. Set up environment variables

Copy the example file and add your API keys:

```bash
cp .env.example .env
```

#### Option A: SambaNova (Recommended - Free, Fast, 70B Model)

1. Get a free API key from [SambaNova Cloud](https://cloud.sambanova.ai/apis)
2. Edit `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
SAMBANOVA_API_KEY=your_sambanova_key_here
OPENAI_API_KEY=your_sambanova_key_here
OPENAI_API_BASE=https://api.sambanova.ai/v1
MODEL_NAME=openai/Meta-Llama-3.3-70B-Instruct
```

**Why this works:** SambaNova provides an OpenAI-compatible API endpoint. By setting `OPENAI_API_KEY` and `OPENAI_API_BASE`, LiteLLM routes requests through its OpenAI provider to SambaNova's servers. The `openai/` prefix in `MODEL_NAME` tells LiteLLM to use the OpenAI-compatible format.

#### Option B: Google Gemini (Free 1M TPM)

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
2. Edit `.env`:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
MODEL_NAME=gemini-2.0-flash
```

#### Option C: Groq (Free, Fast but Rate Limited)

1. Get a free API key from [Groq Console](https://console.groq.com/keys)
2. Edit `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=groq/llama-3.1-8b-instant
```

> **Note:** `GOOGLE_API_KEY` is always required by Google ADK even when using a different LLM provider.

## Usage

### Start the ADK Backend

```bash
adk web .
```

This starts the agent server at http://127.0.0.1:8000.

### Start the Streamlit Frontend

In a separate terminal:

```bash
streamlit run streamlit_app.py --server.headless true
```

Open http://localhost:8501 in your browser.

### Example Prompts

**Career:**
- "Find me Python developer jobs in Bangalore"
- "Give me a 4-week DSA study plan"
- "Interview questions for backend developer"
- "Analyze my skills for full stack developer"

**Wellness:**
- "I want to log my mood"
- "Guide me through a breathing exercise"
- "Give me some motivation"
- "Give me a journal prompt"

**Planning:**
- "Add task: Complete LeetCode daily challenge"
- "Show my current tasks"
- "Give me my weekly progress report"

**Finance:**
- "Add expense 500 food lunch"
- "Show my expense summary for this month"
- "Set savings goal Emergency Fund 100000"
- "Show my financial summary"

## Running Tests

```bash
pytest tests/ -v
```

All 138 tests should pass.

## Project Structure

```
adk_job_application_advisor/
├── job_application_agent/
│   ├── __init__.py
│   ├── agent.py                    # Main agent (31 tools, Life Pilot persona)
│   └── tools/
│       ├── __init__.py
│       ├── job_search.py           # Job search across 6 platforms
│       ├── career_tools.py         # DSA roadmap, resume tips, portfolio ideas
│       ├── interview_prep.py       # Interview question generator
│       ├── skill_analysis.py       # Skill gap analyzer
│       ├── application_tracker.py  # Job application tracker
│       ├── wellness.py             # Mood, journal, breathing, motivation
│       ├── daily_planner.py        # Tasks, habits, goals, progress
│       └── finance.py              # Expenses, income, budget, savings
├── tests/
│   ├── test_job_search.py
│   ├── test_career_tools.py
│   ├── test_interview_prep.py
│   ├── test_skill_analysis.py
│   ├── test_application_tracker.py
│   ├── test_wellness.py
│   ├── test_daily_planner.py
│   └── test_finance.py
├── streamlit_app.py                # Streamlit chat frontend
├── requirements.txt
├── .env.example                    # Environment template
├── .env                            # Your API keys (not committed)
└── README.md
```

## Tech Stack

- **Google ADK** - Agent Development Kit for building AI agents with tool-calling
- **LiteLLM** - Multi-provider LLM abstraction (routes to SambaNova/Gemini/Groq)
- **Streamlit** - Chat frontend with quick action buttons
- **SambaNova** - LLaMA 3.3 70B inference (free tier, OpenAI-compatible API)
- **Python 3.10+**
- **pytest** - 138 unit tests

## Troubleshooting

### Rate Limit Error
If using Groq free tier, wait 30 seconds between requests. Consider switching to SambaNova (Option A) for higher limits.

### Model Not Found
Make sure your `MODEL_NAME` in `.env` matches the provider format:
- SambaNova: `openai/Meta-Llama-3.3-70B-Instruct`
- Gemini: `gemini-2.0-flash`
- Groq: `groq/llama-3.1-8b-instant`

### Cannot Connect to ADK Server
Make sure the ADK backend is running (`adk web .`) before starting Streamlit.

### Port Already in Use
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
