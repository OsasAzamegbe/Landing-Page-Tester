from django.db import models

# Create your models here.
class Traffic(models.Model):
    page_url = models.URLField(max_length=300)
    stats = models.FloatField()

    def __str__(self):
        return '%s %s' % ('Page URL:', self.page_url)


class Page(models.Model):
    page_url = models.URLField(max_length=300)
    page_name = models.CharField(max_length=100)
    page_rank = models.BigIntegerField(default=0000)    
    page_views_per_million = models.FloatField(default=0)
    page_views_per_user = models.FloatField(default=0)
    page_status = models.IntegerField(default=0)
    reach_per_million = models.FloatField(default=0)
    
    def __str__(self):
        return '%s %s' % ('Page:', self.page_url)

class Speed(models.Model):
    page_url = models.URLField(max_length=300)
    page_name = models.CharField(max_length=100)
    median_load_time = models.FloatField(default=0)
    percentile = models.FloatField(default=0)

    def __str__(self):
        return self.page_name
    
class LinkCount(models.Model):
    page_url = models.URLField(max_length=300)
    page_name = models.CharField(max_length=100)
    links_in_count = models.IntegerField(default=0)

    def __str__(self):
        return self.page_name