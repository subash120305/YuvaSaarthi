from fpdf import FPDF
import re

class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Title
        self.cell(0, 10, 'YuvaSaarthi 2.0 - Presentation Cheatsheet', 0, 1, 'C')
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

def create_pdf(input_file, output_file):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
            
        # Handle Headers
        if line.startswith('## '):
            pdf.set_font('Arial', 'B', 14)
            # Remove Markdown syntax
            text = line.replace('## ', '')
            pdf.cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
            pdf.set_font('Arial', '', 12)
        elif line.startswith('### '):
            pdf.set_font('Arial', 'B', 13)
            text = line.replace('### ', '')
            pdf.cell(0, 10, text.encode('latin-1', 'replace').decode('latin-1'), 0, 1)
            pdf.set_font('Arial', '', 12)
        elif line.startswith('**') and line.endswith('**'): # Bold Line
            pdf.set_font('Arial', 'B', 12)
            text = line.replace('**', '')
            pdf.multi_cell(0, 8, text.encode('latin-1', 'replace').decode('latin-1'))
            pdf.set_font('Arial', '', 12)
        elif line.startswith('- ') or line.startswith('* '): # Bullet
            text = '  ' + chr(149) + ' ' + line[2:]
            pdf.multi_cell(0, 8, text.encode('latin-1', 'replace').decode('latin-1'))
        else:
            # Body text
            # Handle bold inside text roughly
            text = line.replace('**', '') 
            pdf.multi_cell(0, 8, text.encode('latin-1', 'replace').decode('latin-1'))
            
    pdf.output(output_file, 'F')
    print(f"PDF created: {output_file}")

if __name__ == "__main__":
    create_pdf('PRESENTATION_CHEATSHEET.md', 'YuvaSaarthi_Presentation.pdf')
