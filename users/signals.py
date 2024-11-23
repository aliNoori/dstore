# users/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models.product import Product
from users.models.customuser import CustomUser

        
ROLES_AND_PERMISSIONS = {
    'admin': ['edit', 'read', 'delete', 'create'],
    'editor': ['edit', 'read', 'create'],
    'citizen': ['read']
}

@receiver(post_migrate)

def create_roles_and_permissions(sender, **kwargs):
    
    content_type = ContentType.objects.get_for_model(Product)

    print(content_type)

    for role_name, permissions in ROLES_AND_PERMISSIONS.items():
        # ایجاد یا پیدا کردن نقش
        group, _ = Group.objects.get_or_create(name=role_name)

        for permission_codename in permissions:
            # ایجاد یا پیدا کردن مجوز
            permission, _ = Permission.objects.get_or_create(
                codename=permission_codename,
                defaults={
                    'name': f'{permission_codename.replace("_", " ").title()}',
                    'content_type': content_type,
                }
            )
            print(permission)
            # تخصیص مجوز به نقش
            group.permissions.add(permission)
