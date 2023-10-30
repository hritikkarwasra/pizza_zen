# Generated by Django 4.2.6 on 2023-10-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('base_type', models.CharField(choices=[('Thin Crust', 'Thin Crust'), ('Normal', 'Normal'), ('Cheese Burst', 'Cheese Burst')], max_length=100)),
                ('cheese_type', models.CharField(choices=[('Mozzarella', 'Mozzarella'), ('Melted Cheese', 'Melted Cheese'), ('Masaledaar Cheese', 'Masaledaar Cheese'), ('Cheese Dhamaka', 'Cheese Dhamaka')], max_length=100)),
                ('description', models.TextField()),
                ('toppings', models.ManyToManyField(blank=True, null=True, to='apis.topping')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
