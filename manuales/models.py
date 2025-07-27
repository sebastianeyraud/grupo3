from django.db import models

# Create your models here.
class Manual(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo_pdf = models.FileField(upload_to='manuales/')