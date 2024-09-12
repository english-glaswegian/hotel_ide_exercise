# from contextlib import contextmanager
import logging
from fastapi import FastAPI

from hotel.db.engine import init_db
from hotel.routers import rooms, customers, bookings, amenities

app = FastAPI()
DB_FILE = "sqlite:///hotel.db"
log = logging.getLogger("uvicorn")
app.include_router(rooms.router)
app.include_router(customers.router)
app.include_router(bookings.router)
app.include_router(amenities.router)


@app.on_event("startup")
def startup_event():
    log.info("Starting up...")
    init_db(DB_FILE)


# @contextmanager DID NOT WORK, CAUSED BIND ERROR WITH SQLALCHEMY
# def lifespan():
#     log.info("Starting up...")
#     init_db(DB_FILE)
#     yield
#     log.info("Shutting down...")


@app.get("/")
def read_root():
    return "The server is running."
