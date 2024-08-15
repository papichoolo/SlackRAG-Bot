import os
import random
import time
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from slack_sdk import WebClient
from dotenv import find_dotenv, load_dotenv
from pdflogic import RAGSystem

# Load environment variables
load_dotenv(find_dotenv())

# Set up Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set up Slack app
slack_app = App(token=os.environ["SLACK_BOT_TOKEN"])
handler = SlackRequestHandler(slack_app)
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize RAG system
rag_system = RAGSystem()

# Fun loading messages
loading_messages = [
    "Hmm, let me think about that for a second...",
    "Searching through the document forest...",
    "Consulting my digital crystal ball...",
    "Crunching numbers and letters...",
    "Let me dig into that for you...",
]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the uploaded PDF
            rag_system.setup(file_path)
            
            return f"File uploaded and processed successfully. You can now ask questions about {filename}."
    return render_template('upload.html')

@app.route('/slack/events', methods=['POST'])
def slack_events():
    return handler.handle(request)

@slack_app.event("app_mention")
def handle_mentions(body, say):
    text = body["event"]["text"]
    user = body["event"]["user"]
    channel = body["event"]["channel"]
    mention = f"<@{os.environ['SLACK_BOT_USER_ID']}>"
    text = text.replace(mention, "").strip()
    
    if text.lower().startswith("q!") or text.lower().startswith("question!"):
        question = text[2:].strip() if text.lower().startswith("q!") else text[9:].strip()
        
        # Send a random loading message
        loading_message = random.choice(loading_messages)
        message = client.chat_postMessage(channel=channel, text=f"<@{user}> {loading_message}")
        
        # Simulate typing time
        time.sleep(0.5)
        
        # Get the answer
        answer = rag_system.answer_question(question)
        
        # Update the message with the answer
        client.chat_update(
            channel=channel,
            ts=message['ts'],
            text=f"<@{user}> Here's what I found:\n\n{answer}"
        )
    
    elif text.lower() == "help":
        help_message = (
            "Here's how you can interact with me:\n"
            "• Ask a question by starting your message with 'q!' or 'question!'\n"
            "• Type 'help' to see this message again\n"
            "• Say 'hello' or 'hi' for a friendly greeting\n"
            "• Use 'status' to check if a PDF has been uploaded"
        )
        say(help_message)
    
    elif text.lower() in ["hello", "hi", "hey"]:
        greetings = [
            f"Hello there, <@{user}>! How can I assist you today?",
            f"Hi <@{user}>! Got any interesting questions for me?",
            f"Hey <@{user}>! Ready to explore some documents?"
        ]
        say(random.choice(greetings))
    
    elif text.lower() == "status":
        if rag_system.is_ready():
            say(f"<@{user}> A PDF has been uploaded and I'm ready to answer questions!")
        else:
            say(f"<@{user}> No PDF has been uploaded yet. Please upload a document first.")
    
    else:
        say(f"<@{user}> Not sure what you mean. Type 'help' to see what I can do!")

# Error handler
@slack_app.error
def custom_error_handler(error, body, logger):
    logger.exception(f"Error: {error}")
    say = body["say"]
    say("Oops! Something went wrong. Please try again later or contact support.")

if __name__ == '__main__':
    app.run(debug=True)