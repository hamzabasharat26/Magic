from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from .models import CustomUser, OperatorSession
from .forms import AdminLoginForm, OperatorLoginForm, UserCreateForm, UserEditForm
from products.models import PurchaseOrder, Product

# Helper functions for role checking
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_operator(user):
    return user.is_authenticated and user.role == 'operator'

# UNIFIED FRONT LOGIN VIEW
def unified_login_view(request):
    """Unified front login page with hexagonal keypad - Database-backed numeric password authentication"""
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('dashboard')
        elif request.user.role == 'operator':
            return redirect('operator_panel')
    
    # Handle POST request from keypad (AJAX or form submission)
    if request.method == 'POST':
        pin = request.POST.get('pin', '')
        
        try:
            # Database lookup: Find user by numeric_password
            user = CustomUser.objects.get(numeric_password=pin, is_active=True)
            
            # Log the user in without password verification (PIN already verified)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # Return JSON response for AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                redirect_url = 'dashboard' if user.role == 'admin' else 'operator_panel'
                return JsonResponse({
                    'success': True,
                    'role': user.role,
                    'redirect_url': redirect_url,
                    'username': user.username
                })
            
            # Standard redirect for form submission
            messages.success(request, f'Welcome, {user.username}!')
            if user.role == 'admin':
                return redirect('dashboard')
            else:
                return redirect('operator_panel')
                
        except CustomUser.DoesNotExist:
            # Invalid PIN
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid access code'
                }, status=400)
            
            messages.error(request, 'Invalid access code. Please try again.')
            return redirect('unified_login')
    
    return render(request, 'accounts/unified_login.html')

# ADMIN AUTHENTICATION VIEWS
def admin_login_view(request):
    """Admin login page for ManagerQC"""
    if request.user.is_authenticated and request.user.is_admin():
        return redirect('dashboard')
    
    # Check for PIN-based authentication from unified login
    pin = request.GET.get('pin')
    if pin == '0001':
        # Auto-login default admin user
        user = authenticate(request, username='ManagerQC', password='mqc001')
        if user and user.role == 'admin':
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'admin':
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Access denied. Admin credentials required.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AdminLoginForm()
    
    return render(request, 'accounts/admin_login.html', {'form': form})

