from fastapi import FastAPI

app = FastAPI(title="Knowledge Assistant API")


@app.get("/")
def root():
    return {"message": "Knowledge Assistant API is running 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}