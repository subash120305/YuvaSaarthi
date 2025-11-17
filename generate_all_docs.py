"""
Generate comprehensive sample documents for all categories
"""
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import textwrap

def create_pdf(file_path, content):
    """Create PDF from text content"""
    c = canvas.Canvas(str(file_path), pagesize=letter)
    width, height = letter
    y = height - 1*72

    for line in content.split('\n'):
        if y < 72:
            c.showPage()
            y = height - 1*72

        if line.startswith('###'):
            c.setFont('Helvetica-Bold', 11)
            text = line.replace('###', '').strip()
        elif line.startswith('##'):
            c.setFont('Helvetica-Bold', 13)
            text = line.replace('##', '').strip()
            y -= 5
        elif line.startswith('#'):
            c.setFont('Helvetica-Bold', 16)
            text = line.replace('#', '').strip()
            y -= 10
        else:
            c.setFont('Helvetica', 10)
            text = line.strip()

        if text:
            wrapped = textwrap.wrap(text, width=80)
            for wline in wrapped:
                if y < 72:
                    c.showPage()
                    y = height - 1*72
                c.drawString(72, y, wline)
                y -= 14
        else:
            y -= 7

    c.save()


# Content for each category
categories = {
    'administrative': """
# Rajasthan Technical Education - Administrative Information

## Fee Structure 2024-25

### Polytechnic Diploma Courses
- Tuition Fee: Rs. 15,000 per year
- Development Fee: Rs. 3,000 per year
- Examination Fee: Rs. 1,500 per year
- Total: Rs. 19,500 per year

### B.Tech Programs
- Tuition Fee: Rs. 55,000 per year
- Development Fee: Rs. 8,000 per year
- Laboratory Fee: Rs. 6,000 per year
- Total: Rs. 69,000 per year

### Fee Concessions
- SC/ST Students: 50% tuition waiver
- Girl Students: 25% concession
- Below Poverty Line: 100% waiver

## Contact Information
Department of Technical Education
Jhalana Doongri, Jaipur - 302004
Phone: 0141-2711000
Email: dte.rajasthan@gov.in
""",

    'admissions': """
# Admission Guidelines 2024-25

## Important Dates
- Application Start: June 1, 2024
- Application End: July 15, 2024
- Merit List: August 5, 2024
- Counseling: August 10-25, 2024

## Eligibility - Polytechnic
- 10th pass with 35% marks
- Mathematics and Science mandatory
- Minimum age: 15 years
- Rajasthan domicile required

## Eligibility - B.Tech
- 12th with PCM, 45% marks
- Valid JEE Main score
- No age limit

## Required Documents
1. 10th Marksheet
2. 12th Marksheet (BTech)
3. Caste Certificate
4. Income Certificate
5. Domicile Certificate
6. Aadhar Card
7. Passport photos

## Application Fees
- General: Rs. 500
- OBC: Rs. 400
- SC/ST: Rs. 300
""",

    'engineering': """
# Engineering Programs

## Computer Science Engineering
Duration: 4 Years (8 Semesters)

Key Subjects:
- Programming (C, C++, Java, Python)
- Data Structures & Algorithms
- Database Management Systems
- Operating Systems
- Computer Networks
- Software Engineering
- Artificial Intelligence
- Machine Learning

Career Options:
- Software Developer (Rs. 3.5-15 LPA)
- Data Scientist (Rs. 6-20 LPA)
- System Administrator
- Network Engineer

## Mechanical Engineering
- Thermodynamics
- Fluid Mechanics
- Machine Design
- Manufacturing Technology

## Electrical Engineering
- Power Systems
- Control Systems
- Electrical Machines
- Power Electronics

## Civil Engineering
- Structural Engineering
- Transportation Engineering
- Environmental Engineering
""",

    'general': """
# General Information

## FAQs

Q: Can I apply for multiple courses?
A: Yes, up to 3 courses in order of preference.

Q: Is hostel available?
A: Yes, separate hostels for boys and girls.

Q: What about scholarships?
A: Multiple scholarships available:
- Post-matric for SC/ST
- Merit scholarship
- Girl child scholarship

Q: Placement support?
A: Yes, dedicated placement cell in every college.

## Helpline Numbers
- Admission: 0141-2711001
- Technical: 0141-2711002
- Scholarship: 0141-2711003

Hours: 10 AM - 5 PM (Mon-Fri)
""",

    'polytechnic': """
# Polytechnic Diploma Programs

## Civil Engineering (3 Years)
What You Learn:
- Building Construction
- Surveying
- Structural Design
- Estimation and Costing

Jobs:
- Junior Engineer (Rs. 15,000-25,000/month)
- Site Supervisor
- Surveyor

## Mechanical Engineering
Subjects:
- Workshop Technology
- Thermal Engineering
- Manufacturing Processes
- Machine Design

Skills:
- CNC Programming
- Welding
- Quality Control

## Electrical Engineering
- Electrical Circuits
- Electrical Machines
- Power Systems
- Renewable Energy

## Computer Science
Programming Languages:
- C, C++, Java, Python
- Web Development
- Database Management
- Mobile Apps

Salary: Rs. 18,000-35,000/month

## Why Choose Polytechnic?
- Start career after 10th
- 60% practical training
- Lower cost than BTech
- 3 years duration
- Can join BTech 2nd year later
"""
}

# Generate all PDFs
print("Generating comprehensive sample documents...")
print("=" * 60)

for category, content in categories.items():
    dir_path = Path(f'data/documents/{category}')
    dir_path.mkdir(parents=True, exist_ok=True)
    pdf_file = dir_path / f'{category}_info.pdf'
    create_pdf(pdf_file, content)
    print(f"[OK] Created: data/documents/{category}/{category}_info.pdf")

print("=" * 60)
print("[SUCCESS] All category PDFs generated successfully!")
print("\nGenerated files for:")
print("  - administrative/ (fees, contact info)")
print("  - admissions/ (eligibility, dates, process)")
print("  - engineering/ (BTech programs, subjects)")
print("  - general/ (FAQs, helpline)")
print("  - polytechnic/ (diploma programs, jobs)")
