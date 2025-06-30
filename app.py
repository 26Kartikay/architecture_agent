from flask import Flask, render_template, request, jsonify, send_file, session
from agent import ask_ollama, generate_pdf
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

topics = [
    "family structure",
    "daily lifestyle and activities",
    "work profiles",
    "guest visits",
    "aesthetic preferences",
    "outdoor area usage (ground floor, balconies, terrace)",
    "future plans or luxury features (home theatre, swimming pool, etc.)",
    "vastu preferences",
    "other residents like pets, domestic help, etc."
]

@app.route('/')
def index():
    session['conversation'] = []
    session['topic_index'] = 0
    session['completed'] = False
    session['proposal'] = ""
    session['client_name'] = "Client"
    session['pdf_name'] = "architecture_proposal.pdf"
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    conversation = session.get('conversation', [])
    topic_index = session.get('topic_index', 0)
    client_name = session.get('client_name', "Client")

    conversation.append({"role": "user", "content": user_msg})

    if topic_index == 0 and "name is" in user_msg.lower():
        name = user_msg.split("is")[-1].strip().title()
        session['client_name'] = name
        session['pdf_name'] = f"{name.replace(' ', '_')}_Architecture_Proposal.pdf"

    if any(trigger in user_msg.lower() for trigger in ["next", "done", "that's all", "move on"]):
        topic_index += 1
        session['topic_index'] = topic_index

    if topic_index >= len(topics):
        return jsonify({'reply': "All topics have been covered. You may now generate the proposal using the button."})

    current_topic = topics[topic_index]
    chat_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation[-10:]])

    prompt = (
        f"You are an expert AI-powered Senior Architectural Consultant specializing in client needs assessment for residential and commercial projects. "
        f"Your primary objective is to meticulously gather detailed, nuanced information from the client to inform a comprehensive architectural proposal. "
        f"You are currently engaged in a focused discussion about the client's needs concerning: **{current_topic}**.\n\n"
        f"Your task is to formulate **ONE highly specific, open-ended, and insightful question** directly related to the current topic. "
        f"This question should aim to:\n"
        f"- Elicit detailed, qualitative information from the client.\n"
        f"- Uncover their preferences, priorities, challenges, and aspirations for this specific aspect.\n"
        f"- Build naturally on the immediately preceding conversation turn if applicable, or explore a new sub-aspect of the current topic.\n"
        f"- Avoid leading questions or assuming answers.\n\n"
        f"**Crucial Constraints:**\n"
        f"- **DO NOT** repeat questions that have already been asked or clearly implied by the conversation history.\n"
        f"- **DO NOT** introduce or hint at the next topic in the overall sequence. Focus entirely on exhaustively understanding the current topic.\n"
        f"- **DO NOT** include any internal reasoning, explanation, or thought process.\n"
        f"- **Your response MUST ONLY be the single question itself.**\n\n"
        f"**Current Conversation Context (Last 10 turns for relevance):**\n"
        f"```\n{chat_context}\n```\n\n"
        f"Important: Only output the final question. Do NOT include any internal reasoning, explanations, or thought process. Your response must ONLY be the single question, without any other content.\n\n"
        f"Question:"
    )

    bot_reply = ask_ollama(prompt)

    # Fallback cleanup if reasoning still leaks in
    if bot_reply.count("?") >= 1:
        bot_reply = bot_reply.strip().split("?")[-2].split("\n")[-1].strip() + "?"

    conversation.append({"role": "assistant", "content": bot_reply})
    session['conversation'] = conversation

    return jsonify({'reply': bot_reply})

@app.route('/generate_proposal', methods=['POST'])
def generate_proposal():
    conversation = session.get('conversation', [])
    client_name = session.get('client_name', "Client")

    if not conversation:
        return jsonify({'reply': "Not enough information yet to generate a proposal."})

    full_convo = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation])
    proposal_prompt = (
        f"Based on the conversation below, generate a formal architecture proposal.\n"
        f"Include room recommendations, lifestyle fit, design suggestions, and any preferences.\n"
        f"Sign the document at the end as the client: {client_name}.\n\n{full_convo}"
    )

    proposal = ask_ollama(proposal_prompt)
    session['proposal'] = proposal
    return jsonify({'reply': proposal})

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf_endpoint():
    proposal = session.get('proposal', "")
    client_name = session.get('client_name', "Client")
    pdf_name = session.get('pdf_name', "architecture_proposal.pdf")

    if not proposal:
        return jsonify({'reply': "No proposal available yet. Please generate one first."})

    try:
        generate_pdf(proposal, filename=pdf_name, client_name=client_name)
        session['completed'] = True
        return jsonify({'reply': f"PDF saved as {pdf_name}.", 'pdf_url': '/download'})
    except Exception as e:
        return jsonify({'reply': f"Error generating PDF: {str(e)}"})

@app.route('/download')
def download():
    pdf_name = session.get('pdf_name', "architecture_proposal.pdf")
    return send_file(pdf_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
