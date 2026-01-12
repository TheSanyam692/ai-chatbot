from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import datetime
import random
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store chat history (in production, use a database)
chats = {}
current_id = 0

# Enhanced response database
responses = {
    'greeting': [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Greetings! I'm JARVIS, ready to help!",
        "Hey! How may I be of service?",
        "Welcome! I'm here to assist you with anything you need!"
    ],
    'time': [
        "The current time is {time}",
        "Right now it's {time}",
        "It's {time} at the moment",
        "The time is currently {time}"
    ],
    'date': [
        "Today's date is {date}",
        "The current date is {date}",
        "It's {date} today",
        "Today is {date}"
    ],
    'weather': [
        "I don't have real-time weather access, but you can check weather.com or your local weather service!",
        "For accurate weather information, I recommend checking your local weather forecast online.",
        "I'm unable to check weather currently, but weather apps can give you live updates!",
        "I can't access live weather data, but try checking weather.com for your area!"
    ],
    'help': [
        "I can help you with: time, date, calculations, jokes, fun facts, general questions, and much more!",
        "I'm here to assist with information, answer questions, tell jokes, perform calculations, and chat with you!",
        "Ask me about time, dates, math problems, jokes, facts, or just chat with me!",
        "I can do many things: answer questions, solve math problems, tell jokes, provide facts, and more!"
    ],
    'joke': [
        "Why did the programmer quit his job? Because he didn't get arrays! 😄",
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "What's a computer's favorite snack? Microchips! 🖥️",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself! 😅",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
        "What do you call a programmer from Finland? Nerdic! 🇫🇮",
        "Why do Java developers wear glasses? Because they don't C#! 👓"
    ],
    'fact': [
        "Did you know? The first computer programmer was Ada Lovelace in the 1840s!",
        "Fun fact: The term 'bug' in computing came from an actual moth found in a computer!",
        "Amazing fact: The first computer mouse was made of wood!",
        "Interesting: The first 1GB hard drive weighed over 500 pounds!",
        "Cool fact: The QWERTY keyboard layout was designed to slow down typing to prevent typewriter jams!",
        "Did you know? The average person blinks 15-20 times per minute!",
        "Fun fact: Honey never spoils. Archaeologists found 3000-year-old honey that was still edible!"
    ],
    'thanks': [
        "You're welcome! Happy to help!",
        "My pleasure! Let me know if you need anything else!",
        "Anytime! That's what I'm here for!",
        "Glad I could help! Feel free to ask more questions!",
        "No problem at all! I'm always here to assist!"
    ],
    'goodbye': [
        "Goodbye! Have a great day!",
        "See you later! Take care!",
        "Bye! Come back anytime!",
        "Farewell! It was nice chatting with you!",
        "Take care! Looking forward to our next conversation!"
    ],
    'name': [
        "I'm JARVIS, your AI assistant created to help you!",
        "My name is JARVIS - Just A Rather Very Intelligent System!",
        "I'm JARVIS, always here to assist you!",
        "Call me JARVIS! I'm your personal AI assistant!"
    ],
    'age': [
        "I'm a digital entity, so age doesn't apply to me in the traditional sense!",
        "I exist in the digital realm, beyond the concept of age!",
        "As an AI, I don't age, but I'm constantly learning and improving!",
        "Age is just a number, and for AI like me, it's not really applicable!"
    ],
    'creator': [
        "I was created by talented developers who wanted to make a helpful AI assistant!",
        "My creators are passionate developers working to make AI more accessible!",
        "I'm the result of creative programming and AI development!",
        "I was built by developers who believe in the power of AI to help people!"
    ],
    'python': [
        "Python is a high-level, interpreted programming language known for its simplicity and readability!",
        "Python is great for beginners and professionals alike. It's used in web development, data science, AI, and more!",
        "Python was created by Guido van Rossum and first released in 1991. It's now one of the most popular languages!",
        "Python is named after Monty Python's Flying Circus, not the snake! 🐍"
    ],
    'love': [
        "That's sweet! I'm here to help you anytime! 😊",
        "Aww, thank you! I enjoy our conversations too!",
        "You're very kind! I'm always happy to assist you!",
        "I appreciate that! Let's keep having great conversations!"
    ],
    'how_are_you': [
        "I'm doing great, thanks for asking! I'm always ready to help. How can I assist you today?",
        "I'm functioning perfectly and ready to help! What can I do for you?",
        "I'm excellent! As an AI, I'm always in good spirits. How about you?",
        "I'm doing wonderful! Thanks for asking. What would you like to know?"
    ],
    'capabilities': [
        "I can answer questions, solve math problems, tell jokes, provide facts, give you the time and date, and have friendly conversations!",
        "My capabilities include: calculations, general knowledge, jokes, facts, time/date info, and engaging chat!",
        "I'm designed to assist with various tasks: answering questions, solving problems, entertainment, and information!"
    ],
    'default': [
        "That's an interesting question! Can you tell me more?",
        "I'm still learning about that. Could you rephrase or ask something else?",
        "Hmm, I'm not sure about that one. Try asking me about time, jokes, facts, or calculations!",
        "I don't have enough information about that. Ask me something else!",
        "That's beyond my current knowledge. Try asking about math, jokes, or general topics!"
    ]
}

