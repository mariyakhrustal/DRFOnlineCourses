import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Create Stripe Product."""
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(product_id, amount):
    """Create Stripe Price."""
    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product=product_id,
    )
    return price


def create_stripe_session(price_id):
    """Create Stripe Session."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        cancel_url="http://127.0.0.1:8000/",
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session
