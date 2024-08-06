import google.generativeai as genai
from langchain_community.document_loaders import TextLoader

# Configure Google Generative AI
genai.configure(api_key='AIzaSyC9sCDwIjo3tRjoqGDY_clTPq8ypRUltyc')

# Function to query Google Generative AI
def query_google_generative_ai(prompt):
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    
    # Use 'generate_content' with 'contents' parameter
    response = model.generate_content(contents=prompt)
    return response.text if hasattr(response, 'text') else "Sorry, I couldn't generate a response."

# Load documents
def load_documents():
    doc_paths = [
        r'C:\Users\Dell\chatbot_project\doc1.txt',
        r'C:\Users\Dell\chatbot_project\doc2.txt',
        r'C:\Users\Dell\chatbot_project\doc3.txt'
    ]

    documents = []
    for path in doc_paths:
        loader = TextLoader(path)
        docs = loader.load()
        documents.extend(docs)
        for doc in docs:
            print(doc.page_content)  # Print document content for verification
    return documents

# Query documents
def query_documents(query):
    documents = load_documents()
    relevant_docs = [doc for doc in documents if query.lower() in doc.page_content.lower()]
    
    if not relevant_docs:
        combined_prompt = query  # If no relevant documents, use the query alone
    else:
        doc_texts = [doc.page_content for doc in relevant_docs]
        combined_prompt = f"The user asked: {query}\n\nHere are some relevant documents:\n\n" + "\n\n".join(doc_texts)

    # Query Google Generative AI with the combined prompt
    response = query_google_generative_ai(combined_prompt)
    return response

