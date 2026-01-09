import datetime
import wikipedia

def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I help you?"

    elif "time" in user_input:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}"

    elif "date" in user_input:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}"

    elif "wikipedia" in user_input:
        try:
            query = user_input.replace("wikipedia", "").strip()
            result = wikipedia.summary(query, sentences=2)
            return result
        except:
            return "Sorry, I could not find anything on Wikipedia."

    else:
        return "I am still learning. Please ask something else."
