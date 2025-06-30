import os
import logging
from datetime import datetime
from huggingface_hub import InferenceClient
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load .env from root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

HF_API_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "Qwen/Qwen3-32B"

if not HF_API_TOKEN:
    logging.error("❌ HF_TOKEN is not set in .env or environment variables.")
else:
    logging.info("✅ HF_TOKEN loaded successfully.")

# Initialize Inference Client
try:
    client = InferenceClient(provider="hf-inference", api_key=HF_API_TOKEN)
    logging.info(f"✅ InferenceClient initialized for model: {MODEL_NAME}")
except Exception as e:
    logging.exception("❌ Failed to initialize InferenceClient")

def ask_ollama(prompt: str) -> str:
    logging.debug(f"📨 Prompt sent: {prompt[:200]}...")
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
        )
        reply = completion.choices[0].message.content.strip()
        logging.debug(f"✅ Model response: {reply[:200]}...")
        return reply
    except Exception as e:
        logging.exception("❌ Error during model inference")
        return f"Error: {str(e)}"

def generate_pdf(proposal_text: str, filename: str = "architecture_proposal.pdf", client_name: str = "Client") -> str:
    logging.info(f"📄 Generating PDF: {filename}")
    try:
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=72,
            bottomMargin=50
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name="TitleStyle", fontSize=28, leading=36, alignment=1, textColor=colors.HexColor("#0D47A1"), spaceAfter=10)
        subtitle_style = ParagraphStyle(name="SubtitleStyle", fontSize=14, leading=20, alignment=1, textColor=colors.HexColor("#546E7A"), spaceAfter=30)
        section_header = ParagraphStyle(name="SectionHeader", fontSize=16, leading=22, textColor=colors.HexColor("#1A237E"), spaceBefore=16, spaceAfter=8, underlineWidth=1, underlineOffset=-2)
        body_style = ParagraphStyle(name="BodyStyle", fontSize=12, leading=18, textColor=colors.HexColor("#212121"), spaceAfter=10)

        story = [
            Spacer(1, 2.5 * inch),
            Paragraph("Architecture Proposal", title_style),
            Paragraph("Prepared by Architecture Assistant", subtitle_style),
            Paragraph(f"<i>{datetime.now().strftime('%B %d, %Y')}</i>", subtitle_style),
            PageBreak()
        ]

        sections = proposal_text.strip().split("\n\n")
        for para in sections:
            para = para.strip()
            if not para:
                continue
            if any(para.lower().startswith(f"{n}.") for n in range(1, 21)):
                story.append(HRFlowable(width="100%", color=colors.HexColor("#90CAF9"), thickness=1, spaceBefore=10, spaceAfter=6))
                story.append(Paragraph(f"<u><b>{para}</b></u>", section_header))
            elif para.lstrip().startswith(("- ", "* ", "•", "1. ")):
                items = [line.strip("-*• ").strip() for line in para.splitlines() if line.strip()]
                list_flow = ListFlowable([ListItem(Paragraph(item, body_style)) for item in items], bulletType='bullet', leftIndent=20)
                story.append(list_flow)
            else:
                story.append(Paragraph(para.replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 0.15 * inch))

        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(f"Sincerely,<br/>{client_name}<br/>Architectural Assistant", body_style))
        doc.build(story)
        logging.info("✅ PDF generation completed.")
        return filename

    except Exception as e:
        logging.exception("❌ Failed to generate PDF")
        return "Error generating PDF"
