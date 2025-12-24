# management/commands/load_standard_sizes.py
from django.core.management.base import BaseCommand
from products.models import StandardSizeChart

class Command(BaseCommand):
    help = 'Load standard size chart data'
    
    def handle(self, *args, **options):
        sizes_data = [
            {
                'size': '6/7',
                'A_length_from_shoulder': 60.0, 'B_chest_width': 44.0, 'C_chest_width_armholes': 35.8,
                'D_bottom_width': 42.0, 'E_new_width': 36.0, 'F_back_width': 41.8,
                'G_back_width_armholes': 39.8, 'H_neck_width': 16.8, 'I_sleeve_length': 37.0,
                'J_sleeve_width': 17.7, 'K_sleeve_width_above_cuff': 12.2, 'L_sleeve_opening': 7.8,
                'M_cuff_length': 8.8, 'N_armhole': 30.0, 'O_back_neck_drop': 2.2,
                'P_front_neck_drop': 6.3, 'Q_collar_width': 2.0, 'R_shoulder_drop': 4.7,
                'S_waistband_length': 6.8, 'T_forward_shoulder_seam': 3.0, 'front_placement_from_cf': 0.0
            },
            # Add other sizes similarly...
        ]
        
        for data in sizes_data:
            StandardSizeChart.objects.update_or_create(
                size=data['size'],
                defaults=data
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded standard size chart data'))