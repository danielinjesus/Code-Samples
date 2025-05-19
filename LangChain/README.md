# LangChain and RAG Learning Example

This is a simple example to help you get started with LangChain and RAG (Retrieval Augmented Generation).

## Setup

1. Install the requirements:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Example

Run the example with:
```bash
python simple_rag.py
```

## What This Example Shows

This example demonstrates:
1. Loading documents
2. Splitting text into chunks
3. Creating embeddings
4. Storing embeddings in a vector database
5. Creating a RAG chain
6. Asking questions about the content

## Key Concepts

### LangChain
- A framework for building LLM-powered applications
- Provides tools for working with language models
- Makes it easy to create chains of operations

### RAG (Retrieval Augmented Generation)
- Combines document retrieval with LLM generation
- Helps LLMs provide more accurate and contextual responses
- Uses vector databases to store and retrieve relevant information

## Next Steps

1. Try modifying the sample text in `sample.txt`
2. Experiment with different questions
3. Try different chunk sizes and overlap values
4. Explore other LangChain components and chains 