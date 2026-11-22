# LLM Tool Calling Calculator

A Generative AI calculator application built using Python, LangChain, Ollama and Streamlit.

The application uses an LLM to select and execute calculator tools based on the user's mathematical question.

## Features

- Addition
- Subtraction
- Multiplication
- Division
- Division-by-zero handling
- LangChain tool calling using the @tool decorator
- Ollama Llama 3.2 integration
- Streamlit chat interface

## Technologies

- Python
- LangChain
- LangChain Ollama
- Ollama
- Llama 3.2
- Streamlit

## Setup

1. Clone the repository.

2. Create a virtual environment:

   python -m venv venv

3. Activate the environment (Windows):

   .\venv\Scripts\Activate.ps1

4. Install dependencies:

   pip install -r requirements.txt

5. Install and start Ollama.

6. Download the model:

   ollama pull llama3.2

## Run the Application

Start the Streamlit application:

streamlit run ui/streamlit_app.py

For the console version:

python main.py

## Project Structure

LLM_ToolCalculator/
|
|-- calculator_tools.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- ui/
|   |-- streamlit_app.py
|-- .gitignore

## How It Works

1. The user submits a mathematical question.
2. The LLM identifies the required calculator tool.
3. LangChain executes the selected Python function.
4. The tool result is returned to the LLM.
5. The LLM generates the final response.

## Model

Llama 3.2 running locally through Ollama.
