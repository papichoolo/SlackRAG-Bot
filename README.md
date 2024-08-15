# Slack RAG Bot

## Overview
The application is a Flask-based web server that integrates a Slack bot with a RAG (Retrieval-Augmented Generation) system for answering questions about uploaded PDF documents. It uses the Slack Bolt framework for handling Slack events and the custom RAGSystem for processing PDFs and answering questions.

## Demo Video

A demonstration of this project can be viewed [here](https://drive.google.com/file/d/1S-LT3pWbtdOz9M_6LhSVvTOpmQOJbw8f/view?usp=sharing).

## Key Components

Flask App: Handles web requests, including file uploads.
Slack App: Manages Slack events and interactions.
RAG System: Processes PDFs and answers questions based on their content.

# Setting up Slack RAG Bot

## 1. Set up your local environment

1. Clone your GitHub repository and navigate to the project directory.
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```
   pip install flask slack-bolt python-dotenv werkzeug langchain langchain-community langchain-openai langchain-chroma chromadb openai
   ```

## 2. Set up ngrok

1. Download and install ngrok from https://ngrok.com/download
2. Authenticate ngrok with your account token:
   ```
   ngrok authtoken YOUR_AUTH_TOKEN
   ```

## 3. Create a Slack App

1. Go to https://api.slack.com/apps and click "Create New App"
2. Choose "From scratch" and give your app a name
3. Select the workspace where you want to develop your app

## 4. Configure your Slack App

1. In the "Basic Information" section, note down your "Signing Secret"
2. Go to "OAuth & Permissions" and add the following bot token scopes:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
3. Install the app to your workspace
4. Note down the "Bot User OAuth Token"

## 5. Set up environment variables

Create a `.env` file in your project root with the following content:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
SLACK_BOT_USER_ID=your-bot-user-id
OPENAI_API_KEY=your-openai-api-key
```

Replace the placeholders with your actual values. Note the addition of the OPENAI_API_KEY, which is required for the RAG system.

## 6. Configure the RAG System

Make sure the `pdflogic.py` file (which imports `RAGSystem`) is also present and correctly implemented.

## 7. Start your local server and ngrok

1. Start your Flask server:
   ```
   python app.py
   ```
2. In a new terminal, start ngrok:
   ```
   ngrok http 5000
   ```
3. Note the HTTPS URL provided by ngrok (e.g., `https://1234-abcd-efgh.ngrok.io`)

## 8. Configure Slack Event Subscriptions

1. Go to your Slack App's "Event Subscriptions" page
2. Enable events and enter your ngrok URL + `/slack/events` as the Request URL
   (e.g., `https://1234-abcd-efgh.ngrok.io/slack/events`)
3. Subscribe to the `app_mention` bot event

## 9. Test your bot

1. Invite your bot to a channel in your Slack workspace
2. Upload a PDF: Access your ngrok URL in a web browser and use the upload form
3. Ask questions: In Slack, mention your bot and start with `q!` or `question!`, e.g., `@YourBot q! What's in the PDF?`

## Usage

- Upload a PDF: Access your ngrok URL in a web browser and use the upload form
- Ask questions: In Slack, mention your bot and start with `q!` or `question!`
- Get help: Mention your bot and type `help`
- Check status: Mention your bot and type `status`

## Important Notes

1. Keep your `.env` file secure and never commit it to your repository. Add it to your `.gitignore` file.
2. The ngrok URL changes each time you restart ngrok. Update your Slack App's Event Subscriptions URL when this happens.
3. Ensure your Flask app is running on port 5000, as that's what the ngrok command is set up for.
4. The RAG system uses OpenAI's GPT-4o-mini model. Make sure you have access to this model and sufficient API credits.
5. The first question after uploading a PDF might take longer to answer as the system processes the document.

Remember to upload a PDF through the web interface before trying to ask questions about it in Slack.
