from rest_framework import serializers
from files.models.file import File
from products.models.history import History
from products.models.product import Product
from products.models.category import Category
from products.serializers.category import CategoryResource  # فرض می‌کنیم CategorySerializer از قبل تعریف شده

class CreateUpdateProductFormSerializer(serializers.ModelSerializer):

    #category = CategoryResource()  # اینجا می‌تواند PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False) هم باشد
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', required=True)
    # اضافه کردن فیلد تصویر به سریالایزر
    image = serializers.ImageField(required=False)  # فیلد تصویر اختیاری

    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'price', 'stock', 'discount', 'description', 'image', 'category_id']

    # متد ایجاد محصول جدید
    def create(self, validated_data):
        #category_data = validated_data.pop('category', None)
        #category_id = self.initial_data.get('category_id')
        #category = Category.objects.get(id=category_id)
        category = validated_data['category']
        product = Product.objects.create(
            name=validated_data['name'],
            price=validated_data['price'],
            stock=validated_data['stock'],
            discount=validated_data['discount'],
            description=validated_data.get('description', ''),
            sku=validated_data.get('sku', ''),
            category=category,
        )

        # اگر تصویر وجود داشته باشد
        image = validated_data.get('image', None)
        if image:
            File.objects.create(product=product, file=image) 

        # اگر دسته‌بندی وجود داشته باشد
        #if category_data:
         #   category = Category.objects.get(id=category_data['id'])
          #  product.category = category

        product.save()
        return product

    # متد به‌روزرسانی محصول
    def update(self, instance, validated_data):
        # ذخیره قیمت قبلی محصول برای بررسی تغییرات
        old_price = instance.price

        # به‌روزرسانی فیلدها
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.description = validated_data.get('description', instance.description)
        instance.sku = validated_data.get('sku', instance.sku)

        # مدیریت تصویر
        image = validated_data.get('image', None)
        if image:
            # حذف تصویر قبلی اگر وجود داشته باشد
            old_file = File.objects.filter(product=instance).first()
            if old_file:
                old_file.delete()

            # ذخیره تصویر جدید
            File.objects.create(product=instance, file=image)

        # مدیریت دسته‌بندی
        category = validated_data['category']
        if category:
            instance.category = category

        instance.save()

        # اگر قیمت تغییر کرده باشد، ایجاد تاریخچه جدید
        if old_price != instance.price:
            History.objects.create(
                product=instance,
                price_history=old_price  # ذخیره قیمت قبلی به‌عنوان تاریخچه
            )

        return instance
