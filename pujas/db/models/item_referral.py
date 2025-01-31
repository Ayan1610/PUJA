from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from datetime import date

class Item_Referral(models.Model):
    item_id = fields.IntField()
    referred_by = fields.IntField()
    referred_to = fields.IntField()
    referral_date = fields.DateField()
    referral_status = fields.BooleanField()

    class Meta:
        table = 'item_referral'
        # unique_together = ("item_id", "referred_by", "referred_to", "referral_date")



Item_Referral_Pydantic = pydantic_model_creator(Item_Referral, name="Item_Referral")
Item_ReferralIn_Pydantic = pydantic_model_creator(Item_Referral, name="Item_ReferralIn", exclude_readonly=True)


class Item_ReferralBase(BaseModel):
    item_id: int
    referred_by: int
    referred_to: int
    referral_date: date


class Item_ReferralCreate(BaseModel):
    item_id: int
    referred_by: int
    referred_to: int
    referral_date: date


class Item_ReferralUpdate(BaseModel):
    item_id: int = None
    referred_by: int = None
    referred_to: int = None
    referral_date: date = None
    referral_status: bool = None

