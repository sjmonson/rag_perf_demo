# importing all the required modules
from langchain_community.document_loaders import PyPDFLoader

def read_pdf_file(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    return pages
