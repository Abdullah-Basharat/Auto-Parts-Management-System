from django.db import models

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=50,primary_key=True)

class Car(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)

class Type(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Car_Type(models.Model):
    id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    type = models.ForeignKey(Type,on_delete=models.CASCADE)

class Part(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

class Car_Parts(models.Model):
    id = models.BigAutoField(primary_key=True)
    car_type = models.ForeignKey(Car_Type, on_delete=models.CASCADE)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

class History(models.Model):
    date = models.DateField(primary_key=True)
    earn = models.IntegerField()