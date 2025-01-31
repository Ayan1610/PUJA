import os
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from routers import item_catalog
from routers import item_master



app = FastAPI()

app.include_router(item_catalog.router)
app.include_router(item_master.router)

register_tortoise(
    app,
    db_url=os.environ.get('DB_CONFIG'),
    modules= {'models': ['db.models.orders','db.models.plans','db.models.billings','db.models.services','db.models.notifications']},
    generate_schemas=True,
    add_exception_handlers=True,
)