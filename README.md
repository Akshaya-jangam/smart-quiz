# Smart Quiz Generator Microservice

A containerized, goal-aligned quiz generator microservice that generates multiple-choice and short-answer questions based on user goals.

## Features

- Accepts JSON input with goal, number of questions, and difficulty level
- Generates questions using:
  - Retrieval-based (TF-IDF) from question bank
  - Template-based generation
- Provides REST API endpoints
- Fully configurable via config.json
- Dockerized deployment

## API Endpoints

- `POST /generate` - Generate quiz questions
- `GET /health` - Health check
- `GET /version` - Service version information

## Quick Start

1. Build the Docker image:
```bash
docker build -t smart-quiz .