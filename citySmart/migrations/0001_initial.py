# Generated by Django 2.0.4 on 2018-09-23 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dustbin',
            fields=[
                ('dustbin_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('street_number', models.PositiveSmallIntegerField()),
                ('filled_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('no_of_residents', models.PositiveSmallIntegerField()),
                ('no_of_vehicles', models.PositiveSmallIntegerField()),
                ('street_number', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('aadhar_number', models.DecimalField(decimal_places=0, max_digits=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField()),
                ('profession', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('mobile_number', models.DecimalField(blank=True, decimal_places=0, max_digits=10)),
                ('residence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citySmart.House')),
            ],
        ),
        migrations.CreateModel(
            name='Street_light',
            fields=[
                ('light_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('street_number', models.PositiveSmallIntegerField()),
                ('live_status', models.CharField(choices=[('ALIVE', 'alive'), ('SICK', 'sick'), ('DEAD', 'dead')], default='DEAD', max_length=5)),
                ('running_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Water_tank',
            fields=[
                ('water_tank_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('street_number', models.PositiveSmallIntegerField()),
                ('filled_percentage', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('zone_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('person_incharge', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='water_tank',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citySmart.Zone'),
        ),
        migrations.AddField(
            model_name='street_light',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citySmart.Zone'),
        ),
        migrations.AddField(
            model_name='house',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citySmart.Zone'),
        ),
        migrations.AddField(
            model_name='dustbin',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citySmart.Zone'),
        ),
    ]
