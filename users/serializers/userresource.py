from rest_framework import serializers


from users.models.customuser import CustomUser


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        if value:
            # Assuming the File model stores the image's file path in `file` field
            return {"path": value.file.url}  # Adjust this based on your file URL/path logic
        return None
    

class UserResource(serializers.ModelSerializer):

    image = CustomImageField(source='file.first')  # Assuming a user has a related file through `file_set`
    orders_count = serializers.SerializerMethodField()
    items_cart = serializers.SerializerMethodField()  # تنظیم کنید اگر این فیلد رابطه معکوس نیست
    coupons_count=serializers.SerializerMethodField()
    wallet_balance = serializers.SerializerMethodField()  # تنظیم کنید اگر این فیلد رابطه معکوس نیست
    score = serializers.SerializerMethodField()  # اضافه کردن فیلد مجموع امتیازات
    roles = serializers.SerializerMethodField()  # افزودن گروه‌ها

   
    class Meta:
        model = CustomUser
        fields = ['id','name', 'username', 'email', 'is_active', 'date_joined','image',
                  'wallet_balance','coupons_count','items_cart','orders_count','score','roles']

    def get_image(self, obj):
        return obj.image if hasattr(obj, 'image') else None

    def get_orders_count(self, obj):
    # تعداد سفارشات مربوط به این کاربر را محاسبه کنید
        return obj.orders.count() if hasattr(obj, 'orders') else 0

    def get_coupons_count(self, obj):
    # تعداد سفارشات مربوط به این کاربر را محاسبه کنید
        return obj.coupons.count() if hasattr(obj, 'coupons') else 0

    def get_items_cart(self, obj):
    # تعداد آیتم‌های موجود در سبد خرید کاربر را محاسبه کنید
        return obj.cart.items.count() if hasattr(obj, 'cart') and hasattr(obj.cart, 'items') else 0

    def get_score(self, obj):
    # محاسبه امتیاز در صورتی که کاربر دارای userscores باشد
        return sum(score.score for score in obj.userscores.all()) if hasattr(obj, 'userscores') else 0

    def get_wallet_balance(self, obj):
    # بررسی و بازگشت موجودی کیف پول کاربر
        return obj.wallet.balance if hasattr(obj, 'wallet') else 0
    
    def get_roles(self, obj):
        # بازگرداندن لیست گروه‌های کاربر
        #return [{'id': group.id, 'name': group.name} for group in obj.groups.all()]
        return [{group.name} for group in obj.groups.all()]


