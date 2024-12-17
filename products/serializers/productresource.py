from rest_framework import serializers

from products.models.like import Like
from products.models.product import Product
from products.serializers.category import CategoryResource
from products.serializers.historiyresource import HistoryResource
from products.serializers.reviewresource import ReviewResource
from users.serializers.userresource import CustomImageField


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        if value:
            # Assuming the File model stores the image's file path in `file` field
            return {"path": value.file.url}  # Adjust this based on your file URL/path logic
        return None

class ProductResource(serializers.ModelSerializer):


    category = CategoryResource()  # اینجا می‌تواند PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False) هم باشد
    views=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    histories=HistoryResource(many=True)
    reviews=ReviewResource(many=True)
    #isLiked = serializers.SerializerMethodField()  # فیلد جدید برای نشان دادن وضعیت لایک

    image = CustomImageField(source='file.first')  # Assuming a user has a related file through `file_set`
   
    class Meta:
        model = Product
        fields = ['id','sku','name', 'price','discount', 'stock', 'description','views','likes','reviews','histories','image','category']

    def get_image(self, obj):
              
        return obj.image  
     
    def get_views(self, obj):
        # تعداد ویوها مربوط به این محصول را محاسبه کنید
        return obj.views.count() 
    
    def get_likes(self, obj):
        # تعداد لایک مربوط به این محصول را محاسبه کنید
        return obj.likes.count() 

