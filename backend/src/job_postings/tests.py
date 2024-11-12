import os
import sys
import django
from random import randint, choice

from faker import Faker

# Dynamically add the project directory to the sys.path
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(project_path)
print(project_path)
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from job_postings.models import CompanyDim, SkillsDim, JobPostingsFact, SkillsJobDim
from django.db import models




# Query: What are the top-paying data analyst jobs?

# SELECT job_title_short, salary_year_avg
# FROM job_postings_fact
# WHERE LOWER(job_title_short) LIKE '%analyst%' AND salary_year_avg IS NOT NULL
# ORDER BY salary_year_avg DESC
# LIMIT 10;

# queryset = JobPostingsFact.objects.values('job_title_short','salary_year_avg') \
#                         .filter(salary_year_avg__isnull=False, job_title_short__icontains='analyst') \
#                         .order_by('-salary_year_avg')[:10]




# Query: What are the most optimal skills to learn (aka it’s in high demand and a high-paying skill)?

# WITH optimal_skill AS (
    # SELECT sjd.skill_id, ROUND(SUM(jpf.salary_year_avg), 2) salary
    # FROM job_postings_fact jpf
    # JOIN skills_job_dim sjd ON sjd.job_id = jpf.job_id
    # WHERE jpf.salary_year_avg IS NOT NULL
    # GROUP BY sjd.skill_id
    # ORDER BY SUM(jpf.salary_year_avg) DESC
    # LIMIT 10
# )

# WITH optimal_skill AS (
# 	SELECT sjd.skill_id, COUNT(jpf.job_id) count
#     FROM job_postings_fact jpf
#     JOIN skills_job_dim sjd ON sjd.job_id = jpf.job_id
#     GROUP BY sjd.skill_id
#     ORDER BY COUNT(jpf.job_id) DESC
#     LIMIT 10
# )

# SELECT ops.*, sd.skills skill_name
# FROM optimal_skill ops
# JOIN skills_dim sd ON sd.skill_id = ops.skill_id
# ORDER BY ops.count DESC;
pass 
# top_paying_jobs = JobPostingsFact.objects \
#                 .filter(salary_year_avg__isnull=False) \
#                 .values(skill_id=models.F('skills_through__skill__skill_id')) \
#                 .annotate(salary=models.Sum('salary_year_avg')) \
#                 .order_by('salary')[:10]
top_paying_jobs = JobPostingsFact.objects \
                .filter(salary_year_avg__isnull=False, skills_through__skill__skill_id__isnull=False) \
                .values(skill_id=models.F('skills_through__skill__skill_id')) \
                .order_by('salary_year_avg')[:10]
