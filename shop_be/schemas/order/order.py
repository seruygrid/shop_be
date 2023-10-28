from pydantic import BaseModel

from shop_be.schemas.shop.product import ProductSchema
from shop_be.schemas.shop.shop import AddressSchema


class ProductItem(BaseModel):
    product_id: int
    order_quantity: int
    unit_price: float
    subtotal: float


class OrderVerifyRequest(BaseModel):
    amount: float
    products: list[ProductItem]
    billing_address: AddressSchema | None
    shipping_address: AddressSchema | None


class OrderVerifyResponse(BaseModel):
    total_tax: float = 0
    shipping_charge: float = 0
    unavailable_products: list[dict] = []
    wallet_currency: float = 0
    wallet_amount: float = 0


class InvoiceTranslatedText(BaseModel):
    subtotal: str
    discount: str
    tax: str
    delivery_fee: str
    total: str
    products: str
    quantity: str
    invoice_no: str
    date: str


class CreateOrderRequest(BaseModel):
    products: list[ProductItem]
    amount: float
    coupon_id: int | None
    discount: float
    paid_total: float
    sales_tax: float
    delivery_fee: float
    total: float
    delivery_time: str
    customer_contact: str
    customer_name: str
    note: str
    payment_gateway: str
    payment_sub_gateway: str
    use_wallet_points: bool
    isFullWalletPayment: bool
    billing_address: AddressSchema | None = None
    shipping_address: AddressSchema
    language: str
    invoice_translated_text: InvoiceTranslatedText


class CustomerInfo(BaseModel):
    id: int
    name: str
    email: str
    email_verified_at: str | None
    created_at: str
    updated_at: str
    is_active: int
    shop_id: int | None


class OrderInfo(BaseModel):
    id: int
    tracking_number: str
    customer_id: int
    customer_contact: str
    amount: float
    sales_tax: float
    paid_total: float
    total: float
    cancelled_amount: str
    language: str
    coupon_id: int | None
    parent_id: int | None
    shop_id: int | None
    discount: float = 0
    payment_gateway: str
    shipping_address: AddressSchema
    billing_address: AddressSchema | None
    logistics_provider: str | None
    delivery_fee: float
    delivery_time: str
    order_status: str
    payment_status: str
    created_at: str
    payment_intent: str | None
    customer: CustomerInfo | None
    products: list[ProductSchema]
    children: list['OrderInfo']
    wallet_point: float | None
