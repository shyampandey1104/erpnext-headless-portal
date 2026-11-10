# 🌐 ERPNext Headless Customer & Vendor Web Portal

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)](https://erpnext.com)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0+-38B2AC.svg?logo=tailwind-css)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, high-speed, decoupled **Headless Web Portal** for **ERPNext** built with **FastAPI**, JWT role-based security, and a responsive Tailwind CSS / Alpine.js Single Page Application.

Replaces standard heavy Frappe Desk portals with a blazingly fast, branded customer experience for viewing invoices, tracking sales orders, downloading PDF statements, and submitting support tickets.

---

## ✨ Features

- ⚡ **Decoupled Architecture**: Fully separated presentation layer from Frappe core; zero load on Frappe Desk during high portal traffic.
- 🔐 **JWT Token Authentication**: Secure sessionless authentication proxying Frappe user validation without exposing ERPNext administrative API keys.
- 📊 **Real-time Financial KPI Cards**: Live lifetime billing, pending balance due, and active order counters.
- 🧾 **Invoices & Statements**: Live Sales Invoice table with color-coded status badges (`Paid`, `Unpaid`, `Partly Paid`) and PDF download integration.
- 📦 **Order Fulfillment Tracker**: Visual progress bar tracking order delivery and dispatch stages (`SAL-ORD`).
- 🎫 **Support Ticketing**: Direct Frappe `Issue` DocType creation for inquiries and discrepancies.
- 🎨 **Modern Dark UI**: Designed with glassmorphism, Phosphor icons, and full mobile responsiveness.

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────┐
│             Headless Portal Web Client                 │
│      (Tailwind CSS + Alpine.js SPA / Responsive)       │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON (JWT Auth)
                            ▼
┌────────────────────────────────────────────────────────┐
│               FastAPI Portal Backend                   │
│   • JWT Auth & Permission Scopes                       │
│   • Frappe REST API Proxy                              │
│   • Aggregated Financial Metrics                       │
│   • OpenAPI 3.0 Documentation (/docs)                  │
└───────────────────────────┬────────────────────────────┘
                            │ Whitelist RPC & REST
                            ▼
┌────────────────────────────────────────────────────────┐
│                  ERPNext / Frappe                      │
│     (Customer, Sales Invoice, Sales Order, Issue)      │
└────────────────────────────────────────────────────────┘
```

---

## ⚙️ Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-headless-portal.git
cd erpnext-headless-portal
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env`:
```env
ERPNEXT_URL=https://your-site.frappe.cloud
ERPNEXT_API_KEY=your_api_key
ERPNEXT_API_SECRET=your_api_secret
SECRET_KEY=your_secure_jwt_secret_key
```

### 3. Run Development Server

```bash
uvicorn backend.main:app --reload --port 8000
```
- Open `http://localhost:8000` to view the Portal.
- Open `http://localhost:8000/docs` for interactive Swagger API documentation.

### 4. Demo Login Credentials

For demonstration without a live Frappe server:
- **Email**: `demo@customer.com`
- **Password**: `demo123`

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

Author: **Shyamkumar Bhupendra Pandey** ([@shyampandey1104](https://github.com/shyampandey1104))
