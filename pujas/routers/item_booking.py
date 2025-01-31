from fastapi import APIRouter, HTTPException, status, Request, Response, Query
from db.models.item_booking import Item_Booking, Item_Booking_Pydantic, Item_BookingCreate, Item_BookingIn_Pydantic, Item_BookingUpdate
from datetime import datetime
from typing import List

router = APIRouter()

# Insert a new booking into Item_Booking
@router.post('/api/v1_0/createbooking', status_code=status.HTTP_201_CREATED)
async def create_booking(
    bookingset: Item_BookingCreate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    booking_in_db = await Item_Booking.filter(
        user_id=bookingset.user_id,
        vendor_id=bookingset.vendor_id,
        item_id=bookingset.item_id,
        booking_date=bookingset.booking_date
    ).first()

    if booking_in_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Booking already exists for this user, vendor, and item on the specified date.',
        )

    booking_obj = Item_Booking(
        user_id=bookingset.user_id,
        vendor_id=bookingset.vendor_id,
        item_id=bookingset.item_id,
        booking_date=bookingset.booking_date,
        fees=bookingset.fees
    )

    await booking_obj.save()

    return {'status': statusStr, 'data': booking_obj}

# Get all bookings from Item_Booking
@router.get('/api/v1_0/bookings', status_code=status.HTTP_200_OK)
async def get_bookings(
    request: Request,
    response: Response,
    limit: int = Query(100, description="Limit the number of results"),
    offset: int = Query(0, description="Offset the starting point of results")
):
    bookings = await Item_Booking.all().offset(offset).limit(limit)
    return bookings

# Update booking in Item_Booking
@router.put("/api/v1_0/updatebooking/{item_order_id}", status_code=status.HTTP_200_OK)
async def update_booking(
    item_order_id: int,
    bookingset: Item_BookingUpdate,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    booking_in_db = await Item_Booking.get_or_none(item_order_id=item_order_id)
    if not booking_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found with this order ID.',
        )

    booking_in_db.user_id = bookingset.user_id if bookingset.user_id != "" else booking_in_db.user_id
    booking_in_db.vendor_id = bookingset.vendor_id if bookingset.vendor_id != "" else booking_in_db.vendor_id
    booking_in_db.item_id = bookingset.item_id if bookingset.item_id != "" else booking_in_db.item_id
    booking_in_db.booking_date = bookingset.booking_date if bookingset.booking_date != "" else booking_in_db.booking_date
    booking_in_db.fees = bookingset.fees if bookingset.fees != "" else booking_in_db.fees
    

    await booking_in_db.save()

    return {'status': statusStr, 'data': booking_in_db}


# Delete booking from Item_Booking (soft delete)
@router.delete("/api/v1_0/deletebooking/{item_order_id}", status_code=status.HTTP_200_OK)
async def delete_booking(
    item_order_id: int,
    request: Request,
    response: Response
):
    statusStr: str = 'Success'

    booking_in_db = await Item_Booking.get_or_none(item_order_id=item_order_id)
    if not booking_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Booking not found with this order ID.',
        )

    booking_in_db.booking_status = False

    await booking_in_db.save()

    return {'status': statusStr, 'data': booking_in_db}
