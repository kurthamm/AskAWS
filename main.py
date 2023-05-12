import os
import pdfplumber
import numpy as np
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import openai
import requests
from flask import Flask, render_template, request

openai.api_key = "ADD_OPENAI_KEY"

SENTENCE_EMBEDDINGS_FILE = "sentence_embeddings.npy"

def extract_text_from_pdf(file_path):
    print("Extracting text from PDF...")
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        text = ""
        for page in pages:
            text += page.extract_text()
    return text

def generate_sentence_embeddings(sentences):
    print("Generating sentence embeddings...")
    model = SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(sentences)
    return embeddings

def load_sentence_embeddings():
    if os.path.exists(SENTENCE_EMBEDDINGS_FILE):
        print("Loading sentence embeddings from file...")
        embeddings = np.load(SENTENCE_EMBEDDINGS_FILE)
        with open("sentences.txt", "r", encoding="utf-8") as f:
            sentences = [line.strip() for line in f]
    else:
        file_path = "c:\stuff\AWSALL.pdf"
        text = extract_text_from_pdf(file_path)
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 0]
        embeddings = generate_sentence_embeddings(sentences)
        np.save(SENTENCE_EMBEDDINGS_FILE, embeddings)
        with open("sentences.txt", "w", encoding="utf-8") as f:
            for sentence in sentences:
                f.write(sentence + "\n")
    return embeddings, sentences


def find_top_sentences(query, sentences, embeddings, top_k=8):
    print("Finding top sentences related to the query...")
    query_embedding = generate_sentence_embeddings([query])[0]
    distances = np.inner(query_embedding, embeddings)
    top_indices = distances.argsort()[-top_k:][::-1]
    return [sentences[i] for i in top_indices]

def submit_to_openai_api(prompt):
    ip_address = request.remote_addr
    print(f"Submitting prompt to OpenAI API from {ip_address}...")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

def generate_openai_prompt(question, sentences):
    prompt = f"Answer the following question in a comprehensive and detailed manner based on the provided context:<br><br>Question: {question}<br><br>Context:<br>"
    for i, sentence in enumerate(sentences):
        prompt += f"{i+1}. {sentence}<br>"
    return prompt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        embeddings, sentences = load_sentence_embeddings()

        question = request.form['question'].strip()

        top_sentences = find_top_sentences(question, sentences, embeddings)

        openai_prompt = generate_openai_prompt(question, top_sentences)
        answer = submit_to_openai_api(openai_prompt)

        return render_template('index.html', answer=answer)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

