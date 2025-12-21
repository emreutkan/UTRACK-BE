from django.db import models
from django.utils import timezone
from core.models import TimestampedModel
from user.models import CustomUser
import math

class BodyMeasurement(TimestampedModel):
    """Store user body measurements for tracking progress"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='body_measurements')
    
    # Measurements (all in cm)
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    waist = models.DecimalField(max_digits=5, decimal_places=2, help_text="Waist measurement in cm")
    neck = models.DecimalField(max_digits=5, decimal_places=2, help_text="Neck measurement in cm")
    hips = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Hips measurement in cm (required for women)")
    
    # Calculated fields
    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Calculated body fat % using US Navy method")
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], help_text="Gender for body fat calculation")
    
    # Optional notes
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.created_at.date()} - {self.body_fat_percentage}% BF"
    
    def calculate_body_fat_navy_method(self):
        """
        Calculate body fat percentage using US Navy method.
        Returns body fat percentage or None if calculation fails.
        """
        try:
            # Convert to float for calculations
            height_cm = float(self.height)
            waist_cm = float(self.waist)
            neck_cm = float(self.neck)
            
            if self.gender == 'male':
                # Men: 495 / (1.0324 - 0.19077 * log10(waist - neck) + 0.15456 * log10(height)) - 450
                if waist_cm <= neck_cm:
                    return None  # Invalid measurement
                
                log_waist_neck = math.log10(waist_cm - neck_cm)
                log_height = math.log10(height_cm)
                
                denominator = 1.0324 - (0.19077 * log_waist_neck) + (0.15456 * log_height)
                
                if denominator <= 0:
                    return None
                
                body_fat = (495 / denominator) - 450
                
            else:  # female
                # Women: 495 / (1.29579 - 0.35004 * log10(waist + hips - neck) + 0.22100 * log10(height)) - 450
                if not self.hips:
                    return None  # Hips required for women
                
                hips_cm = float(self.hips)
                
                if (waist_cm + hips_cm) <= neck_cm:
                    return None  # Invalid measurement
                
                log_waist_hips_neck = math.log10(waist_cm + hips_cm - neck_cm)
                log_height = math.log10(height_cm)
                
                denominator = 1.29579 - (0.35004 * log_waist_hips_neck) + (0.22100 * log_height)
                
                if denominator <= 0:
                    return None
                
                body_fat = (495 / denominator) - 450
            
            # Ensure body fat is within reasonable range (0-50%)
            if body_fat < 0 or body_fat > 50:
                return None
            
            return round(body_fat, 2)
            
        except (ValueError, TypeError, ZeroDivisionError) as e:
            return None
    
    def save(self, *args, **kwargs):
        # Auto-calculate body fat when saving
        # If gender not set, try to get from user
        if not self.gender and hasattr(self, 'user') and self.user:
            self.gender = self.user.gender or 'male'
        
        if self.height and self.weight and self.waist and self.neck:
            if self.gender == 'female' and not self.hips:
                # Don't calculate if hips missing for women
                self.body_fat_percentage = None
            else:
                self.body_fat_percentage = self.calculate_body_fat_navy_method()
        super().save(*args, **kwargs)
