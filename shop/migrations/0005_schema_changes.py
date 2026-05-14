from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0004_order_email_order_full_name_order_phone_and_more"),
    ]

    operations = [
        # timestamps (nullable for now)
        migrations.AddField(
            model_name="category",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="inventory",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="inventory",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="shopuser",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="shopuser",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="created_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="updated_at",
            field=models.DateTimeField(null=True),
        ),

        # make numeric fields accept null for now so we can populate safely
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(max_digits=10, decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="quantity",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(max_digits=10, decimal_places=2, null=True),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(max_digits=10, decimal_places=2, null=True),
        ),

        # add indexes (safe)
        migrations.AddIndex(
            model_name="order",
            index=models.Index(fields=["date"], name="shop_order_date_idx"),
        ),
        migrations.AddIndex(
            model_name="order",
            index=models.Index(fields=["status"], name="shop_order_status_idx"),
        ),
        migrations.AddIndex(
            model_name="order",
            index=models.Index(fields=["payment_method"], name="shop_order_payment_idx"),
        ),
    ]
