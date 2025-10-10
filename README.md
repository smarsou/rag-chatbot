# RAG Chatbot - API used on my Portfolio

This repository is the code of my chatbot API built using Flask and OpenAI's API, designed to enhance my portfolio website and to showcase my skills in web development and AI integration.

## Flask

Flask REST API developed following the official documentation for a production-ready application. The project demonstrates:

- Modular architecture using Blueprints.
- Integration with OpenAI's API for processing user requests securely and efficiently.
- Implementation of request limits and input validation to ensure stability and security.

## RAG

The data is retrieved at each request using a RAG system.

For this RAG, we use langchain alongside PostgreSQL as a Vector Database. 

The data is ingested using the script `rag/ingest.py` which get the data from the file `rag/rag_docs.txt`. 

The retrieval can be tested using the script `rag/test_rag.py`.

## Deployment

This API is deployed on an Ubuntu server, alongside:

- My portfolio Spring Boot web application.
- My portfolio CRUD api which handles my projects' data.
- some other projects...
  
Deployment is managed using Docker, ensuring consistency and ease of replication. This approach showcases my proficiency in:

- Containerization and DevOps workflows.
- Managing and hosting multiple services on a single server.

For more details, see the repository *smarsou/spring-web-portfolio* 

## Skills Highlighted

- **Web Development**: Building REST APIs with Flask.
- **AI Integration**: Implemented RAG system for generative tasks.
- **DevOps**: Deployed the API and other services using Docker.
- **Security**: Enforced request limits and input validation.


