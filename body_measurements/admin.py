from django.contrib import admin
from .models import BodyMeasurement

@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'weight', 'body_fat_percentage', 'gender']
    list_filter = ['gender', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['body_fat_percentage', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Measurements', {
            'fields': ('height', 'weight', 'waist', 'neck', 'hips', 'gender')
        }),
        ('Calculated', {
            'fields': ('body_fat_percentage',)
        }),
        ('Additional', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )
