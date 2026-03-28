import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from leads.models import Lead
from decimal import Decimal


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def lead_data():
    return {
        'nombre': 'Juan Prueba',
        'email': 'juan.prueba@gmail.com',
        'telefono': '3001234567',
        'fuente': 'instagram',
        'producto_interes': 'Curso de Marketing',
        'presupuesto': 300.00,
    }


@pytest.fixture
def lead_en_db(db):
    return Lead.objects.create(
        nombre='Lead Existente',
        email='existente@gmail.com',
        telefono='3009876543',
        fuente='facebook',
        producto_interes='Mentoría',
        presupuesto=Decimal('500.00'),
    )


# TEST 1: Crear un lead exitosamente
@pytest.mark.django_db
def test_crear_lead_exitoso(client, lead_data):
    response = client.post('/leads/', lead_data, format='json')
    assert response.status_code == 201
    assert response.data['email'] == lead_data['email']
    assert response.data['nombre'] == lead_data['nombre']


# TEST 2: No permite email duplicado
@pytest.mark.django_db
def test_email_duplicado(client, lead_data, lead_en_db):
    lead_data['email'] = lead_en_db.email
    response = client.post('/leads/', lead_data, format='json')
    assert response.status_code == 400
    assert 'email' in response.data


# TEST 3: Nombre muy corto
@pytest.mark.django_db
def test_nombre_muy_corto(client, lead_data):
    lead_data['nombre'] = 'A'
    response = client.post('/leads/', lead_data, format='json')
    assert response.status_code == 400
    assert 'nombre' in response.data


# TEST 4: Fuente invalida
@pytest.mark.django_db
def test_fuente_invalida(client, lead_data):
    lead_data['fuente'] = 'tiktok'
    response = client.post('/leads/', lead_data, format='json')
    assert response.status_code == 400
    assert 'fuente' in response.data


# TEST 5: Listar leads con paginacion
@pytest.mark.django_db
def test_listar_leads(client, lead_en_db):
    response = client.get('/leads/?page=1&limit=10')
    assert response.status_code == 200
    assert 'results' in response.data
    assert response.data['total'] >= 1


# TEST 6: Obtener lead por ID
@pytest.mark.django_db
def test_obtener_lead_por_id(client, lead_en_db):
    response = client.get(f'/leads/{lead_en_db.id}/')
    assert response.status_code == 200
    assert response.data['email'] == lead_en_db.email


# TEST 7: Soft delete de un lead 
@pytest.mark.django_db
def test_soft_delete_lead(client, lead_en_db):
    response = client.delete(f'/leads/{lead_en_db.id}/')
    assert response.status_code == 200
    lead_en_db.refresh_from_db()
    assert lead_en_db.deleted_at is not None


# TEST 8: Actualizar un lead 
@pytest.mark.django_db
def test_actualizar_lead(client, lead_en_db):
    response = client.patch(
        f'/leads/{lead_en_db.id}/',
        {'producto_interes': 'Nuevo Producto'},
        format='json'
    )
    assert response.status_code == 200
    assert response.data['producto_interes'] == 'Nuevo Producto'


# TEST 9: Estadisticas
@pytest.mark.django_db
def test_estadisticas(client, lead_en_db):
    response = client.get('/leads/stats/')
    assert response.status_code == 200
    assert 'total_leads' in response.data
    assert 'leads_por_fuente' in response.data
    assert 'promedio_presupuesto' in response.data
    assert 'leads_ultimos_7_dias' in response.data


# TEST 10: Lead no encontrado 
@pytest.mark.django_db
def test_lead_no_encontrado(client):
    response = client.get('/leads/99999/')
    assert response.status_code == 404