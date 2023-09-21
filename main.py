from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from routes import item_routes, order_routes, sold_item_routes
import db_conn

# FastAPI
app = FastAPI()

# CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initial route is swagger ui docs
@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    response = RedirectResponse(url='/docs')
    return response

# create database engine
db_conn.base.metadata.create_all(db_conn.engine)

# include routes
app.include_router(item_routes.approute)
app.include_router(order_routes.approute)
app.include_router(sold_item_routes.approute)

# file path
app.mount("/images", StaticFiles(directory = "images"), name="images")