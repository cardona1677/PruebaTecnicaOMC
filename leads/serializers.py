from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):

    FUENTES_PERMITIDAS = ['instagram', 'facebook', 'landing_page', 'referido', 'otro']

    class Meta:
        model = Lead
        fields = [
            'id', 'nombre', 'email', 'telefono', 'fuente',
            'producto_interes', 'presupuesto', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_nombre(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 2 caracteres."
            )
        return value.strip()

    def validate_email(self, value):
        email = value.lower().strip()
        instance = self.instance
        qs = Lead.objects.filter(email=email, deleted_at__isnull=True)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Ya existe un lead registrado con este email."
            )
        return email

    def validate_fuente(self, value):
        if value not in self.FUENTES_PERMITIDAS:
            raise serializers.ValidationError(
                f"Fuente inválida. Opciones permitidas: {', '.join(self.FUENTES_PERMITIDAS)}"
            )
        return value

    def validate_presupuesto(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "El presupuesto no puede ser negativo."
            )
        return value