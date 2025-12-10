
from rest_framework import serializers
from .models import Exercise

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'instructions', 'safety_tips', 'image', 'video_url', 'is_active', 'primary_muscle', 'secondary_muscles', 'equipment_type', 'category', 'difficulty_level']

    
class AddExerciseToWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id']