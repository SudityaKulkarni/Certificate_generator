from django.db import models

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    date_issued = models.DateField(auto_now_add=True)


def __str__(self):
        return f"{self.name} - {self.course}"