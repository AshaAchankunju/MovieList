from django.db import models

# Create your models here.



class Movie(models.Model):
    title=models.CharField(max_length=100, unique=200)
    director=models.CharField(max_length=200)
    genre=models.CharField(max_length=200)
    run_time=models.IntegerField()
    language=models.CharField(max_length=200)
    year=models.CharField(max_length=200)

    def __str__(self) :
        return self.title