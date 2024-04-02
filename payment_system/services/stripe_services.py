import os
from dotenv import load_dotenv
import stripe


load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_payment_session(borrowing):
    from payment_system.models import Payment
    total_amount = borrowing.calculate_borrowing_amount()

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(total_amount * 100),
                "product_data": {
                    "name": f"Borrowing: {borrowing.id}",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    payment = Payment.objects.create(
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=total_amount,
    )

    return payment
