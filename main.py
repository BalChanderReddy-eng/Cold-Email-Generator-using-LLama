import streamlit as st
import traceback

try:
    from langchain_community.document_loaders import WebBaseLoader
    from chains import Chain
    from utils import clean_text, extract_text_from_pdf

    st.write("✅ Imports OK!")

except Exception as e:
    st.error("❌ Error loading app:")
    st.exception(e)  # <-- shows full traceback
    st.stop()
    
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/141.0.0.0 Safari/537.36"
)
# -------------------------------------------------------

# -------------------- Optional USER_AGENT --------------------
import os
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
# ------------------------------------------------------------

# Your original Streamlit code starts here
def create_streamlit_app(chain):
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input("Enter a Job URL:", value="")
    uploaded_file = st.file_uploader("Upload your Resume (PDF):", type="pdf")

    if st.button("Analyze & Generate Email"):
        if not url_input:
            st.error("⚠️ Please enter a job URL.")
            return

        if not uploaded_file:
            st.error("⚠️ Please upload a resume.")
            return

        try:
            loader = WebBaseLoader([url_input])
            job_text = clean_text(loader.load().pop().page_content)

            jobs = chain.extract_jobs(job_text)
            if not jobs:
                st.error("⚠️ No job postings found in the given URL.")
                return

            job = jobs[0]

            st.subheader("📝 Extracted Job Details")
            st.write(f"**Role:** {job.get('role', 'N/A')}")
            st.write(f"**Experience:** {job.get('experience', 'N/A')}")
            st.write(f"**Skills Required:** {', '.join(job.get('skills', []))}")
            st.write(f"**Job Description:** {job.get('description', 'N/A')}")

            resume_text = extract_text_from_pdf(uploaded_file)
            resume_skills = chain.extract_skills(resume_text)

            job_skills = job.get("skills", [])
            match_score = chain.calculate_match_score(resume_skills, job_skills)

            st.subheader("📊 Resume Match Score")
            st.write(f"**{match_score:.1f}%**")

            if match_score < 40:
                st.error("❌ Not fit for the job. Consider updating your resume.")
            elif 50 <= match_score < 60:
                st.warning("⚠️ Resume needs improvements. Modify your skills.")
            else:
                st.success("✅ Good fit! Generating cold email...")
                email = chain.write_mail(job, links=[])
                st.subheader("📧 Generated Cold Email")
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain)


# import streamlit as st
# import os
# import traceback

# # -------------------- SET USER_AGENT --------------------
# os.environ["USER_AGENT"] = (
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#     "AppleWebKit/537.36 (KHTML, like Gecko) "
#     "Chrome/141.0.0.0 Safari/537.36"
# )
# # ---------------------------------------------------------

# # -------------------- SAFE IMPORTS ----------------------
# try:
#     from langchain_community.document_loaders import WebBaseLoader
#     from chains import Chain
#     from utils import clean_text, extract_text_from_pdf
#     st.write("✅ Imports OK!")
# except Exception as e:
#     st.error("❌ Error loading app:")
#     st.exception(e)
#     st.stop()  # Stop execution if imports fail
# # ---------------------------------------------------------

# # -------------------- STREAMLIT APP --------------------
# def create_streamlit_app():
#     st.title("📧 Cold Email Generator")

#     # Lazy initialize Chain
#     chain = None

#     # Job URL input
#     url_input = st.text_input("Enter a Job URL:", value="")
#     # Resume upload
#     uploaded_file = st.file_uploader("Upload your Resume (PDF):", type="pdf")

#     # Submit button
#     if st.button("Analyze & Generate Email"):
#         if not url_input:
#             st.error("⚠️ Please enter a job URL.")
#             return
#         if not uploaded_file:
#             st.error("⚠️ Please upload a resume.")
#             return

#         # Initialize Chain only here
#         if chain is None:
#             try:
#                 chain = Chain()
#             except Exception as e:
#                 st.error("❌ Error initializing LLaMA/Groq model:")
#                 st.exception(e)
#                 return

#         # ----------------- PROCESS JOB -----------------
#         try:
#             loader = WebBaseLoader([url_input])
#             pages = loader.load()
#             if not pages:
#                 st.error("⚠️ No content found at the given URL.")
#                 return

#             job_text = clean_text(pages[0].page_content)
#             if not job_text.strip():
#                 st.error("⚠️ Job page returned empty content.")
#                 return

#             # Extract job details from LLM
#             try:
#                 jobs = chain.extract_jobs(job_text)
#             except Exception as e:
#                 st.error("❌ Error extracting job details via LLaMA/Groq:")
#                 st.exception(e)
#                 return

#             if not jobs:
#                 st.error("⚠️ No job postings found in the given URL.")
#                 return

#             job = jobs[0]  # Use first job posting

#             # Display extracted job info
#             st.subheader("📝 Extracted Job Details")
#             st.write(f"**Role:** {job.get('role', 'N/A')}")
#             st.write(f"**Experience:** {job.get('experience', 'N/A')}")
#             st.write(f"**Skills Required:** {', '.join(job.get('skills', []))}")
#             st.write(f"**Job Description:** {job.get('description', 'N/A')}")

#             # Extract resume text
#             resume_text = extract_text_from_pdf(uploaded_file)
#             resume_skills = chain.extract_skills(resume_text)

#             # Match score
#             job_skills = job.get("skills", [])
#             match_score = chain.calculate_match_score(resume_skills, job_skills)

#             st.subheader("📊 Resume Match Score")
#             st.write(f"**{match_score:.1f}%**")

#             # Decide email generation
#             if match_score < 40:
#                 st.error("❌ Not fit for the job. Consider updating your resume.")
#             elif 50 <= match_score < 60:
#                 st.warning("⚠️ Resume needs improvements. Modify your skills.")
#             else:
#                 st.success("✅ Good fit! Generating cold email...")
#                 try:
#                     email = chain.write_mail(job, links=[])
#                     st.subheader("📧 Generated Cold Email")
#                     st.code(email, language="markdown")
#                 except Exception as e:
#                     st.error("❌ Error generating cold email via LLaMA/Groq:")
#                     st.exception(e)

#         except Exception as e:
#             st.error("❌ An unexpected error occurred:")
#             st.exception(e)

# # ---------------------------------------------------------

# if __name__ == "__main__":
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     create_streamlit_app()




