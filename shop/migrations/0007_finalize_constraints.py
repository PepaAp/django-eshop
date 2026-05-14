from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0006_populate_defaults"),
    ]

    operations = [
        # make fields non-nullable now that we populated data
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0),
        ),
        migrations.AlterField(
            model_name="inventory",
            name="quantity",
            field=models.IntegerField(null=False, default=0),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(null=False, default=0),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0),
        ),

        # make timestamps non-nullable
        migrations.AlterField(model_name="category", name="created_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="category", name="updated_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="product", name="created_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="product", name="updated_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="inventory", name="created_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="inventory", name="updated_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="shopuser", name="created_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="shopuser", name="updated_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="order", name="created_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="order", name="updated_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="orderitem", name="created_at", field=models.DateTimeField(null=False)),
        migrations.AlterField(model_name="orderitem", name="updated_at", field=models.DateTimeField(null=False)),

        # Constraints were causing import-time errors on this Django version.
        # They can be added later via a DB-specific migration or raw SQL if needed.
    ]
