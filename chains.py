import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

class Chain:
    def __init__(self):
        self.llm = None  # Initialize lazily

    def _init_llm(self):
        if self.llm is None:
            groq_api_key = os.environ.get("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("GROQ_API_KEY missing in Streamlit secrets!")
            self.llm = ChatGroq(
                temperature=0,
                groq_api_key=groq_api_key,
                model_name="llama-3.3-70b-versatile"
            )

    def extract_jobs(self, cleaned_text):
        self._init_llm()
        prompt = PromptTemplate.from_template("""
        ### SCRAPED TEXT:
        {page_data}
        ### INSTRUCTION:
        Extract jobs as JSON: role, experience, skills, description.
        Only return JSON.
        """)
        chain_extract = prompt | self.llm
        res = chain_extract.invoke({"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except (OutputParserException, ValueError) as e:
            raise OutputParserException(f"Error parsing JSON: {e}")
        return res if isinstance(res, list) else [res]

    def extract_skills(self, text):
        self._init_llm()
        prompt = PromptTemplate.from_template("""
        ### TEXT:
        {text}
        ### INSTRUCTION:
        Extract relevant skills as comma-separated keywords.
        """)
        chain_extract = prompt | self.llm
        res = chain_extract.invoke({"text": text})
        return res.content.split(",")

    def calculate_match_score(self, resume_skills, job_skills):
        resume_skills = set([s.strip().lower() for s in resume_skills])
        job_skills = set([s.strip().lower() for s in job_skills])
        matched = resume_skills.intersection(job_skills)
        return (len(matched) / len(job_skills)) * 100 if job_skills else 0

    def write_mail(self, job, links):
        self._init_llm()
        prompt = PromptTemplate.from_template("""
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        Write a professional cold email highlighting relevant skills & experience.
        ### EMAIL:
        """)
        chain_email = prompt | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content
