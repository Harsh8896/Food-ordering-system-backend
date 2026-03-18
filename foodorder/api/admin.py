from django.contrib import admin
from .models import (
    User, Category, Food, Order, 
    OrderAddress, FoodTracking, PaymentDetail, Review, Wishlist
)

# 1. Food Tracking: Yahan Cancel karne wale ka naam dikhega
@admin.register(FoodTracking)
class FoodTrackingAdmin(admin.ModelAdmin):
    list_display = ('get_order_no', 'get_user_name', 'status', 'order_cancelled_by_user', 'status_date')
    list_filter = ('order_cancelled_by_user', 'status', 'status_date')
    search_fields = ('order__order_number', 'order__user__first_name', 'order__user__last_name')

    def get_order_no(self, obj):
        return obj.order.order_number if obj.order else "N/A"
    get_order_no.short_description = 'Order Number'

    def get_user_name(self, obj):
        # Tracking -> Order -> User ka connection
        if obj.order and obj.order.user:
            return f"{obj.order.user.first_name} {obj.order.user.last_name}"
        return "Unknown User"
    get_user_name.short_description = 'Customer Name'

# 2. Order Address: Isse aap "Confirmed Orders" filter kar sakte hain
@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'get_customer', 'order_final_status', 'order_time')
    list_filter = ('order_final_status', 'order_time')
    search_fields = ('order_number', 'user__first_name', 'address')

    def get_customer(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_customer.short_description = 'Customer'

# 3. User Admin: Registration details ke saath
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'mobile', 'reg_date')
    search_fields = ('email', 'first_name', 'mobile')

# 4. Food Admin: Stock aur Price management
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category', 'item_price', 'is_available', 'item_quantity')
    list_filter = ('category', 'is_available')
    search_fields = ('item_name',)

# 5. Order Admin: Raw items in cart
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'food', 'quantity', 'is_order_placed')
    list_filter = ('is_order_placed',)

# 6. Reviews: Star ratings track karne ke liye
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('food', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

# 7. Payment Details: Transactions dekhne ke liye
@admin.register(PaymentDetail)
class PaymentDetailAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'payment_mode', 'payment_date')
    list_filter = ('payment_mode',)

# Baki simple models
admin.site.register(Category)
admin.site.register(Wishlist)


    