from django.db import models
from django.utils import timezone
import json

from core.models import TimestampedModel
# Create your models here.

from user.models import CustomUser
from exercise.models import Exercise
class Workout(TimestampedModel):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)  # When the workout actually happened (defaults to created_at if not specified)
    duration = models.PositiveIntegerField(default=0) ## duration is the time in seconds that the workout took
    intensity = models.CharField(max_length=255, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]) ## intensity is the intensity of the workout
    notes = models.TextField(blank=True, null=True) ## notes is a text field that the user can add to the workout
    is_done = models.BooleanField(default=False) ## is_done is a boolean field that indicates whether the workout has been completed
    is_rest_day = models.BooleanField(default=False) ## is_rest_day marks the workout as a rest day but it still counts as a workout
    calories_burned = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True) ## calories burned during the workout
##    body_parts_worked = models.JSONField(default=list, blank=True, null=True) ## body_parts_worked is a json field that contains the body parts worked in the workout
    
    def calculate_calories(self):
        """
        Calculate calories burned using MET (Metabolic Equivalent of Task) method.
        
        Formula: Calories = MET × weight_kg × duration_hours
        
        MET Values:
        - Light Effort (3.0): Small isolation moves with long rests
        - Moderate/General (3.5): Standard gym routine, mixing machines and free weights
        - Vigorous/Bodybuilding (6.0): High intensity, heavy weights, short rest
        - Powerlifting (5.0): Very heavy loads but very long rest periods
        
        Returns the calculated calories.
        """
        from user.models import UserProfile
        
        # Get user body weight (default to 70kg if not set)
        try:
            profile = UserProfile.objects.get(user=self.user)
            body_weight_kg = float(profile.body_weight) if profile.body_weight else 70.0
        except UserProfile.DoesNotExist:
            body_weight_kg = 70.0  # Default average body weight
        
        # Get all workout exercises with their sets
        workout_exercises = WorkoutExercise.objects.filter(workout=self).select_related('exercise').prefetch_related('sets')
        
        if not workout_exercises.exists():
            # No exercises, return 0
            self.calories_burned = 0
            self.save(update_fields=['calories_burned'])
            return 0.0
        
        # Analyze workout to determine MET value
        total_sets = 0
        total_rest_seconds = 0
        compound_count = 0
        isolation_count = 0
        total_volume = 0.0  # Total weight × reps
        max_weight = 0.0
        
        for workout_exercise in workout_exercises:
            exercise = workout_exercise.exercise
            sets = workout_exercise.sets.all()
            
            if exercise.category == 'compound':
                compound_count += 1
            else:
                isolation_count += 1
            
            for exercise_set in sets:
                if exercise_set.is_warmup:
                    continue
                
                total_sets += 1
                weight_kg = float(exercise_set.weight) if exercise_set.weight else 0.0
                reps = exercise_set.reps if exercise_set.reps else 0
                
                if weight_kg > 0 and reps > 0:
                    total_volume += weight_kg * reps
                    max_weight = max(max_weight, weight_kg)
                
                if exercise_set.rest_time_before_set:
                    total_rest_seconds += exercise_set.rest_time_before_set
        
        # Calculate average rest time per set
        avg_rest_seconds = total_rest_seconds / total_sets if total_sets > 0 else 0
        avg_rest_minutes = avg_rest_seconds / 60.0
        
        # Determine MET value based on workout characteristics
        # Use workout intensity if explicitly set, otherwise calculate
        if self.intensity == 'high':
            met_value = 6.0  # Vigorous/Bodybuilding
        elif self.intensity == 'low':
            met_value = 3.0  # Light Effort
        else:
            # Auto-determine based on workout characteristics
            compound_ratio = compound_count / (compound_count + isolation_count) if (compound_count + isolation_count) > 0 else 0
            
            # Powerlifting: Very heavy weights with long rest (>3 min average)
            if max_weight > 100 and avg_rest_minutes > 3.0:
                met_value = 5.0
            # Vigorous/Bodybuilding: High compound ratio, heavy weights, short rest
            elif compound_ratio > 0.5 and max_weight > 50 and avg_rest_minutes < 2.0:
                met_value = 6.0
            # Moderate: Standard gym routine
            elif compound_ratio > 0.3 or total_sets > 15:
                met_value = 3.5
            # Light: Mostly isolation, long rests
            else:
                met_value = 3.0
        
        # Use workout duration (in seconds), convert to hours
        # Duration should include rest time (total time from start to finish)
        workout_duration_hours = self.duration / 3600.0 if self.duration > 0 else 0
        
        # If duration is not set or seems too short, estimate from sets and rest
        if workout_duration_hours < 0.1:  # Less than 6 minutes
            # Estimate: ~30 seconds per set + rest time
            estimated_set_time = total_sets * 0.5  # 30 seconds per set
            estimated_total_seconds = estimated_set_time * 60 + total_rest_seconds
            workout_duration_hours = estimated_total_seconds / 3600.0
        
        # Calculate calories using MET formula
        # Calories = MET × weight_kg × duration_hours
        calories = met_value * body_weight_kg * workout_duration_hours
        
        calories = round(calories, 2)
        self.calories_burned = calories
        self.save(update_fields=['calories_burned'])
        return calories


