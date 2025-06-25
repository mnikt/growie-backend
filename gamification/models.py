from django.db import models

# Create your models here.
class Challenge(models.Model):
    class Period(models.IntegerChoices):
        ONETIME = 0, 'One Time'
        DAILY = 1, 'Daily'
        WEEKLY = 2, 'Weekly'
        MONTHLY = 3, 'Monthly'

    class Type(models.IntegerChoices):
        QR_CODE = 0, 'QR Code'
        ENTRANCE = 1, 'Entrance'

    name = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    period = models.IntegerField(choices=Period.choices)
    type = models.IntegerField(choices=Type.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='challenges')
    joined = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
