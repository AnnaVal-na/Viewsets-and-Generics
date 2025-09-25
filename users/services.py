import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name, description):
    """Создание продукта в Stripe"""
    try:
        product = stripe.Product.create(name=name, description=description)
        return product.id
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e}")


def create_stripe_price(product_id, amount):
    """Создание цены в Stripe"""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),  # Переводим в копейки
            currency="rub",
        )
        return price.id
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e}")


def create_stripe_session(price_id, success_url, cancel_url):
    """Создание сессии оплаты"""
    try:
        session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session.url, session.id
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e}")


def get_stripe_session_status(session_id):
    """Получение статуса сессии"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {e}")
