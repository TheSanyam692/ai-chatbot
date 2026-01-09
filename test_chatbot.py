from chatbot import chatbot_response

while True:
    user = input("You: ")
    print("Bot:", chatbot_response(user))
