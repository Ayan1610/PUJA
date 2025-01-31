from fastapi import APIRouter, HTTPException, status, Request, Response, Query
from db.models.item_vendor import Item_Vendor, Item_Vendor_Pydantic, Item_VendorCreate, Item_VendorIn_Pydantic, Item_VendorUpdate
from datetime import datetime
from typing import List

router = APIRouter()

# Insert a new item-vendor relationship into Item_Vendor
@router.post('/api/v1_0/createitemvendor', status_code=status.HTTP_201_CREATED)
async def create_item_vendor(
    vendorset: Item_VendorCreate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    vendor_in_db = await Item_Vendor.filter(
        item_id=vendorset.item_id,
        vendor_id=vendorset.vendor_id
    ).first()

    if vendor_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Vendor already linked with this item.',
        )

    vendor_obj = Item_Vendor(
        item_id=vendorset.item_id,
        vendor_id=vendorset.vendor_id,
        fees=vendorset.fees,
        url_for_vendor=vendorset.url_for_vendor
    )

    await vendor_obj.save()

    return {'status': statusStr, 'data': vendor_obj}

# Get all item-vendor relationships from Item_Vendor
@router.get('/api/v1_0/itemvendors', status_code=status.HTTP_200_OK)
async def get_item_vendors(
    request: Request,
    response: Response,
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    vendors = await Item_Vendor.all().offset(offset).limit(limit)
    return vendors

# Update vendor in Item_Vendor
@router.put("/api/v1_0/updatevendor/{item_id}/{vendor_id}", status_code=status.HTTP_200_OK)
async def update_vendor(
    item_id: int,
    vendor_id: int,
    vendorset: Item_VendorUpdate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    vendor_in_db = await Item_Vendor.get_or_none(item_id=item_id, vendor_id=vendor_id)
    if not vendor_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Vendor not found with this item ID and vendor ID.',
        )

    vendor_in_db.fees = vendorset.fees if vendorset.fees != "" else vendor_in_db.fees
    vendor_in_db.url_for_vendor = vendorset.url_for_vendor if vendorset.url_for_vendor != "" else vendor_in_db.url_for_vendor
    vendor_in_db.vendor_id = vendorset.vendor_id if vendorset.vendor_id != "" else vendor_in_db.vendor_id
    vendor_in_db.item_id = vendorset.item_id if vendorset.item_id != "" else vendor_in_db.item_id

    
    await vendor_in_db.save()

    return {'status': statusStr, 'data': vendor_in_db}



# Delete item-vendor relationship from Item_Vendor (soft delete)
@router.delete("/api/v1_0/deleteitemvendor/{item_id}/{vendor_id}", status_code=status.HTTP_200_OK)
async def delete_item_vendor(
    item_id: int,
    vendor_id: int,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    vendor_in_db = await Item_Vendor.get_or_none(item_id=item_id, vendor_id=vendor_id)
    if not vendor_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Item-Vendor relationship not found with this id combination.',
        )

    vendor_in_db.vendor_status = False

    await vendor_in_db.save()

    return {'status': statusStr, 'data': vendor_in_db}
