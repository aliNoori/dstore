# Create your views here.
# views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from files.models.file import File
from orders.models.order import Order
from products.models.category import Category
from products.models.like import Like
from products.models.product import Product
from products.models.reviews import Review
from products.models.view import View
from products.serializers.category import CategoryResource, CreateUpdateCategoryFormSerializer
from products.serializers.createupdate import CreateUpdateProductFormSerializer

from products.serializers.productresource import ProductResource
from products.serializers.reviewresource import ReviewResource
from users.decorators.checkpermission import PermissionMixin



class ProductCreateView(PermissionMixin, APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)
    required_permission = 'users.create'  # تعیین دسترسی مورد نیاز

    def post(self, request):
         # بررسی دسترسی‌ها
        permission_response = self.hasPermission(request)
        if permission_response:
            return permission_response
        
        serializer = CreateUpdateProductFormSerializer(data=request.data)
        if serializer.is_valid():

            product = serializer.save()  # ذخیره کاربر جدید
            # سریالایز کردن اطلاعات کاربر
            product_data = ProductResource(product).data
            # بازگرداندن داده‌های سریالایز شده
            return Response(product_data)
            # return Response({
            #     "user": RegisterUserFormSerializer(user).data,
            #     "refresh": str(refresh),
            #     "access": str(refresh.access_token),
            # }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductShowView(APIView):

    #permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request, id):
        # پیاده‌سازی برای نمایش یک کاربر خاص
        # فرض بر این است که شما یک مدل User دارید که اطلاعات کاربران را نگه می‌دارد
        try:
            product = Product.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است
            # سریالایز کردن اطلاعات کاربر
            product_data = ProductResource(product).data
            # بازگرداندن داده‌های سریالایز شده
            return Response({"data":product_data},status=status.HTTP_200_OK)
            
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND) 

