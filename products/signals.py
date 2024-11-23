from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from products.models.product import Product

ROLES_AND_PERMISSIONS = {
    'admin': ['edit', 'read', 'delete', 'create'],
    'editor': ['edit', 'read', 'create'],
    'citizen': ['read']
}

@receiver(post_migrate)
def create_roles_and_permissions(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(Product)
    # ایجاد نقش‌ها و پرمیژن‌ها
    for role_name, permissions in ROLES_AND_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=role_name)
        for permission_codename in permissions:
            permission, created = Permission.objects.get_or_create(
                codename=permission_codename,
                defaults={
                    'name': f'{permission_codename.replace("_", " ").title()}',
                    'content_type': content_type,
                }
            )
            if created:
                print(f"Permission {permission_codename} created for group {role_name}.")
            group.permissions.add(permission)
