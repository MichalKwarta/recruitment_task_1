# Generated by Django 4.0.4 on 2022-04-14 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0011_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
