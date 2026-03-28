from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from leads.models import Lead
from decimal import Decimal
import random

fake = Faker('es_CO')

FUENTES = ['instagram', 'facebook', 'landing_page', 'referido', 'otro']
PRODUCTOS = [
    'Curso de Marketing Digital',
    'Mentoría 1 a 1',
    'Pack de Templates',
    'Masterclass Ventas',
    'Ebook Copywriting',
    'Programa Acelerador',
    'Consultoría Estratégica',
    'Comunidad Premium',
]


class Command(BaseCommand):
    help = 'Carga 15 leads de ejemplo en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Iniciando seed...')

        # Limpiar leads existentes
        Lead.objects.all().delete()

        leads = [
            Lead(
                nombre='Carlos Rodríguez',
                email='carlos.rodriguez@gmail.com',
                telefono='3001234567',
                fuente='instagram',
                producto_interes='Curso de Marketing Digital',
                presupuesto=Decimal('250.00'),
                created_at=timezone.now() - timezone.timedelta(days=1),
            ),
            Lead(
                nombre='María Fernández',
                email='maria.fernandez@hotmail.com',
                telefono='3109876543',
                fuente='facebook',
                producto_interes='Mentoría 1 a 1',
                presupuesto=Decimal('500.00'),
                created_at=timezone.now() - timezone.timedelta(days=2),
            ),
            Lead(
                nombre='Andrés Torres',
                email='andres.torres@gmail.com',
                telefono='3205551234',
                fuente='landing_page',
                producto_interes='Masterclass Ventas',
                presupuesto=Decimal('150.00'),
                created_at=timezone.now() - timezone.timedelta(days=3),
            ),
            Lead(
                nombre='Laura Gómez',
                email='laura.gomez@yahoo.com',
                telefono=None,
                fuente='referido',
                producto_interes='Pack de Templates',
                presupuesto=Decimal('80.00'),
                created_at=timezone.now() - timezone.timedelta(days=4),
            ),
            Lead(
                nombre='Santiago Pérez',
                email='santiago.perez@gmail.com',
                telefono='3157778899',
                fuente='instagram',
                producto_interes='Programa Acelerador',
                presupuesto=Decimal('1200.00'),
                created_at=timezone.now() - timezone.timedelta(days=5),
            ),
            Lead(
                nombre='Valentina Ruiz',
                email='valentina.ruiz@gmail.com',
                telefono='3001112233',
                fuente='facebook',
                producto_interes='Ebook Copywriting',
                presupuesto=Decimal('30.00'),
                created_at=timezone.now() - timezone.timedelta(days=6),
            ),
            Lead(
                nombre='Felipe Mora',
                email='felipe.mora@outlook.com',
                telefono='3209990011',
                fuente='landing_page',
                producto_interes='Consultoría Estratégica',
                presupuesto=Decimal('800.00'),
                created_at=timezone.now() - timezone.timedelta(days=10),
            ),
            Lead(
                nombre='Daniela Castro',
                email='daniela.castro@gmail.com',
                telefono=None,
                fuente='otro',
                producto_interes='Comunidad Premium',
                presupuesto=Decimal('200.00'),
                created_at=timezone.now() - timezone.timedelta(days=15),
            ),
            Lead(
                nombre='Julián Herrera',
                email='julian.herrera@gmail.com',
                telefono='3143334455',
                fuente='referido',
                producto_interes='Mentoría 1 a 1',
                presupuesto=Decimal('500.00'),
                created_at=timezone.now() - timezone.timedelta(days=20),
            ),
            Lead(
                nombre='Camila Vargas',
                email='camila.vargas@hotmail.com',
                telefono='3056667788',
                fuente='instagram',
                producto_interes='Masterclass Ventas',
                presupuesto=None,
                created_at=timezone.now() - timezone.timedelta(days=25),
            ),
        ]

        # Se agregan 5 leads aleatorios con Faker
        for _ in range(5):
            nombre = fake.name()
            leads.append(Lead(
                nombre=nombre,
                email=fake.unique.email(),
                telefono=fake.numerify('3#########'),
                fuente=random.choice(FUENTES),
                producto_interes=random.choice(PRODUCTOS),
                presupuesto=Decimal(str(round(random.uniform(50, 2000), 2))),
                created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30)),
            ))

        Lead.objects.bulk_create(leads)

        self.stdout.write(self.style.SUCCESS(f'✅ Seed completado: {len(leads)} leads creados.'))