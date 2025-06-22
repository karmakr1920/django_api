from django.db import models

class Cloth(models.Model):
    cloth_name = models.CharField(max_length=50)
    cloth_brand = models.CharField(max_length=50)
