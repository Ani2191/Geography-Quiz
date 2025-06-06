from flask import Flask, render_template, request, session, jsonify, send_from_directory
import random
import os
from base64 import b64encode
import webbrowser
from threading import Timer
from collections import deque

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Keep track of recently used questions globally
recent_questions = deque(maxlen=24)  # 8 questions × 3 rounds = 24 questions to track

# Categorize questions by difficulty
QUESTIONS = {
    'easy': [
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/4/43/Flag_of_Ireland_and_GPO_Dublin_-_150524_171318.jpg",
            "question": "What is the capital city of Ireland?",
            "options": ["Dublin", "Belfast", "Cork", "Galway"],
            "correct": 0
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/8/85/Tour_Eiffel_Wikimedia_Commons.jpg",
            "question": "The Eiffel Tower is located in which city?",
            "options": ["London", "Paris", "Rome", "Berlin"],
            "correct": 1
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Canberra_montage.jpg",
            "question": "What is the capital city of Australia?",
            "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
            "correct": 2
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Antartica.jpg",
            "question": "Which is the largest desert in the world?",
            "options": ["Sahara Desert", "Arabian Desert", "Antarctic Desert", "Gobi Desert"],
            "correct": 2
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Wellington_Harbour_from_Mount_Victoria.jpg",
            "question": "What is the capital city of New Zealand?",
            "options": ["Auckland", "Wellington", "Christchurch", "Hamilton"],
            "correct": 1
        }
    ],
    'medium': [
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/2/21/Dead_sea_newspaper.jpg",
            "question": "Which body of water is the lowest point on Earth's surface?",
            "options": ["Caspian Sea", "Dead Sea", "Red Sea", "Black Sea"],
            "correct": 1
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Stockholm_Archipelago.jpg",
            "question": "Which country has the most islands in the world?",
            "options": ["Indonesia", "Japan", "Philippines", "Sweden"],
            "correct": 3
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/8/87/Eyjafjallaj%C3%B6kull_first_crater_20100329.jpg",
            "question": "Which country is known as the 'Land of Fire and Ice'?",
            "options": ["Norway", "Iceland", "Greenland", "Finland"],
            "correct": 1
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/4/44/Pacific_Ring_of_Fire.svg",
            "question": "The 'Ring of Fire' is located in which ocean?",
            "options": ["Atlantic", "Indian", "Pacific", "Arctic"],
            "correct": 2
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/1/10/Lalibela%2C_san_giorgio%2C_esterno_05.jpg",
            "question": "Which African nation was never colonized by Europeans?",
            "options": ["Ethiopia", "Libya", "Egypt", "Sudan"],
            "correct": 0
        }
    ],
    'hard': [
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/7/75/Strait_of_Malacca_%28orthographic_projection%29.png",
            "question": "The Strait of Malacca connects which two bodies of water?",
            "options": ["South China Sea & Indian Ocean", "Pacific & Indian Ocean", "Bay of Bengal & Arabian Sea", "Java Sea & Indian Ocean"],
            "correct": 0
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/9/9f/Bhutan_tiger%27s_nest_monastery.jpg",
            "question": "Which country has the world's only carbon-negative economy?",
            "options": ["Norway", "Bhutan", "Costa Rica", "New Zealand"],
            "correct": 1
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/9/97/Dallol_hot_springs.jpg",
            "question": "The Danakil Depression, one of the lowest and hottest places on Earth, is located in which country?",
            "options": ["Ethiopia", "Saudi Arabia", "Yemen", "Sudan"],
            "correct": 0
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Sargasso_Sea_map.png",
            "question": "The Sargasso Sea is the only sea without shores. In which ocean is it located?",
            "options": ["Pacific Ocean", "Indian Ocean", "Atlantic Ocean", "Southern Ocean"],
            "correct": 2
        },
        {
            "image": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Flag_of_Burkina_Faso.svg",
            "question": "Which African country was formerly known as Upper Volta?",
            "options": ["Mali", "Niger", "Burkina Faso", "Chad"],
            "correct": 2
        }
    ]
}

def get_image_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            return b64encode(image_file.read()).decode('utf-8')
    except:
        return None

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

def get_random_questions(difficulty, num_questions=8):
    questions = QUESTIONS.get(difficulty, QUESTIONS['medium'])  # Default to medium if invalid difficulty
    available_questions = [q for q in questions if q not in recent_questions]
    
    if len(available_questions) < num_questions:
        recent_questions.clear()
        available_questions = questions
    
    # Ensure we don't try to select more questions than available
    num_to_select = min(num_questions, len(available_questions))
    selected = random.sample(available_questions, num_to_select)
    
    for q in selected:
        recent_questions.append(q)
    return selected

@app.route('/')
def index():
    return render_template('quiz.html')

@app.route('/start')
def start_quiz():
    difficulty = request.args.get('difficulty', 'medium')
    if difficulty not in QUESTIONS:
        difficulty = 'medium'
    
    questions = get_random_questions(difficulty, 5)  # Reduced to 5 questions per round
    session['questions'] = questions
    session['current_question'] = 0
    session['score'] = 0
    return jsonify({'success': True})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/question')
def get_question():
    questions = session.get('questions', [])
    current = session.get('current_question', 0)
    
    if not questions or current >= len(questions):
        return jsonify({'error': 'No more questions'})
    
    question = questions[current]
    return jsonify({
        'image': question['image'],
        'question': question['question'],
        'options': question['options'],
        'current': current + 1,
        'total': len(questions)
    })

@app.route('/answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    questions = session.get('questions', [])
    current = session.get('current_question', 0)
    
    if not questions or current >= len(questions):
        return jsonify({'error': 'No more questions'}), 400
    
    question = questions[current]
    answer = data.get('answer')
    
    if answer is None:
        return jsonify({'error': 'No answer provided'}), 400
    
    is_correct = answer == question['correct']
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    session['current_question'] = current + 1
    
    return jsonify({
        'correct': is_correct,
        'score': session['score'],
        'total': len(questions),
        'isLast': current + 1 >= len(questions)
    })

if __name__ == '__main__':
    Timer(1, open_browser).start()  # Open browser after 1 second
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
