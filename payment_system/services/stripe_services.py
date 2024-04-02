import os
from dotenv import load_dotenv
import stripe

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_test_payment_session():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "Test Book borrowing",
                },
                "unit_amount": 10000,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return session


print(create_test_payment_session())
