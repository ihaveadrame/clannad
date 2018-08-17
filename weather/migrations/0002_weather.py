# Generated by Django 2.1 on 2018-08-17 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('air_quality', models.CharField(default='', max_length=10, verbose_name='空气质量')),
                ('air_quality_number', models.IntegerField(default=0, verbose_name='空气质量指数')),
                ('humidity', models.IntegerField(default=0, verbose_name='湿度')),
                ('current_temp', models.IntegerField(default=0, verbose_name='当前温度')),
                ('max_temp', models.IntegerField(default=0, verbose_name='最高温度')),
                ('min_temp', models.IntegerField(default=0, verbose_name='最低温度')),
                ('week_max_temp', models.CharField(default='', max_length=50, verbose_name='昨天起7天最高温度')),
                ('week_min_temp', models.CharField(default='', max_length=50, verbose_name='昨天起7天最低温度')),
                ('wind', models.CharField(default='', max_length=10, verbose_name='风向')),
                ('wind_lv', models.CharField(default='', max_length=10, verbose_name='风力')),
                ('weather', models.CharField(default='', max_length=10, verbose_name='天气')),
                ('date_p', models.DateField(null=True, verbose_name='公历')),
                ('date_n', models.CharField(default='', max_length=10, null=True, verbose_name='农历')),
                ('week', models.CharField(default='', max_length=10, null=True, verbose_name='星期')),
                ('create_time', models.DateTimeField(null=True, verbose_name='创建时间')),
                ('town_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.Town')),
            ],
        ),
    ]
