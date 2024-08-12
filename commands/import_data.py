import numpy as np
from tqdm import tqdm

from db import get_connection
from embedding import generate_embeddings, read_pdf_file


def import_data(args, model, device, tokenizer):
    data = read_pdf_file(args.data_source)

    print("Generating Embeddings")
    embeddings = []
    for line in tqdm(data):
        embeddings.append(generate_embeddings(tokenizer=tokenizer, model=model, device=device, text=line))
    print("Generated Embeddings")

    conn = get_connection()
    cursor = conn.cursor()

    # Store each embedding in the database
    for i, (doc_fragment, embedding) in enumerate(embeddings):
        cursor.execute(
            "INSERT INTO embeddings (id, doc_fragment, embeddings) VALUES (%s, %s, %s)",
            (i, doc_fragment, embedding[0]),
        )
    conn.commit()

    print(
        "import-data command executed. Data source: {}".format(
            args.data_source
        )
    )
