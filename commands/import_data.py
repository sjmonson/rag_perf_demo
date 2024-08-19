from itertools import chain
from db import VectorDB
from embedding import read_pdf_file

def import_data(args, model, device, tokenizer):
    documents = list(chain(*[ read_pdf_file(doc) for doc in args.data_source ]))

    db = VectorDB()
    conn = db.populate_db(documents)