class WorkoutExercise(TimestampedModel):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  # Link to Exercise template
    order = models.PositiveIntegerField(default=0)
    one_rep_max = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Calculated 1RM from sets
    class Meta:
        ordering = ['order']

# workout/models.py - ExerciseSet
class ExerciseSet(TimestampedModel):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    set_number = models.PositiveIntegerField()  # Keep this, remove 'set'
    reps = models.PositiveIntegerField(default=0)  # Change 'rep' to 'reps'
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # Change to DecimalField
    rest_time_before_set = models.PositiveIntegerField(default=0)
    is_warmup = models.BooleanField(default=False)
    reps_in_reserve = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['set_number']
    
    def __str__(self):
        return f"Set {self.set_number} - {self.reps} reps @ {self.weight}"

class TemplateWorkout(TimestampedModel):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise, through='TemplateWorkoutExercise')
    notes = models.TextField(blank=True, null=True)  # Optional notes for the template

    def __str__(self):
        return self.title

class TemplateWorkoutExercise(TimestampedModel):
    template_workout = models.ForeignKey(TemplateWorkout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

class TrainingResearch(TimestampedModel):
    """Research-backed training information and recommendations"""
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    
    CATEGORY_CHOICES = [
        ('INTENSITY_GUIDELINES', 'Intensity Guidelines'),
        ('PROTEIN_SYNTHESIS', 'Protein Synthesis'),
        ('MUSCLE_GROUPS', 'Muscle Groups'),
        ('MUSCLE_RECOVERY', 'Muscle Recovery'),
        ('REST_PERIODS', 'Rest Periods'),
        ('TRAINING_FREQUENCY', 'Training Frequency'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, blank=True)
    
    # Source information
    source_title = models.CharField(max_length=255, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)
    source_authors = models.JSONField(default=list, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    
    # Evidence quality
    evidence_level = models.CharField(max_length=50, blank=True, null=True)  # high, moderate, low
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)  # 0.0 to 1.0
    
    # Applicability
    applicable_muscle_groups = models.JSONField(default=list, blank=True)  # ["chest", "back", "all"]
    applicable_exercise_types = models.JSONField(default=list, blank=True)  # ["compound", "isolation", "all"]
    
    # Parameters (JSON field for flexible data storage)
    parameters = models.JSONField(default=dict, blank=True)  # e.g., {"recovery_time_hours": 48, "optimal_rpe_range": [7, 9]}
    
    is_active = models.BooleanField(default=True)
    is_validated = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)  # Higher priority = shown first
    
    class Meta:
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title
