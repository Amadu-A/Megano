# Generated by Django 4.2 on 2023-09-29 15:12

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0003_alter_price_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('city', models.CharField(max_length=30, verbose_name='city')),
                ('address', models.CharField(max_length=200, verbose_name='address')),
                ('pay_type', models.CharField(choices=[('bank_card', 'bank card'), ('spb', 'spb')], default='bank_card', max_length=10, verbose_name='payment type')),
                ('delivery_type', models.CharField(choices=[('EXPRESS', 'express delivery'), ('REGULAR', 'reqular delivery')], default='REGULAR', max_length=10, verbose_name='delivery type')),
                ('status', models.CharField(choices=[('NOT_PAID', 'is not paid'), ('PAID', 'is paid'), ('DELIVERY', 'is delivered'), ('CLOSE', 'is closed')], default='NOT_PAID', max_length=10, verbose_name='status')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=10, verbose_name='order amount')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('count', models.IntegerField(verbose_name='count product')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='amount')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='order_app.order', verbose_name='order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.seller', verbose_name='seller')),
            ],
            options={
                'verbose_name': 'OrderItem',
            },
        ),
    ]
