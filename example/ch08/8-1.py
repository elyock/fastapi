from fastapi import FastAPI
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
app = FastAPI()

@app.get("/")
def top():
    return "top here"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
