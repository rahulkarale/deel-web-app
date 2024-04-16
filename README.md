# Deel Web App

This Flask application reverses the IP address of incoming requests and stores them in a SQLite database. It can be deployed as a Docker container.

## Overview

The Deel Web App provides a simple yet powerful functionality to reverse the IP address of incoming requests. It serves as a demonstration of building and deploying a Flask application in a containerized environment.

## Setup Instructions

To set up the Deel Web App locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd deel-web-app
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Building Docker Image

To build the Docker image of the Deel Web App, run:

```bash
docker build -t deel-web-app .
```

## Usage

### Running the Docker Container

To run the Deel Web App as a Docker container, use the following command:

```bash
docker run -d -p 5001:5001 deel-web-app:latest
```

### Sending HTTP Requests

Once the Deel Web App is running, you can send HTTP requests to its endpoint to reverse IP addresses.

- **Reverse IP Address**: Send a GET request to the root endpoint (`/`) to reverse your IP address.
    ```bash
    curl http://localhost:5001/
    ```

- **View Stored IP Addresses**: View stored IP addresses by sending a GET request to the `/ip_addresses` endpoint.
    ```bash
    curl http://localhost:5001/ip_addresses
    ```
