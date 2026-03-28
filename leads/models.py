from django.db import models


class Lead(models.Model):

    FUENTE_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('landing_page', 'Landing Page'),
        ('referido', 'Referido'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fuente = models.CharField(max_length=20, choices=FUENTE_CHOICES)
    producto_interes = models.CharField(max_length=255, blank=True, null=True)
    presupuesto = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    deleted_at = models.DateTimeField(blank=True, null=True)  # soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nombre} <{self.email}>"

    @property
    def is_deleted(self):
        return self.deleted_at is not None