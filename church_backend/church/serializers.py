from rest_framework import serializers
from .models import user_register,helping_hand,donate,timings

class user_registerSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_register
        fields = '__all__'

class helping_handSerializer(serializers.ModelSerializer):
    class Meta:
        model = helping_hand
        fields = '__all__'
class donateSerializer(serializers.ModelSerializer):
    class Meta:
        model = donate
        fields = '__all__'

class timingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = timings
        fields = '__all__'