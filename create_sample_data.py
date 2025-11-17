"""
Generate Sample Educational Data for Demo
Creates sample documents for testing when real PDFs are not available
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import textwrap


def create_sample_pdfs():
    """Create sample PDF documents for demo"""

    # Create directories
    docs_dir = Path("data/documents")
    textbooks_dir = docs_dir / "textbooks"
    admin_dir = docs_dir / "administrative"
    general_dir = docs_dir / "general"

    for directory in [textbooks_dir, admin_dir, general_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    print("Creating sample PDFs for demo...")

    # Sample textbook content
    textbooks = {
        "class_10_mathematics.pdf": """
# Class 10 Mathematics - Key Concepts

## Chapter 1: Real Numbers

### Euclid's Division Lemma
For any two positive integers a and b, there exist unique integers q and r such that:
a = bq + r, where 0 ≤ r < b

This is the basis for finding HCF (Highest Common Factor) of two numbers.

### Fundamental Theorem of Arithmetic
Every composite number can be expressed as a product of primes, and this factorization is unique.

Example: 84 = 2 × 2 × 3 × 7 = 2² × 3 × 7

## Chapter 2: Polynomials

### Polynomial Definition
A polynomial p(x) in one variable x is an algebraic expression of the form:
p(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ

Where a₀, a₁, ..., aₙ are real numbers and n is a whole number.

### Zeros of a Polynomial
A zero of a polynomial p(x) is a number α such that p(α) = 0.

## Chapter 3: Linear Equations in Two Variables

Standard form: ax + by + c = 0
Where a, b, c are real numbers and both a and b are not zero.

Solution: Any pair (x, y) that satisfies the equation.

## Chapter 4: Quadratic Equations

Standard form: ax² + bx + c = 0, where a ≠ 0

### Quadratic Formula
x = [-b ± √(b² - 4ac)] / 2a

Discriminant: D = b² - 4ac
- If D > 0: Two distinct real roots
- If D = 0: Two equal real roots
- If D < 0: No real roots

## Chapter 5: Arithmetic Progressions (AP)

An arithmetic progression is a sequence where each term after the first is obtained by adding a constant difference.

General term: aₙ = a + (n-1)d
Where a = first term, d = common difference, n = term number

Sum of first n terms: Sₙ = n/2[2a + (n-1)d]

## Chapter 6: Triangles

### Pythagoras Theorem
In a right-angled triangle, the square of the hypotenuse equals the sum of squares of the other two sides.
c² = a² + b²

### Similar Triangles
Two triangles are similar if:
1. Their corresponding angles are equal
2. Their corresponding sides are proportional

Criteria for similarity:
- AAA (Angle-Angle-Angle)
- SSS (Side-Side-Side)
- SAS (Side-Angle-Side)

## Practice Problems

1. Find the HCF of 96 and 404 using Euclid's algorithm.
2. Find the zeros of polynomial: p(x) = x² - 5x + 6
3. Solve quadratic equation: 2x² - 7x + 3 = 0
4. Find the 10th term of AP: 2, 7, 12, 17, ...

## Important Formulas

- Area of triangle = 1/2 × base × height
- Heron's formula: √[s(s-a)(s-b)(s-c)], where s = (a+b+c)/2
- Distance formula: √[(x₂-x₁)² + (y₂-y₁)²]
- Section formula: ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n))

Remember: Practice regularly and understand the concepts rather than memorizing!
""",

        "class_10_science.pdf": """
# Class 10 Science - Important Topics

## Physics

### Light - Reflection and Refraction

#### Laws of Reflection
1. Angle of incidence = Angle of reflection
2. Incident ray, reflected ray, and normal lie in the same plane

#### Mirror Formula
1/f = 1/v + 1/u
Where f = focal length, v = image distance, u = object distance

#### Refraction
When light passes from one medium to another, it changes direction.

Snell's Law: n₁ sin i = n₂ sin r
Where n = refractive index, i = angle of incidence, r = angle of refraction

### Electricity

#### Ohm's Law
V = IR
Where V = potential difference, I = current, R = resistance

#### Electrical Power
P = VI = I²R = V²/R
Where P = power in watts

#### Series Circuit
- Same current flows through all components
- Total resistance: R = R₁ + R₂ + R₃

#### Parallel Circuit
- Same voltage across all components
- Total resistance: 1/R = 1/R₁ + 1/R₂ + 1/R₃

### Magnetic Effects of Electric Current

When electric current flows through a conductor, it produces a magnetic field around it.

#### Fleming's Left Hand Rule
Used to find direction of force on current-carrying conductor in magnetic field.

#### Electromagnetic Induction
When a conductor moves in a magnetic field, an EMF is induced.

## Chemistry

### Chemical Reactions

