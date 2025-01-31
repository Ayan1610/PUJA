from fastapi import APIRouter, HTTPException, status, Request, Response, Header, Query
from db.models.item_master import Item_Master,Item_Master_Pydantic,Item_MasterCreate,Item_MasterIn_Pydantic,Item_MasterUpdate
from datetime import datetime
from typing import List

router = APIRouter()

# Insert a new item into Item_Master
@router.post('/api/v1_0/createitem', status_code=status.HTTP_201_CREATED)
async def create_item(
    itemset: Item_MasterCreate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    item_in_db = await Item_Master.filter(
        category_id=itemset.category_id,
        sub_category_id=itemset.sub_category_id,
        item_description=itemset.item_description
    ).first()

    if item_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Item already exists with this description in the specified category and sub-category.',
        )

    item_obj = Item_Master(
        category_id=itemset.category_id,
        sub_category_id=itemset.sub_category_id,
        item_description=itemset.item_description,
        item_image=itemset.item_image
    )

    await item_obj.save()

    return {'status': statusStr, 'data': item_obj}

# Get all items from Item_Master
@router.get('/api/v1_0/items', status_code=status.HTTP_200_OK)
async def get_items(
    request: Request,
    response: Response,
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    items = await Item_Master.all().offset(offset).limit(limit)
    return items

# Update item in Item_Master
@router.put("/api/v1_0/updateitem/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(
    item_id: int,
    itemset: Item_MasterUpdate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    item_in_db = await Item_Master.get_or_none(item_id=item_id)
    if not item_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found with this id.',
        )

    item_in_db.item_description = itemset.item_description if itemset.item_description != "" else item_in_db.item_description
    item_in_db.item_image = itemset.item_image if itemset.item_image != "" else item_in_db.item_image
    item_in_db.category_id = itemset.category_id if itemset.category_id != "" else item_in_db.category_id
    item_in_db.sub_category_id = itemset.sub_category_id if itemset.sub_category_id != "" else item_in_db.sub_category_id

    await item_in_db.save()

    return {'status': statusStr, 'data': item_in_db}

# Delete item from Item_Master
@router.delete("/api/v1_0/deleteitem/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(
    item_id: int,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    item_in_db = await Item_Master.get_or_none(item_id=item_id)
    if not item_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item not found with this id.',
        )

    await item_in_db.item_status = False

    await item_in_db.save()

    return {'status': statusStr, 'data': item_in_db}

# TASK:add get item by id
# NOTE