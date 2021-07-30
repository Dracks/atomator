# Generated by Django 3.0.6 on 2020-06-05 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScriptFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'Ansible Script'), (2, 'Inventory File')])),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ScriptsProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('folder', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.ManyToManyField(related_name='ScriptFile', to='scripting.ScriptFile')),
            ],
        ),
        migrations.AddField(
            model_name='scriptfile',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scripting.ScriptsProvider'),
        ),
        migrations.CreateModel(
            name='ExcludedPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exclude_path_set', to='scripting.ScriptsProvider')),
            ],
        ),
        migrations.AddIndex(
            model_name='scriptfile',
            index=models.Index(fields=['name'], name='name_idx'),
        ),
    ]