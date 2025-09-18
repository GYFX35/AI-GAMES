import stripe
import os
from fastapi import APIRouter, Request
from pydantic import BaseModel

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

router = APIRouter()

@router.on_event("startup")
async def startup_event():
    if not stripe.api_key:
        raise Exception("STRIPE_SECRET_KEY environment variable not set")

class Product(BaseModel):
    name: str
    price: int # in cents
    quantity: int

class Sponsorship(BaseModel):
    amount: int # in cents

@router.post("/create-checkout-session")
async def create_checkout_session(product: Product):
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.name,
                    },
                    'unit_amount': product.price,
                },
                'quantity': product.quantity,
            }],
            mode='payment',
            automatic_payment_methods={
                'enabled': True,
            },
            success_url='http://localhost/success.html',
            cancel_url='http://localhost/cancel.html',
        )
        return {"id": session.id}
    except Exception as e:
        return {"error": str(e)}

@router.post("/create-sponsorship-checkout-session")
async def create_sponsorship_checkout_session(sponsorship: Sponsorship):
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'ngn',
                    'product_data': {
                        'name': 'Sponsorship',
                    },
                    'unit_amount': sponsorship.amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            automatic_payment_methods={
                'enabled': True,
            },
            success_url='http://localhost/success.html',
            cancel_url='http://localhost/cancel.html',
        )
        return {"id": session.id}
    except Exception as e:
        return {"error": str(e)}
