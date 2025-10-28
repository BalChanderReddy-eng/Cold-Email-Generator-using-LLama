# 🚀 Cold Email Generator using LLaMA 3.1

## 📘 Overview
The **Cold Email Generator** is an AI-powered application that automatically creates personalized cold emails for job applications. It analyzes the user’s **resume** and a **job posting URL**, determines how well the user’s skills and experiences match the job requirements, and generates a customized email only if certain conditions are met.

This project uses **LLaMA 3.1** as the core model for text generation and intelligent reasoning.

---

## 🧠 How It Works
1. **Input Stage**  
   - The system asks the user to upload their **resume** (PDF or text format).  
   - The user also provides a **job URL** (e.g., from LinkedIn, Indeed, etc.).  

2. **Data Extraction**  
   - The system **extracts key information** such as skills, education, and experience from the resume.  
   - It also **scrapes and processes** the job description from the provided URL.  

3. **Matching & Analysis**  
   - The model compares the **skills and experience** from the resume with the **job description**.  
   - If the user’s experience matches the role requirements or if the role requires **less than 2–3 years of experience**, the model proceeds to generate an email.  
   - If the user’s experience doesn’t align with the job description, the system **does not generate an email** and instead provides feedback.

4. **Email Generation**  
   - Using **LLaMA 3.1**, the system composes a **professional and personalized cold email** tailored to the specific job and company.  
   - The email highlights relevant skills and experiences to maximize the chance of getting noticed by recruiters.

---

## ⚙️ Features
- ✅ Resume and job description extraction  
- ✅ Skill and experience matching system  
- ✅ Automated email generation using **LLaMA 3.1**  
- ✅ Conditional generation logic based on experience (< 3 years)  
- ✅ Intelligent feedback when match score is low  

---

## 🧩 Tech Stack
- **Language:** Python  
- **Framework:** Streamlit (for UI)  
- **AI Model:** LLaMA 3.1 (via Groq API or local setup)  
- **Libraries Used:**  
  - `langchain`  
  - `groq`  
  - `beautifulsoup4` (for web scraping)  
  - `dotenv`  
  - `PyPDF2` / `pdfplumber` (for resume parsing)

---

## 🚀 Future Improvements
- Add **resume ranking** system for multiple candidates  
- Implement **recruiter email finder** for automated outreach  
- Include **multi-model evaluation** (compare outputs from LLaMA 3.1, GPT-4, etc.)  
- Provide detailed **feedback reports** on resume-job fit  

---

## 🧑‍💻 Author
**Balchander Reddy Yedla**  


## 🛠 Skills
Javascript, HTML, CSS...

