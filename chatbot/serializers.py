from rest_framework import serializers
from .models import UserData, UserScoring
import random
from datetime import datetime

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'


class UserScoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScoring
        fields = '__all__'


def generate_random_scores():
    # Function to generate random scores
    return {
        'insurance_risk_score': random.uniform(0.0, 1.0),  # Random float between 0 and 1
        'diabetes_risk_score': random.uniform(0.0, 1.0),
        'last_scored': datetime.now()
    }
