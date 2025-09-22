import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(product_title):
    """Создает продукт (курс) в stripe"""
    stripe_product = stripe.Product.create(name=product_title)
    return stripe_product.get("id")


def create_stripe_price(amount, product_id):
    """Создает цену в stripe"""
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product=product_id,
    )
    return stripe_price.id


def create_stripe_session(price):
    """Создает сессию на оплату в stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/fail/",
        line_items=[
            {
                "price": price,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return session["id"], session["url"]
