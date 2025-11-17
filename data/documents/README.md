# Sample Educational Data

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
