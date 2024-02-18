# Pitch Health Monitoring System

This project implements a RESTful API for monitoring and maintaining pitch health, developed with FastAPI, MongoDB and Pydantic. It includes a CRUD interface for pitch data management and specialized routes for maintenance operations. The system is designed to automatically assess pitch conditions every 30 minutes, taking into account weather impacts to determine necessary maintenance actions. For that, the system uses the OpenWeather API, which is already included in this demo code for demonstrations. 

## Getting Started

### Clone the Repository
````
git clone <your-repository-url>
cd <your-repository-directory>
````

### Alternative 1: Running with Docker Compose
1. **Start the Application**: Run the following command in the project's root directory to start all services, including MongoDB and the FastAPI application:

    ```bash
    docker-compose up
    ```

2. **Stop the Application**: To stop and remove the containers, use:

    ```bash
    docker-compose down
    ```

### Alternative 2: Running with Traditional Setup
If you prefer a manual setup instead of using Docker Compose, follow the instructions below.


Setup Environment with Poetry
Install Poetry and the project dependencies:
#### Setup Environment with Poetry
Install Poetry if you haven't already:
````
curl -sSL https://install.python-poetry.org | python3 -
````

Install the project dependencies using Poetry:

````
poetry install
````

#### Running MongoDB with Docker
````
docker run -d -p 27017:27017 --name mongodb -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo:jammy
````

This command pulls the MongoDB image and runs it in a container, making the database available on port 27017.

#### Start the FastAPI Application
Activate the Poetry shell to use the virtual environment:
````
poetry shell
````

Then, start the FastAPI server:
````
uvicorn app.main:app --reload
````

The application will be available at http://localhost:8000.

### API Documentation
Navigate to http://localhost:8000/docs to view the Swagger UI documentation, which provides detailed information about the API's endpoints and their usage.
