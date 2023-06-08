from django.db import models
from django.contrib.auth.models import AbstractUser


class Sector(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    Status = (('director', 'Director'),
              ('manager', 'Manager'),
              ('admin', 'Admin'),
              ('employee', 'Employee'),)

    status = models.CharField(max_length=15, choices=Status, default='employee')
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    shior = models.CharField(max_length=35, blank=True)
    main_task = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=14, blank=True)
    photo = models.ImageField(upload_to='photos', default='photos/1.png')

    def __str__(self):
        return self.username

