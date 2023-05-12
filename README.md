AskAWS Knowledge Extractor
AskAWS is a Python Flask application that leverages the OpenAI API, Sentence Transformers, and other Python libraries to extract knowledge from a PDF document and generate answers to user queries based on the extracted information.

Features
The application:

Extracts and stores text from a specified PDF document.
Generates and stores sentence embeddings for future use.
Takes a user query and identifies the most relevant sentences from the stored text.
Uses the OpenAI API to generate comprehensive responses to user queries.
Getting Started
Ensure you have Python 3.7 or higher installed before proceeding.

Clone the repository: Run git clone https://github.com/kurthamm/AskAWS.git to clone the repository to your local machine.

Navigate into the directory: Run cd AskAWS to move into the repository's root directory.

Install dependencies: Run pip install -r requirements.txt to install the necessary libraries.

Usage
Set up OpenAI API key: Open the main.py file and replace the placeholder with your OpenAI API key.

Start the application: Run python main.py to start the application.

Interact with the application: Open a web browser and go to localhost:5000 to interact with the application.

How it Works
If pre-generated sentence embeddings exist, the application loads them. Otherwise, it generates new embeddings by extracting text from a specified PDF file, splitting the text into sentences, and encoding these sentences using the SentenceTransformer model.

When a query is submitted via the web interface, the application uses the sentence embeddings to identify sentences most relevant to the question.

The application then uses these sentences, along with the question, to form a prompt that is submitted to the OpenAI API. The API's response is treated as the answer to the query.

Finally, the answer is displayed on the web page.

Contributing
We welcome contributions! Feel free to submit a Pull Request.

License
AskAWS is licensed under the MIT License.

Disclaimer
This code is intended for educational purposes only. We accept no responsibility for misuse.

For more information, visit the repository.
