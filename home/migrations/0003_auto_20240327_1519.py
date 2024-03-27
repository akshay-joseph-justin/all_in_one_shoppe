# Generated by Django 3.2.25 on 2024-03-27 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_categorymodel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='discount_percentage',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]