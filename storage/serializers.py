from rest_framework import serializers
from .models import Storage, Organization


class StorageSerializer(serializers.ModelSerializer):
    organizations_list = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Storage
        fields = ['id', 'name', 'latitude', 'longitude', 'current_waste', 'max_capacity', 'organizations_list']


class OrganizationSerializer(serializers.ModelSerializer):
    storage = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'name', 'latitude', 'longitude', 'waste_generated', 'storage']
