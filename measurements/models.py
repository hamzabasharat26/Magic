from django.db import models
from products.models import Product

class MeasurementSession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class CapturedImage(models.Model):
    session = models.ForeignKey(MeasurementSession, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='captured_images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_reference = models.BooleanField(default=False)

class KeyPoint(models.Model):
    POINT_CHOICES = [
        ('A', 'A - Length from shoulder'),
        ('B', 'B - Chest width'),
        ('C', 'C - Chest width (armholes)'),
        ('D', 'D - Bottom width'),
        ('E', 'E - New width'),
        ('F', 'F - Back width'),
        ('G', 'G - Back width (armholes)'),
        ('H', 'H - Neck width'),
        ('I', 'I - Sleeve length'),
        ('J', 'J - Sleeve width'),
        ('K', 'K - Sleeve width above cuff'),
        ('L', 'L - Sleeve opening'),
        ('M', 'M - Cuff length'),
        ('N', 'N - Armhole'),
        ('O', 'O - Back neck drop'),
        ('P', 'P - Front neck drop'),
        ('Q', 'Q - Collar width'),
        ('R', 'R - Shoulder drop'),
        ('S', 'S - Waistband length'),
        ('T', 'T - Forward shoulder seam'),
    ]
    
    image = models.ForeignKey(CapturedImage, on_delete=models.CASCADE, related_name='keypoints')
    point_type = models.CharField(max_length=1, choices=POINT_CHOICES)
    x_coord = models.FloatField()
    y_coord = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class MeasurementResult(models.Model):
    """Stores validated measurement results"""
    session = models.OneToOneField(MeasurementSession, on_delete=models.CASCADE, related_name='measurement_result')
    size = models.CharField(max_length=20, default='UNKNOWN')
    measured_values = models.JSONField(default=dict)  # Store all measured values
    standard_values = models.JSONField(default=dict)  # Store standard values for comparison
    deviations = models.JSONField(default=dict)  # Store per-measurement deviations
    measurement_details = models.JSONField(default=dict)  # Detailed results for each measurement
    overall_score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    operator_id = models.CharField(max_length=100, null=True, blank=True)
    validation_timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['passed']),
            models.Index(fields=['validation_timestamp']),
        ]
    
    def __str__(self):
        return f"Measurement Result - {self.size} - {'PASS' if self.passed else 'FAIL'}"