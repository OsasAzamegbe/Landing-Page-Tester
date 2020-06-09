from django.db import models

# Create your models here.
class Traffic(models.Model):
    page_url = models.URLField(max_length=300)
    stats = models.FloatField()

    def __str__(self):
        return '%s %s' % ('Page URL:', self.page_url)


class Page(models.Model):
    page_name = models.CharField(max_length=100)    
    page_url = models.URLField(max_length=300)
    page_traffic = models.FloatField()
    page_status = models.IntegerField()
    page_signups = models.FloatField()


    def __str__(self):
        return '%s %s' % ('Page:', self.page_name)


