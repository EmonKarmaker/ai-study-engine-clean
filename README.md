# AI Study Engine

An AI-powered study platform that transforms your notes into interactive learning tools.

Live Demo: https://ai-study-engine.onrender.com

GitHub: https://github.com/EmonKarmaker/ai-study-engine

---

## Features

- Flashcard Generation - Create Q&A pairs from any study content
- Quiz Generation - Generate MCQ quizzes with AI or create manually
- Notes Summarization - Condense long notes while keeping key concepts
- Answer Evaluation - Get AI feedback on your answers with scores
- Matching Games - Interactive term-definition matching
- Study Guide Builder - Convert notes into organized study guides

---

## Tech Stack

- Python 3.11.9
- Streamlit
- Groq API (LLaMA 3.3 70B)
- SQLite
- Docker
- PyPDF2

---

## Project Structure

```
ai-study-engine/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── Dockerfile          # Docker configuration
├── render.yaml         # Render deployment config
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

---

## Installation

1. Clone the repository
```
git clone https://github.com/EmonKarmaker/ai-study-engine.git
cd ai-study-engine
```

2. Create virtual environment
```
py -3.11 -m venv venv
```

3. Activate virtual environment
```
venv\Scripts\activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Create environment file
```
copy .env.example .env
```

6. Add your Groq API key to .env file
```
GROQ_API_KEY=your_api_key_here
```

7. Run the application
```
streamlit run app.py
```

App opens at http://localhost:8501

---

## Getting Groq API Key

1. Go to https://console.groq.com
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy and paste in .env file

---

## Deployment

Deployed on Render with Docker.

Live URL: https://ai-study-engine.onrender.com

To deploy your own:
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variable GROQ_API_KEY
4. Deploy

---

## Usage

1. Open the app
2. Sign up or log in
3. Choose a feature from sidebar
4. Paste your study content or upload PDF/TXT
5. Generate flashcards, quizzes, or summaries
6. Study and track your progress

---

## Author

Emon Karmaker

GitHub: https://github.com/EmonKarmaker
