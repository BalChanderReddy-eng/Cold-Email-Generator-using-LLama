import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )
        # self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        """Extract job details from the job description text."""
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills`, and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke({"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except (OutputParserException, ValueError) as e:
            raise OutputParserException(f"Error parsing JSON: {e}")
        return res if isinstance(res, list) else [res]

    def extract_skills(self, text):
        """Extract relevant skills from the resume or job description text."""
        prompt_extract_skills = PromptTemplate.from_template(
            """
            ### TEXT:
            {text}
            ### INSTRUCTION:
            Extract the most relevant technical skills and programming languages mentioned in the text.
            Return the skills as a comma-separated list of keywords.
            """
        )
        chain_extract_skills = prompt_extract_skills | self.llm
        res = chain_extract_skills.invoke({"text": text})
        return res.content.split(",")  # Extracting the list of skills

    def calculate_match_score(self, resume_skills, job_skills):
        """Compare resume skills with job required skills and calculate a match score."""
        # Normalize the skills (lowercase) to ensure case-insensitive comparison
        resume_skills = set([skill.strip().lower() for skill in resume_skills])
        job_skills = set([skill.strip().lower() for skill in job_skills])

        # Find intersection of skills
        matched_skills = resume_skills.intersection(job_skills)

        # Calculate match score as the percentage of matched skills over job skills
        match_score = (len(matched_skills) / len(job_skills)) * 100 if job_skills else 0
        return match_score

    def write_mail(self, job, links):
        """Generate a cold email from the applicant's perspective."""
        prompt_email = PromptTemplate.from_template(
            """
        ### JOB DESCRIPTION:
        {job_description}

        ### INSTRUCTION:
        You are a job applicant looking to apply for the above job. Your goal is to write a **professional cold email** 
        expressing interest in the role. The email should be concise, personalized, and highlight relevant skills/experience 
        matching the job description. 

        **Structure the email as follows:**
        1. **Subject**: A compelling subject line.
        2. **Introduction**: A short greeting and statement of interest.
        3. **Skills & Experience**: Briefly mention relevant skills and experiences that match the job.
        4. **Closing & Call to Action**: Express enthusiasm and request the next steps.

        **Tone:** Professional, polite, and confident.
        
        **Do not include unnecessary information.**
        **Do not provide a preamble.**
        
        ### EMAIL (NO PREAMBLE):
        """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))