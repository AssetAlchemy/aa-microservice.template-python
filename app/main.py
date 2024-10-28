from fastapi import FastAPI

# FastAPI instance
app = FastAPI()

# Test route
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
