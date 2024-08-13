import os
from rag import rag_query
from vllm import LLM


template = """<s>[INST]
You are a friendly documentation search bot.
Use following piece of context to answer the question.
If the context is empty, try your best to answer without it.
Never mention the context.
Try to keep your answers concise unless asked to provide details.

Context: {context}
Question: {question}
[/INST]</s>
Answer:
"""

def chat(args, embed_model, device, tokenizer):
    model = LLM(model=os.getenv("SERVE_MODEL"),
                max_model_len=512,
                enable_chunked_prefill=True)
    print("Chat started. Type 'exit' to end the chat.")

    while True:
        question = input("Ask a question: ")

        if question.lower() == "exit":
            break

        retrieved = rag_query(tokenizer=tokenizer, model=embed_model, device=device, query=question)

        query = template.format(context=retrieved, question=question)

        # Generate the response
        response = model.generate(query)
        answer = response[0].outputs[0].text

        print(f"You Asked: {question}")
        print(f"Answer: {answer}")

    print("Chat ended.")
