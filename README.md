# architecture_agent
AI-Powered Architectural Assistant
This project is an AI-powered Architectural Assistant designed to streamline the initial client needs assessment phase for architectural projects. It interacts with clients through a chat interface to gather detailed information on various aspects of their lifestyle, preferences, and project requirements. Once sufficient data is collected, it can generate a comprehensive architectural proposal in PDF format.

 Features
Interactive Chat Interface: Engages users in a structured conversation to collect project requirements.

Intelligent Questioning: Uses an AI model (Qwen/Qwen3-32B via Hugging Face Inference API) to ask specific, open-ended questions based on predefined topics.

Dynamic Client Name Capture: Automatically extracts the client's name from the conversation for personalization.

Comprehensive Proposal Generation: Synthesizes collected information into a formal architectural proposal.

PDF Export: Generates professional-looking PDF documents of the architectural proposals using ReportLab.

Session Management: Maintains conversation history and project state using Flask sessions.

 Technologies Used
Python: The core programming language.

Flask: Web framework for building the application's backend and serving the chat interface.

Hugging Face Inference Client: For interacting with large language models (specifically Qwen/Qwen3-32B).

ReportLab: Python library for generating PDF documents.

python-dotenv: For managing environment variables.

secrets: For generating secure session keys.

Logging: For application monitoring and debugging.

 Project Structure
.
├── .env (create this file for your HF_TOKEN)
├── __pycache__/
├── archagent/
│   ├── __init__.py
│   └── (other potential modules if expanded)
├── static/
│   └── css/
│       └── style.css (presumed, for chat UI)
│   └── js/
│       └── script.js (presumed, for chat UI)
├── templates/
│   └── chat.html
├── agent.py
├── app.py
├── requirements.txt
└── README.md
app.py: The main Flask application, handling routes, user interaction, and session management. It orchestrates the conversation flow and calls agent.py for AI inference and PDF generation.

agent.py: Contains the core logic for interacting with the Hugging Face Inference Client (ask_ollama function) and generating PDF documents (generate_pdf function).

requirements.txt: Lists all Python dependencies required for the project.

.env: (To be created) Stores sensitive information like your Hugging Face API token.

templates/: Contains HTML templates (e.g., chat.html for the chat interface).

static/: Contains static assets like CSS and JavaScript files for the frontend (not explicitly shown in code but implied by render_template).

 Installation and Setup
Follow these steps to get the project up and running on your local machine:

Clone the Repository:

Bash

git clone <repository_url>
cd <repository_name>
Create a Virtual Environment (Recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

Bash

pip install -r requirements.txt
Configure Environment Variables:
Create a file named .env in the root directory of your project (at the same level as app.py and agent.py). Add your Hugging Face API token to it:

HF_TOKEN="your_hugging_face_api_token_here"
You can obtain a Hugging Face API token from your Hugging Face settings page.

Run the Application:

Bash

python app.py
The application will typically run on http://0.0.0.0:5000 (or http://127.0.0.1:5000).

 Usage
Start the Application: Run python app.py and navigate to the displayed URL in your web browser.

Begin Conversation: The chat interface will prompt you with the first question.

Provide Information: Answer the questions asked by the AI assistant regarding your architectural needs. The assistant will guide you through various topics like family structure, lifestyle, aesthetic preferences, etc.

Advance Topics: You can type "next", "done", "that's all", or "move on" to explicitly move to the next topic if you feel you've provided enough information for the current one.

Generate Proposal: Once all topics are covered (or you feel you have provided sufficient details), click the "Generate Proposal" button (this button would be present in your chat.html template, though not explicitly shown in the provided code, it's implied by the /generate_proposal endpoint).

Download PDF: After the proposal is generated, a "Download PDF" button (implied by the /download endpoint) will appear, allowing you to save the architectural proposal as a PDF document. The PDF will be named [Client_Name]_Architecture_Proposal.pdf if the client's name was identified.

 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Make your changes.

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a Pull Request.
