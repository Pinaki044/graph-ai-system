# 📊 Graph-Based Business Query System

## 🚀 Overview

This project builds a **context graph system with an LLM-powered query interface**.

It transforms fragmented business data (orders, deliveries, billing, payments) into a **connected graph** and allows users to query it using **natural language**.

---

## 🧠 Key Features

### 🔗 Graph Construction
- Nodes: Customers, Orders, Products, Deliveries, Billing, Payments
- Relationships:
  - Customer → Order
  - Order → Delivery
  - Order → Billing
  - Billing → Payment
  - Delivery → Product
  - Billing → Product

---

### 💬 LLM-Powered Query Interface
- Uses **OpenRouter API**
- Converts natural language → structured intent
- Dynamically routes queries to backend functions

Example:
> "Which products generated highest sales?"

→ LLM → `top_products()` → Graph query → Result

---

### 🔍 Supported Queries

- Top billed products
- Orders without delivery
- Delivered but not billed
- Billed but not delivered
- Trace full order flow

---

### 🛡️ Guardrails

- Restricts queries to business dataset only
- Rejects irrelevant prompts

Example:
> "Who is the Prime Minister of India?"

→ ❌ Rejected

---

## 🖥️ UI

- Built using **Streamlit**
- Two-panel layout:
  - 📊 Graph visualization
  - 💬 Chat interface

---

## 🏗️ Tech Stack

- Python
- NetworkX (Graph modeling)
- Streamlit (UI)
- OpenRouter (LLM API)
- Pandas (Data processing)

---

## 📂 Project Structure