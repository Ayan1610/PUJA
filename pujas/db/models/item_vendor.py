from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date



class Item_Vendor(models.Model):
    item_id = fields.IntField()
    vendor_id = fields.IntField()
    fees = fields.DecimalField(max_digits=10, decimal_places=2)
    url_for_vendor = fields.CharField(max_length=255)
    vendor_status = fields.BooleanField()

    class Meta:
        table = 'item_vendor'
        # unique_together = ("item_id", "vendor_id")



Item_Vendor_Pydantic = pydantic_model_creator(Item_Vendor, name="Item_Vendor")
Item_VendorIn_Pydantic = pydantic_model_creator(Item_Vendor, name="Item_VendorIn", exclude_readonly=True)


class Item_VendorIn_Pydantic(BaseModel):
    item_id: int
    vendor_id: int
    fees: float
    url_for_vendor: str
    vendor_status: bool


class Item_VendorCreate(BaseModel):
    item_id: int
    vendor_id: int
    fees: float
    url_for_vendor: str


class Item_VendorUpdate(BaseModel):
    item_id: int = None
    vendor_id: int = None
    fees: float = None
    url_for_vendor: str = None
    vendor_status: bool = None


