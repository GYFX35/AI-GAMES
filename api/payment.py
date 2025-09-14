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

@router.post("/create-checkout-session")
async def create_checkout_session(product: Product):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
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
            success_url='http://localhost/success.html',
            cancel_url='http://localhost/cancel.html',
        )
        return {"id": session.id}
    except Exception as e:
        return {"error": str(e)}
