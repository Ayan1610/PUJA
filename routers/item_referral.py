from fastapi import APIRouter, HTTPException, status, Request, Response, Query
from db.models.item_referral import Item_Referral, Item_Referral_Pydantic, Item_ReferralCreate, Item_ReferralIn_Pydantic, Item_ReferralUpdate
from datetime import datetime
from typing import List


router = APIRouter()


# Insert a new item into Item_Referral
@router.post('/api/v1_0/createreferral', status_code=status.HTTP_201_CREATED)
async def create_referral(
    referralset: Item_ReferralCreate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    referral_in_db = await Item_Referral.filter(
        item_id=referralset.item_id,
        referred_by=referralset.referred_by,
        referred_to=referralset.referred_to,
        referral_date=referralset.referral_date
    ).first()

    if referral_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Referral already exists with this item, referrer, and referee on the specified date.',
        )

    referral_obj = Item_Referral(
        item_id=referralset.item_id,
        referred_by=referralset.referred_by,
        referred_to=referralset.referred_to,
        referral_date=referralset.referral_date
    )

    await referral_obj.save()

    return {'status': statusStr, 'data': referral_obj}

# Get all referrals from Item_Referral
@router.get('/api/v1_0/referrals', status_code=status.HTTP_200_OK)
async def get_referrals(
    request: Request,
    response: Response,
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    referrals = await Item_Referral.all().offset(offset).limit(limit)
    return referrals

# Update referral in Item_Referral
@router.put("/api/v1_0/updatereferral/{referral_id}", status_code=status.HTTP_200_OK)
async def update_referral(
    referral_id: int,
    referralset: Item_ReferralUpdate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    referral_in_db = await Item_Referral.get_or_none(id=referral_id)
    if not referral_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Referral not found with this id.',
        )

    referral_in_db.item_id = referralset.item_id if referralset.item_id != "" else referral_in_db.item_id
    referral_in_db.referred_by = referralset.referred_by if referralset.referred_by != "" else referral_in_db.referred_by
    referral_in_db.referred_to = referralset.referred_to if referralset.referred_to != "" else referral_in_db.referred_to
    referral_in_db.referral_date = referralset.referral_date if referralset.referral_date != "" else referral_in_db.referral_date
    

    await referral_in_db.save()

    return {'status': statusStr, 'data': referral_in_db}

# Delete referral from Item_Referral
@router.delete("/api/v1_0/deletereferral/{referral_id}", status_code=status.HTTP_200_OK)
async def delete_referral(
    referral_id: int,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    referral_in_db = await Item_Referral.get_or_none(id=referral_id)
    if not referral_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Referral not found with this id.',
        )

    referral_in_db.referral_status = False

    await referral_in_db.save()

    return {'status': statusStr, 'data': referral_in_db}

