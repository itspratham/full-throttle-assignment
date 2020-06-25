from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=12,primary_key=True)
    real_name = models.CharField(max_length=50)
    tz = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return str(self.real_name)

class ActivityPeriod(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user_id)
