"""
My Study Buddy - AI Study Engine
Complete with Onboarding, Login/Signup, and All Features
Compatible with Streamlit 1.28.0 | Python 3.11.9
Deployed at: https://ai-study-engine.onrender.com/
"""

import streamlit as st
import json
import os
import re
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"
ENV_PATH = BASE_DIR / ".env"

from dotenv import load_dotenv

load_dotenv(dotenv_path=ENV_PATH)

def get_db_connection():
    """Get database connection using absolute path."""
    return sqlite3.connect(str(DB_PATH))

def init_database():
    """Initialize SQLite database for user storage."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_user(email: str, name: str, password_hash: str) -> bool:
    """Add a new user to the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)',
            (email, name, password_hash)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(email: str) -> dict:
    """Get user by email."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT email, name, password_hash FROM users WHERE email = ?', (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"email": row[0], "name": row[1], "password": row[2]}
    return None

def get_all_users() -> list:
    """Get all registered users (for admin view)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, password_hash, created_at FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows

init_database()

st.set_page_config(
    page_title="My Study Buddy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Main background */
    .stApp { 
        background-color:
    }
    
    .main .block-container { 
        padding-top: 2rem; 
        max-width: 1200px; 
    }
    
    /* ALL TEXT IN MAIN AREA - DARK */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color:
    }
    
    .main p, .main span, .main label, .main div {
        color:
    }
    
    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown span {
        color:
    }
    
    /* Headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color:
    }
    
    /* Text area labels */
    .stTextArea label, .stTextInput label, .stSelectbox label {
        color:
        font-weight: 600 !important;
    }
    
    /* Text area placeholder */
    .stTextArea textarea::placeholder {
        color:
    }
    
    /* Text inside text areas */
    .stTextArea textarea, .stTextInput input {
        color:
        background-color: white !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        color:
        background-color: white !important;
    }
    
    /* Purple buttons */
    .stButton > button {
        background: linear-gradient(135deg,
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg,
        color: white !important;
    }
    
    /* Feature boxes */
    .feature-box {
        background: white !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .feature-box h4 {
        color:
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    
    .feature-box p {
        color:
        margin: 0;
        font-size: 0.95rem;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        color:
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .sub-title {
        text-align: center;
        color:
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Page titles */
    .page-title {
        color:
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .page-desc {
        color:
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Section headers */
    .section-header {
        color:
        font-weight: 600;
        font-size: 1.1rem;
        margin: 1rem 0 0.5rem 0;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color:
        background-color: white !important;
        border-radius: 8px !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color:
        color: white !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        color:
        background-color:
        font-weight: 600;
    }
    
    .streamlit-expanderContent {
        color:
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color:
    }
    
    [data-testid="stMetricLabel"] {
        color:
    }
    
    /* Radio buttons */
    .stRadio > label {
        color:
        font-weight: 600 !important;
    }
    
    .stRadio > div {
        color:
    }
    
    /* Number input */
    .stNumberInput label {
        color:
        font-weight: 600 !important;
    }
    
    .stNumberInput input {
        color:
        background-color: white !important;
    }
    
    /* Alerts/info boxes */
    .stAlert {
        color:
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color:
    }
    
    [data-testid="stSidebar"] * {
        color:
    }
    
    /* Hide default elements */
    footer {visibility: hidden;}
    
    /* Spinner text */
    .stSpinner > div {
        color:
    }
    
    /* Onboarding card */
    .onboarding-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    
    .onboarding-title {
        color:
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .onboarding-text {
        color:
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    
    /* Auth card */
    .auth-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    
    .auth-title {
        color:
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .auth-subtitle {
        color:
        font-size: 0.9rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Welcome badge */
    .welcome-badge {
        background: linear-gradient(135deg,
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    /* Skip button */
    .skip-btn {
        color:
        font-size: 0.9rem;
        text-decoration: underline;
        cursor: pointer;
    }
    
    /* Dots indicator */
    .dots-container {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin: 1rem 0;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color:
    }
    
    .dot.active {
        background-color:
    }
</style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'onboarding_complete' not in st.session_state:
    st.session_state.onboarding_complete = False
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 0
if 'users_db' not in st.session_state:
    st.session_state.users_db = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "splash"

def hash_password(password):
    """Hash password for storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def robot_svg(size=100):
    """Return robot mascot SVG."""
    scale = size / 100
    return f"""
    <div style="text-align: center;">
        <svg width="{int(120*scale)}" height="{int(140*scale)}" viewBox="0 0 120 140" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="60" cy="12" r="8" fill="#8B7EC8"/>
            <rect x="57" y="18" width="6" height="15" fill="#8B7EC8"/>
            <rect x="20" y="30" width="80" height="60" rx="12" fill="#B8ACE0"/>
            <rect x="25" y="35" width="70" height="50" rx="8" fill="#E8E4F0"/>
            <circle cx="45" cy="55" r="10" fill="white"/>
            <circle cx="75" cy="55" r="10" fill="white"/>
            <circle cx="45" cy="55" r="5" fill="#2D2D2D"/>
            <circle cx="75" cy="55" r="5" fill="#2D2D2D"/>
            <rect x="40" y="72" width="40" height="6" rx="3" fill="#2D2D2D"/>
            <rect x="30" y="95" width="60" height="40" rx="8" fill="#8B7EC8"/>
            <rect x="10" y="100" width="18" height="8" rx="4" fill="#B8ACE0"/>
            <rect x="92" y="100" width="18" height="8" rx="4" fill="#B8ACE0"/>
        </svg>
    </div>
    """

def dots_indicator(current, total):
    """Return dots indicator HTML."""
    dots = ""
    for i in range(total):
        active = "active" if i == current else ""
        dots += f'<div class="dot {active}"></div>'
    return f'<div class="dots-container">{dots}</div>'

class AIProvider:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        
    def is_configured(self):
        return bool(self.groq_key)
    
    def get_provider_name(self):
        return "Groq (LLaMA 3.3 70B)"
    
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        from groq import Groq
        
        
        client = Groq(api_key=self.groq_key)
        
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=4096
            )
            
            result = response.choices[0].message.content
            
            return result
            
        except Exception as e:
            raise e

def extract_json(text: str) -> dict:
    """Extract JSON from AI response - handles multiple formats."""
    
    text = text.strip()
    
    try:
        return json.loads(text)
    except:
        pass
    
    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except:
            pass
    
    match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except:
            pass
    
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except:
            json_str = json_str.replace('\n', ' ').replace('\r', '')
            try:
                return json.loads(json_str)
            except:
                pass
    
    match = re.search(r'\[[\s\S]*\]', text)
    if match:
        try:
            return {"items": json.loads(match.group(0))}
        except:
            pass
    
    questions = []
    q_matches = re.findall(r'(?:Q\d+|Question\s*\d*)[:\.]?\s*(.+?)(?=(?:Q\d+|Question|A\d+|Answer|$))', text, re.IGNORECASE | re.DOTALL)
    a_matches = re.findall(r'(?:A\d+|Answer\s*\d*)[:\.]?\s*(.+?)(?=(?:Q\d+|Question|A\d+|Answer|$))', text, re.IGNORECASE | re.DOTALL)
    
    if q_matches and a_matches:
        for i, (q, a) in enumerate(zip(q_matches, a_matches)):
            questions.append({
                "id": i + 1,
                "question": q.strip(),
                "answer": a.strip()
            })
        if questions:
            return {"flashcards": questions, "title": "Generated Content", "total_count": len(questions)}
    
    raise ValueError(f"Could not extract JSON from response: {text[:200]}...")

FLASHCARD_SYSTEM = """You are an expert flashcard creator. Create flashcards DIRECTLY from the provided content.
RULES:
1. Questions and answers MUST come from the content provided
2. Make questions clear and answers accurate
3. Output ONLY valid JSON - no explanations, no markdown"""

FLASHCARD_USER = """Read this content and create {num} flashcards based ONLY on the information given:

CONTENT:
{content}

Create question-answer pairs that help memorize key facts from the above content.

Output ONLY this JSON:
{{"title": "Flashcards", "flashcards": [{{"id": 1, "question": "Question from content?", "answer": "Answer from content"}}]}}"""

QUIZ_SYSTEM = """You are an expert quiz creator. Your job is to create quiz questions DIRECTLY from the provided content.
RULES:
1. Questions MUST be based on facts from the content provided
2. All answer options must be plausible but only ONE is correct
3. Output ONLY valid JSON - no explanations, no markdown"""

QUIZ_USER = """Read this content carefully and create {num} multiple-choice questions based ONLY on the information given:

CONTENT:
{content}

Create questions that test understanding of the above content. Each question must have exactly 4 options with only ONE correct answer.

Output ONLY this JSON:
{{"title": "Quiz", "questions": [{{"id": 1, "question": "Question from the content?", "options": [{{"label": "A", "text": "Wrong option", "is_correct": false}}, {{"label": "B", "text": "Correct from content", "is_correct": true}}, {{"label": "C", "text": "Wrong option", "is_correct": false}}, {{"label": "D", "text": "Wrong option", "is_correct": false}}], "explanation": "This is correct because the content states..."}}]}}"""

MATCHING_SYSTEM = """You are an educational game creator. Generate matching pairs as JSON.
IMPORTANT: Output ONLY valid JSON. No explanations, no markdown, no extra text."""

MATCHING_USER = """Create {num} term-definition pairs from this content:

{content}

Output this exact JSON structure:
{{"title": "Matching Game", "pairs": [{{"id": 1, "term": "Term 1", "definition": "Definition 1"}}, {{"id": 2, "term": "Term 2", "definition": "Definition 2"}}]}}"""

STUDY_GUIDE_SYSTEM = """You are a study guide creator. Generate study materials as JSON.
IMPORTANT: Output ONLY valid JSON. No explanations, no markdown, no extra text."""

STUDY_GUIDE_USER = """Create a study guide from this content:

{content}

Subject: {subject}

Output this exact JSON structure:
{{"title": "Study Guide", "subject": "{subject}", "summary": "2-3 paragraph summary here", "outlines": [{{"id": 1, "title": "Section", "content": "Overview", "sub_items": ["Point 1", "Point 2"]}}], "bullet_takeaways": ["Takeaway 1", "Takeaway 2"], "key_topics": [{{"id": 1, "topic": "Topic", "importance": "high"}}], "facts": [{{"id": 1, "fact": "Fact", "category": "Category"}}]}}"""

EVAL_SYSTEM = """You are an answer evaluator. Assess student answers as JSON.
IMPORTANT: Output ONLY valid JSON. No explanations, no markdown, no extra text."""

EVAL_USER = """Evaluate this answer:

Question: {question}
Correct Answer: {correct}
Student Answer: {user_answer}

Output this exact JSON structure:
{{"is_correct": true, "score": 0.85, "feedback": "Feedback text", "suggestions": ["Suggestion 1", "Suggestion 2"]}}"""

SUMMARY_SYSTEM = """You are an expert note summarizer. Create concise, informative summaries that preserve key concepts.
RULES:
1. Identify and preserve the most important concepts
2. Use clear, concise language
3. Organize information logically
4. Output ONLY valid JSON - no explanations, no markdown"""

SUMMARY_USER = """Summarize these study notes into a concise summary while preserving all key concepts:

NOTES:
{content}

Create a summary with:
- A brief overview (2-3 sentences)
- Key points (bullet points)
- Important terms and definitions
- Main takeaways

Output ONLY this JSON:
{{"title": "Summary", "overview": "Brief 2-3 sentence overview of the content", "key_points": ["Key point 1", "Key point 2", "Key point 3"], "terms": [{{"term": "Important Term", "definition": "What it means"}}], "takeaways": ["Main takeaway 1", "Main takeaway 2"], "word_count_original": 0, "word_count_summary": 0}}"""

ONBOARDING_STEPS = [
    {
        "title": "Turn your notes, lectures, or videos into flashcards, quizzes, study guides and fun study games.",
        "features": ["📝 Notes", "🎴 Flashcards", "❓ Quizzes", "🎮 Games"]
    },
    {
        "title": "How It Works",
        "description": "Record or upload your lectures, and MyStudyBuddy will turn them into organized notes and study tools - instantly."
    },
    {
        "title": "Why You'll Love It",
        "description": "Study solo or play with friends — test your knowledge through games, track your friends, and make studying fun again."
    }
]

def show_splash():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(robot_svg(150), unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">My Study Buddy</h1>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Get Started", key="splash_start"):
            st.session_state.current_page = "onboarding"
            st.rerun()

def show_onboarding():
    step = st.session_state.onboarding_step
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(robot_svg(100), unsafe_allow_html=True)
        
        content = ONBOARDING_STEPS[step]
        
        st.markdown(f'<p class="onboarding-title">{content["title"]}</p>', unsafe_allow_html=True)
        
        if "description" in content:
            st.markdown(f'<p class="onboarding-text">{content["description"]}</p>', unsafe_allow_html=True)
        
        if "features" in content:
            fcols = st.columns(4)
            for i, feat in enumerate(content["features"]):
                with fcols[i]:
                    st.markdown(f"""
                    <div style="background: #F5F0E8; padding: 0.5rem; border-radius: 8px; text-align: center; font-size: 0.8rem; color: #2D2D2D;">
                        {feat}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown(dots_indicator(step, len(ONBOARDING_STEPS)), unsafe_allow_html=True)
        
        col_skip, col_next = st.columns(2)
        
        with col_skip:
            if st.button("Skip", key="skip_onboarding"):
                st.session_state.onboarding_complete = True
                st.session_state.current_page = "welcome"
                st.rerun()
        
        with col_next:
            btn_text = "Continue" if step < len(ONBOARDING_STEPS) - 1 else "Get Started"
            if st.button(btn_text, key="next_onboarding"):
                if step < len(ONBOARDING_STEPS) - 1:
                    st.session_state.onboarding_step += 1
                    st.rerun()
                else:
                    st.session_state.onboarding_complete = True
                    st.session_state.current_page = "welcome"
                    st.rerun()

def show_welcome():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="color: #2D2D2D; font-size: 2.5rem; margin-bottom: 0.5rem;">Welcome</h1>
            <p style="color: #666666; font-size: 1rem;">Study Smarter, Not Harder.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(robot_svg(120), unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem;'>Let's Get Started!</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_signup, col_login = st.columns(2)
        
        with col_signup:
            if st.button("📝 Sign Up", key="welcome_signup", use_container_width=True):
                st.session_state.current_page = "signup"
                st.rerun()
        
        with col_login:
            if st.button("🔑 Log In", key="welcome_login", use_container_width=True):
                st.session_state.current_page = "login"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <p style="text-align: center; color: #888; font-size: 0.85rem;">
            By continuing, you agree to our <a href="#" style="color: #6B5CA5;">Terms</a> and <a href="#" style="color: #6B5CA5;">Privacy Policy</a>.
        </p>
        """, unsafe_allow_html=True)

def show_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(robot_svg(80), unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #2D2D2D;">Welcome Back!</h2>
            <p style="color: #666666; font-size: 0.9rem;">Sign in to your account</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-header">Log into your account</p>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="example@gmail.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Log In", key="login_btn"):
            if email and password:
                hashed = hash_password(password)
                user = get_user(email)
                if user and user["password"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.username = user["name"]
                    st.session_state.current_page = "app"
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please fill in all fields")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Forgot Password?", key="forgot_btn"):
                st.info("Password reset feature coming soon!")
        with col_b:
            if st.button("Create Account", key="to_signup"):
                st.session_state.current_page = "signup"
                st.rerun()

def show_signup():
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(robot_svg(80), unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #2D2D2D;"><span style="color: #6B5CA5;">Sign</span> up for your account</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col_fn, col_ln = st.columns(2)
        with col_fn:
            first_name = st.text_input("First Name", placeholder="Your Name", key="signup_fname")
        with col_ln:
            last_name = st.text_input("Last Name", placeholder="Your Name", key="signup_lname")
        
        email = st.text_input("Email", placeholder="example@gmail.com", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="abc12345", key="signup_password")
        confirm_password = st.text_input("Re-type Password", type="password", placeholder="abc12345", key="signup_confirm")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Sign Up", key="signup_btn"):
            if first_name and last_name and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    hashed = hash_password(password)
                    if add_user(email, f"{first_name} {last_name}", hashed):
                        st.session_state.authenticated = True
                        st.session_state.username = f"{first_name} {last_name}"
                        st.session_state.current_page = "name_prompt"
                        st.rerun()
                    else:
                        st.error("Email already registered")
            else:
                st.warning("Please fill in all fields")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <p style="text-align: center; color: #888; font-size: 0.85rem;">
            Already have an account?
        </p>
        """, unsafe_allow_html=True)
        
        if st.button("Log In", key="to_login"):
            st.session_state.current_page = "login"
            st.rerun()

def show_name_prompt():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(robot_svg(100), unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center;">
            <h2 style="color: #2D2D2D;">My Study Buddy</h2>
            <p style="color: #666666;">What should I call you?</p>
        </div>
        """, unsafe_allow_html=True)
        
        nickname = st.text_input("", placeholder="Enter your nickname", key="nickname_input", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Continue", key="name_continue"):
            if nickname:
                st.session_state.username = nickname
            st.session_state.current_page = "app"
            st.rerun()

def show_main_app():
    provider = AIProvider()
    
    with st.sidebar:
        st.markdown("## 📚 Study Buddy")
        if st.session_state.username:
            st.markdown(f"👋 Hello, **{st.session_state.username}**!")
        st.caption("AI-Powered Learning")
        st.markdown("---")
        
        page = st.radio(
            "Navigate",
            ["🏠 Home", "🎴 Flashcards", "❓ Quiz", "🔗 Matching", "📝 Notes Summary", "📖 Study Guide", "✅ Evaluation"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ AI Provider")
        if provider.is_configured():
            st.success(f"✅ {provider.get_provider_name()}")
        else:
            st.error("❌ Not configured")
            st.caption("Set GROQ_API_KEY")
        
        st.markdown("---")
        if st.button("🚪 Logout", key="logout_btn"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.current_page = "splash"
            st.rerun()
    
    if page == "🏠 Home":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(robot_svg(100), unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">My Study Buddy</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Turn your notes into flashcards, quizzes, study guides, and fun study games.</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-box">
                <h4>🎴 Flashcards</h4>
                <p>Generate question-answer pairs for effective memorization.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h4>🔗 Matching Sprint</h4>
                <p>Create term-definition matching games.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h4>📝 Notes Summary</h4>
                <p>Summarize long notes while preserving key concepts.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
                <h4>❓ Quiz Race</h4>
                <p>Create multiple-choice quizzes to test knowledge.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h4>📖 Study Guide</h4>
                <p>Transform notes into organized summaries.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-box">
                <h4>✅ Evaluation</h4>
                <p>Get AI feedback on your answers.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")
        st.info("👈 Select a feature from the sidebar to get started!")
    
    elif page == "🎴 Flashcards":
        st.markdown('<p class="page-title">🎴 Flashcard Generation</p>', unsafe_allow_html=True)
        st.markdown('<p class="page-desc">Generate question-answer pairs from your study material</p>', unsafe_allow_html=True)
        
        if not provider.is_configured():
            st.error("❌ AI Provider not configured. Set GROQ_API_KEY environment variable.")
        else:
            content = st.text_area(
                "📝 Enter your study content",
                height=150,
                placeholder="Paste your notes, textbook content, or any study material here..."
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                num_cards = st.number_input("Number of flashcards", min_value=1, max_value=20, value=5)
            
            if st.button("🎴 Generate Flashcards", disabled=not content):
                with st.spinner("Creating flashcards..."):
                    try:
                        response = provider.generate(
                            FLASHCARD_SYSTEM,
                            FLASHCARD_USER.format(num=num_cards, content=content)
                        )
                        data = extract_json(response)
                        
                        st.success(f"✅ Generated: {data.get('title', 'Flashcards')}")
                        
                        if "flashcards" in data:
                            for card in data["flashcards"]:
                                with st.expander(f"Card {card['id']}: {card['question'][:50]}..."):
                                    st.markdown(f"**Question:** {card['question']}")
                                    st.markdown(f"**Answer:** {card['answer']}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    

    elif page == "❓ Quiz":
        st.markdown('<p class="page-title">❓ Quiz Race</p>', unsafe_allow_html=True)
        
        if 'quiz_step' not in st.session_state:
            st.session_state.quiz_step = 'menu'
        if 'quiz_data' not in st.session_state:
            st.session_state.quiz_data = None
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {}
        if 'quiz_submitted' not in st.session_state:
            st.session_state.quiz_submitted = False
        if 'custom_questions' not in st.session_state:
            st.session_state.custom_questions = []
        if 'quiz_content' not in st.session_state:
            st.session_state.quiz_content = ""
        
        if st.session_state.quiz_step == 'play' and st.session_state.quiz_data:
            data = st.session_state.quiz_data
            questions = data.get("questions", [])
            
            if not questions:
                st.error("No questions found!")
                if st.button("Back to Menu"):
                    st.session_state.quiz_step = 'menu'
                    st.rerun()
            else:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {data.get('title', 'Quiz')}")
                with col2:
                    if st.button("Exit Quiz"):
                        st.session_state.quiz_step = 'menu'
                        st.session_state.quiz_data = None
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                
                st.markdown("---")
                
                if not st.session_state.quiz_submitted:
                    for q in questions:
                        st.markdown(f"**Q{q['id']}: {q['question']}**")
                        opts = [f"{o['label']}. {o['text']}" for o in q['options']]
                        ans = st.radio(f"q{q['id']}", opts, key=f"pq_{q['id']}", label_visibility="collapsed")
                        st.session_state.quiz_answers[q['id']] = ans[0] if ans else ""
                        st.markdown("---")
                    
                    if st.button("Submit Answers", type="primary"):
                        st.session_state.quiz_submitted = True
                        st.rerun()
                else:
                    correct = 0
                    for q in questions:
                        user_ans = st.session_state.quiz_answers.get(q['id'], '')
                        correct_opt = next((o for o in q['options'] if o['is_correct']), None)
                        is_right = user_ans == correct_opt['label'] if correct_opt else False
                        if is_right:
                            correct += 1
                        
                        icon = "✅" if is_right else "❌"
                        st.markdown(f"**{icon} Q{q['id']}: {q['question']}**")
                        for o in q['options']:
                            if o['is_correct']:
                                st.markdown(f"  ✅ {o['label']}. {o['text']} *(Correct)*")
                            elif o['label'] == user_ans:
                                st.markdown(f"  ❌ {o['label']}. {o['text']} *(Your answer)*")
                            else:
                                st.markdown(f"  ⬜ {o['label']}. {o['text']}")
                        st.markdown("---")
                    
                    pct = int((correct / len(questions)) * 100) if questions else 0
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Score", f"{correct}/{len(questions)}")
                    c2.metric("Percent", f"{pct}%")
                    c3.metric("Grade", "A" if pct>=90 else "B" if pct>=80 else "C" if pct>=70 else "D" if pct>=60 else "F")
                    
                    c1, c2 = st.columns(2)
                    if c1.button("Retry"):
                        st.session_state.quiz_submitted = False
                        st.session_state.quiz_answers = {}
                        st.rerun()
                    if c2.button("Back to Menu"):
                        st.session_state.quiz_step = 'menu'
                        st.session_state.quiz_data = None
                        st.session_state.quiz_submitted = False
                        st.rerun()
        
        elif st.session_state.quiz_step == 'menu':
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 🤖 AI Generate")
                st.write("Upload content, AI creates quiz")
                if st.button("Start AI Quiz"):
                    st.session_state.quiz_step = 'ai_upload'
                    st.rerun()
            with c2:
                st.markdown("### ✏️ Create Manual")
                st.write("Create your own questions")
                if st.button("Create Manually"):
                    st.session_state.quiz_step = 'manual'
                    st.rerun()
            
            if st.session_state.custom_questions:
                st.markdown("---")
                st.write(f"You have {len(st.session_state.custom_questions)} saved questions")
                if st.button("Play Saved Quiz"):
                    st.session_state.quiz_data = {"title": "My Quiz", "questions": st.session_state.custom_questions}
                    st.session_state.quiz_step = 'play'
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()
        
        elif st.session_state.quiz_step == 'manual':
            if st.button("← Back"):
                st.session_state.quiz_step = 'menu'
                st.rerun()
            
            st.markdown("### Add Question")
            q_text = st.text_area("Question", key="m_q")
            c1, c2 = st.columns(2)
            opt_a = c1.text_input("Option A", key="m_a")
            opt_b = c2.text_input("Option B", key="m_b")
            opt_c = c1.text_input("Option C", key="m_c")
            opt_d = c2.text_input("Option D", key="m_d")
            correct = st.selectbox("Correct", ["A","B","C","D"], key="m_cor")
            
            if st.button("Add Question"):
                if q_text and opt_a and opt_b:
                    st.session_state.custom_questions.append({
                        "id": len(st.session_state.custom_questions)+1,
                        "question": q_text,
                        "options": [
                            {"label":"A","text":opt_a,"is_correct":correct=="A"},
                            {"label":"B","text":opt_b,"is_correct":correct=="B"},
                            {"label":"C","text":opt_c or "N/A","is_correct":correct=="C"},
                            {"label":"D","text":opt_d or "N/A","is_correct":correct=="D"},
                        ],
                        "explanation": ""
                    })
                    st.success("Added!")
            
            if st.session_state.custom_questions:
                st.markdown("---")
                st.write(f"**{len(st.session_state.custom_questions)} Questions:**")
                for i, q in enumerate(st.session_state.custom_questions):
                    st.write(f"{q['id']}. {q['question'][:50]}...")
                
                c1, c2 = st.columns(2)
                if c1.button("Play Quiz"):
                    st.session_state.quiz_data = {"title": "My Quiz", "questions": st.session_state.custom_questions}
                    st.session_state.quiz_step = 'play'
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.rerun()
                if c2.button("Clear All"):
                    st.session_state.custom_questions = []
                    st.rerun()
        
        elif st.session_state.quiz_step == 'ai_upload':
            if st.button("← Back"):
                st.session_state.quiz_step = 'menu'
                st.rerun()
            
            st.markdown("### Upload Content")
            content = st.text_area("Paste notes", height=150, key="ai_txt")
            
            uploaded = st.file_uploader("Or upload file", type=['txt','pdf'], key="ai_up")
            if uploaded:
                if uploaded.name.endswith('.txt'):
                    content = uploaded.read().decode('utf-8', errors='ignore')
                elif uploaded.name.endswith('.pdf'):
                    try:
                        import PyPDF2
                        r = PyPDF2.PdfReader(uploaded)
                        content = "".join(p.extract_text() or "" for p in r.pages)
                    except:
                        st.error("Cannot read PDF")
                if content:
                    st.success(f"Loaded {len(content)} chars")
            
            if st.button("Continue", disabled=not content):
                st.session_state.quiz_content = content
                st.session_state.quiz_step = 'ai_settings'
                st.rerun()
        
        elif st.session_state.quiz_step == 'ai_settings':
            if st.button("← Back"):
                st.session_state.quiz_step = 'ai_upload'
                st.rerun()
            
            st.markdown("### Quiz Settings")
            num_q = st.selectbox("Number of Questions", [3,5,10,15], index=1)
            
            if st.button("Generate Quiz", type="primary"):
                content = st.session_state.get('quiz_content', '')
                content = ''.join(c for c in content if c.isprintable() or c in '\n\r\t')[:3000]
                
                with st.spinner("Generating..."):
                    try:
                        resp = provider.generate(QUIZ_SYSTEM, QUIZ_USER.format(num=num_q, content=content))
                        data = extract_json(resp)
                        st.session_state.quiz_data = data
                        st.session_state.quiz_step = 'play'
                        st.session_state.quiz_answers = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        
        else:
            st.session_state.quiz_step = 'menu'
            st.rerun()

    elif page == "🔗 Matching":
        st.markdown('<p class="page-title">🔗 Matching Sprint</p>', unsafe_allow_html=True)
        st.markdown('<p class="page-desc">Create term-definition matching games</p>', unsafe_allow_html=True)
        
        if not provider.is_configured():
            st.error("❌ AI Provider not configured. Set GROQ_API_KEY environment variable.")
        else:
            content = st.text_area(
                "📝 Enter your study content",
                height=150,
                placeholder="Paste your notes with key terms and concepts...",
                key="matching_content"
            )
            
            col1, col2 = st.columns([1, 3])
            with col1:
                num_pairs = st.number_input("Number of pairs", min_value=2, max_value=15, value=5)
            
            if st.button("🔗 Generate Matching Game", disabled=not content):
                with st.spinner("Creating matching pairs..."):
                    try:
                        response = provider.generate(
                            MATCHING_SYSTEM,
                            MATCHING_USER.format(num=num_pairs, content=content)
                        )
                        data = extract_json(response)
                        
                        st.success(f"✅ Generated: {data.get('title', 'Matching Game')}")
                        
                        if "pairs" in data:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("### 📝 Terms")
                                for pair in data["pairs"]:
                                    st.markdown(f"""
                                    <div style="background: #8B7EC8; color: white; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                                        {pair['term']}
                                    </div>
                                    """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown("### 📖 Definitions")
                                for pair in data["pairs"]:
                                    st.markdown(f"""
                                    <div style="background: white; border: 2px solid #E5DDD0; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; color: #333;">
                                        {pair['definition']}
                                    </div>
                                    """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    elif page == "📝 Notes Summary":
        st.markdown('<p class="page-title">📝 Notes Summarization</p>', unsafe_allow_html=True)
        st.markdown('<p class="page-desc">Create concise summaries from long study notes while preserving key concepts</p>', unsafe_allow_html=True)
        
        if not provider.is_configured():
            st.error("❌ AI Provider not configured. Set GROQ_API_KEY environment variable.")
        else:
            input_method = st.radio("Input Method", ["📝 Paste Text", "📄 Upload File"], horizontal=True)
            
            content = ""
            
            if input_method == "📝 Paste Text":
                content = st.text_area(
                    "Paste your study notes here",
                    height=250,
                    placeholder="Paste your long study notes, lecture content, or any text you want to summarize...",
                    key="summary_content"
                )
            else:
                uploaded_file = st.file_uploader("Upload your notes", type=['txt', 'pdf'], key="summary_file")
                if uploaded_file:
                    if uploaded_file.name.endswith('.txt'):
                        content = uploaded_file.read().decode('utf-8', errors='ignore')
                        st.success(f"✅ Loaded {len(content)} characters")
                    elif uploaded_file.name.endswith('.pdf'):
                        try:
                            import PyPDF2
                            reader = PyPDF2.PdfReader(uploaded_file)
                            content = ""
                            for page in reader.pages:
                                text = page.extract_text()
                                if text:
                                    content += text + "\n"
                            st.success(f"✅ Extracted {len(content)} characters from {len(reader.pages)} pages")
                        except Exception as e:
                            st.error(f"❌ Error reading PDF: {e}")
                    
                    if content:
                        with st.expander("📄 Preview Content"):
                            st.text(content[:1000] + "..." if len(content) > 1000 else content)
            
            if content:
                word_count = len(content.split())
                st.info(f"📊 Word count: {word_count} words")
            
            if st.button("📝 Generate Summary", disabled=not content, type="primary"):
                with st.spinner("⏳ Analyzing and summarizing your notes..."):
                    try:
                        clean_content = ''.join(c for c in content if c.isprintable() or c in '\n\r\t')
                        clean_content = clean_content[:5000]
                        
                        response = provider.generate(
                            SUMMARY_SYSTEM,
                            SUMMARY_USER.format(content=clean_content)
                        )
                        data = extract_json(response)
                        
                        st.success("✅ Summary Generated!")
                        
                        st.markdown("### 📋 Overview")
                        st.markdown(f"""
                        <div style="background: #F5F0E8; padding: 1rem; border-radius: 10px; color: #2D2D2D;">
                            {data.get('overview', 'No overview available')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("### 🔑 Key Points")
                        for point in data.get('key_points', []):
                            st.markdown(f"• {point}")
                        
                        if data.get('terms'):
                            st.markdown("### 📚 Important Terms")
                            for term_item in data['terms']:
                                with st.expander(f"📖 {term_item.get('term', 'Term')}"):
                                    st.write(term_item.get('definition', 'No definition'))
                        
                        st.markdown("### 🎯 Main Takeaways")
                        for i, takeaway in enumerate(data.get('takeaways', []), 1):
                            st.markdown(f"""
                            <div style="background: #E8F5E9; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #4CAF50; color: #2D2D2D;">
                                <strong>{i}.</strong> {takeaway}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Original Words", len(content.split()))
                        with col2:
                            summary_text = data.get('overview', '') + ' '.join(data.get('key_points', []))
                            st.metric("Summary Words", len(summary_text.split()))
                        with col3:
                            reduction = int((1 - len(summary_text.split()) / max(len(content.split()), 1)) * 100)
                            st.metric("Reduction", f"{reduction}%")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    elif page == "📖 Study Guide":
        st.markdown('<p class="page-title">📖 Study Guide Generator</p>', unsafe_allow_html=True)
        st.markdown('<p class="page-desc">Transform your notes into comprehensive study guides</p>', unsafe_allow_html=True)
        
        if not provider.is_configured():
            st.error("❌ AI Provider not configured. Set GROQ_API_KEY environment variable.")
        else:
            subject = st.text_input("📚 Subject/Topic Name", placeholder="e.g., Biology, History, Physics")
            
            content = st.text_area(
                "📝 Enter your study content",
                height=200,
                placeholder="Paste your lecture notes, textbook content, or study material...",
                key="guide_content"
            )
            
            if st.button("📖 Generate Study Guide", disabled=not content or not subject):
                with st.spinner("Creating study guide..."):
                    try:
                        response = provider.generate(
                            STUDY_GUIDE_SYSTEM,
                            STUDY_GUIDE_USER.format(subject=subject, content=content)
                        )
                        data = extract_json(response)
                        
                        st.success(f"✅ Generated: {data.get('title', 'Study Guide')}")
                        
                        tabs = st.tabs(["📋 Outline", "📝 Summary", "🎯 Key Takeaways", "📊 Key Topics", "💡 Facts"])
                        
                        with tabs[0]:
                            if "outlines" in data:
                                for outline in data["outlines"]:
                                    with st.expander(f"📌 {outline['title']}"):
                                        st.write(outline.get('content', ''))
                                        if 'sub_items' in outline:
                                            for item in outline['sub_items']:
                                                st.markdown(f"• {item}")
                        
                        with tabs[1]:
                            st.markdown(data.get('summary', 'No summary available'))
                        
                        with tabs[2]:
                            if "bullet_takeaways" in data:
                                for takeaway in data["bullet_takeaways"]:
                                    st.markdown(f"✅ {takeaway}")
                        
                        with tabs[3]:
                            if "key_topics" in data:
                                for topic in data["key_topics"]:
                                    importance = topic.get('importance', 'medium')
                                    color = "#FF6B6B" if importance == "high" else "#FFB84D" if importance == "medium" else "#4ECDC4"
                                    st.markdown(f"""
                                    <span style="background: {color}; color: white; padding: 0.25rem 0.75rem; border-radius: 15px; margin-right: 0.5rem; display: inline-block; margin-bottom: 0.5rem;">
                                        {topic['topic']}
                                    </span>
                                    """, unsafe_allow_html=True)
                        
                        with tabs[4]:
                            if "facts" in data:
                                for fact in data["facts"]:
                                    st.info(f"💡 {fact['fact']}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    elif page == "✅ Evaluation":
        st.markdown('<p class="page-title">✅ Answer Evaluation</p>', unsafe_allow_html=True)
        st.markdown('<p class="page-desc">Get AI feedback on your answers</p>', unsafe_allow_html=True)
        
        if not provider.is_configured():
            st.error("❌ AI Provider not configured. Set GROQ_API_KEY environment variable.")
        else:
            question = st.text_area(
                "❓ Question",
                height=80,
                placeholder="Enter the question...",
                key="eval_question"
            )
            
            correct_answer = st.text_area(
                "✅ Correct Answer",
                height=80,
                placeholder="Enter the correct/expected answer...",
                key="eval_correct"
            )
            
            user_answer = st.text_area(
                "📝 Your Answer",
                height=80,
                placeholder="Enter your answer to evaluate...",
                key="eval_user"
            )
            
            if st.button("✅ Evaluate Answer", disabled=not all([question, correct_answer, user_answer])):
                with st.spinner("Evaluating..."):
                    try:
                        response = provider.generate(
                            EVAL_SYSTEM,
                            EVAL_USER.format(
                                question=question,
                                correct=correct_answer,
                                user_answer=user_answer
                            )
                        )
                        data = extract_json(response)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            score = data.get('score', 0)
                            st.metric("Score", f"{int(score * 100)}%")
                        with col2:
                            is_correct = data.get('is_correct', False)
                            st.metric("Status", "✅ Correct" if is_correct else "❌ Needs Work")
                        
                        st.markdown("### 💬 Feedback")
                        st.write(data.get('feedback', 'No feedback available'))
                        
                        if "suggestions" in data and data["suggestions"]:
                            st.markdown("### 💡 Suggestions for Improvement")
                            for suggestion in data["suggestions"]:
                                st.markdown(f"• {suggestion}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

def main():
    if st.session_state.current_page == "splash":
        show_splash()
    elif st.session_state.current_page == "onboarding":
        show_onboarding()
    elif st.session_state.current_page == "welcome":
        show_welcome()
    elif st.session_state.current_page == "login":
        show_login()
    elif st.session_state.current_page == "signup":
        show_signup()
    elif st.session_state.current_page == "name_prompt":
        show_name_prompt()
    elif st.session_state.current_page == "app":
        show_main_app()
    else:
        show_splash()

if __name__ == "__main__":
    main()
