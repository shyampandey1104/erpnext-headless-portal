"""Customer and Vendor portal data endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.core.security import get_current_user
from backend.services.frappe_client import FrappeProxy

router = APIRouter(prefix="/portal", tags=["Portal Data"])
frappe_proxy = FrappeProxy()


class SupportTicketRequest(BaseModel):
    subject: str
    description: str


# Sample mock data fallback for live showcase testing without requiring running ERPNext instance
MOCK_INVOICES = [
    {"name": "ACC-SINV-2026-00102", "posting_date": "2026-11-01", "due_date": "2026-11-15", "grand_total": 45000.0, "outstanding_amount": 0.0, "status": "Paid"},
    {"name": "ACC-SINV-2026-00108", "posting_date": "2026-11-05", "due_date": "2026-11-20", "grand_total": 82500.0, "outstanding_amount": 82500.0, "status": "Unpaid"},
    {"name": "ACC-SINV-2026-00115", "posting_date": "2026-11-08", "due_date": "2026-11-25", "grand_total": 31200.0, "outstanding_amount": 10000.0, "status": "Partly Paid"},
]

MOCK_ORDERS = [
    {"name": "SAL-ORD-2026-00054", "transaction_date": "2026-11-02", "delivery_date": "2026-11-18", "grand_total": 125000.0, "status": "To Deliver and Bill", "per_delivered": 60.0},
    {"name": "SAL-ORD-2026-00059", "transaction_date": "2026-11-06", "delivery_date": "2026-11-22", "grand_total": 54000.0, "status": "In Process", "per_delivered": 0.0},
]


@router.get("/dashboard-summary")
async def get_dashboard_summary(current_user: dict = Depends(get_current_user)):
    """Fetch high-level financial summary metrics."""
    customer = current_user.get("customer_id", "Acme Industries Ltd")
    invoices = await frappe_proxy.get_customer_invoices(customer) or MOCK_INVOICES
    orders = await frappe_proxy.get_customer_orders(customer) or MOCK_ORDERS

    total_spend = sum(inv.get("grand_total", 0.0) for inv in invoices)
    total_outstanding = sum(inv.get("outstanding_amount", 0.0) for inv in invoices)
    open_orders = len([o for o in orders if o.get("status") != "Completed"])

    return {
        "customer": customer,
        "total_spend": total_spend,
        "total_outstanding": total_outstanding,
        "open_orders_count": open_orders,
        "total_invoices_count": len(invoices),
    }


@router.get("/invoices")
async def list_invoices(current_user: dict = Depends(get_current_user)):
    """List customer sales invoices."""
    customer = current_user.get("customer_id", "Acme Industries Ltd")
    invoices = await frappe_proxy.get_customer_invoices(customer)
    return invoices if invoices else MOCK_INVOICES


@router.get("/orders")
async def list_orders(current_user: dict = Depends(get_current_user)):
    """List customer sales orders and fulfillment percentages."""
    customer = current_user.get("customer_id", "Acme Industries Ltd")
    orders = await frappe_proxy.get_customer_orders(customer)
    return orders if orders else MOCK_ORDERS


@router.post("/tickets")
async def create_ticket(ticket: SupportTicketRequest, current_user: dict = Depends(get_current_user)):
    """File a support issue into ERPNext."""
    customer = current_user.get("customer_id", "Acme Industries Ltd")
    email = current_user.get("sub", "demo@customer.com")
    result = await frappe_proxy.create_support_issue(
        customer=customer,
        email=email,
        subject=ticket.subject,
        description=ticket.description,
    )
    return {
        "status": "created",
        "ticket_id": result.get("name", "ISSUE-2026-0001"),
        "subject": ticket.subject,
    }
