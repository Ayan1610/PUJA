from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date

class Item_Catalog(models.Model):
    catalog_id = fields.IntField(pk=True)
    category_id = fields.IntField()
    category_description = fields.CharField(max_length=255)
    sub_category_id = fields.IntField()
    sub_category_description = fields.CharField(max_length=255)
    catalog_status = fields.BooleanField()

    class Meta:
        table = 'item_catalog'


Item_Catalog_Pydantic = pydantic_model_creator(Item_Catalog, name="Item_Catalog")
Item_CatalogIn_Pydantic = pydantic_model_creator(Item_Catalog, name="Item_CatalogIn", exclude_readonly=True)


class Item_CatalogIn_Pydantic(BaseModel):
    catalog_id: int
    category_id: int
    category_description: str
    sub_category_id: int
    sub_category_description: str
    catalog_status: bool


class Item_CatalogCreate(BaseModel):
    category_id: int
    category_description: str
    sub_category_id: int
    sub_category_description: str

class Item_CatalogUpdate(BaseModel):
    category_id: int = None
    sub_category_id: int = None
    category_description: str = None
    sub_category_description: str = None
    catalog_status: bool = None 