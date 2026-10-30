from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from chat import Chat
from db import DATA_DIR, FILE_DIR

MAX_UPLOAD_SIZE = 10


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.chat = Chat()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/ask")
def ask_question(question: str = Query(..., min_length=1)) -> dict[str, object]:
    try:
        result = app.state.chat.qa.invoke(question)
        answer = result.content[0]["text"] if hasattr(result, "content") else result
        return {"answer": answer}
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get an answer: {exc}",
        ) from exc


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)) -> dict[str, str]:
    if not file.filename or Path(file.filename).suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = None

    try:
        with NamedTemporaryFile(
            mode="wb", dir=DATA_DIR, suffix=".tmp", delete=False
        ) as destination:
            temp_path = Path(destination.name)
            size = 0
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size >= MAX_UPLOAD_SIZE * 1024 * 1024:
                    raise HTTPException(
                        status_code=413,
                        detail="File must be smaller than 10 MB.",
                    )
                destination.write(chunk)

        if size == 0:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")

        temp_path.replace(FILE_DIR)
        temp_path = None
        app.state.chat.set_db()
        return {"message": "PDF uploaded successfully."}
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
