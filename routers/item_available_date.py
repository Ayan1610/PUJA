from fastapi import APIRouter, HTTPException, status, Request, Response, Query
from db.models.item_available_date import Item_Available_Date, Item_Available_Date_Pydantic, Item_Available_DateCreate, Item_Available_DateIn_Pydantic, Item_Available_DateUpdate
from datetime import datetime
from typing import List


router = APIRouter()


# Insert a new item into Item_Available_Date
@router.post('/api/v1_0/createavailabledate', status_code=status.HTTP_201_CREATED)
async def create_available_date(
    available_dateset: Item_Available_DateCreate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    date_in_db = await Item_Available_Date.filter(
        item_id=available_dateset.item_id,
        vendor_id=available_dateset.vendor_id,
        available_date=available_dateset.available_date
    ).first()

    if date_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Available date already exists for this item and vendor.',
        )

    date_obj = Item_Available_Date(
        item_id=available_dateset.item_id,
        vendor_id=available_dateset.vendor_id,
        available_date=available_dateset.available_date,
        item_status=True
    )

    await date_obj.save()

    return {'status': statusStr, 'data': date_obj}


# Get all items from Item_Available_Date
@router.get('/api/v1_0/availabledates', status_code=status.HTTP_200_OK)
async def get_available_dates(
    request: Request,
    response: Response,
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    dates = await Item_Available_Date.all().offset(offset).limit(limit)
    return dates


# Update item in Item_Available_Date
@router.put("/api/v1_0/updateavailabledate/{available_date_id}", status_code=status.HTTP_200_OK)
async def update_available_date(
    available_date_id: int,
    available_dateset: Item_Available_DateUpdate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    date_in_db = await Item_Available_Date.get_or_none(id=available_date_id)
    if not date_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Available date not found with this id.',
        )

    date_in_db.item_id = available_dateset.item_id if available_dateset.item_id != "" else date_in_db.item_id
    date_in_db.vendor_id = available_dateset.vendor_id if available_dateset.vendor_id != "" else date_in_db.vendor_id
    date_in_db.available_date = available_dateset.available_date if available_dateset.available_date != "" else date_in_db.available_date
    
    
    await date_in_db.save()

    return {'status': statusStr, 'data': date_in_db}


# Delete item from Item_Available_Date
@router.delete("/api/v1_0/deleteavailabledate/{available_date_id}", status_code=status.HTTP_200_OK)
async def delete_available_date(
    available_date_id: int,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    date_in_db = await Item_Available_Date.get_or_none(id=available_date_id)
    if not date_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Available date not found with this id.',
        )

    date_in_db.item_status = False
    await date_in_db.save()

    return {'status': statusStr, 'data': date_in_db}
