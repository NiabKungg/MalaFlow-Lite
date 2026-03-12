import os
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import models
from database import engine, get_db
from websocket_manager import manager
from routers import menu, tables, orders, history, auth
import telegram_bot

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create all tables
models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Telegram bot in background
    asyncio.create_task(telegram_bot.start_telegram_bot())
    yield
    await telegram_bot.stop_telegram_bot()


app = FastAPI(
    title="MalaFlow POS",
    description="Restaurant Management & POS System for Mala/Shabu",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(menu.router)
app.include_router(tables.router)
app.include_router(orders.router)
app.include_router(history.router)
app.include_router(auth.router)


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/img", StaticFiles(directory="img"), name="img")

# Root redirect to menu
@app.get("/")
async def root():
    return FileResponse("static/order.html")


@app.get("/order")
async def order_page():
    return FileResponse("static/order.html")


@app.get("/order-status")
async def order_status_page():
    return FileResponse("static/order-status.html")


@app.get("/pos")
async def pos_page():
    return FileResponse("static/pos.html")


@app.get("/history")
async def history_page():
    return FileResponse("static/history.html")


@app.get("/table={table_number}")
async def table_qr_redirect(table_number: int):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/order?table={table_number}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
