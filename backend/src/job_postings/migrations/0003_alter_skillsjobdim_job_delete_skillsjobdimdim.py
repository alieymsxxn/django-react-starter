# Generated by Django 5.1.2 on 2024-11-10 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_postings', '0002_to_roll_back'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillsjobdim',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills_through', to='job_postings.jobpostingsfact'),
        ),
        migrations.DeleteModel(
            name='SkillsJobDimDim',
        ),
    ]