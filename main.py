import os
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from routers import item_catalog
from routers import item_master
from routers import item_vendor
from routers import item_booking
from routers import item_available_date
from routers import item_referral


app = FastAPI()

app.include_router(item_catalog.router)
app.include_router(item_master.router)
app.include_router(item_vendor.router)
app.include_router(item_booking.router)
app.include_router(item_available_date.router)
app.include_router(item_referral.router)


register_tortoise(
    app,
    db_url=os.environ.get('DB_CONFIG'),
    modules= {'models': ['db.models.item_catalog','db.models.item_master','db.models.item_vendor','db.models.item_booking','db.models.item_available_date','db.models.item_referral']},
    generate_schemas=True,
    add_exception_handlers=True,
)