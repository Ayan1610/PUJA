from fastapi import APIRouter, HTTPException, status, Request, Response, Query
from db.models.item_catalog import Item_Catalog, Item_Catalog_Pydantic, Item_CatalogCreate, Item_CatalogIn_Pydantic, Item_CatalogUpdate
from datetime import datetime
from typing import List

router = APIRouter()

# Insert a new item into Item_Catalog

@router.post('/api/v1_0/createcatalog', status_code=status.HTTP_201_CREATED)
async def create_catalog(
    catalogset: Item_CatalogCreate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    catalog_in_db = await Item_Catalog.filter(
        category_id=catalogset.category_id,
        sub_category_id=catalogset.sub_category_id,
        category_description=catalogset.category_description,
        sub_category_description=catalogset.sub_category_description
    ).first()

    if catalog_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Catalog already exists with this description in the specified category and sub-category.',
        )

    catalog_obj = Item_Catalog(
        category_id=catalogset.category_id,
        category_description=catalogset.category_description,
        sub_category_id=catalogset.sub_category_id,
        sub_category_description=catalogset.sub_category_description
    )

    await catalog_obj.save()

    return {'status': statusStr, 'data': catalog_obj}

# Get all items from Item_Catalog

@router.get('/api/v1_0/catalogs', status_code=status.HTTP_200_OK)
async def get_catalogs(
    request: Request,
    response: Response,
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    catalogs = await Item_Catalog.all().offset(offset).limit(limit)
    return catalogs

# Update item in Item_Catalog

@router.put("/api/v1_0/updatecatalog/{catalog_id}", status_code=status.HTTP_200_OK)
async def update_catalog(
    catalog_id: int,
    catalogset: Item_CatalogUpdate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    catalog_in_db = await Item_Catalog.get_or_none(catalog_id=catalog_id)
    if not catalog_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Catalog not found with this id.',
        )

    catalog_in_db.category_description = catalogset.category_description if catalogset.category_description != "" else catalog_in_db.category_description
    catalog_in_db.sub_category_description = catalogset.sub_category_description if catalogset.sub_category_description != "" else catalog_in_db.sub_category_description
    catalog_in_db.category_id = catalogset.category_id if catalogset.category_id != "" else catalog_in_db.category_id
    catalog_in_db.sub_category_id = catalogset.sub_category_id if catalogset.sub_category_id != "" else catalog_in_db.sub_category_id
    
    
    await catalog_in_db.save()

    return {'status': statusStr, 'data': catalog_in_db}



# Delete item from Item_Catalog

@router.delete("/api/v1_0/deletecatalog/{catalog_id}", status_code=status.HTTP_200_OK)
async def delete_catalog(
    catalog_id: int,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    catalog_in_db = await Item_Catalog.get_or_none(catalog_id=catalog_id)
    if not catalog_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Catalog not found with this id.',
        )

    await catalog_in_db.catalog_status = False

    await catalog_in_db.save()

    return {'status': statusStr, 'data': catalog_in_db}

