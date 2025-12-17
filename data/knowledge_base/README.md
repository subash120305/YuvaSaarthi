# 📚 YuvaSaarthi Knowledge Base

This directory contains comprehensive educational reference materials for the YuvaSaarthi chatbot.

## 📁 Files Overview

### 1. **national_education_kb.json** (Structured Data)
- **Format:** JSON
- **Size:** 9.4 KB
- **Purpose:** Machine-readable structured knowledge base
- **Content:**
  - Education boards (CBSE, ICSE, IB, NIOS, State boards)
  - National & state scholarships (NMMSS, INSPIRE, etc.)
  - Reservation policies (Central & state-wise)
  - Competitive exams (JEE, NEET, CUET, CLAT, CAT, UPSC, etc.)
  - Government colleges (Engineering, Medical, Law)
  - National portals & statistics

### 2. **national_education_guide.md** (Main Reference Guide)
- **Format:** Markdown
- **Size:** 16.7 KB (530 lines)
- **Purpose:** Comprehensive human-readable education guide
- **Coverage:**
  - Classes 8-12 students
  - All degree programs
  - All states & education boards
  - Academic years 2025-26 & 2026-27
- **Key Sections:**
  - Education boards (Central & State)
  - National scholarship schemes
  - State-specific scholarships
  - Reservation policies (SC/ST/OBC/EWS/PwD)
  - Competitive exams with dates
  - Government colleges by state
  - Important national portals
  - Statistics & enrollment data
  - Chatbot usage notes

### 3. **exam_portals_directory.md** (Exam Links)
- **Format:** Markdown
- **Size:** 11.3 KB (301 lines)
- **Purpose:** Directory of 80+ competitive exam portals
- **Content:**
  - Engineering exams (JEE, GATE, State exams)
  - Medical exams (NEET, AIIMS, counselling)
  - Law exams (CLAT, NLUs)
  - MBA exams (CAT, XAT, SNAP, NMAT)
  - Civil services (UPSC, SSC, RRB)
  - Banking exams (IBPS, SBI, RBI)
  - Defense exams (NDA, AFCAT)
  - International tests (TOEFL, IELTS, GRE, GMAT)
  - Professional exams (CA, CS, CMA, KVPY)

### 4. **resource_links_directory.md** (Reference Links)
- **Format:** Markdown
- **Size:** 12.2 KB (373 lines)
- **Purpose:** Comprehensive directory of 150+ verified URLs
- **Categories:**
  - Official central board portals (CBSE, ICSE, IB, NIOS)
  - State education boards (All major states)
  - National scholarship portals
  - State scholarship portals
  - Competitive exam portals
  - Medical counselling portals
  - Government colleges & universities
  - Digital learning platforms (DIKSHA, SWAYAM, e-Pathshala)
  - Admissions & counselling portals
  - Contact & grievance portals

### 5. **competitive_exams_guide.md** (Exams Detail)
- **Format:** Markdown
- **Size:** 10.3 KB (359 lines)
- **Purpose:** Complete guide to 50+ competitive exams
- **Content:**
  - Exam dates for 2025-26 & 2026-27
  - Eligibility criteria
  - Registration details
  - Number of seats/posts
  - Official portals
  - Expected cutoffs (where applicable)
- **Exam Categories:**
  - Engineering (JEE, GATE, State exams)
  - Medical (NEET UG/PG/SS)
  - Law (CLAT, NLUs)
  - MBA (CAT, XAT, SNAP, NMAT, MAT, CMAT)
  - Civil services (UPSC CSE, SSC, RRB)
  - Banking (IBPS, SBI, RBI)
  - Defense (NDA, AFCAT)
  - International tests (TOEFL, IELTS, GRE, GMAT, SAT)
  - Professional exams (KVPY, INSPIRE, CA, CS, CMA)

---

## 🎯 Usage Guidelines

### For Chatbot Integration

1. **Primary Source:** Use `national_education_kb.json` for structured queries
2. **Detailed Responses:** Reference `.md` files for comprehensive answers
3. **Links:** Always provide official portal links from the directories
4. **Verification:** All links verified as of December 12, 2025
5. **Updates:** Next verification scheduled for March 2026

### For Document Ingestion

To make these files searchable by the chatbot, run:

```bash
python ingest_documents.py
```

This will process all knowledge base files and make them available for RAG-based queries.

---

## 📅 Metadata

- **Version:** 1.0
- **Created:** December 17, 2025
- **Last Updated:** December 17, 2025
- **Coverage:** Academic Years 2025-26 & 2026-27
- **Scope:** All Indian boards, all states, Classes 8-12 + all degree programs
- **Next Update:** March 2026
- **Purpose:** National Education Chatbot - Government Project

---

## 🔄 Update History

| Date | Version | Changes |
|------|---------|---------|
| 2025-12-17 | 1.0 | Initial knowledge base created with 5 comprehensive reference files |

---

## 📝 Notes

- All URLs are verified and active as of December 2025
- Exam dates are for academic years 2025-26 and 2026-27
- Scholarship amounts and eligibility criteria are subject to government updates
- Reservation policies may vary by state - always verify with official sources
- For the latest information, always direct users to official government portals

---

## 🔗 Related Directories

- **PDF Documents:** `/data/documents/` - Textbooks, administrative docs, admission info
- **Textbooks:** `/data/documents/textbooks/` - Class-wise educational PDFs
- **Scripts:** Root directory - `ingest_documents.py` for document processing

---

**Maintained by:** YuvaSaarthi Team  
**Contact:** Check project README for support information