#@hasPermission('update')
class ProductUpdateView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # دریافت داده‌های ورودی و استفاده از serializer برای به‌روزرسانی
        serializer = CreateUpdateProductFormSerializer(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            product=serializer.save()
            # سریالایز کردن اطلاعات کاربر
            product_data = ProductResource(product).data
            return Response(product_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ProductsListView(APIView):

    #permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)
    
    def get(self, request):
        products = Product.objects.all()
        product_data = ProductResource(products, many=True).data
        return Response({"data":product_data}, status=status.HTTP_200_OK)  

#@hasPermission('delete')
class ProductDeleteView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def delete(self, request, id):
        # پیاده‌سازی برای حذف یک کاربر خاص
        try:
            product = Product.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است

            # حذف تصویر قبلی اگر وجود داشته باشد
            old_file = File.objects.filter(product=product).first()
            if old_file:
                old_file.delete()  # حذف تصویر قبلی

            product.delete()
            return Response({'message': 'Product deleted'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)                   



###############################  CATEGORY  ##########################
#@hasPermission('create')
class CategoryCreateView(APIView):

    ########user be login
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request):
        serializer = CreateUpdateCategoryFormSerializer(data=request.data)
        if serializer.is_valid():

            category = serializer.save()  # ذخیره کاربر جدید
            # سریالایز کردن اطلاعات دیته بندی
            category_data = CategoryResource(category).data
            # بازگرداندن داده‌های سریالایز شده
            return Response(category_data,status=status.HTTP_201_CREATED)
            # return Response({
            #     "user": RegisterUserFormSerializer(user).data,
            #     "refresh": str(refresh),
            #     "access": str(refresh.access_token),
            # }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#@hasPermission('update')
class CategoryUpdateView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # دریافت داده‌های ورودی و استفاده از serializer برای به‌روزرسانی
        serializer = CreateUpdateCategoryFormSerializer(category, data=request.data, partial=True)
        
        if serializer.is_valid():
            category=serializer.save()
            # سریالایز کردن اطلاعات کاربر
            category_data = CategoryResource(category).data
            return Response(category_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class CategoryShowView(APIView):

    #permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def get(self, request, id):
        # پیاده‌سازی برای نمایش یک کاربر خاص
        # فرض بر این است که شما یک مدل User دارید که اطلاعات کاربران را نگه می‌دارد
        try:
            category = Category.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است
            # سریالایز کردن اطلاعات کاربر
            category_data = CategoryResource(category).data
            # بازگرداندن داده‌های سریالایز شده
            return Response({"data":category_data},status=status.HTTP_200_OK)
            
        except Category.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND) 


class CategoriesListView(APIView):

    #permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)
    
    def get(self, request):
        categories = Category.objects.all()
        categories_data = CategoryResource(categories, many=True).data
        return Response({"data":categories_data}, status=status.HTTP_200_OK)  

#@hasPermission('delete')
class CategoryDeleteView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def delete(self, request, id):
        # پیاده‌سازی برای حذف یک کاربر خاص
        try:
            category = Category.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است

            # حذف تصویر قبلی اگر وجود داشته باشد
            old_file = File.objects.filter(category=category)
            if old_file:
                old_file.delete()  # حذف تصویر قبلی

            category.delete()
            return Response({'message': 'Category deleted'}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)                   



################################# VIEW #################

class ProductAddView(APIView):


    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
       
        product = Product.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است
        user=request.user

        view=View.objects.create(user=user,product=product)
        
        product_data = ProductResource(product).data
            # بازگرداندن داده‌های سریالایز شده
        return Response({"data":product_data},status=status.HTTP_200_OK)


class ToggleLikeView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
        try:
            # پیدا کردن محصول بر اساس ID
            product = Product.objects.get(id=id)
            user = request.user

            # بررسی وجود لایک
            like = Like.objects.filter(user=user, product=product).first()

            if like:
                # حذف لایک در صورت وجود
                like.delete()
                isLiked = False
                message = "Like removed successfully."
            else:
                # ایجاد لایک در صورت عدم وجود
                Like.objects.create(user=user, product=product)
                isLiked = True
                message = "Like added successfully."

            # سریالایز کردن اطلاعات محصول
            product_data = ProductResource(product).data

            # افزودن مقدار isLiked به اطلاعات محصول
            product_data['isLiked'] = isLiked

            # بازگرداندن کل اطلاعات محصول به همراه وضعیت isLiked
            return Response({
                "message": message,
                "data": product_data
            }, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class ProductReviewView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
        try:
            # پیدا کردن محصول بر اساس id
            product = Product.objects.get(id=id)
            user = request.user

            # بررسی اینکه آیا کاربر محصول را خریداری کرده است
            has_purchased = Order.objects.filter(user=user, details__product=product, status='processing').exists()

            if not has_purchased:
                return Response({"error": "You must purchase the product before reviewing it."}, status=status.HTTP_400_BAD_REQUEST)


            # بررسی اینکه آیا کاربر قبلاً برای این محصول نظر داده است
            existing_review = Review.objects.filter(user=user, product=product).first()

            if existing_review:
                # اگر نظر قبلاً وجود داشت، آن را به‌روزرسانی می‌کنیم
                existing_review.rating = request.data.get('rating')
                existing_review.review = request.data.get('review')
                existing_review.save()  # ذخیره تغییرات
                message = "Review updated successfully."
            else:
                # اگر نظر قبلاً وجود نداشت، نظر جدید ایجاد می‌کنیم
                Review.objects.create(
                    user=user,
                    product=product,
                    rating=request.data.get('rating'),
                    review=request.data.get('review'),
                )
                message = "Review added successfully."

            # سریالایز کردن داده‌های محصول برای بازگشت
            product_data = ProductResource(product).data

            # بازگشت پاسخ به کلاینت
            return Response({"message": message, "data": product_data}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


    # متد GET برای دریافت لیست نظرات
    def get(self, request, id):
        try:
            # پیدا کردن محصول بر اساس id
            product = Product.objects.get(id=id)

            # بازیابی لیست نظرات مربوط به محصول
            reviews = Review.objects.filter(product=product)

            # استفاده از ReviewResource برای سریالایز کردن نظرات
            review_data = ReviewResource(reviews, many=True).data

            # بازگشت پاسخ نظرات
            return Response({"reviews": review_data}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)   
