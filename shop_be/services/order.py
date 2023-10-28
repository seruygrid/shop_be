from decimal import Decimal
from collections import defaultdict
from typing import Sequence

from sqlalchemy.orm import selectinload

from db_models.db_models import Order, ChildOrder, Product, Address
from shop_be.conf.constants import ErrorMessages
from shop_be.exceptions import DoesNotExistException
from shop_be.schemas.order.order import CreateOrderRequest
from shop_be.schemas.shop.shop import AddressSchema
from shop_be.services.base import BaseService


class OrderService(BaseService[Order]):
    MODEL = Order

    async def get_by_tracking_id(self, tracking_id: str) -> 'Order':
        options = (
            selectinload(self.MODEL.shipping_address),
            selectinload(self.MODEL.billing_address),
            selectinload(self.MODEL.customer),
            selectinload(self.MODEL.products).selectinload(Product.image),
            selectinload(self.MODEL.products).selectinload(Product.rating_count),
            selectinload(self.MODEL.products).selectinload(Product.my_review),
            selectinload(self.MODEL.children).selectinload(ChildOrder.products).selectinload(Product.image),
            selectinload(self.MODEL.children).selectinload(ChildOrder.products).selectinload(Product.rating_count),
            selectinload(self.MODEL.children).selectinload(ChildOrder.products).selectinload(Product.my_review),
        )
        if obj := await self.fetch_one(filters=(self.MODEL.tracking_number == tracking_id,), options=options):
            return obj

        raise DoesNotExistException(ErrorMessages.ORDER_DOES_NOT_EXIST)

    async def create_child_orders(
            self,
            order: 'Order',
            data: CreateOrderRequest,
            products: Sequence['Product'],
            products_count: dict[int, int],
    ) -> list['ChildOrder']:
        child_orders = []
        shops = defaultdict(list)
        for product in products:
            shops[product.shop_id].append(product)

        for shop, products in shops.items():
            order_sum = sum(product.price * products_count[product.id] for product in products)
            child_order = ChildOrder(
                customer_contact=data.customer_contact,
                amount=order_sum,
                sales_tax=Decimal(),
                paid_total=Decimal(),
                total=order_sum,
                language=data.language,
                payment_gateway=data.payment_gateway,
                delivery_time=data.delivery_time,
                order_status='order-pending',
                payment_status='payment-pending',
                shop_id=shop,
                parent_id=order.id,
            )
            for product in products:
                child_order.products.append(product)
            obj = await self.insert_obj(child_order, commit=False)
            child_orders.append(obj)

        return child_orders

    async def create(self, data: CreateOrderRequest, products: Sequence['Product']) -> Order:
        products_count = {i.product_id: i.order_quantity for i in data.products}
        order_sum = sum(product.price * products_count[product.id] for product in products)
        address = await self.create_address(data.shipping_address)
        order = self.MODEL(
            customer_contact=data.customer_contact,
            amount=order_sum,
            sales_tax=Decimal(),
            paid_total=Decimal(),
            total=order_sum,
            language=data.language,
            payment_gateway=data.payment_gateway,
            delivery_time=data.delivery_time,
            order_status='order-pending',
            payment_status='payment-pending',
            shipping_address_id=address.id,
            billing_address_id=address.id,
        )
        await self.create_child_orders(order, data, products, products_count)
        obj = await self.insert_obj(order)
        return await self.get_by_tracking_id(obj.tracking_number)

    async def create_address(self, address: AddressSchema) -> 'Address':
        address = Address(**address.model_dump())
        return await self.insert_obj(address, commit=False)
