from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class Challenge(models.Model):
    class Meta:
        ordering = ['start_date']

    class Period(models.IntegerChoices):
        ONETIME = 0, 'Jednorazowe'
        DAILY = 1, 'Codzienne'
        WEEKLY = 2, 'Cotygodniowe'
        MONTHLY = 3, 'Comiesięczne'

    class Type(models.IntegerChoices):
        QR_CODE = 0, 'Kod QR'

    name = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField()
    period = models.IntegerField(choices=Period.choices)
    type = models.IntegerField(choices=Type.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField(upload_to='challenges')

    def __str__(self):
        return f'Wyzwanie {self.name}'


class ChallengeUser(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False)


class Quiz(models.Model):
    question = models.CharField(max_length=200)
    answer_a = models.CharField(max_length=200)
    answer_b = models.CharField(max_length=200)
    answer_c = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)
    date = models.DateField()
    points = models.IntegerField()

    def __str__(self):
        return f"Codzienny quiz"


class QuizAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)


class Event(models.Model):
    class Meta:
        ordering = ['date']

    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='events')
    limit = models.IntegerField()


class EventUser(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Pets(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pets')
