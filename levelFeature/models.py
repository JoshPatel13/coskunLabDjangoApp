from django.db import models

# Create your models here.


class LevelReading(models.Model):
    sr_num = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    reading_value = models.DecimalField(max_digits=8, decimal_places=2)

    def __int__(self):
        return self.sr_num


class Livestream(models.Model):
    url = models.URLField()

    def __int__(self):
        return self.url


