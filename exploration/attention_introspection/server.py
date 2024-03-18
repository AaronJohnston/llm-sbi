from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import attention

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html", context={"request": request}
    )


@app.post("/api/attention", response_class=HTMLResponse)
def get_attention(request: Request, prompt: Annotated[str, Form()]):
    tokens = attention.text_completion_with_attention(prompt)
    return templates.TemplateResponse(
        name="attention.html", context={"request": request, "prompt": prompt, "tokens": tokens}
    )
