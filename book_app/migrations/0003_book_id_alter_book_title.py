# Generated by Django 4.0.4 on 2022-04-13 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0002_rename_pub_data_book_pub_date_remove_book_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
