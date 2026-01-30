from fastapi import FastAPI
from app.routes.whatsapp_webhook import router as whatsapp_router

app = FastAPI(title="TicketIQ – Sariah")

app.include_router(whatsapp_router)
