from django.db import models


# Create your models here.


class Issuer(models.Model):
    title = models.CharField(max_length=150)


class Security(models.Model):
    title = models.CharField(max_length=150)
    issuer = models.ForeignKey(Issuer, on_delete=models.CASCADE, related_name='securities')
    isin = models.CharField(max_length=150)
    code = models.CharField(max_length=20)
    type = models.CharField(max_length=100)


class Price(models.Model):
    date = models.DateField()
    price = models.FloatField()
    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='prices')


class Industry(models.Model):
    name = models.CharField(max_length=150)
    issuer = models.OneToOneField(Issuer, on_delete=models.CASCADE, related_name='industry')


class Portfolio(models.Model):
    security = models.OneToOneField(Security, on_delete=models.CASCADE, related_name='portfolio')
    count = models.IntegerField()
