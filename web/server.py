"""Handle the server through various resources"""

from fastapi import FastAPI
from uvicorn import run

app = FastAPI()


if __name__ == "__main__":
    run("server:app", host="0.0.0.0", port=5000, log_level="info")