Types of Chemical Reactions:
1. Combination: A + B → AB
2. Decomposition: AB → A + B
3. Displacement: A + BC → AC + B
4. Double Displacement: AB + CD → AD + CB
5. Redox: Oxidation and Reduction occur simultaneously

### Acids, Bases and Salts

#### Acids
- Taste sour
- Turn blue litmus red
- pH < 7

#### Bases
- Taste bitter, feel soapy
- Turn red litmus blue
- pH > 7

pH scale: 0 to 14
pH = 7 is neutral

### Metals and Non-metals

Properties of Metals:
- Good conductors of heat and electricity
- Malleable and ductile
- High melting and boiling points
- Lustre (shine)

Properties of Non-metals:
- Poor conductors
- Brittle
- Low melting and boiling points
- No lustre (except iodine)

### Carbon Compounds

Carbon forms covalent bonds and shows catenation (self-linking).

Hydrocarbons:
- Alkanes: CₙH₂ₙ₊₂ (single bonds)
- Alkenes: CₙH₂ₙ (one double bond)
- Alkynes: CₙH₂ₙ₋₂ (one triple bond)

## Biology

### Life Processes

Seven life processes: Nutrition, Respiration, Transportation, Excretion, Control & Coordination, Growth, Reproduction

#### Respiration
Glucose + Oxygen → Carbon dioxide + Water + Energy
C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP

#### Photosynthesis
Carbon dioxide + Water → Glucose + Oxygen
(In presence of sunlight and chlorophyll)

### Human Body Systems

#### Digestive System
Mouth → Esophagus → Stomach → Small Intestine → Large Intestine

#### Respiratory System
Nose → Pharynx → Larynx → Trachea → Bronchi → Bronchioles → Alveoli

#### Circulatory System
Heart has 4 chambers: 2 Atria and 2 Ventricles
Blood flow: Heart → Arteries → Capillaries → Veins → Heart

### Heredity and Evolution

Mendel's Laws of Inheritance:
1. Law of Dominance
2. Law of Segregation
3. Law of Independent Assortment

DNA (Deoxyribonucleic Acid) carries genetic information.

Natural Selection: Organisms best adapted to environment survive and reproduce.

## Study Tips
- Make concept maps
- Practice numerical problems daily
- Conduct experiments to understand concepts
- Relate science to everyday life
- Review regularly
""",

        "class_12_physics.pdf": """
# Class 12 Physics - Advanced Concepts

## Electrostatics

### Coulomb's Law
Force between two point charges:
F = k(q₁q₂)/r²
Where k = 9 × 10⁹ Nm²/C²

### Electric Field
E = F/q = kQ/r²
Direction: Away from positive charge, towards negative charge

### Gauss's Law
Electric flux through a closed surface equals charge enclosed divided by ε₀:
Φ = Q/ε₀

### Capacitance
C = Q/V
For parallel plate capacitor: C = ε₀A/d

Energy stored: U = 1/2 CV²

## Current Electricity

### Kirchhoff's Laws

#### Kirchhoff's Current Law (KCL)
Sum of currents entering a junction = Sum of currents leaving the junction

#### Kirchhoff's Voltage Law (KVL)
In any closed loop, the sum of EMFs equals the sum of voltage drops

### Wheatstone Bridge
Balanced condition: P/Q = R/S

### Meter Bridge
Used to find unknown resistance using balanced Wheatstone bridge principle

## Magnetic Effects of Current and Magnetism

### Biot-Savart Law
dB = (μ₀/4π) × (I dl sin θ)/r²

### Ampere's Circuital Law
∮B·dl = μ₀I

### Magnetic Force
F = qvB sin θ (on moving charge)
F = BIL sin θ (on current-carrying conductor)

### Magnetic Dipole Moment
M = NIA
Where N = number of turns, I = current, A = area

## Electromagnetic Induction

### Faraday's Laws
1. Change in magnetic flux induces EMF
2. Induced EMF = -dΦ/dt

### Lenz's Law
Direction of induced current opposes the change causing it

### Self and Mutual Inductance
Self inductance: ε = -L(dI/dt)
Mutual inductance: ε₂ = -M(dI₁/dt)

## Alternating Current

### AC Voltage and Current
V = V₀ sin ωt
I = I₀ sin(ωt ± φ)

### RMS Values
Vᵣₘₛ = V₀/√2
Iᵣₘₛ = I₀/√2

### Impedance
Z = √(R² + (Xₗ - Xc)²)
Where Xₗ = ωL, Xc = 1/ωC

### Power Factor
cos φ = R/Z
Average power: P = Vᵣₘₛ Iᵣₘₛ cos φ

## Electromagnetic Waves

Speed of light: c = 1/√(μ₀ε₀) = 3 × 10⁸ m/s

Electromagnetic Spectrum (increasing wavelength):
Gamma rays → X-rays → UV → Visible → IR → Microwaves → Radio waves

## Ray Optics

