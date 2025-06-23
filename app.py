from flask import Flask, render_template, request, jsonify, send_file, session
from agent import ask_ollama, generate_pdf
import os

app = Flask(__name__)
app.secret_key = "very_secret_key"

questions = [
    "What is your name?",
    "What is the type of project? (Residential, Commercial, etc.)",
    "How many people are in your family?",
    "Do you have any pets?",
    "How many bedrooms and bathrooms do you want?",
    "Do you need a study, pooja room, or home office?",
    "What is the plot size?",
    "Do you have style preferences? (Modern, traditional, vastu, etc.)",
    "Do you need parking? For how many vehicles?",
    "Would you like a garden, balcony, or terrace?",
    "What's the climate like in your area?",
    "Do you need any eco-friendly features? (solar, rainwater harvesting)",
    "What is your budget?",
    "What's your expected construction timeline?"
]

@app.route('/')
def index():
    session['answers'] = []
    session['current_q'] = 0
    session['proposal'] = ""
    session['confirmed'] = False
    session['pdf_name'] = ""
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message']
    answers = session.get('answers', [])
    current_q = session.get('current_q', 0)
    confirmed = session.get('confirmed', False)
    proposal = session.get('proposal', "")
    pdf_name = session.get('pdf_name', "architecture_proposal.pdf")

    if proposal and not confirmed:
        if user_msg.strip().lower() in ["yes", "download", "y"]:
            generate_pdf(proposal, filename=pdf_name)
            session['confirmed'] = True
            return jsonify({'reply': f"✅ PDF saved as '{pdf_name}'. Click below to download.", 'done': True, 'pdf_url': '/download'})
        else:
            return jsonify({'reply': "❌ Okay, the PDF won't be saved. Let me know if you change your mind."})

    if current_q < len(questions):
        answers.append(user_msg)
        session['answers'] = answers
        session['current_q'] = current_q + 1

        if current_q == 0:
            safe_name = user_msg.strip().replace(" ", "_")
            session['pdf_name'] = f"{safe_name}_Architecture_Proposal.pdf"

        if current_q + 1 < len(questions):
            return jsonify({'reply': questions[current_q + 1]})
        else:
            detail_text = "\n".join([f"{questions[i]} {answers[i]}" for i in range(len(answers))])
            processing_message = "⏳ Got it! Processing your responses and creating the proposal..."
            prompt = f"You are an architectural assistant. Based on the following details, write a formal architecture proposal:\n\n{detail_text}"

            proposal_text = ask_ollama(prompt)
            session['proposal'] = proposal_text

            reply = f"{processing_message}\n\n📄 Here's your proposal:\n\n{proposal_text}\n\nWould you like to save this as a PDF?"
            return jsonify({'reply': reply})

    return jsonify({'reply': "⚠️ Something went wrong. Please refresh and try again."})

@app.route('/download')
def download():
    pdf_name = session.get('pdf_name', "architecture_proposal.pdf")
    return send_file(pdf_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
