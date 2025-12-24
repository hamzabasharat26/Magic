from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Custom user model with role-based access"""
    ROLE_CHOICES = [
        ('admin', 'Admin (ManagerQC)'),
        ('operator', 'Operator (OperatorQC)'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='operator')
    full_name = models.CharField(max_length=100, blank=True)
    numeric_password = models.CharField(max_length=4, blank=True, null=True, help_text='4-digit numeric PIN for login')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_operator(self):
        return self.role == 'operator'

class OperatorSession(models.Model):
    """Track operator measurement sessions"""
    operator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'operator'})
    purchase_order = models.ForeignKey('products.PurchaseOrder', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    measurements_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused')
    ], default='active')
    
    class Meta:
        verbose_name = 'Operator Session'
        verbose_name_plural = 'Operator Sessions'
    
    def __str__(self):
        return f"{self.operator.username} - {self.product} - {self.started_at}"
