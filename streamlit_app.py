"""Life Pilot - Streamlit Chat Frontend for ADK Agent."""
import json
import requests
import streamlit as st
import uuid

# --- Page Config ---
st.set_page_config(
    page_title="Life Pilot - Your AI Life Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Constants ---
ADK_URL = "http://127.0.0.1:8000"
APP_NAME = "job_application_agent"

# --- Custom CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        color: white;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #e0e0e0;
        font-size: 1rem;
    }
    .quick-action {
        background: #1a1a2e;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 12px 16px;
        cursor: pointer;
        transition: all 0.2s;
        text-align: center;
    }
    .quick-action:hover {
        border-color: #667eea;
        background: #16213e;
    }
    .sidebar-section {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "user_id" not in st.session_state:
    st.session_state.user_id = "streamlit_user"


def create_session():
    """Create a new ADK session."""
    try:
        resp = requests.post(
            f"{ADK_URL}/apps/{APP_NAME}/users/{st.session_state.user_id}/sessions",
            json={},
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            st.session_state.session_id = data["id"]
            return True
    except requests.ConnectionError:
        return False
    return False


def send_message(message: str) -> str:
    """Send a message to the ADK agent and get the response."""
    if not st.session_state.session_id:
        if not create_session():
            return "Could not connect to the ADK server. Make sure it's running with `adk web .`"

    try:
        resp = requests.post(
            f"{ADK_URL}/run_sse",
            json={
                "app_name": APP_NAME,
                "user_id": st.session_state.user_id,
                "session_id": st.session_state.session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}],
                },
            },
            timeout=60,
            stream=True,
        )

        full_response = ""
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data: "):
                try:
                    data = json.loads(line[6:])
                    if "error" in data:
                        error_msg = data["error"]
                        if "RateLimitError" in error_msg:
                            return full_response + "\n\n*(Rate limit hit - wait 30s and try again)*" if full_response else "Rate limit reached. Please wait 30 seconds and try again."
                        return f"Error: {error_msg}"
                    if "content" in data and "parts" in data["content"]:
                        for part in data["content"]["parts"]:
                            if "text" in part:
                                full_response = part["text"]
                except json.JSONDecodeError:
                    continue

        return full_response if full_response else "No response received. Try again."

    except requests.ConnectionError:
        return "Cannot connect to ADK server. Run `adk web .` in your project directory first."
    except requests.Timeout:
        return "Request timed out. The server might be busy. Try again."


# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🚀 Life Pilot")
    st.markdown("Your personal AI life assistant")
    st.divider()

    # Quick Actions
    st.markdown("#### ⚡ Quick Actions")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Job Search", use_container_width=True):
            st.session_state.quick_action = "Search for software developer jobs in India"
        if st.button("📊 DSA Plan", use_container_width=True):
            st.session_state.quick_action = "Give me a 4 week DSA study plan"
        if st.button("😊 Log Mood", use_container_width=True):
            st.session_state.quick_action = "I want to log my mood"
        if st.button("💰 Expenses", use_container_width=True):
            st.session_state.quick_action = "Show my expense summary for this month"

    with col2:
        if st.button("📝 Resume Tips", use_container_width=True):
            st.session_state.quick_action = "Give me resume tips"
        if st.button("🎯 Skill Gap", use_container_width=True):
            st.session_state.quick_action = "Analyze my skills for full stack developer"
        if st.button("✅ My Tasks", use_container_width=True):
            st.session_state.quick_action = "Show my current tasks"
        if st.button("💪 Motivate Me", use_container_width=True):
            st.session_state.quick_action = "Give me some motivation"

    st.divider()

    # More actions
    st.markdown("#### 📋 More")
    col3, col4 = st.columns(2)
    with col3:
        if st.button("🎤 Interview Prep", use_container_width=True):
            st.session_state.quick_action = "Give me interview questions for Python backend developer"
        if st.button("📓 Journal", use_container_width=True):
            st.session_state.quick_action = "Give me a journal prompt"
        if st.button("🫁 Breathing", use_container_width=True):
            st.session_state.quick_action = "Guide me through a breathing exercise"
    with col4:
        if st.button("💼 Applications", use_container_width=True):
            st.session_state.quick_action = "Show my job applications"
        if st.button("🏆 Weekly Report", use_container_width=True):
            st.session_state.quick_action = "Give me my weekly progress report"
        if st.button("🏦 Savings", use_container_width=True):
            st.session_state.quick_action = "Show my savings goals"

    st.divider()

    # Reset
    if st.button("🔄 New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

    st.markdown("---")
    st.caption("Built with Google ADK + Groq + Streamlit")


# --- Main Content ---
st.markdown("""
<div class="main-header">
    <h1>🚀 Life Pilot</h1>
    <p>Career • Wellness • Planning • Finance — All in one AI assistant</p>
</div>
""", unsafe_allow_html=True)

# Show welcome message if no messages
if not st.session_state.messages:
    st.markdown("""
    **Hey there! I'm Life Pilot, your personal AI assistant.** Here's what I can help with:

    | 💼 **Career** | 🧘 **Wellness** | 📋 **Planning** | 💰 **Finance** |
    |---|---|---|---|
    | Job search across 6 platforms | Mood tracking & history | Daily task management | Expense tracking |
    | DSA study roadmaps | Breathing exercises | Habit tracking with streaks | Budget management |
    | Interview prep (tech + behavioral) | Journaling & prompts | Weekly goals | Savings goals |
    | Skill gap analysis | Stress management tips | Progress reports | Financial summaries |
    | Resume & portfolio advice | Motivational quotes | Schedule planning | Income tracking |

    **Try typing something or click a quick action button in the sidebar!**
    """)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🚀" if msg["role"] == "assistant" else "👤"):
        st.markdown(msg["content"])

# Handle quick actions
if "quick_action" in st.session_state and st.session_state.quick_action:
    prompt = st.session_state.quick_action
    st.session_state.quick_action = None

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🚀"):
        with st.spinner("Thinking..."):
            response = send_message(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Chat input
if prompt := st.chat_input("Ask me anything - jobs, mood, tasks, finances..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🚀"):
        with st.spinner("Thinking..."):
            response = send_message(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
