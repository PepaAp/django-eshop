from django.contrib import admin

from .models import (
	Category,
	Inventory,
	Order,
	OrderItem,
	Product,
	ShopUser,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id_category", "name", "parent")
	list_filter = ("parent",)
	search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("id_product", "name", "category", "price")
	list_filter = ("category",)
	search_fields = ("name",)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
	list_display = ("id_inventory", "product", "quantity")
	list_filter = ("product",)


@admin.register(ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
	list_display = ("id_user", "surname", "lastname", "email")
	search_fields = ("surname", "lastname", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("id_order", "user", "status", "date", "total_price")
	list_filter = ("status", "payment_method")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ("id_order_item", "order", "product", "quantity", "price")
