# importing all the required modules
from langchain_community.document_loaders import PyPDFLoader
import torch

def generate_embeddings(tokenizer, model, device, text):
    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=512
    ).to(device)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    return text, outputs.hidden_states[-1].mean(dim=1).tolist()


def read_pdf_file(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    return pages
