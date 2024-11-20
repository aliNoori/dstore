# serializers.py
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from files.models.file import File
from users.models import CustomUser  # مدل کاربر شما
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import  Group

from users.models.coupon import Coupon
from users.models.score import Score
from users.models.wallet import Wallet
from carts.models.cart import Cart

class CreateUpdateUserFormSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirmation = serializers.CharField(write_only=True, required=True)  # برای تایید رمز عبور

    #add image feild to serializers
    image = serializers.ImageField(required=False)  # اضافه کردن فیلد آواتار


    class Meta:
        model = CustomUser
        fields = ['username','name', 'email', 'password', 'password_confirmation','image']  # فیلدهایی که نیاز دارید

    # متد برای بررسی اینکه دو رمز عبور با هم مطابقت دارند
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')

        # بررسی اینکه اگر رمز عبور و تایید رمز عبور ارائه شده باشند، با یکدیگر مطابقت داشته باشند
        if password and password_confirmation:
            if password != password_confirmation:
                raise serializers.ValidationError({"password": "Passwords do not match."})

        return attrs

    # متد ایجاد کاربر جدید
    def create(self, validated_data):
        validated_data.pop('password_confirmation')  # حذف فیلد تایید رمز عبور
        user = CustomUser.objects.create(
            username=validated_data['username'],
            name=validated_data['name'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])  # رمز عبور را هش کنید



        image = validated_data['image']
        if image:
            File.objects.create(user=user, file=image)  


        user.save()  

        # اضافه کردن کاربر به گروه‌ها اگر نیاز باشد
        groups = self.initial_data.get('groups')
        if groups:
            user.groups.set(Group.objects.filter(name__in=groups))
              
        return user
    # متد به‌روزرسانی کاربر
    def update(self, instance, validated_data):
        validated_data.pop('password_confirmation', None)

        # به‌روزرسانی فیلدها
        instance.username = validated_data.get('username', instance.username)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)

        # به‌روزرسانی رمز عبور در صورتی که وجود داشته باشد
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        image = validated_data['image']
        if image:
            # حذف تصویر قبلی اگر وجود داشته باشد
            old_file = File.objects.filter(user=instance).first()
            if old_file:
                old_file.delete()  # حذف تصویر قبلی

            # ذخیره تصویر جدید
            File.objects.create(user=instance, file=image)    

        instance.save()

        # به‌روزرسانی گروه‌ها در صورت وجود
        groups = self.initial_data.get('groups')
        if groups:
            instance.groups.set(Group.objects.filter(name__in=groups))

        return instance
