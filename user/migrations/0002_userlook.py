# Generated by Django 2.1.5 on 2019-01-18 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=5, verbose_name='用户id')),
                ('count', models.IntegerField(max_length=5, verbose_name='次数')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('last_time', models.DateTimeField(auto_now=True, verbose_name='最近查看时间')),
                ('goods_id', models.ForeignKey(max_length=5, on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品id')),
            ],
            options={
                'db_table': 'f_user_looks',
            },
        ),
    ]