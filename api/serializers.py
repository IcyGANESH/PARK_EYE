from rest_framework import serializers
from .models import Suspected, VehicleRecord, Location, Police


class SuspectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspected
        fields = '__all__'


class VehicleRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRecord
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class PoliceSerializer(serializers.ModelSerializer):
    locations = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Location.objects.all()
    )

    class Meta:
        model = Police
        fields = ['id', 'username', 'password', 'locations']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        locations = validated_data.pop('locations', [])
        police = Police(username=validated_data['username'])
        police.set_password(validated_data['password'])
        police.save()
        police.locations.set(locations)
        return police

    def update(self, instance, validated_data):
        locations = validated_data.pop('locations', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        if locations is not None:
            instance.locations.set(locations)

        instance.save()
        return instance
