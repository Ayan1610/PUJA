from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date


class Item_Available_Date(models.Model):
    item_id = fields.IntField()
    vendor_id = fields.IntField()
    available_date = fields.DateField()
    item_status = fields.BooleanField()

    class Meta:
        table = 'item_available_date'
        # unique_together = ("item_id", "vendor_id", "available_date")





Item_Available_Date_Pydantic = pydantic_model_creator(Item_Available_Date, name="Item_Available_Date")
Item_Available_DateIn_Pydantic = pydantic_model_creator(Item_Available_Date, name="Item_Available_DateIn", exclude_readonly=True)


class Item_Available_DateBase(BaseModel):
    item_id: int
    vendor_id: int
    available_date: date


class Item_Available_DateCreate(BaseModel):
    item_id: int
    vendor_id: int
    available_date: date


class Item_Available_DateUpdate(BaseModel):
    item_id: int = None
    vendor_id: int = None
    available_date: date = None
    item_status:bool = None