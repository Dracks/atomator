# Generated by Django 3.0.6 on 2020-06-05 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('version_manager', '0001_initial'),
        ('application', '0001_initial'),
        ('scripting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigEnvironment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment', models.SmallIntegerField(choices=[(0, 'Development'), (1, 'Pre-Production'), (2, 'Production')])),
            ],
        ),
        migrations.CreateModel(
            name='ExecutionOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(-1, 'Pending'), (0, 'Working'), (1, 'OK'), (2, 'Error')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('build', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='version_manager.Build')),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployment.ConfigEnvironment')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment', models.SmallIntegerField(choices=[(0, 'Development'), (1, 'Pre-Production'), (2, 'Production')])),
                ('name', models.CharField(max_length=255)),
                ('services_installed_list', models.ManyToManyField(to='version_manager.Build')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TaskOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.SmallIntegerField(choices=[(0, 'Nothing done'), (1, 'Changed'), (2, 'Error')])),
                ('stdout', models.TextField(blank=True, null=True)),
                ('stderr', models.TextField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('execution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployment.ExecutionOutput')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployment.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='ExecutionError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('stacktrace', models.TextField()),
                ('execution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='error', to='deployment.ExecutionOutput')),
            ],
        ),
        migrations.CreateModel(
            name='DeploymentConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configurations_set', to='application.Application')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='scripting.ScriptsProvider')),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='scripting.ScriptFile')),
                ('tags_list', models.ManyToManyField(blank=True, related_name='_deploymentconfiguration_tags_list_+', to='deployment.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='configenvironment',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='environments', to='deployment.DeploymentConfiguration'),
        ),
        migrations.AddField(
            model_name='configenvironment',
            name='inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='scripting.ScriptFile'),
        ),
    ]
