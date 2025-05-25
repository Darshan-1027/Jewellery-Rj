from django.contrib import admin
from .models import CategorysModel, ProductModel, RegisterDataModel,Order, OrderItem

# ✅ Admin for CategorysModel
@admin.register(CategorysModel)
class ShowCategory(admin.ModelAdmin):
    list_display = ["Name", "cat_photos"]
    search_fields = ["Name"]

# ✅ Admin for ProductModel
@admin.register(ProductModel)
class ShowProducts(admin.ModelAdmin):
    list_display = [
        "id", "Category", "Name", "Price", "First", "Second",
        "Material", "Length", "Waight", "Type_Of_work",
        "Availability", "Timestamp"
    ]
    search_fields = ["Name", "Material"]
    list_filter = ["Availability", "Category"]

# ✅ Admin for RegisterDataModel
@admin.register(RegisterDataModel)
class ShowRegister(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "phone", "address"]  # 🔐 Removed password
    search_fields = ["first_name", "email"]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'phone_number', 'state', 'city', 'pincode']
    inlines = [OrderItemInline]  # This shows OrderItems inline inside Order

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']