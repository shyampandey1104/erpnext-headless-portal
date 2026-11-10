"""Authentication router for customer/vendor portal login."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from backend.core.security import create_access_token
from backend.services.frappe_client import FrappeProxy

router = APIRouter(prefix="/auth", tags=["Authentication"])
frappe_proxy = FrappeProxy()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest):
    # Support demonstration mock mode or live ERPNext validation
    if req.email == "demo@customer.com" and req.password == "demo123":
        user_data = {"email": req.email, "full_name": "Demo Enterprise Client", "customer": "Acme Industries Ltd"}
        token = create_access_token(subject=req.email, role="Customer", customer_id="Acme Industries Ltd")
        return {"access_token": token, "token_type": "bearer", "user": user_data}

    frappe_user = await frappe_proxy.authenticate_user(req.email, req.password)
    if not frappe_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    token = create_access_token(subject=frappe_user["email"], role="Customer")
    return {"access_token": token, "token_type": "bearer", "user": frappe_user}
