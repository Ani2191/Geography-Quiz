# Geography Quiz

An interactive geography quiz featuring questions about world landmarks, capitals, and interesting geographical facts. The quiz includes 50 diverse questions and shows 8 random questions per round, with a mechanism to prevent question repetition in consecutive rounds.

## Features

- 50 diverse geography questions
- Random selection of 8 questions per round
- No question repetition for 3 consecutive rounds
- Beautiful animated gradient background
- Responsive design
- Score tracking
- Interactive UI with visual feedback
- Created by: Ani

## Deployment Instructions

1. Create an account on [Render.com](https://render.com)
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the deployment:
   - Name: geography-quiz (or your preferred name)
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn web_quiz:app`
5. Click "Create Web Service"

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python web_quiz.py
   ```
5. Open http://localhost:5000 in your browser

## Technologies Used

- Python/Flask
- HTML/CSS/JavaScript
- Gunicorn (Production server) 