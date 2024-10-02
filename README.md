# FastAPI Recipe Generation Project

This project is a FastAPI application that uses OpenAI's Large Language Model (LLM) to generate recipes and calculate
nutritional values based on user input. The project integrates OpenAI's API and provides both synchronous and
asynchronous methods to interact with the LLM.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [License](#license)

## Features

- **FastAPI**: A modern web framework for building APIs with Python.
- **OpenAI Integration**: Generates recipes and nutritional values using OpenAI's GPT models.
- **Synchronous & Asynchronous Support**: Provides both sync and async methods to interact with OpenAI API.
- **Environment-Based Configuration**: Loads API keys and configurations from environment variables.

## Requirements

To run this project, you will need:

- **Docker, docker compose**
- **OpenAI API Key** (required for interacting with OpenAI's API)

## Building the docker image

1. Make sure you in the the recipie_fastapi directory
    ```bash
    docker compose build
    ```

2. **Set up environment variables**:
    - Create a `.env` file in the project root directory with the following content:
    ```env
    OPENAI_KEY=your-openai-api-key
    OPENAI_LLM=gpt-3.5-turbo
    ```

## Environment Variables

The project uses the following environment variables:

| Variable        | Description                             | Default         |
|-----------------|-----------------------------------------|-----------------|
| `OPENAI_KEY`    | Your OpenAI API key                     | **Required**    |
| `OPENAI_LLM`    | The OpenAI model to use (e.g., GPT-3.5) | `gpt-3.5-turbo` |
| `WORKERS_COUNT` | Number of worker processes for Uvicorn  | 1               |

These variables can be configured in a `.env` file located in the root of your project.

## Running the Application

1. **Run the application**:
    ```bash
    docker compose up
    ```

   2. The FastAPI app will be running at `http://localhost:8002` by default. You can modify the port in docker-compose.yml:
       - **GET /**: Returns a message confirming that the app is running.
         - **POST /** recipie/generate/
           - ```bash
             curl --location 'http://localhost:8002/recipie/generate/' \
               --header 'Content-Type: application/json' \
               --data '{
                 "amountOfPersons": 4,
                 "dishType": "pasta",
                 "maxCooking": 30,
                 "allergieList": ["gluten", "nuts"],
                 "dietRequirements": ["vegetarian", "low-carb"],
                 "cuisineList": ["Italian", "Mediterranean"],
                 "outputDataFormat": "{\"CookingTime\": \"string\", \"RequiredTools\": [\"tool1\", \"tool2\"], \"Ingredients\": [{\"Name\": \"ingredient1\", \"Measurement\": {\"amount\": 100, \"unit\": \"grams\"}}, {\"Name\": \"ingredient2\", \"Measurement\": {\"amount\": 200, \"unit\": \"ml\"}}], \"StepByStep\": [\"Step 1: Do something\", \"Step 2: Do something else\"]}"
               }'
             ```
       - You can define additional endpoints in `main.py` as needed.

3. **Swagger UI**: FastAPI automatically generates interactive API documentation at:
    - `http://localhost:8002/docs`

4. **ReDoc**: Another API documentation at:
    - `http://localhost:8002/redoc`

