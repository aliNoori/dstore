from files.models.file import File
from products.models.category import Category
from rest_framework import serializers


class CustomImageField(serializers.Field):
    def to_representation(self, value):
        if value:
            # Assuming the File model stores the image's file path in `file` field
            return {"path": value.file.url}  # Adjust this based on your file URL/path logic
        return None


class CategoryResource(serializers.ModelSerializer):


    image = CustomImageField(source='file')  # Assuming a user has a related file through `file_set`
    class Meta:
        model = Category
        fields = ['id', 'name','parent','image']

    def get_image(self, obj):
              
        return obj.image     


class CreateUpdateCategoryFormSerializer(serializers.ModelSerializer):

    # اضافه کردن فیلد تصویر به سریالایزر
    image = serializers.ImageField(required=False)  # فیلد تصویر اختیاری

    class Meta:
        model = Category
        fields = ['id','parent', 'name', 'image']

    # متد ایجاد محصول جدید
    def create(self, validated_data):
        
        category = Category.objects.create(
            name=validated_data['name'],
            parent=validated_data['parent'],
            
        )

        # اگر تصویر وجود داشته باشد
        image = validated_data.get('image', None)
        if image:
            File.objects.create(category=category, file=image)

        category.save()
        return category

    # متد به‌روزرسانی محصول
    def update(self, instance, validated_data):
       
        # به‌روزرسانی فیلدها
        instance.name = validated_data.get('name', instance.name)
        instance.parent = validated_data.get('parent', instance.parent)
        
        # مدیریت تصویر
        image = validated_data.get('image', None)
        if image:
            # حذف تصویر قبلی اگر وجود داشته باشد
            old_file = File.objects.filter(category=instance).first()
            if old_file:
                old_file.delete()

            # ذخیره تصویر جدید
            File.objects.create(category=instance, file=image)
       
        instance.save()

        return instance    