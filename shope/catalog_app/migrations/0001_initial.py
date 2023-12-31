# Generated by Django 4.2 on 2023-10-23 20:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=255, verbose_name='discount name')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='priority')),
                ('value', models.PositiveIntegerField(default=1, verbose_name='sale value')),
                ('data_start', models.DateField(default=django.utils.timezone.now, verbose_name='date of discount start')),
                ('data_end', models.DateField(default=django.utils.timezone.now, verbose_name='date of discount end')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(null=True, upload_to='images/%Y/%m/%d', verbose_name='image')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=7, verbose_name='amount of products for a success discount')),
                ('quantity', models.PositiveIntegerField(default=2, verbose_name='quantity of products for a success discount')),
            ],
            options={
                'verbose_name': 'cart discount',
                'verbose_name_plural': 'cart discounts',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('image', models.FileField(blank=True, default='/img/icons/allDep.svg', null=True, upload_to='images/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(['svg'])], verbose_name='image')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CharacteristicType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'type characteristic of product',
                'verbose_name_plural': 'types characteristic of product',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='image')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('number_of_sales', models.IntegerField(blank=True, default=0, verbose_name='number_of_sales')),
                ('is_limited', models.BooleanField(default=True, verbose_name='limited')),
                ('is_delivery', models.BooleanField(default=True, verbose_name='delivery')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.category', verbose_name='category')),
                ('image', models.ManyToManyField(related_name='image_to_product', to='catalog_app.image', verbose_name='image')),
                ('tag', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'slider',
                'verbose_name_plural': 'sliders',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Rewiew',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('text', models.TextField(verbose_name='text')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'rewiew',
                'verbose_name_plural': 'reviews',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductViewed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'viewed product',
                'verbose_name_plural': 'viewed products',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DiscountProductGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=255, verbose_name='discount name')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='priority')),
                ('value', models.PositiveIntegerField(default=1, verbose_name='sale value')),
                ('data_start', models.DateField(default=django.utils.timezone.now, verbose_name='date of discount start')),
                ('data_end', models.DateField(default=django.utils.timezone.now, verbose_name='date of discount end')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(null=True, upload_to='images/%Y/%m/%d', verbose_name='image')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='fixed amount of discount')),
                ('fixprice', models.DecimalField(decimal_places=2, default=1, max_digits=7, verbose_name='fixed amount of price')),
                ('category', models.ManyToManyField(to='catalog_app.category', verbose_name='category as group of products')),
            ],
            options={
                'verbose_name': 'group of product discount',
                'verbose_name_plural': 'group of product discounts',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='DiscountProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=255, verbose_name='discount name')),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='priority')),
                ('value', models.PositiveIntegerField(default=1, verbose_name='sale value')),
                ('data_start', models.DateField(default=django.utils.timezone.now, verbose_name='date of discount start')),
                ('data_end', models.DateField(default=django.utils.timezone.now, verbose_name='date of discount end')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('image', models.ImageField(null=True, upload_to='images/%Y/%m/%d', verbose_name='image')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog_app.category', verbose_name='category')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product discount',
                'verbose_name_plural': 'product discounts',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CompareProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('session_key', models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='session key')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product for comparison',
                'verbose_name_plural': 'products for comparison',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CharacteristicValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('value', models.CharField(max_length=100, verbose_name='value')),
                ('characteristic_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_value', to='catalog_app.characteristictype', verbose_name='type of characteristic')),
            ],
            options={
                'verbose_name': 'characteristic value',
                'verbose_name_plural': 'characteristic values',
            },
        ),
        migrations.CreateModel(
            name='CharacteristicProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('characteristic_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='catalog_app.characteristicvalue', verbose_name='value of characteristic')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='catalog_app.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'characteristic of product',
                'verbose_name_plural': 'characteristics of product',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated time')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog_app.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'banner',
                'verbose_name_plural': 'banners',
                'ordering': ['id'],
            },
        ),
    ]