### Lens Formula
1/f = 1/v - 1/u

### Lens Maker's Formula
1/f = (μ-1)(1/R₁ - 1/R₂)

### Power of Lens
P = 1/f (in diopters when f is in meters)

### Magnification
m = v/u = h'/h

## Wave Optics

### Young's Double Slit Experiment
Fringe width: β = λD/d
Where λ = wavelength, D = distance to screen, d = slit separation

### Interference Conditions
Constructive: Path difference = nλ
Destructive: Path difference = (n + 1/2)λ

## Modern Physics

### Photoelectric Effect
Einstein's equation: hν = φ + KEₘₐₓ
Where h = Planck's constant, ν = frequency, φ = work function

### de Broglie Wavelength
λ = h/p = h/mv

### Bohr's Atomic Model
Energy of electron: Eₙ = -13.6/n² eV
Radius of orbit: rₙ = n²r₀

### Radioactivity
N = N₀e^(-λt)
Half-life: t₁/₂ = 0.693/λ

## Important Constants
- Speed of light: c = 3 × 10⁸ m/s
- Planck's constant: h = 6.626 × 10⁻³⁴ Js
- Electron charge: e = 1.6 × 10⁻¹⁹ C
- Permittivity: ε₀ = 8.85 × 10⁻¹² C²/Nm²
- Permeability: μ₀ = 4π × 10⁻⁷ Tm/A

Practice numerical problems daily and understand the derivations!
"""
    }

    # Administrative documents
    admin_docs = {
        "admission_information.pdf": """
# Admission Information
## Department of Technical Education, Government of Rajasthan

### Academic Year 2024-25

## Available Programs

### Secondary Education (8-12th)
- Science Stream (PCM, PCB)
- Commerce Stream
- Arts Stream

### Polytechnic Diploma (3 Years)
- Civil Engineering
- Mechanical Engineering
- Electrical Engineering
- Electronics & Communication
- Computer Science & Engineering

### Engineering Degree (B.Tech - 4 Years)
- Computer Science & Engineering
- Electronics & Communication Engineering
- Mechanical Engineering
- Civil Engineering
- Electrical Engineering

## Eligibility Criteria

### For Class 8
- Completion of Class 7
- No specific percentage requirement
- Age: 12-14 years

### For Class 11 (Science)
- Class 10 passed with minimum 50% marks
- Mathematics and Science subjects mandatory

### For Polytechnic Diploma
- Class 10 passed with minimum 35% marks
- Mathematics and Science mandatory

### For B.Tech
- Class 12 passed with PCM (Physics, Chemistry, Mathematics)
- Minimum 45% marks (40% for reserved categories)
- Valid JEE Main score

## Application Process

1. **Online Registration**: Visit dte.rajasthan.gov.in
2. **Fill Application Form**: Provide personal and academic details
3. **Upload Documents**:
   - Photograph
   - Signature
   - 10th Marksheet
   - 12th Marksheet (for degree programs)
   - Caste Certificate (if applicable)
   - Income Certificate (for scholarship)
4. **Pay Application Fee**:
   - General: ₹500
   - OBC/EWS: ₹400
   - SC/ST: ₹300
5. **Submit Application**
6. **Download Application Receipt**

## Important Dates

- Application Start: June 1, 2024
- Application Deadline: July 15, 2024
- Merit List: July 25, 2024
- Counseling Starts: August 1, 2024
- Classes Commence: August 15, 2024

## Fee Structure

### Classes 8-10
- Tuition Fee: ₹500/year
- Examination Fee: ₹200/year
- Total: ₹700/year

### Classes 11-12
- Tuition Fee: ₹1,000/year
- Laboratory Fee: ₹500/year
- Examination Fee: ₹300/year
- Total: ₹1,800/year

### Polytechnic Diploma
- Tuition Fee: ₹15,000/year
- Laboratory Fee: ₹3,000/year
- Examination Fee: ₹1,000/year
- Total: ₹19,000/year

### B.Tech Programs
- Tuition Fee: ₹45,000/year
- Laboratory Fee: ₹5,000/year
- Examination Fee: ₹2,000/year
- Total: ₹52,000/year

## Scholarships Available

### Merit-Based Scholarships
- Top 10% students: 100% tuition fee waiver
- Top 25% students: 50% tuition fee waiver

### Need-Based Scholarships
- Family income < ₹1 lakh: 100% fee waiver
- Family income < ₹2.5 lakhs: 50% fee waiver

### Reserved Category Scholarships
- SC/ST students: As per government norms
- OBC students: As per government norms

### Girl Child Scholarship
- All female students: 25% fee concession

## Required Documents

1. Class 10th Marksheet and Certificate
2. Class 12th Marksheet and Certificate (for UG programs)
3. Transfer Certificate from previous institution
4. Character Certificate
5. Caste Certificate (if applicable)
6. Income Certificate (for scholarship)
7. Domicile Certificate (Rajasthan resident)
8. Aadhar Card
9. Passport size photographs (4 copies)

