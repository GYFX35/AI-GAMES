GAMES UNIVERSE

## Game Asset Management API

This is a simple API for managing game assets, with a focus on 3D models.

### Setup

1.  **Install dependencies:**
    ```bash
    pip install -r api/requirements.txt
    ```

2.  **Run the API server:**
    ```bash
    cd api
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```
    The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

The API provides the following endpoints for managing 3D models:

*   **Upload a model:**
    *   `POST /models`
    *   **Body:** `multipart/form-data` with a `file` field containing the model file.
    *   **Example using curl:**
        ```bash
        curl -X POST -F "file=@/path/to/your/model.obj" http://127.0.0.1:8000/models
        ```

*   **List all models:**
    *   `GET /models`
    *   **Example using curl:**
        ```bash
        curl http://127.0.0.1:8000/models
        ```

*   **Download a model:**
    *   `GET /models/{model_name}`
    *   **Example using curl:**
        ```bash
        curl http://127.0.0.1:8000/models/your_model.obj -o your_model.obj
        ```

*   **Delete a model:**
    *   `DELETE /models/{model_name}`
    *   **Example using curl:**
        ```bash
        curl -X DELETE http://127.0.0.1:8000/models/your_model.obj
        ```

### API Documentation

The API comes with automatic interactive documentation (Swagger UI). Once the server is running, you can access it at `http://127.0.0.1:8000/docs`.

### Environment Variables

To run the application, you will need to create a `.env` file in the `api` directory with the following environment variables:

```
STRIPE_SECRET_KEY=your_stripe_secret_key
```

You can get your Stripe secret key from the [Stripe dashboard](https://dashboard.stripe.com/apikeys).

## Deployment

This application is containerized using Docker and orchestrated with Docker Compose.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/games-universe.git
    cd games-universe
    ```

2.  **Run the application using Docker Compose:**
    ```bash
    docker-compose up --build
    ```

The application will be available at `http://localhost`.

*   The frontend is served by Nginx on port 80.
*   The backend API is available on port 8000.
*   The Nginx server is configured to proxy requests to the `/api` and `/models` endpoints to the backend service.
