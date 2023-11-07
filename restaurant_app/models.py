from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

class User(AbstractUser):
    username = models.EmailField(_('Correo'), unique=True)
    rut = models.CharField(max_length=200 , null=True,blank=True)
    is_administrador = models.BooleanField('Administrador', default=False)
    is_chef = models.BooleanField('Chef', default=False)
    is_vendedor = models.BooleanField('Vendedor', default=False)

    def __str__(self):
        name = self.first_name + ' ' + self.last_name
        return name

class Platillo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        nombre = self.nombre 
        return nombre

class Inventario(models.Model):
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    porciones_disponibles = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

class Venta(models.Model):
    nombre_vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    cantidad_vendida = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

class Calendario(models.Model):
    nombre=models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ForeignKey(Platillo, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    Porciones =models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True,verbose_name='Porciones' )