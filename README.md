# Driver Geo API

This project consists of a FastAPI-based service that receives random coordinates from a generator script and logs any anomalies. The data is stored in a PostgreSQL database. The service and the generator are both containerized using Docker.

## Features

- Generate random coordinates for drivers and send them to the API.
- FastAPI service with an endpoint to receive and process driver coordinates.
- Logging of anomalous data based on speed, altitude, and unrealistic travel distance.
- Store data in PostgreSQL with indicators of data correctness.
- Health check endpoint to ensure database connectivity.
- Automatic reconnection to the database in case of connection failure.

## Setup and Running

```sh
docker-compose up --build
```

The FastAPI service will be available at `http://localhost:8000`.