# OPERATOR AUTHENTICATION VIEWS
def operator_login_view(request):
    """Operator login page for OperatorQC"""
    if request.user.is_authenticated and request.user.is_operator():
        return redirect('operator_panel')
    
    # Check for PIN-based authentication from unified login
    pin = request.GET.get('pin')
    if pin == '0002':
        # Auto-login default operator user
        user = authenticate(request, username='OperatorQC', password='mqc002')
        if user and user.role == 'operator':
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('operator_panel')
    
    if request.method == 'POST':
        form = OperatorLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'operator':
                login(request, user)
                messages.success(request, f'Welcome, {user.username}!')
                return redirect('operator_panel')
            else:
                messages.error(request, 'Access denied. Operator credentials required.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = OperatorLoginForm()
    
    return render(request, 'accounts/operator_login.html', {'form': form})

# LOGOUT VIEW (shared)
@login_required
def logout_view(request):
    """Logout view for all users - redirects to unified PIN login"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('unified_login')

# ADMIN USER MANAGEMENT VIEWS
@login_required
@user_passes_test(is_admin, login_url='admin_login')
def user_management_view(request):
    """Admin page to manage users (CRUD operations)"""
    users = CustomUser.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
        'total_users': users.count(),
        'admin_count': users.filter(role='admin').count(),
        'operator_count': users.filter(role='operator').count(),
    }
    return render(request, 'accounts/user_management.html', context)

@login_required
@user_passes_test(is_admin, login_url='admin_login')
def user_create_view(request):
    """Create new user"""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreateForm()
    
    return render(request, 'accounts/user_create.html', {'form': form})

@login_required
@user_passes_test(is_admin, login_url='admin_login')
def user_edit_view(request, user_id):
    """Edit existing user"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('user_management')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'accounts/user_edit.html', {'form': form, 'user_obj': user})

@login_required
@user_passes_test(is_admin, login_url='admin_login')
@require_http_methods(["POST"])
def user_delete_view(request, user_id):
    """Delete user"""
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deleting yourself
    if user.id == request.user.id:
        messages.error(request, 'You cannot delete your own account!')
        return redirect('user_management')
    
    username = user.username
    user.delete()
    messages.success(request, f'User {username} deleted successfully!')
    return redirect('user_management')

# OPERATOR PANEL VIEWS
@login_required
@user_passes_test(is_operator, login_url='operator_login')
def operator_panel_view(request):
    """Main operator panel - single page interface"""
    # Get all purchase orders with products
    purchase_orders = PurchaseOrder.objects.all().prefetch_related('products').order_by('-created_at')
    
    # Get unique brands from POs
    brands = purchase_orders.values_list('brand', flat=True).distinct()
    
    # Get article types
    article_types = PurchaseOrder.ARTICLE_TYPE_CHOICES
    
    # Get available sizes
    sizes = Product.SIZE_CHOICES
    
    # Get active session if exists
    active_session = OperatorSession.objects.filter(
        operator=request.user,
        status='active'
    ).first()
    
    context = {
        'purchase_orders': purchase_orders,
        'brands': brands,
        'article_types': article_types,
        'sizes': sizes,
        'active_session': active_session,
    }
    return render(request, 'accounts/operator_panel.html', context)

@login_required
@user_passes_test(is_operator, login_url='operator_login')
def get_products_by_brand(request):
    """AJAX endpoint to get products filtered by brand"""
    brand = request.GET.get('brand')
    article_type = request.GET.get('article_type')
    
    query = PurchaseOrder.objects.filter(brand=brand)
    if article_type:
        query = query.filter(article_type=article_type)
    
    pos = query.prefetch_related('products')
    
    data = []
    for po in pos:
        for product in po.products.all():
            data.append({
                'po_id': po.id,
                'po_number': po.po_number,
                'product_id': product.id,
                'size': product.size,
                'color': product.color,
                'quantity': product.quantity,
                'article_type': po.get_article_type_display(),
            })
    
    return JsonResponse({'products': data})

@login_required
@user_passes_test(is_operator, login_url='operator_login')
def get_available_sizes(request):
    """AJAX endpoint to get available sizes for selected brand and article"""
    brand = request.GET.get('brand')
    article_type = request.GET.get('article_type')
    
    products = Product.objects.filter(
        purchase_order__brand=brand,
        purchase_order__article_type=article_type
    ).values('size').annotate(count=Count('id')).order_by('size')
    
    sizes = [{'size': p['size'], 'count': p['count']} for p in products]
    
    return JsonResponse({'sizes': sizes})

@login_required
@user_passes_test(is_operator, login_url='operator_login')
@require_http_methods(["POST"])
def start_measurement_session(request):
    """Start a new measurement session"""
    import json
    data = json.loads(request.body)
    
    product_id = data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    
    # End any existing active sessions
    OperatorSession.objects.filter(
        operator=request.user,
        status='active'
    ).update(status='completed')
    
    # Create new session
    session = OperatorSession.objects.create(
        operator=request.user,
        purchase_order=product.purchase_order,
        product=product,
        status='active'
    )
    
    return JsonResponse({
        'success': True,
        'session_id': session.id,
        'message': f'Session started for {product.size} {product.color}',
        'redirect_url': '/measurements/'
    })

@login_required
@user_passes_test(is_operator, login_url='operator_login')
def end_measurement_session(request, session_id):
    """End operator measurement session"""
    session = get_object_or_404(OperatorSession, id=session_id, operator=request.user)
    
    from django.utils import timezone
    session.ended_at = timezone.now()
    session.status = 'completed'
    session.save()
    
    messages.success(request, 'Measurement session completed!')
    return redirect('operator_panel')
