from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from web import explorer, creature, user
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

top = Path(__file__).resolve().parent
template_obj = Jinja2Templates(directory=f"{top}/template")

from fake.creature import _creatures as fake_creatures
from fake.explorer import _explorers as fake_explorers

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

app.mount("/static",
          StaticFiles(directory=f"{top}/static", html=True))

def gen_file(path: str):
    with open(file=path, mode="rb") as file:
        yield file.read()

@app.get("/download_big/{name}")
async def download_big_file(name: str):
    gen_expr = gen_file(name)
    response = StreamingResponse(
        content=gen_expr,
        status_code=200,
    )
    return response

@app.get("/small/{name}")
async def download_small_file(name: str):
    return FileResponse(name)

@app.post("/who2")
def greet2(name: str = Form()) -> str:
    return f"Hello {name}!"

@app.post("/small")
async def upload_small_file(small_file: bytes = File()) -> str:
    return f"file size: {len(small_file)}"

@app.post("/big")
async def upload_big_file(big_file: UploadFile) -> str:
    return f"file size: {big_file.size}, name: {big_file.filename}"

@app.get("/list")
def explorer_list(request: Request):
    return template_obj.TemplateResponse("list.html", 
        {"request": request, "creatures": fake_creatures,
                                    "explorers": fake_explorers})

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
