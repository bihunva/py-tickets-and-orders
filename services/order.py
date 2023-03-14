from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


@transaction.atomic
def create_order(tickets: list, username: str, date: str = None) -> Order:
    order = Order.objects.create(
        user=get_user_model().objects.get(username=username)
    )
    if date:
        order.created_at = date
    order.save()

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            row=ticket["row"],
            seat=ticket["seat"],
            order=order
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all().order_by("-id")

    if username:
        orders = orders.filter(user__username=username)

    return orders