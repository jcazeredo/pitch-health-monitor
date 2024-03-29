# Pitch Health Monitoring System

This project implements a RESTful API for monitoring and maintaining pitch health, developed with FastAPI, MongoDB and Pydantic. It includes a CRUD interface for pitch data management and specialized routes for maintenance operations. The system is designed to automatically assess pitch conditions every 30 minutes, taking into account weather impacts to determine necessary maintenance actions. For that, the system uses the OpenWeather API, which is already included in this demo code for demonstrations. 

Note: Last version tested with Python 3.9.8

## Getting Started

### Clone the Repository
````
git clone https://github.com/jcazeredo/pitch-health-monitor.git
cd pitch-health-monitor
````

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

This command pulls the MongoDB image and runs it in a container, making the database available on port 27017. In case you have your own MongoDB instance, please change the environment variable `MONGO_URI` accordingly.

#### Start the FastAPI Application
Activate the Poetry shell to use the virtual environment:
````
poetry shell
````

Then, start the FastAPI server:
````
uvicorn pitch_health_monitor.main:app --reload
````

The application will be available at http://localhost:8000.

### API Documentation
Navigate to http://localhost:8000/docs to view the Swagger UI documentation, which provides detailed information about the API's endpoints and their usage.
