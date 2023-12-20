from django.db import models

# Create your models here.
# appname/models.py
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=250)
    isocode = models.CharField(max_length=250)
    m49code = models.CharField(max_length=250)
    region1 = models.CharField(max_length=250)
    region2 = models.CharField(max_length=250)
    continent = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Address(models.Model):
    street = models.CharField(max_length=255)
    long = models.CharField(max_length=255)
    lat = models.CharField(max_length=255)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        if self.town:
            return f"{self.street}, {self.town}, {self.city}"
        else:
            return f"{self.street}, {self.city}"
        
class APIResponse(models.Model):
    status = models.CharField(default="", max_length=50)
    message = models.CharField(default="", max_length=300)
    data = models.JSONField(null=True, blank=True)
