from fastapi import APIRouter , Depends
from fastapi import FastAPI, HTTPException, status, Request, Response, Header, Query
from db.models.orders import Orders_Pydantic, OrdersIn_Pydantic, Orders, OrderCreate, OrderUpdate
from db.models.services import Services
from db.models.plans import Plans
from datetime import datetime, time
from common.utils import execute_native_query
from typing import List





router = APIRouter()


# book a slot 


@router.post('/api/v1_0/placeorder', status_code=status.HTTP_201_CREATED)
async def create_order(orderset: OrderCreate,
                      request: Request, response: Response,
                      request_user_id: str = Header(None),
                      ):
    statusStr: str = 'Success'

    print("************* : " + str(request_user_id) )
    print(orderset.__dict__)

    
    # Parse strings to date and time objects
    order_date = datetime.strptime(orderset.date, '%Y-%m-%d').date()
    start_time = datetime.strptime(orderset.start_time, '%H:%M:%S').time()
    end_time = datetime.strptime(orderset.end_time, '%H:%M:%S').time()

    # Combine date with start_time and end_time
    order_start_time = datetime.combine(order_date, start_time)
    order_end_time = datetime.combine(order_date, end_time)
    
    #print(order_start_time, order_end_time)
    
    order_in_db = await Orders.filter( user_id=request_user_id,
            consultant_id=orderset.consultant_id,
            start_time__lt=order_end_time,
            end_time__gt=order_start_time,
            session_status="Scheduled").first()


    #print("order in Db:==== orders.py:: ",order_in_db)

    if order_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='There is already another Schedule withing the time frame .',
        )

    service = await Services.filter(service_id=orderset.service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Service not found with this service_id.',
        )

    plan = await Plans.filter(service_id=service.service_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Plan not found with this service_id.',
        )
    order_obj = Orders()
    order_obj.consultant_id = orderset.consultant_id
    order_obj.con_category = orderset.con_category
    order_obj.user_id= int(request_user_id)
    order_obj.start_time = order_start_time
    order_obj.end_time = order_end_time
    order_obj.session_status= "Scheduled"
    order_obj.service = service
    order_obj.plan = plan

    await order_obj.save()

    print(order_obj.__dict__)

    return {'status': statusStr, 'data': order_obj}




# Endpoint to get all orders
@router.get('/api/v1_0/admin/orders', response_model=List[Orders_Pydantic], status_code=status.HTTP_200_OK)
async def get_orders(
    request: Request,
    response: Response,
    limit: int = Query(10, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    orders = await Orders.all().offset(offset).limit(limit)
    return orders


# Endpoint to get orders for a consultant

@router.get('/api/v1_0/orders_for_consultant', status_code=status.HTTP_200_OK)
async def get_consultant_orders(
    request: Request,
    response: Response,
    request_consultant_id: str = Header(None),
    limit: int = Query(10, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    
    
    # Get user name
    query = "SELECT orders.* ,users.user_name FROM orders, users WHERE orders.user_id=users.user_id LIMIT %s OFFSET %s"
    params = (limit , offset)
    orders= await execute_native_query(query, params)
    
    

    return {'status': 'Success', 'data': orders}



# Endpoint to get orders for a user
@router.get('/api/v1_0/orders_for_user', status_code=status.HTTP_200_OK)
async def get_user_orders(
    request: Request,
    response: Response,
    request_user_id: str = Header(None),
    limit: int = Query(10, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    
    # Get user name
    query = "SELECT orders.* ,consultant.name FROM orders, consultant WHERE orders.consultant_id=consultant.con_id LIMIT %s OFFSET %s"
    params = (limit , offset)
    orders= await execute_native_query(query, params)
    

    return {'status': 'Success', 'data': orders}




# update order time   
@router.put("/api/v1_0/ordertime/{order_id}", status_code=status.HTTP_200_OK)
async def update_ordertime(order_id: int, orderset: OrderUpdate,request: Request, response: Response,
                      request_user_id: str = Header(None)):
    statusStr: str = 'Success'
    
    
    
    order_start_time = datetime.strptime(orderset.start_time, '%Y-%m-%dT%H:%M:%S')
    order_end_time = datetime.strptime(orderset.end_time, '%Y-%m-%dT%H:%M:%S')
    
     # Fetch schedule from database
     
    order_in_db  = await Orders.get_or_none(order_id=order_id, user_id = request_user_id)
    print("++++++++++")
    print(order_in_db.__dict__)
    if not order_in_db :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='order not found with this id.',
        )
        
    #filter  if needed 
# order_startTime__lt=order_end_time,
# order_endTime__gt=order_start_time,

    orders= Orders()
    
    order_in_db.start_time = order_start_time if orderset.start_time != "" else  order_in_db.start_time
    order_in_db.end_ime = order_end_time if orderset.end_time != "" else  order_in_db.end_time
    order_in_db.session_status = "Scheduled"


    
    await order_in_db.save()

    return {'status': 'Success', 'data': order_in_db}


# Update Order status when Finished 

@router.delete("/api/v1_0/orderend/{order_id}", status_code=status.HTTP_200_OK)
async def update_ordertime(order_id: int, request: Request, response: Response,
                      request_user_id: str = Header(None)):
    statusStr: str = 'Success'
    

    # Fetch order from database
     
    order_in_db  = await Orders.get_or_none(order_id=order_id,user_id = request_user_id)
    print("++++++++++")
    print(order_in_db .__dict__)
    if not order_in_db :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='order not found with this id.',
        )
        
    order_in_db.session_status = "Completed"


    await order_in_db.save()

    return {'status': 'Success', 'data': order_in_db}



# Update Order Status when cancelled 

@router.delete("/api/v1_0/ordercancel/{order_id}", status_code=status.HTTP_200_OK)
async def update_ordertime(order_id: int, request: Request, response: Response,
                      request_user_id: str = Header(None)):
    statusStr: str = 'Success'
    

    # Fetch order from database
     
    order_in_db  = await Orders.get_or_none(order_id=order_id,user_id = request_user_id)
    print("++++++++++")
    print(order_in_db .__dict__)
    if not order_in_db :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='order not found with this id.',
        )
        
    order_in_db.session_status = "Cancelled"


    await order_in_db.save()

    return {'status': 'Success', 'data': order_in_db}
