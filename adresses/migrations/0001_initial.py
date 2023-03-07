# Generated by Django 4.0.7 on 2023-03-07 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=40)),
                ('zip_code', models.CharField(max_length=10)),
                ('number', models.IntegerField()),
                ('complement', models.TextField(null=True)),
                ('city', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
            ],
        ),
    ]
