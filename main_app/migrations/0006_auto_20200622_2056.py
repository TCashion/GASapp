# Generated by Django 3.0.5 on 2020-06-22 20:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0005_instrument_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instrument',
            name='year',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900, 'Year must be greater than 1900'), django.core.validators.MaxValueValidator(2025, 'Year must be less than 2025')], verbose_name='Manufacture year (YYYY)'),
        ),
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('manufacturer', models.CharField(max_length=150)),
                ('year', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900, 'Year must be greater than 1900'), django.core.validators.MaxValueValidator(2025, 'Year must be less than 2025')], verbose_name='Manufacture year (YYYY)')),
                ('serial', models.CharField(blank=True, max_length=250, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0.01, 'Price must be greater than $0.01')])),
                ('condition', models.CharField(choices=[('U', 'Used'), ('P', 'Poor'), ('F', 'Fair'), ('G', 'Good'), ('V', 'Very Good'), ('E', 'Excellent'), ('M', 'Mint'), ('B', 'BrandNew')], default='U', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]