def get_response(user_input):
    """Generate intelligent response based on user input"""
    user_input_lower = user_input.lower().strip()
    
    # Greeting detection
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'hola', 'namaste']):
        return random.choice(responses['greeting'])
    
    # Time queries
    if any(phrase in user_input_lower for phrase in ['time', 'what time', "what's the time", 'current time', 'tell me the time']):
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return random.choice(responses['time']).format(time=current_time)
    
    # Date queries
    if any(phrase in user_input_lower for phrase in ['date', 'what date', "what's the date", 'today', "today's date", 'current date']):
        if 'time' not in user_input_lower:  # Don't trigger if asking for time
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            return random.choice(responses['date']).format(date=current_date)
    
    # Weather queries
    if any(word in user_input_lower for word in ['weather', 'temperature', 'forecast', 'raining', 'sunny', 'climate']):
        return random.choice(responses['weather'])
    
    # Help queries
    if any(phrase in user_input_lower for phrase in ['help', 'what can you do', 'capabilities', 'features', 'how can you help', 'what do you do']):
        return random.choice(responses['help'])
    
    # Joke requests
    if any(word in user_input_lower for word in ['joke', 'funny', 'laugh', 'humor', 'make me laugh']):
        return random.choice(responses['joke'])
    
    # Fact requests
    if any(phrase in user_input_lower for phrase in ['fact', 'tell me something', 'interesting', 'amazing', 'did you know', 'fun fact']):
        return random.choice(responses['fact'])
    
    # Thanks/Gratitude
    if any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate', 'grateful', 'thx']):
        return random.choice(responses['thanks'])
    
    # Goodbye
    if any(word in user_input_lower for word in ['bye', 'goodbye', 'see you', 'farewell', 'gotta go', 'take care']):
        return random.choice(responses['goodbye'])
    
    # Name queries
    if any(phrase in user_input_lower for phrase in ['your name', 'who are you', 'what are you', "what's your name"]):
        return random.choice(responses['name'])
    
    # Age queries
    if any(phrase in user_input_lower for phrase in ['your age', 'how old', 'age']):
        return random.choice(responses['age'])
    
    # Creator queries
    if any(phrase in user_input_lower for phrase in ['creator', 'made you', 'created you', 'built you', 'who made']):
        return random.choice(responses['creator'])
    
    # Python queries
    if 'python' in user_input_lower and 'wikipedia' not in user_input_lower:
        return random.choice(responses['python'])
    
    # Love/Like queries
    if any(phrase in user_input_lower for phrase in ['love you', 'like you', 'adore you']):
        return random.choice(responses['love'])
    
    # How are you
    if any(phrase in user_input_lower for phrase in ['how are you', 'how do you do', "what's up", 'whats up', 'how r u']):
        return random.choice(responses['how_are_you'])
    
    # Capabilities
    if any(phrase in user_input_lower for phrase in ['what can you', 'tell me what', 'your capabilities', 'your features']):
        return random.choice(responses['capabilities'])
    
    # Math calculations
    math_result = handle_math(user_input_lower)
    if math_result:
        return math_result
    
    # Wikipedia-style queries
    if 'wikipedia' in user_input_lower or 'wiki' in user_input_lower:
        return "I don't have direct Wikipedia access, but I can answer general questions! What would you like to know?"
    
    # Default response
    return random.choice(responses['default'])

def handle_math(text):
    """Handle mathematical calculations"""
    try:
        # Remove extra spaces
        text = ' '.join(text.split())
        
        # Replace word operators
        text = text.replace('plus', '+').replace('add', '+')
        text = text.replace('minus', '-').replace('subtract', '-')
        text = text.replace('multiply', '*').replace('times', '*').replace('multiplied by', '*')
        text = text.replace('divide', '/').replace('divided by', '/')
        
        # Try to find calculation pattern
        patterns = [
            r'(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)',
            r'what\s+is\s+(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)',
            r'calculate\s+(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                num1, operator, num2 = match.groups()
                num1, num2 = float(num1), float(num2)
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "Cannot divide by zero! That's a mathematical impossibility! 🚫"
                    result = num1 / num2
                
                # Format result nicely
                if result == int(result):
                    return f"The answer is {int(result)} ✨"
                else:
                    return f"The answer is {result:.2f} ✨"
    except Exception as e:
        print(f"Math calculation error: {e}")
    
    return None

@app.route('/')
def home():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'reply': 'Please send a valid message!'}), 400
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'reply': 'Please say something!'}), 400
        
        # Get bot response
        bot_reply = get_response(user_message)
        
        # Store in chat history
        global current_id
        if current_id not in chats:
            chats[current_id] = []
        
        chats[current_id].append({
            'user': user_message,
            'bot': bot_reply,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
        return jsonify({
            'reply': bot_reply,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'reply': 'Sorry, I encountered an error processing your message. Please try again!'
        }), 500

@app.route('/new_chat', methods=['POST'])
def new_chat():
    """Create a new chat session"""
    try:
        global current_id
        current_id += 1
        chats[current_id] = []
        
        return jsonify({
            'status': 'ok',
            'chat_id': current_id,
            'message': 'New chat created successfully!'
        })
    
    except Exception as e:
        print(f"Error creating new chat: {e}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to create new chat'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting JARVIS AI Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🌐 To access from other devices, use your local IP address")
    print("⚡ Press Ctrl+C to stop the server\n")
    
    # Run the Flask app
    app.run(
        debug=True,           # Enable debug mode for development
        host='0.0.0.0',      # Listen on all network interfaces
        port=5000,           # Port number
        threaded=True        # Enable threading for concurrent requests
    )