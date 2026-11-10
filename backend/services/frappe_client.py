"""Asynchronous Frappe REST API proxy for portal endpoints."""

import httpx
from typing import Any, Dict, List, Optional
from backend.core.config import settings


class FrappeProxy:
    def __init__(self):
        self.base_url = settings.ERPNEXT_URL.rstrip("/")
        self.headers = {
            "Authorization": f"token {settings.ERPNEXT_API_KEY}:{settings.ERPNEXT_API_SECRET}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Validate user credentials against Frappe login endpoint."""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                res = await client.post(
                    f"{self.base_url}/api/method/login",
                    data={"usr": email, "pwd": password},
                )
                if res.status_code == 200:
                    # Fetch linked customer record
                    customer_res = await client.get(
                        f"{self.base_url}/api/resource/Portal User",
                        headers=self.headers,
                        params={"filters": f'[["user", "=", "{email}"]]'},
                    )
                    return {"email": email, "full_name": res.json().get("full_name", email)}
            except Exception:
                pass
        return None

    async def get_customer_invoices(self, customer: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"{self.base_url}/api/resource/Sales Invoice"
            params = {
                "filters": f'[["customer", "=", "{customer}"], ["docstatus", "=", 1]]',
                "fields": '["name", "posting_date", "due_date", "grand_total", "outstanding_amount", "status"]',
                "order_by": "posting_date desc",
                "limit_page_length": "50",
            }
            res = await client.get(url, headers=self.headers, params=params)
            return res.json().get("data", []) if res.status_code == 200 else []

    async def get_customer_orders(self, customer: str) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"{self.base_url}/api/resource/Sales Order"
            params = {
                "filters": f'[["customer", "=", "{customer}"]]',
                "fields": '["name", "transaction_date", "delivery_date", "grand_total", "status", "per_delivered"]',
                "order_by": "transaction_date desc",
                "limit_page_length": "50",
            }
            res = await client.get(url, headers=self.headers, params=params)
            return res.json().get("data", []) if res.status_code == 200 else []

    async def create_support_issue(self, customer: str, email: str, subject: str, description: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            url = f"{self.base_url}/api/resource/Issue"
            payload = {
                "subject": subject,
                "customer": customer,
                "raised_by": email,
                "description": description,
                "status": "Open",
                "priority": "Medium",
            }
            res = await client.post(url, headers=self.headers, json=payload)
            return res.json().get("data", {}) if res.status_code in (200, 201) else {}
