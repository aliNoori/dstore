from django.db import models
#from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)  # نام دسته‌بندی
    #description = models.TextField(null=True, blank=True)  # توضیحات دسته‌بندی
    #slug = models.SlugField(max_length=255, unique=True, blank=True)  # اسلاگ برای URLها
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')  # دسته‌بندی والد
    #is_active = models.BooleanField(default=True)  # فعال یا غیرفعال بودن دسته‌بندی
    created_at = models.DateTimeField(auto_now_add=True)  # زمان ایجاد دسته‌بندی
    updated_at = models.DateTimeField(auto_now=True)  # زمان آخرین به‌روزرسانی 
    
    @property
    def image(self):
       if self.file:  # اطمینان از وجود فایل
            return self.file.file.url  # دسترسی به URL فایل
       return None  # در صورت نبودن فایل، None برگردانید

    def __str__(self) -> str:
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']  # مرتب‌سازی دسته‌بندی‌ها بر اساس نام
