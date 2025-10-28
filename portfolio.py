import pandas as pd
import chromadb
import uuid
import os


class Portfolio:
    def __init__(self, file_path=None):
        # Use the provided file path or default to the absolute path of my_portfolio.csv
        if file_path is None:
            file_path = r"C:\Users\balch\Downloads\Cold_Email_Generator\Cold_Email_Generator\project-genai-cold-email-generator\app\resource\my_portfolio.csv"

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Portfolio file not found at: {file_path}")

        # Load the CSV file
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
