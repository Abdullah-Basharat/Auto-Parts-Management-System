# Generated by Django 4.1.6 on 2023-04-15 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.brand')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('earn', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Car_Type',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.car')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.type')),
            ],
        ),
        migrations.CreateModel(
            name='Car_Parts',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('car_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.car_type')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.part')),
            ],
        ),
    ]