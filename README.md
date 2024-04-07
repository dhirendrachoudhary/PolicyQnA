# Policy QA Service

This is a service for performing question answering on policy documents using FastAPI, Elasticsearch, and OpenAI.

## File Structure

The project structure looks like this:
  
  ```
├── app
│   ├── main.py
│   ├── doc_search.py
├── pdfs
│   ├── document1.pdf
│   ├── document2.pdf
│   └── ...
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
└── README.md
|── streamlit_app.py
```

- `app/`: Contains the main Python code for the FastAPI application.
  - `main.py`: Entry point for the FastAPI application.
  - `doc_search.py`: Module for searching and retrieving information from policy documents.
- `pdfs/`: Directory containing policy documents in PDF format.
- `Dockerfile`: Dockerfile for building the FastAPI application container.
- `docker-compose.yml`: Docker Compose configuration file for running the FastAPI application and Elasticsearch.
- `requirements.txt`: List of Python dependencies required by the FastAPI application.

## Setup Instructions

Follow these steps to set up and run the service:

1. Clone this repository to your local machine:

```bash
git clone <repository-url>
cd policy-qa-service
```

2. Install Docker and Docker Compose if you haven't already.

3. Place your policy documents in the pdfs/ directory.

4. Build and run the Docker containers using Docker Compose:
```bash
docker-compose up --build
```

5. Once the containers are up and running, you can access the FastAPI service at http://localhost:8000.

6. To run the Streamlit app, open a new terminal window and navigate to the project directory. Then, run the following command:
```bash
streamlit run streamlit_app.py
```
The Streamlit app will be accessible in your web browser at http://localhost:8501
 - NOTE: The Streamlit app requires the FastAPI service to be running in order to function properly.



## Usage
### FastAPI Service
Use the /search endpoint to query the service for answers to questions related to policy documents.

Send a POST request to http://localhost:8000/search with a JSON payload containing the query:

```json
{
  "query": "What is the policy on remote work?"
}
```

The service will return a JSON response with the answer to the query:

```json
{
  "answer": "The policy on remote work allows employees to work from home up to 3 days a week."
}
```

### Streamlit App
The Streamlit app provides a user-friendly interface for interacting with the Policy QA Service. You can input your queries and view responses in a chat-like interface.

[![Policy QnA Demo Video]](demo/PolicyQnA.mp4)