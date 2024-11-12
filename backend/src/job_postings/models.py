from django.db import models

class CompanyDim(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.TextField()
    link = models.TextField()
    link_google = models.TextField()
    thumbnail = models.TextField()

    class Meta:
        db_table = 'company_dim'


class SkillsDim(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skills = models.TextField()
    type = models.TextField()

    class Meta:
        db_table = 'skills_dim'


class JobPostingsFact(models.Model):
    job_id = models.AutoField(primary_key=True)
    company = models.ForeignKey(CompanyDim, on_delete=models.CASCADE)
    job_title_short = models.CharField(max_length=255)
    job_title = models.TextField()
    job_location = models.TextField()
    job_via = models.TextField()
    job_schedule_type = models.TextField()
    job_work_from_home = models.BooleanField()
    search_location = models.TextField()
    job_posted_date = models.DateTimeField()
    job_no_degree_mention = models.BooleanField()
    job_health_insurance = models.BooleanField()
    job_country = models.TextField()
    salary_rate = models.TextField()
    salary_year_avg = models.DecimalField(max_digits=10, decimal_places=2)
    salary_hour_avg = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'job_postings_fact'


class SkillsJobDim(models.Model):
    job = models.ForeignKey(JobPostingsFact, on_delete=models.CASCADE, related_name='skills_through')
    skill = models.ForeignKey(SkillsDim, on_delete=models.CASCADE)

    class Meta:
        db_table = 'skills_job_dim'
        unique_together = (('job', 'skill'),)
