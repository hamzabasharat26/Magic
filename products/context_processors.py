from .models import StandardSizeChart

def standard_sizes(request):
    return {
        'standard_sizes': StandardSizeChart.objects.all()
    }