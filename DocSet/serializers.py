from rest_framework import serializers
from .models import DocSet

class DocSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocSet
        fields = '__all__'
