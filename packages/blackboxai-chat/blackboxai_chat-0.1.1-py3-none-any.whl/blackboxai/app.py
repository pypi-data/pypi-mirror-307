import os
import random
import sys
import json
from typing import Dict, List, Optional, AsyncGenerator

from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from blackboxai.session_manager import SessionManager

app = FastAPI()
session_manager = SessionManager()


class UserChatRequest(BaseModel):
    sid: str
    prompt: str
    codebase: str = None


class UserRequest(BaseModel):
    sid: str


@app.post("/chat")
async def chat_repo(sid: str = Form(...), prompt: str = Form(...), repository: UploadFile = File(...)):
    session = session_manager.get_session(sid)
    if session is None:
        repo_content = await repository.read()
        session = session_manager.add_or_restart_session(sid, repository=repo_content)
    coder = session.coder
    state = session.state

    state.messages.append({"role": "user", "content": prompt})
    state.input_history.append(prompt)
    coder.io.add_to_input_history(prompt)

    async def event_generator(prompt: str) -> AsyncGenerator[str, None]:
        num_reflections = 0
        max_reflections = 3
        while prompt:
            async for output in coder.arun_stream(prompt):
                if isinstance(output, str):
                    yield f"data: {json.dumps({'token': output})}\n\n"
                else:
                    yield f"data: {json.dumps({'edits': output, 'format': coder.edit_format})}\n\n"
            prompt = None
            if coder.reflected_message:
                if num_reflections < max_reflections:
                    num_reflections += 1
                    state.messages.append({"role": "info", "content": coder.reflected_message})
                    prompt = coder.reflected_message

    return StreamingResponse(
        event_generator(prompt), 
        media_type="text/event-stream",
    )


@app.post("/clear_chat")
async def clear_chat(request: UserRequest):
    session = session_manager.get_session(sid)
    if session:
        session.coder.done_messages = []
        session.coder.cur_messages = []
    return {"status": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)