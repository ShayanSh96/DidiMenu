# Generated manually for the initial DIDI menu schema.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='نام دسته‌بندی')),
                ('slug', models.SlugField(max_length=140, unique=True, verbose_name='اسلاگ')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
            ],
            options={
                'verbose_name': 'دسته‌بندی',
                'verbose_name_plural': 'دسته‌بندی‌ها',
                'ordering': ['sort_order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160, verbose_name='نام محصول')),
                ('english_name', models.CharField(blank=True, max_length=160, verbose_name='نام انگلیسی')),
                ('slug', models.SlugField(max_length=180, unique=True, verbose_name='اسلاگ')),
                ('description', models.TextField(blank=True, verbose_name='توضیحات')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('image', models.ImageField(blank=True, null=True, upload_to='menu/items/%Y/%m/', verbose_name='تصویر')),
                ('is_available', models.BooleanField(default=True, verbose_name='موجود')),
                ('is_featured', models.BooleanField(default=False, verbose_name='ویژه')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='menu.category', verbose_name='دسته‌بندی')),
            ],
            options={
                'verbose_name': 'محصول منو',
                'verbose_name_plural': 'محصولات منو',
                'ordering': ['category__sort_order', 'sort_order', 'name'],
            },
        ),
    ]
