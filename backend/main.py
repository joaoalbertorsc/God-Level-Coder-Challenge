from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health_router, sales_router, customer_router, filter_router, goal_router

app = FastAPI(
    title="God Level Analytics API",
    description="API for restaurant operational data analytics.",
    version="0.0.1",
)

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router)
app.include_router(sales_router.router)
app.include_router(customer_router.router)
app.include_router(filter_router.router)
app.include_router(goal_router.router)
