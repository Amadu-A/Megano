from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission

from auth_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        staff_users_queryset = User.objects.filter(is_staff=True)

        for users in staff_users_queryset:
            user = User.objects.get(pk=users.pk)

            group, created = Group.objects.get_or_create(
                name="seller"
            )

            permission_add_price = Permission.objects.get(
                codename="add_price"
            )
            permission_change_price = Permission.objects.get(
                codename="change_price"
            )
            permission_delete_price = Permission.objects.get(
                codename="delete_price"
            )
            permission_view_price = Permission.objects.get(
                codename="view_price"
            )
            permission_view_product = Permission.objects.get(
                codename="view_product"
            )

            # добавляем разрешение в группу
            group.permissions.add(permission_add_price, permission_change_price,
                                  permission_delete_price, permission_view_price, permission_view_product)

            # присоединяем пользователя к группе
            user.groups.add(group)

            group.save()
