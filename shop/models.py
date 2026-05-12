from django.db import models


class Category(models.Model):
	id_category = models.AutoField(primary_key=True, db_column="id_category")
	parent = models.ForeignKey(
		"self",
		on_delete=models.PROTECT,
		related_name="children",
		blank=True,
		null=True,
		db_column="parent_id",
	)
	name = models.CharField(max_length=20, blank=True, null=True)

	class Meta:
		db_table = "category"
		verbose_name_plural = "Categories"

	def __str__(self) -> str:
		return self.name or "(unnamed category)"


class Product(models.Model):
	id_product = models.AutoField(primary_key=True, db_column="id_product")
	category = models.ForeignKey(
		Category,
		on_delete=models.PROTECT,
		related_name="products",
		db_column="category_id",
	)
	name = models.CharField(max_length=50, blank=True, null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	image = models.ImageField(upload_to="products/", blank=True, null=True)

	class Meta:
		db_table = "product"

	def __str__(self) -> str:
		return self.name or "(unnamed product)"


class Inventory(models.Model):
	id_inventory = models.AutoField(primary_key=True, db_column="id_inventory")
	product = models.ForeignKey(
		Product,
		on_delete=models.PROTECT,
		related_name="inventory_items",
		db_column="product_id",
	)
	quantity = models.IntegerField(blank=True, null=True)

	class Meta:
		db_table = "inventory"
		verbose_name_plural = "Inventory"

	def __str__(self) -> str:
		return f"{self.product} ({self.quantity})"


class ShopUser(models.Model):
	id_user = models.AutoField(primary_key=True, db_column="id_user")
	surname = models.CharField(max_length=25, blank=True, null=True)
	lastname = models.CharField(max_length=25, blank=True, null=True)
	email = models.EmailField(max_length=30, unique=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=15, blank=True, null=True)
	photo = models.ImageField(upload_to="users/", blank=True, null=True)

	class Meta:
		db_table = "shop_user"
		verbose_name = "user"
		verbose_name_plural = "users"

	def __str__(self) -> str:
		full_name = " ".join(part for part in [self.surname, self.lastname] if part)
		return full_name or self.email


class Order(models.Model):
	class PaymentMethod(models.TextChoices):
		CARD = "card", "card"
		CASH = "cash", "cash"
		PAYPAL = "paypal", "paypal"
		KLARNA = "klarna", "klarna"

	class Status(models.TextChoices):
		CREATED = "created", "created"
		PAYED = "payed", "payed"
		PACKAGING = "packaging", "packaging"
		SHIPPED = "shipped", "shipped"
		IN_TRANSIT = "in_transit", "in_transit"
		DELIVERY = "delivery", "delivery"
		DELIVERED = "delivered", "delivered"

	id_order = models.AutoField(primary_key=True, db_column="id_order")
	user = models.ForeignKey(
		ShopUser,
		on_delete=models.PROTECT,
		related_name="orders",
		db_column="user_id",
	)
	date = models.DateTimeField(blank=True, null=True)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	payment_method = models.CharField(
		max_length=10,
		choices=PaymentMethod.choices,
		blank=True,
		null=True,
	)
	status = models.CharField(
		max_length=20,
		choices=Status.choices,
		blank=True,
		null=True,
	)

	class Meta:
		db_table = "shop_order"

	def __str__(self) -> str:
		return f"Order #{self.id_order}"


class OrderItem(models.Model):
	id_order_item = models.AutoField(primary_key=True, db_column="id_order_item")
	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		related_name="items",
		db_column="order_id",
	)
	product = models.ForeignKey(
		Product,
		on_delete=models.PROTECT,
		related_name="order_items",
		db_column="product_id",
	)
	quantity = models.IntegerField(blank=True, null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		db_table = "order_item"

	def __str__(self) -> str:
		return f"{self.product} x {self.quantity}"
