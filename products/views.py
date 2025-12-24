from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PurchaseOrder, Product, StandardSizeChart
from .forms import PurchaseOrderForm, ProductForm

def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and hasattr(user, 'role') and user.role == 'admin'

@login_required
@user_passes_test(is_admin, login_url='/accounts/admin/login/')
def dashboard(request):
    purchase_orders = PurchaseOrder.objects.all().order_by('-created_at')
    total_products = Product.objects.count() if Product.objects.exists() else 0
    standard_sizes = StandardSizeChart.objects.all()
    
    # Get size distribution for charts
    size_distribution = Product.objects.values('size').annotate(count=Count('id')) if Product.objects.exists() else []
    
    context = {
        'purchase_orders': purchase_orders,
        'total_products': total_products,
        'standard_sizes': standard_sizes,
        'size_distribution': list(size_distribution),
    }
    return render(request, 'products/dashboard.html', context)

@login_required
@user_passes_test(is_admin, login_url='/accounts/admin/login/')
def create_purchase_order(request):
    if request.method == 'POST':
        po_form = PurchaseOrderForm(request.POST)
        
        if po_form.is_valid():
            purchase_order = po_form.save()
            messages.success(request, f'Purchase Order {purchase_order.po_number} created successfully!')
            return redirect('add_product', po_id=purchase_order.id)
    else:
        po_form = PurchaseOrderForm()
    
    context = {
        'po_form': po_form,
        'title': 'Create New Purchase Order',
    }
    return render(request, 'products/create_po.html', context)

@login_required
@user_passes_test(is_admin, login_url='/accounts/admin/login/')
def add_product(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    standard_sizes = StandardSizeChart.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.purchase_order = purchase_order
            product.save()
            
            messages.success(request, f'Product added to PO-{purchase_order.po_number} successfully!')
            
            # Check if user wants to add another product
            if 'add_another' in request.POST:
                return redirect('add_product', po_id=po_id)
            else:
                return redirect('dashboard')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'purchase_order': purchase_order,
        'standard_sizes': standard_sizes,
    }
    return render(request, 'products/add_product.html', context)

@login_required
def get_standard_measurements(request):
    size = request.GET.get('size')
    try:
        standard_size = StandardSizeChart.objects.get(size=size)
        data = {
            'A': float(standard_size.A_length_from_shoulder),
            'B': float(standard_size.B_chest_width),
            'C': float(standard_size.C_chest_width_armholes),
            'D': float(standard_size.D_bottom_width),
            'E': float(standard_size.E_new_width),
            'F': float(standard_size.F_back_width),
            'G': float(standard_size.G_back_width_armholes),
            'H': float(standard_size.H_neck_width),
            'I': float(standard_size.I_sleeve_length),
            'J': float(standard_size.J_sleeve_width),
            'K': float(standard_size.K_sleeve_width_above_cuff),
            'L': float(standard_size.L_sleeve_opening),
            'M': float(standard_size.M_cuff_length),
            'N': float(standard_size.N_armhole),
            'O': float(standard_size.O_back_neck_drop),
            'P': float(standard_size.P_front_neck_drop),
            'Q': float(standard_size.Q_collar_width),
            'R': float(standard_size.R_shoulder_drop),
            'S': float(standard_size.S_waistband_length),
            'T': float(standard_size.T_forward_shoulder_seam),
            'front_placement': float(standard_size.front_placement_from_cf),
        }
        return JsonResponse(data)
    except StandardSizeChart.DoesNotExist:
        return JsonResponse({'error': 'Standard measurements not found for this size'}, status=404)

@login_required
@user_passes_test(is_admin, login_url='/accounts/admin/login/')
def purchase_order_detail(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    products = purchase_order.products.all()
    
    # Calculate total quantity
    total_quantity = sum(product.quantity for product in products)
    
    context = {
        'purchase_order': purchase_order,
        'products': products,
        'total_quantity': total_quantity,
    }
    return render(request, 'products/po_detail.html', context)