from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date



class Item_Booking(models.Model):
    item_order_id = fields.IntField(pk=True)
    user_id = fields.IntField()
    vendor_id = fields.IntField()
    item_id = fields.IntField()
    booking_date = fields.DateField()
    fees = fields.DecimalField(max_digits=10, decimal_places=2)
    booking_status = fields.BooleanField

    class Meta:
        table = 'item_booking'


# Pydantic models
Item_Booking_Pydantic = pydantic_model_creator(Item_Booking, name="Item_Booking")
Item_BookingIn_Pydantic = pydantic_model_creator(Item_Booking, name="Item_BookingIn", exclude_readonly=True)


class Item_BookingBase(BaseModel):
    item_order_id: int
    user_id: int
    vendor_id: int
    item_id: int
    booking_date: date
    fees: float
    booking_status: bool


class Item_BookingCreate(BaseModel):
    user_id: int
    vendor_id: int
    item_id: int
    booking_date: date
    fees: float


class Item_BookingUpdate(BaseModel):
    user_id: int = None
    vendor_id: int = None
    item_id: int = None
    booking_date: date = None
    fees: float = None
    booking_status: bool = None

