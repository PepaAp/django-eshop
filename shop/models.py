from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import transaction
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

	def full_path(self) -> str:
		parts = []
		current = self
		seen = set()
		while current and current.pk and current.pk not in seen:
			seen.add(current.pk)
			parts.append(current.name or "(unnamed category)")
			current = current.parent
		return " / ".join(reversed(parts))

	def __str__(self) -> str:
		return self.full_path()


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
	quantity = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])

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
	shipping_address = models.CharField(max_length=100, blank=True, null=True)
	full_name = models.CharField(max_length=60, blank=True, null=True)
	email = models.EmailField(max_length=30, blank=True, null=True)
	phone = models.CharField(max_length=15, blank=True, null=True)
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

	def save(self, *args, **kwargs):
		if self._state.adding and self.user_id:
			if not self.address:
				self.address = self.user.address
			if not self.shipping_address:
				self.shipping_address = self.user.address
			if not self.phone:
				self.phone = self.user.phone
			if not self.email:
				self.email = self.user.email
			if not self.full_name:
				full_name = " ".join(
					part for part in [self.user.surname, self.user.lastname] if part
				)
				self.full_name = full_name
		super().save(*args, **kwargs)

	def recalculate_total(self) -> None:
		total = Decimal("0.00")
		for item in self.items.all():
			if item.price is None or item.quantity is None:
				continue
			total += item.price * item.quantity
		self.total_price = total
		self.save(update_fields=["total_price"])

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
	quantity = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		db_table = "order_item"

	@staticmethod
	def _apply_inventory_delta(product_id: int, delta: int) -> None:
		if not product_id or delta == 0:
			return
		inventory, _ = Inventory.objects.select_for_update().get_or_create(
			product_id=product_id,
			defaults={"quantity": 0},
		)
		current = inventory.quantity or 0
		new_value = current - delta
		if new_value < 0:
			raise ValidationError("Not enough inventory for this product.")
		inventory.quantity = new_value
		inventory.save(update_fields=["quantity"])

	def save(self, *args, **kwargs):
		if self.price is None and self.product_id:
			self.price = self.product.price

		with transaction.atomic():
			prev_quantity = 0
			prev_product_id = None
			if self.pk:
				previous = OrderItem.objects.select_for_update().get(pk=self.pk)
				prev_quantity = previous.quantity or 0
				prev_product_id = previous.product_id

			new_quantity = self.quantity or 0
			new_product_id = self.product_id

			if prev_product_id and prev_product_id != new_product_id:
				self._apply_inventory_delta(prev_product_id, -prev_quantity)
				prev_quantity = 0

			delta = new_quantity - prev_quantity
			self._apply_inventory_delta(new_product_id, delta)
			super().save(*args, **kwargs)

		if self.order_id:
			self.order.recalculate_total()

	def delete(self, *args, **kwargs):
		product_id = self.product_id
		quantity = self.quantity or 0
		order = self.order if self.order_id else None

		with transaction.atomic():
			self._apply_inventory_delta(product_id, -quantity)
			super().delete(*args, **kwargs)

		if order:
			order.recalculate_total()

	def __str__(self) -> str:
		return f"{self.product} x {self.quantity}"
