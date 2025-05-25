from fpdf import FPDF

def create_pdf(result, output_path="trace_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Social Media Trace Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Input Type: {result['type']}", ln=True)
    pdf.cell(200, 10, txt=f"Input Value: {result['input']}", ln=True)
    pdf.cell(200, 10, txt=f"Valid: {'Yes' if result['valid'] else 'No'}", ln=True)
    pdf.ln(5)

    if result.get("platform_matches"):
        pdf.cell(200, 10, txt="Matched Platforms:", ln=True)
        for match in result["platform_matches"]:
            platform = match['platform'].title()
            confidence = match['confidence']
            url = match['profile_url']
            text = f"- {platform} | Confidence: {confidence}% | URL: {url}"
            pdf.multi_cell(0, 10, txt=text)
    else:
        pdf.cell(200, 10, txt="No matches found.", ln=True)

    pdf.output(output_path)
    return output_path
