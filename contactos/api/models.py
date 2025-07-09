from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
