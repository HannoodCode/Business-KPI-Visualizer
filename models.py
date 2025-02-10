from pydantic import BaseModel
from datetime import date

class Order(BaseModel):
    order_id: str
    date: date
    status: str
    fulfilment: str
    sales_channel: str
    ship_service_level: str
    style: str
    sku: str
    category: str
    size: str
    asin: str
    courier_status: str
    qty: int
    currency: str
    amount: float
    ship_city: str
    ship_state: str
    ship_postal_code: str
    ship_country: str
    promotion_ids: str
    b2b: bool
    fulfilled_by: str
