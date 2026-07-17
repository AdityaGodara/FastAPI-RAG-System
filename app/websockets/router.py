from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.jobs.subscriber import subscribe

router = APIRouter()


@router.websocket("/jobs/{job_id}")

async def job_updates(
    websocket: WebSocket,
    job_id: str,
):
    await websocket.accept()

    try:

        async for message in subscribe(job_id):

            await websocket.send_text(message)

    except WebSocketDisconnect:
        pass