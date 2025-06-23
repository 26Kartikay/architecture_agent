import subprocess
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    HRFlowable,
    ListFlowable,
    ListItem
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


def ask_ollama(prompt: str) -> str:
    """Send prompt to local LLaMA model running via Ollama"""
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def generate_pdf(proposal_text: str, filename: str = "architecture_proposal.pdf") -> str:
    """Generate a stylized architecture proposal PDF with cover page and formatted content"""

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=72,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=28,
        leading=36,
        alignment=1,
        textColor=colors.HexColor("#0D47A1"),
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        name="SubtitleStyle",
        fontSize=14,
        leading=20,
        alignment=1,
        textColor=colors.HexColor("#546E7A"),
        spaceAfter=30
    )

    section_header = ParagraphStyle(
        name="SectionHeader",
        fontSize=16,
        leading=22,
        textColor=colors.HexColor("#1A237E"),
        spaceBefore=16,
        spaceAfter=8,
        underlineWidth=1,
        underlineOffset=-2
    )

    body_style = ParagraphStyle(
        name="BodyStyle",
        fontSize=12,
        leading=18,
        textColor=colors.HexColor("#212121"),
        spaceAfter=10
    )

    story = []

    # ===== PAGE 1: COVER =====
    story.append(Spacer(1, 2.5 * inch))
    story.append(Paragraph("🏗️ <b>Architecture Proposal</b>", title_style))
    story.append(Paragraph("Prepared by Architecture Assistant", subtitle_style))
    story.append(Paragraph(f"<i>{datetime.now().strftime('%B %d, %Y')}</i>", subtitle_style))
    story.append(PageBreak())

    # ===== PAGE 2+: CONTENT =====
    sections = proposal_text.strip().split("\n\n")

    for para in sections:
        para = para.strip()
        if not para:
            continue

        # === If starts with numbered section ===
        if any(para.lower().startswith(f"{n}.") for n in range(1, 21)):
            story.append(HRFlowable(width="100%", color=colors.HexColor("#90CAF9"), thickness=1, spaceBefore=10, spaceAfter=6))
            story.append(Paragraph(f"<u><b>{para}</b></u>", section_header))

        # === If it's a bulleted or indented list (lines with '- ' or numbered) ===
        elif para.startswith("- ") or para.startswith("* "):
            items = [item.strip("-* ").strip() for item in para.splitlines() if item.strip()]
            list_flow = ListFlowable(
                [ListItem(Paragraph(item, body_style)) for item in items],
                bulletType='bullet',
                leftIndent=20
            )
            story.append(list_flow)

        elif para.strip().startswith("•") or para.strip().startswith("1. "):
            lines = para.splitlines()
            items = [line.strip() for line in lines if line.strip()]
            list_flow = ListFlowable(
                [ListItem(Paragraph(item, body_style)) for item in items],
                bulletType='bullet',
                leftIndent=20
            )
            story.append(list_flow)

        # === Regular paragraph ===
        else:
            story.append(Paragraph(para.replace("\n", "<br/>"), body_style))

        story.append(Spacer(1, 0.15 * inch))

    doc.build(story)
    return filename
