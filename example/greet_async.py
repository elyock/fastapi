from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/hi")
async def greet() -> str:
    await asyncio.sleep(1)
    return "Hello? World?"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("greet_async:app")