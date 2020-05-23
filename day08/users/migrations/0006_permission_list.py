# Generated by Django 2.2 on 2020-05-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200507_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '附加权限表',
                'permissions': (('enable_user', '激活用户'), ('disable_user', '禁用用户')),
            },
        ),
    ]
