from django.db import models
from django.core.validators import MinValueValidator

class PurchaseOrder(models.Model):
    BRAND_CHOICES = [
        ('ZARA', 'ZARA'),
        ('INDITEX', 'INDITEX'),
        ('H&M', 'H&M'),
        ('OTHER', 'Other'),
    ]
    
    ARTICLE_TYPE_CHOICES = [
        ('sweat_shirt', 'Sweat Shirt'),
        ('hoodie', 'Hoodie'),
        ('tshirt', 'T-Shirt'),
        ('pants', 'Pants'),
    ]
    
    po_number = models.CharField(max_length=100, unique=True, verbose_name="PO Number")
    date = models.DateField()
    brand = models.CharField(max_length=100, choices=BRAND_CHOICES)
    origin_country = models.CharField(max_length=100, verbose_name="Origin/Country")
    article_type = models.CharField(max_length=20, choices=ARTICLE_TYPE_CHOICES, default='sweat_shirt')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO-{self.po_number}"

class Product(models.Model):
    SIZE_CHOICES = [
        ('6/7', '6/7 Years'),
        ('7/8', '7/8 Years'),
        ('8/9', '8/9 Years'),
        ('9/10', '9/10 Years'),
        ('10/11', '10/11 Years'),
        ('12/13', '12/13 Years'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='products')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.purchase_order.article_type} - {self.size} - {self.color}"

class StandardSizeChart(models.Model):
    SIZE_CHOICES = [
        ('6/7', '6/7 Years'),
        ('7/8', '7/8 Years'), 
        ('8/9', '8/9 Years'),
        ('9/10', '9/10 Years'),
        ('10/11', '10/11 Years'),
        ('12/13', '12/13 Years'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, unique=True)
    
    # Measurements from the provided chart (in cm)
    A_length_from_shoulder = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="A - Length from shoulder")
    B_chest_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="B - Chest width")
    C_chest_width_armholes = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="C - Chest width (12 armholes)")
    D_bottom_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="D - Bottom width")
    E_new_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="E - New width")
    F_back_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="F - Back width")
    G_back_width_armholes = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="G - Back width (12 armholes)")
    H_neck_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="H - Neck width")
    I_sleeve_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="I - Sleeve length")
    J_sleeve_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="J - Sleeve width")
    K_sleeve_width_above_cuff = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="K - Sleeve width above cuff")
    L_sleeve_opening = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="L - Sleeve opening")
    M_cuff_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="M - Cuff length")
    N_armhole = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="N - Armhole")
    O_back_neck_drop = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="O - Back neck drop")
    P_front_neck_drop = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="P - Front neck drop")
    Q_collar_width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Q - Collar width")
    R_shoulder_drop = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="R - Shoulder drop")
    S_waistband_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="S - Waistband length")
    T_forward_shoulder_seam = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="T - Forward shoulder seam")
    front_placement_from_cf = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Front placement from CF")
    
    class Meta:
        verbose_name = "Standard Size Chart"
        verbose_name_plural = "Standard Size Charts"
    
    def __str__(self):
        return f"Standard Size - {self.size}"