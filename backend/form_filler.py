import json
import os
from fpdf import FPDF
from loguru import logger

class FormPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'YuvaSaarthi - Automated Application Form', 0, 1, 'C')
        self.ln(10)

class FormFiller:
    def __init__(self):
        self.forms = {}
        forms_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'forms')
        if os.path.exists(forms_dir):
            for file in os.listdir(forms_dir):
                if file.endswith('.json'):
                    with open(os.path.join(forms_dir, file), 'r') as f:
                        data = json.load(f)
                        self.forms[data['id']] = data
                        
    def generate_pdf(self, form_id: str, fields: dict, output_path: str):
        if form_id not in self.forms:
            logger.error(f"Form {form_id} not found.")
            return False
            
        form_data = self.forms[form_id]
        
        pdf = FormPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=form_data['title'], ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        
        for q in form_data['questions']:
            label = q['label']
            key = q['key']
            answer = fields.get(key, '__________')
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, txt=f"{label}:", ln=True)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, txt=answer, ln=True)
            pdf.ln(5)
            
        pdf.ln(20)
        pdf.cell(0, 10, txt="Signature: ______________________", ln=True, align='R')
        
        try:
            pdf.output(output_path)
            return True
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            return False

form_filler = FormFiller()
