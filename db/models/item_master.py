from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date

class Item_Master(models.Model):
    item_id = fields.IntField(pk=True)
    category_id = fields.IntField()
    sub_category_id = fields.IntField()
    item_description = fields.CharField(max_length=255)
    item_image = fields.CharField(max_length=255)
    item_status = fields.BooleanField()

    class Meta:
        table = 'item_master'


Item_Master_Pydantic = pydantic_model_creator(Item_Master, name="Item_Master")
Item_MasterIn_Pydantic = pydantic_model_creator(Item_Master, name="Item_MasterIn", exclude_readonly=True)


class Item_MasterIn_Pydantic(BaseModel):
    category_id: int
    sub_category_id: int
    item_id: int
    item_description: str
    item_image: str
    item_status: bool


class Item_MasterCreate(BaseModel):
    category_id: int
    sub_category_id: int
    item_description: str
    item_image: str

class Item_MasterUpdate(BaseModel):
    category_id: int = None
    sub_category_id: int = None
    item_description: str = None
    item_image: str = None
    item_status: bool = None

    