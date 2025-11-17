from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents
from schemas import Event, TicketType, Voucher, Order, ScanEvent

app = FastAPI(title="Duatix API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Health(BaseModel):
    status: str
    time: datetime


@app.get("/health", response_model=Health)
async def health():
    return Health(status="ok", time=datetime.utcnow())


@app.get("/events", response_model=List[Event])
async def list_events(limit: int = 50):
    items = get_documents("event", {}, limit)
    return items


@app.post("/events", response_model=Event)
async def create_event(event: Event):
    created = create_document("event", event.model_dump())
    return created


@app.get("/tickets", response_model=List[TicketType])
async def list_ticket_types(event_id: Optional[str] = None, limit: int = 100):
    filt = {"event_id": event_id} if event_id else {}
    items = get_documents("tickettype", filt, limit)
    return items


@app.post("/tickets", response_model=TicketType)
async def create_ticket_type(ticket: TicketType):
    created = create_document("tickettype", ticket.model_dump())
    return created


@app.get("/vouchers", response_model=List[Voucher])
async def list_vouchers(event_id: Optional[str] = None, limit: int = 100):
    filt = {"event_id": event_id} if event_id else {}
    items = get_documents("voucher", filt, limit)
    return items


@app.post("/vouchers", response_model=Voucher)
async def create_voucher(voucher: Voucher):
    created = create_document("voucher", voucher.model_dump())
    return created


@app.post("/orders", response_model=Order)
async def create_order(order: Order):
    # In a real system, integrate a payment provider here
    created = create_document("order", order.model_dump())
    return created


@app.post("/scan")
async def scan_ticket(scan: ScanEvent):
    # Placeholder scan verification logic
    # In a complete system, decode QR, verify order/ticket in DB
    if not scan.qr:
        raise HTTPException(status_code=400, detail="Invalid QR")
    return {"status": "valid", "qr": scan.qr, "scanned_at": datetime.utcnow().isoformat()}
