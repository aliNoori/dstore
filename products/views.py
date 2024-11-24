# Create your views here.
# views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from files.models.file import File
from products.models.category import Category
from products.models.like import Like
from products.models.product import Product
from products.models.reviews import Review
from products.models.view import View
from products.serializers.category import CategoryResource, CreateUpdateCategoryFormSerializer
from products.serializers.createupdate import CreateUpdateProductFormSerializer

from products.serializers.productresource import ProductResource
from users.decorators.checkpermission import PermissionMixin



class ProductCreateView(PermissionMixin, APIView):
    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)
    required_permission = 'users.create'  # تعیین دسترسی مورد نیاز

    def post(self, request):

        print(request.user)
        print(request.user.get_all_permissions())
        print(request.user.has_perm('users.create'))

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


class ProductLikeView(APIView):


    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
       
        product = Product.objects.get(id=id)  # فرض بر اینکه User مدل کاربران است
        user=request.user

        like=Like.objects.create(user=user,product=product)
        
        product_data = ProductResource(product).data
            # بازگرداندن داده‌های سریالایز شده
        return Response({"data":product_data},status=status.HTTP_200_OK)
    
class ProductDislikeView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def delete(self, request, id):
        try:
            # پیدا کردن محصول بر اساس id
            product = Product.objects.get(id=id)
            user = request.user

            # پیدا کردن لایک مرتبط با کاربر و محصول
            like = Like.objects.filter(user=user, product=product).first()

            if like:
                # حذف لایک
                like.delete()
                # سریالایز کردن اطلاعات محصول
                product_data = ProductResource(product).data
                # بازگرداندن داده‌های سریالایز شده
                return Response({"data": product_data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Like not found."}, status=status.HTTP_404_NOT_FOUND)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)




class ProductReviewView(APIView):

    permission_classes = [IsAuthenticated]  # Middleware (Authentication Required)

    def post(self, request, id):
    
        # پیدا کردن محصول بر اساس id
        product = Product.objects.get(id=id)
        user = request.user

        review=Review.objects.create(
            user=user,
            product=product,
           rating=request.data.get('rating'),  # گرفتن امتیاز از داده‌های درخواست
           review=request.data.get('review')  # گرفتن متن نظر از داده‌های درخواست

        )
           
        product_data = ProductResource(product).data
        # بازگرداندن داده‌های سریالایز شده
        return Response({"data": product_data}, status=status.HTTP_200_OK)