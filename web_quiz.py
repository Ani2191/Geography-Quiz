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

# Question database
QUESTIONS = [
    {
        "image": "images/taj_mahal.jpg",
        "question": "In which country is the Taj Mahal located?",
        "options": ["India", "Pakistan", "Bangladesh", "Nepal"],
        "correct": 0
    },
    {
        "image": "images/eiffel_tower.jpg",
        "question": "The Eiffel Tower is located in which city?",
        "options": ["London", "Paris", "Rome", "Berlin"],
        "correct": 1
    },
    {
        "image": "images/great_wall.jpg",
        "question": "How long is the Great Wall of China approximately?",
        "options": ["4,000 km", "8,000 km", "12,000 km", "21,196 km"],
        "correct": 3
    },
    {
        "image": "images/machu_picchu.jpg",
        "question": "Machu Picchu is located in which country?",
        "options": ["Peru", "Chile", "Bolivia", "Ecuador"],
        "correct": 0
    },
    {
        "image": "images/pyramids.jpg",
        "question": "The Great Pyramid of Giza is located in which country?",
        "options": ["Sudan", "Libya", "Egypt", "Morocco"],
        "correct": 2
    },
    {
        "image": "images/colosseum.jpg",
        "question": "The Colosseum is located in which city?",
        "options": ["Athens", "Rome", "Venice", "Milan"],
        "correct": 1
    },
    {
        "image": "images/christ_redeemer.jpg",
        "question": "The Christ the Redeemer statue is in which city?",
        "options": ["São Paulo", "Buenos Aires", "Rio de Janeiro", "Lima"],
        "correct": 2
    },
    {
        "image": "images/angkor_wat.jpg",
        "question": "Angkor Wat is located in which country?",
        "options": ["Thailand", "Cambodia", "Vietnam", "Laos"],
        "correct": 1
    },
    {
        "image": "images/statue_of_liberty.jpg",
        "question": "The Statue of Liberty is located in which city?",
        "options": ["New York City", "Boston", "Washington D.C.", "Philadelphia"],
        "correct": 0
    },
    {
        "image": "images/petra.jpg",
        "question": "The ancient city of Petra is carved into rose-colored rock in which country?",
        "options": ["Jordan", "Egypt", "Israel", "Lebanon"],
        "correct": 0
    },
    {
        "image": "images/santorini.jpg",
        "question": "The beautiful white and blue buildings of Santorini are located in which country?",
        "options": ["Italy", "Greece", "Spain", "Croatia"],
        "correct": 1
    },
    {
        "image": "images/mount_fuji.jpg",
        "question": "Mount Fuji is the highest mountain in which country?",
        "options": ["China", "South Korea", "Japan", "Taiwan"],
        "correct": 2
    },
    {
        "image": "images/grand_canyon.jpg",
        "question": "The Grand Canyon is located in which US state?",
        "options": ["Arizona", "Utah", "Nevada", "New Mexico"],
        "correct": 0
    },
    {
        "image": "images/venice.jpg",
        "question": "The famous canals and gondolas are found in which Italian city?",
        "options": ["Rome", "Florence", "Venice", "Milan"],
        "correct": 2
    },
    {
        "image": "images/sydney_opera.jpg",
        "question": "The iconic Opera House is a symbol of which Australian city?",
        "options": ["Melbourne", "Sydney", "Brisbane", "Perth"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=1",
        "question": "What is the capital city of Ireland?",
        "options": ["Dublin", "Belfast", "Cork", "Galway"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=2",
        "question": "Which river is known as the 'Sorrow of China'?",
        "options": ["Yangtze River", "Yellow River", "Pearl River", "Mekong River"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=3",
        "question": "What is the capital city of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=4",
        "question": "Which river has the largest water flow in the world?",
        "options": ["Nile", "Amazon", "Mississippi", "Ganges"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=5",
        "question": "What is the capital city of New Zealand?",
        "options": ["Auckland", "Wellington", "Christchurch", "Hamilton"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=6",
        "question": "Which body of water is the lowest point on Earth's surface?",
        "options": ["Caspian Sea", "Dead Sea", "Red Sea", "Black Sea"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=7",
        "question": "What is the capital city of Canada?",
        "options": ["Toronto", "Vancouver", "Montreal", "Ottawa"],
        "correct": 3
    },
    {
        "image": "https://picsum.photos/800/600?random=8",
        "question": "Which is the largest desert in the world?",
        "options": ["Sahara Desert", "Arabian Desert", "Antarctic Desert", "Gobi Desert"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=9",
        "question": "Which country has the most islands in the world?",
        "options": ["Indonesia", "Japan", "Philippines", "Sweden"],
        "correct": 3
    },
    {
        "image": "https://picsum.photos/800/600?random=10",
        "question": "What is the deepest point on Earth?",
        "options": ["Mariana Trench", "Tonga Trench", "Philippine Trench", "Puerto Rico Trench"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=11",
        "question": "Which is the smallest country in the world?",
        "options": ["Monaco", "San Marino", "Vatican City", "Liechtenstein"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=12",
        "question": "Which continent is known as the 'Land of the Midnight Sun'?",
        "options": ["North America", "Europe", "Antarctica", "Asia"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=13",
        "question": "What is the highest waterfall in the world?",
        "options": ["Niagara Falls", "Victoria Falls", "Iguazu Falls", "Angel Falls"],
        "correct": 3
    },
    {
        "image": "https://picsum.photos/800/600?random=14",
        "question": "Which mountain range is the longest in the world?",
        "options": ["Himalayas", "Rocky Mountains", "Andes", "Alps"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=15",
        "question": "Which country is known as the 'Land of Fire and Ice'?",
        "options": ["Norway", "Iceland", "Greenland", "Finland"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=16",
        "question": "What is the largest lake by surface area in the world?",
        "options": ["Lake Victoria", "Lake Superior", "Caspian Sea", "Lake Huron"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=17",
        "question": "Which country has the most active volcanoes?",
        "options": ["Indonesia", "Japan", "United States", "Italy"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=18",
        "question": "Which country is known as the 'Land of Thousand Lakes'?",
        "options": ["Sweden", "Norway", "Finland", "Denmark"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=19",
        "question": "Which country is known as the 'Land of the Rising Sun'?",
        "options": ["China", "South Korea", "Japan", "Vietnam"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=20",
        "question": "Which is the largest coral reef system in the world?",
        "options": ["Great Barrier Reef", "Red Sea Coral Reef", "New Caledonia Barrier Reef", "Mesoamerican Barrier Reef"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=21",
        "question": "Which country is known as the 'Land of the Long White Cloud'?",
        "options": ["Ireland", "Scotland", "New Zealand", "Iceland"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=22",
        "question": "What is the driest desert in the world?",
        "options": ["Sahara Desert", "Atacama Desert", "Arabian Desert", "Gobi Desert"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=23",
        "question": "Which country has the most time zones?",
        "options": ["Russia", "United States", "France", "China"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=24",
        "question": "Which is the oldest known living tree in the world?",
        "options": ["General Sherman", "Methuselah", "Old Tjikko", "Prometheus"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=25",
        "question": "Which country is known as the 'Land of Smiles'?",
        "options": ["Vietnam", "Thailand", "Philippines", "Malaysia"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=26",
        "question": "What is the largest island in the world?",
        "options": ["New Guinea", "Borneo", "Madagascar", "Greenland"],
        "correct": 3
    },
    {
        "image": "https://picsum.photos/800/600?random=27",
        "question": "Which sea has no coastline?",
        "options": ["Sargasso Sea", "Dead Sea", "Red Sea", "Black Sea"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=28",
        "question": "Which country is known as the 'Land of the Thunder Dragon'?",
        "options": ["Nepal", "Tibet", "Bhutan", "Myanmar"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=29",
        "question": "What is the deepest lake in the world?",
        "options": ["Lake Baikal", "Lake Tanganyika", "Caspian Sea", "Lake Superior"],
        "correct": 0
    },
    {
        "image": "https://picsum.photos/800/600?random=30",
        "question": "Which country has the most lakes?",
        "options": ["United States", "Russia", "Canada", "Finland"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=31",
        "question": "Which is the windiest continent on Earth?",
        "options": ["North America", "Europe", "Antarctica", "Asia"],
        "correct": 2
    },
    {
        "image": "https://picsum.photos/800/600?random=32",
        "question": "Which country is known as the 'Land of Fire'?",
        "options": ["Iceland", "Azerbaijan", "Indonesia", "Chile"],
        "correct": 1
    },
    {
        "image": "https://picsum.photos/800/600?random=33",
        "question": "What percentage of the world's freshwater is stored in Antarctica?",
        "options": ["50%", "60%", "70%", "90%"],
        "correct": 3
    },
    {
        "image": "https://picsum.photos/800/600?random=34",
        "question": "Which mountain has the highest base-to-peak height on Earth?",
        "options": ["Mount Everest", "Mauna Kea", "K2", "Mount Kilimanjaro"],
        "correct": 1
    }
]

def get_image_base64(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            return b64encode(image_file.read()).decode('utf-8')
    except:
        return None

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

def get_random_questions(num_questions=8):
    global recent_questions
    
    # Convert deque to list for easier checking
    recently_used = list(recent_questions)
    
    # Filter out recently used questions
    available_questions = [q for q in QUESTIONS if q not in recently_used]
    
    # If we don't have enough available questions, clear some old ones
    if len(available_questions) < num_questions:
        # Keep only the most recent round of questions in history
        recent_questions = deque(list(recent_questions)[-8:], maxlen=24)
        recently_used = list(recent_questions)
        available_questions = [q for q in QUESTIONS if q not in recently_used]
    
    # Select random questions from available ones
    selected_questions = random.sample(available_questions, num_questions)
    
    # Add selected questions to recent questions
    recent_questions.extend(selected_questions)
    
    return selected_questions

@app.route('/')
def index():
    # Start new quiz with 8 questions
    session['questions'] = get_random_questions()
    session['current_question'] = 0
    session['score'] = 0
    return render_template('quiz.html', creator="Ani")

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/question')
def get_question():
    if 'questions' not in session:
        session['questions'] = get_random_questions()
        session['current_question'] = 0
        session['score'] = 0
    
    if session['current_question'] >= 8:
        return jsonify({
            'finished': True,
            'score': session['score']
        })
    
    question = session['questions'][session['current_question']]
    image_data = get_image_base64(question['image'])
    
    return jsonify({
        'image': question['image'],
        'question': question['question'],
        'options': question['options'],
        'question_number': session['current_question'] + 1,
        'score': session['score'],
        'finished': False
    })

@app.route('/answer', methods=['POST'])
def check_answer():
    if 'questions' not in session:
        return jsonify({'error': 'No active quiz'}), 400
    
    data = request.get_json()
    if 'answer' not in data:
        return jsonify({'error': 'No answer provided'}), 400
    
    current_question = session['questions'][session['current_question']]
    is_correct = data['answer'] == current_question['correct']
    
    if is_correct:
        session['score'] += 1
    
    session['current_question'] += 1
    finished = session['current_question'] >= 8
    
    return jsonify({
        'correct': is_correct,
        'score': session['score'],
        'finished': finished
    })

if __name__ == '__main__':
    Timer(1, open_browser).start()  # Open browser after 1 second
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 