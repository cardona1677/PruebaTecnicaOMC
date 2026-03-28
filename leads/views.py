from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Avg, Count, Q
from datetime import timedelta
import os
import requests

from .models import Lead
from .serializers import LeadSerializer


class LeadListCreateView(APIView):

    # GET /leads — POST /leads
    def get(self, request):
        leads = Lead.objects.filter(deleted_at__isnull=True)

        # Filtro por fuente
        fuente = request.query_params.get('fuente')
        if fuente:
            leads = leads.filter(fuente=fuente)

        # Filtro por rango de fechas
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        if fecha_inicio:
            leads = leads.filter(created_at__date__gte=fecha_inicio)
        if fecha_fin:
            leads = leads.filter(created_at__date__lte=fecha_fin)

        # Paginación manual
        page = int(request.query_params.get('page', 1))
        limit = int(request.query_params.get('limit', 10))
        offset = (page - 1) * limit
        total = leads.count()
        leads_page = leads[offset:offset + limit]

        serializer = LeadSerializer(leads_page, many=True)
        return Response({
            'total': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit,
            'results': serializer.data
        })

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadDetailView(APIView):

    # GET /leads/:id — PATCH /leads/:id — DELETE /leads/:id
    def get_object(self, pk):
        try:
            return Lead.objects.get(pk=pk, deleted_at__isnull=True)
        except Lead.DoesNotExist:
            return None

    def get(self, request, pk):
        lead = self.get_object(pk)
        if not lead:
            return Response(
                {'error': 'Lead no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = LeadSerializer(lead)
        return Response(serializer.data)

    def patch(self, request, pk):
        lead = self.get_object(pk)
        if not lead:
            return Response(
                {'error': 'Lead no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = LeadSerializer(lead, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        lead = self.get_object(pk)
        if not lead:
            return Response(
                {'error': 'Lead no encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        lead.deleted_at = timezone.now()
        lead.save()
        return Response(
            {'message': 'Lead eliminado correctamente.'},
            status=status.HTTP_200_OK
        )


class LeadStatsView(APIView):
    
    # GET /leads/stats
    def get(self, request):
        leads = Lead.objects.filter(deleted_at__isnull=True)

        total = leads.count()

        por_fuente = leads.values('fuente').annotate(total=Count('id'))
        fuentes = {item['fuente']: item['total'] for item in por_fuente}

        promedio_presupuesto = leads.aggregate(
            promedio=Avg('presupuesto')
        )['promedio']

        hace_7_dias = timezone.now() - timedelta(days=7)
        leads_ultimos_7_dias = leads.filter(created_at__gte=hace_7_dias).count()

        return Response({
            'total_leads': total,
            'leads_por_fuente': fuentes,
            'promedio_presupuesto': round(float(promedio_presupuesto), 2) if promedio_presupuesto else 0,
            'leads_ultimos_7_dias': leads_ultimos_7_dias,
        })


class LeadAISummaryView(APIView):
    
    # POST /leads/ai/summary
    def post(self, request):
        leads = Lead.objects.filter(deleted_at__isnull=True)

        fuente = request.data.get('fuente')
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')

        if fuente:
            leads = leads.filter(fuente=fuente)
        if fecha_inicio:
            leads = leads.filter(created_at__date__gte=fecha_inicio)
        if fecha_fin:
            leads = leads.filter(created_at__date__lte=fecha_fin)

        if not leads.exists():
            return Response(
                {'error': 'No se encontraron leads con los filtros indicados.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Aqui se Preparan datos para el LLM
        leads_data = LeadSerializer(leads, many=True).data
        leads_text = "\n".join([
            f"- {l['nombre']} | {l['fuente']} | presupuesto: {l['presupuesto']} USD | producto: {l['producto_interes']}"
            for l in leads_data
        ])

        prompt = f"""Eres un analista de marketing digital. Analiza estos leads y genera un resumen ejecutivo.

Leads:
{leads_text}

Genera:
1. Análisis general del grupo de leads
2. Fuente principal de leads
3. Recomendaciones accionables para el equipo de ventas
"""

        api_key = os.getenv('ANTHROPIC_API_KEY')

        if not api_key:
            # Mock documentado para cuando no hay API key
            summary = self._mock_summary(leads_data)
        else:
            summary = self._call_anthropic(prompt, api_key)

        return Response({'summary': summary})

    def _call_anthropic(self, prompt, api_key):
        try:
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json',
                },
                json={
                    'model': 'claude-3-haiku-20240307',
                    'max_tokens': 1024,
                    'messages': [{'role': 'user', 'content': prompt}]
                }
            )
            data = response.json()
            return data['content'][0]['text']
        except Exception as e:
            return f"Error al contactar el LLM: {str(e)}"

    def _mock_summary(self, leads_data):
        total = len(leads_data)
        fuentes = {}
        for l in leads_data:
            fuentes[l['fuente']] = fuentes.get(l['fuente'], 0) + 1
        fuente_principal = max(fuentes, key=fuentes.get)

        return (
            f"[MOCK - Simulación de respuesta IA]\n\n"
            f"**Análisis General:** Se analizaron {total} leads en total. "
            f"El grupo muestra interés variado en productos digitales.\n\n"
            f"**Fuente Principal:** '{fuente_principal}' con {fuentes[fuente_principal]} leads.\n\n"
            f"**Recomendaciones:**\n"
            f"1. Reforzar la inversión en '{fuente_principal}' por ser el canal más efectivo.\n"
            f"2. Hacer seguimiento prioritario a leads con presupuesto definido.\n"
            f"3. Diseñar una secuencia de emails de nurturing para leads sin presupuesto.\n\n"
            f"*Para activar el análisis real, configura ANTHROPIC_API_KEY en el .env*"
        )


class LeadWebhookView(APIView):
    
    # POST /leads/webhook — Simula recepción desde Typeform
    def post(self, request):
        # Typeform envía los datos en este formato
        form_response = request.data.get('form_response', {})
        answers = form_response.get('answers', [])

        # Mapear respuestas de Typeform a nuestro modelo
        lead_data = {}
        field_map = {
            'nombre': ['nombre', 'name', 'full_name'],
            'email': ['email'],
            'telefono': ['telefono', 'phone'],
            'fuente': ['fuente', 'source'],
            'producto_interes': ['producto', 'product'],
            'presupuesto': ['presupuesto', 'budget'],
        }

        for answer in answers:
            field_id = answer.get('field', {}).get('ref', '')
            value = answer.get('text') or answer.get('email') or answer.get('number')
            for our_field, aliases in field_map.items():
                if field_id in aliases:
                    lead_data[our_field] = value

        if not lead_data:
            lead_data = request.data

        serializer = LeadSerializer(data=lead_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Lead registrado desde webhook.', 'lead': serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)