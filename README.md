# Bisection Method API

This API performs root-finding using the bisection method for given functions and intervals.

## Setup Instructions

1. **Clone the repository**:
    ```
    git clone <repository-url>
    cd api_project
    ```

2. **Create a virtual environment and install dependencies**:
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```
    flask run
    ```

## Docker Instructions

1. **Build the Docker image**:
    ```
    docker build -t api_project .
    ```

2. **Run the Docker container**:
    ```
    docker run -p 5000:5000 api_project
    ```

## API Endpoints

### POST /bisection
Creates a new bisection method calculation.

**Request:**
```bash
curl -u user:password -X POST -H "Content-Type: application/json" -d '{
    "function": "x**3 - x - 2",
    "interval": [1, 2],
    "tolerance": 0.001
}' http://localhost:5000/bisection
