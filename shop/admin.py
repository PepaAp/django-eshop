from django.contrib import admin

from .models import (
	Category,
	Inventory,
	Order,
	OrderItem,
	Product,
	ShopUser,
)


class CategoryTreeFilter(admin.SimpleListFilter):
	title = "category"
	parameter_name = "category"

	def lookups(self, request, model_admin):
		categories = Category.objects.select_related("parent").order_by("name")
		return [(category.pk, category.full_path()) for category in categories]

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(category_id=self.value())
		return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id_category", "full_path", "parent")
	list_filter = ("parent",)
	search_fields = ("name",)

	@admin.display(description="category")
	def full_path(self, obj: Category) -> str:
		return obj.full_path()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("id_product", "name", "category", "price")
	list_filter = (CategoryTreeFilter,)
	search_fields = ("name",)
	autocomplete_fields = ("category",)


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
