from flask import Flask, render_template, request, jsonify
import datetime
import random
import re

app = Flask(__name__)

# Enhanced response database
responses = {
    'greeting': [
        "Hello! How can I assist you today?",
        "Hi there! What can I help you with?",
        "Greetings! I'm JARVIS, ready to help!",
        "Hey! How may I be of service?"
    ],
    'time': [
        "The current time is {time}",
        "Right now it's {time}",
        "It's {time} at the moment"
    ],
    'date': [
        "Today's date is {date}",
        "The current date is {date}",
        "It's {date} today"
    ],
    'help': [
        "I can help you with: time, date, calculations, jokes, fun facts, general questions, and much more!",
        "I'm here to assist with information, answer questions, tell jokes, perform calculations, and chat with you!"
    ],
    'joke': [
        "Why did the programmer quit his job? Because he didn't get arrays! 😄",
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "What's a computer's favorite snack? Microchips! 🖥️"
    ],
    'fact': [
        "Did you know? The first computer programmer was Ada Lovelace in the 1840s!",
        "Fun fact: The term 'bug' in computing came from an actual moth found in a computer!",
        "Amazing fact: The first computer mouse was made of wood!"
    ],
    'thanks': [
        "You're welcome! Happy to help!",
        "My pleasure! Let me know if you need anything else!"
    ],
    'python': [
        "Python is a high-level programming language known for its simplicity and readability!",
        "Python is great for beginners and professionals alike!"
    ],
    'how_are_you': [
        "I'm doing great, thanks for asking! How can I assist you today?",
        "I'm functioning perfectly and ready to help!"
    ]
}

def get_response(user_input):
    """Generate intelligent response based on user input"""
    text = user_input.lower().strip()
    
    # Greeting
    if any(word in text for word in ['hello', 'hi', 'hey', 'greetings']):
        return random.choice(responses['greeting'])
    
    # Time
    if 'time' in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return random.choice(responses['time']).format(time=current_time)
    
    # Date
    if 'date' in text or 'today' in text:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        return random.choice(responses['date']).format(date=current_date)
    
    # Help
    if 'help' in text or 'what can you do' in text:
        return random.choice(responses['help'])
    
    # Jokes
    if 'joke' in text or 'funny' in text:
        return random.choice(responses['joke'])
    
    # Facts
    if 'fact' in text or 'interesting' in text:
        return random.choice(responses['fact'])
    
    # Thanks
    if 'thank' in text:
        return random.choice(responses['thanks'])
    
    # Python
    if 'python' in text:
        return random.choice(responses['python'])
    
    # How are you
    if 'how are you' in text or 'whats up' in text:
        return random.choice(responses['how_are_you'])
    
    # Math
    try:
        # Simple math detection
        if any(op in text for op in ['+', '-', '*', '/', 'plus', 'minus']):
            text = text.replace('plus', '+').replace('minus', '-')
            text = text.replace('times', '*').replace('divide', '/')
            
            match = re.search(r'(\d+\.?\d*)\s*([+\-*/])\s*(\d+\.?\d*)', text)
            if match:
                num1, op, num2 = match.groups()
                num1, num2 = float(num1), float(num2)
                
                if op == '+': result = num1 + num2
                elif op == '-': result = num1 - num2
                elif op == '*': result = num1 * num2
                elif op == '/': 
                    if num2 == 0: return "Cannot divide by zero!"
                    result = num1 / num2
                
                return f"The answer is {result}"
    except:
        pass
    
    # Default
    return "I'm here to help! Try asking me about time, jokes, facts, or math calculations!"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        bot_reply = get_response(user_message)
        return jsonify({'reply': bot_reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'reply': 'I can help you! Try asking about time, jokes, or facts!'})

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 JARVIS AI Server Starting...")
    print("="*50)
    print("📍 Open your browser and go to: http://localhost:5000")
    print("⚡ Press Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)