## Contact Information

**Admission Office**
Department of Technical Education
Government of Rajasthan
Jaipur, Rajasthan - 302001

**Phone**: +91-141-2227XXX
**Email**: admissions@dte.rajasthan.gov.in
**Website**: www.dte.rajasthan.gov.in

**Helpline Hours**: 10:00 AM to 5:00 PM (Monday to Friday)

## Frequently Asked Questions

**Q: Can I apply for multiple programs?**
A: Yes, you can apply for multiple programs by filling separate application forms.

**Q: Is hostel facility available?**
A: Yes, hostel facilities are available for outstation students.

**Q: Can I get admission without entrance exam?**
A: For classes 8-12 and polytechnic, admission is merit-based. For B.Tech, valid JEE Main score is mandatory.

**Q: What if I miss the application deadline?**
A: Late applications are accepted with a late fee of ₹200 within 7 days of deadline.

**Q: How do I check my application status?**
A: Login to the admission portal using your registration number.

For more information, visit our website or contact the admission office.
"""
    }

    # Create PDFs
    for filename, content in {**textbooks, **admin_docs}.items():
        if "class" in filename:
            file_path = textbooks_dir / filename
        else:
            file_path = admin_dir / filename

        create_pdf(file_path, content)
        print(f"[OK] Created: {filename}")

    # Create a README file
    readme_content = """# Sample Educational Data

This folder contains sample educational documents for demo purposes.

## How to Add Your Own Documents

1. **Textbooks**: Place your PDF files in `textbooks/` folder
   - Name format: `class_10_mathematics.pdf`, `class_11_physics.pdf`, etc.

2. **Administrative**: Place admission, fee, scholarship documents in `administrative/`

3. **General**: FAQs, guides in `general/` folder

## File Naming Convention

For best results, name your files following these patterns:

### Textbooks:
- `class_{grade}_{subject}.pdf`
- Examples: `class_10_science.pdf`, `class_12_chemistry.pdf`

### With chapters:
- `class_{grade}_{subject}_chapter_{number}.pdf`
- Example: `class_10_mathematics_chapter_5.pdf`

### Polytechnic/Engineering:
- `polytechnic_{branch}_semester_{number}.pdf`
- `btech_{branch}_semester_{number}.pdf`

## After Adding Documents

Run the document ingestion script:

```bash
python ingest_documents.py
```

This will process all PDFs and make them searchable by the chatbot.

## Supported Formats

- PDF files (.pdf)
- Text should be selectable (not scanned images)
- Hindi/English/Mixed language content supported

## Tips

- Use clear, descriptive filenames
- One subject per file works best
- Include class/grade in filename
- Keep file sizes reasonable (< 50MB per file)
"""

    with open(docs_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"\n[OK] Created README.md")
    print(f"\n[SUCCESS] Sample data created successfully!")
    print(f"\nNext steps:")
    print(f"1. Run: python ingest_documents.py")
    print(f"2. Add your own PDF files to data/documents/textbooks/")
    print(f"3. Run ingestion again to update the knowledge base")


def create_pdf(file_path: Path, content: str):
    """Create a PDF file from text content"""
    c = canvas.Canvas(str(file_path), pagesize=letter)
    width, height = letter

    # Set up margins
    left_margin = 1 * inch
    right_margin = 1 * inch
    top_margin = 1 * inch
    bottom_margin = 1 * inch
    line_height = 14

    # Starting position
    y = height - top_margin

    # Process content
    lines = content.split('\n')

    for line in lines:
        # Check if we need a new page
        if y < bottom_margin:
            c.showPage()
            y = height - top_margin

        # Handle headers (lines starting with #)
        if line.startswith('###'):
            c.setFont("Helvetica-Bold", 11)
            text = line.replace('###', '').strip()
        elif line.startswith('##'):
            c.setFont("Helvetica-Bold", 13)
            text = line.replace('##', '').strip()
            y -= 5  # Extra space before headers
        elif line.startswith('#'):
            c.setFont("Helvetica-Bold", 16)
            text = line.replace('#', '').strip()
            y -= 10  # Extra space before main headers
        else:
            c.setFont("Helvetica", 10)
            text = line.strip()

        # Wrap long lines
        max_width = width - left_margin - right_margin
        if text:
            wrapped_lines = textwrap.wrap(text, width=80)
            for wrapped_line in wrapped_lines:
                if y < bottom_margin:
                    c.showPage()
                    y = height - top_margin
                c.drawString(left_margin, y, wrapped_line)
                y -= line_height
        else:
            y -= line_height / 2  # Half space for empty lines

    c.save()


if __name__ == "__main__":
    create_sample_pdfs()
