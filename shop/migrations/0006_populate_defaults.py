from decimal import Decimal
from django.db import migrations
import django.utils.timezone as timezone


def forwards(apps, schema_editor):
    Product = apps.get_model("shop", "Product")
    Inventory = apps.get_model("shop", "Inventory")
    Order = apps.get_model("shop", "Order")
    OrderItem = apps.get_model("shop", "OrderItem")

    now = timezone.now()

    # timestamps
    for model in (Product, Inventory, Order, OrderItem, apps.get_model("shop", "Category"), apps.get_model("shop", "ShopUser")):
        qs = model.objects.filter(created_at__isnull=True)
        if qs.exists():
            qs.update(created_at=now, updated_at=now)

    # product prices
    for p in Product.objects.filter(price__isnull=True):
        p.price = Decimal("0.00")
        p.save(update_fields=["price"])

    # inventory quantities
    for inv in Inventory.objects.filter(quantity__isnull=True):
        inv.quantity = 0
        inv.save(update_fields=["quantity"])

    # order items: set price from product when missing
    for oi in OrderItem.objects.filter(price__isnull=True):
        try:
            prod_price = oi.product.price if oi.product_id else Decimal("0.00")
        except Exception:
            prod_price = Decimal("0.00")
        oi.price = prod_price or Decimal("0.00")
        oi.save(update_fields=["price"])

    # order totals: recalculate from items
    for order in Order.objects.all():
        total = Decimal("0.00")
        for item in order.items.all():
            if item.price is None or item.quantity is None:
                continue
            total += item.price * item.quantity
        order.total_price = total
        order.save(update_fields=["total_price"])

    # order status default
    Order.objects.filter(status__isnull=True).update(status="created")


def reverse(apps, schema_editor):
    # no-op reverse: keep data
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0005_schema_changes"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse),
    ]
