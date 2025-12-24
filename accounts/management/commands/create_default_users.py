from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Create default admin and operator accounts'
    
    def handle(self, *args, **options):
        # Create default admin account
        admin_username = 'ManagerQC'
        admin_password = 'mqc001'
        
        if not CustomUser.objects.filter(username=admin_username).exists():
            admin_user = CustomUser.objects.create_user(
                username=admin_username,
                password=admin_password,
                role='admin',
                full_name='Manager QC Admin',
                email='admin@magicqc.com',
                is_staff=True,
                is_superuser=True
            )
            admin_user.numeric_password = '0001'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(
                f'✓ Admin account created: {admin_username} / {admin_password} (PIN: 0001)'
            ))
        else:
            # Update existing admin with numeric password
            admin_user = CustomUser.objects.get(username=admin_username)
            admin_user.numeric_password = '0001'
            admin_user.save()
            self.stdout.write(self.style.WARNING(
                f'Admin account "{admin_username}" already exists (PIN updated to 0001)'
            ))
        
        # Create default operator account
        operator_username = 'OperatorQC'
        operator_password = 'mqc002'
        
        if not CustomUser.objects.filter(username=operator_username).exists():
            operator_user = CustomUser.objects.create_user(
                username=operator_username,
                password=operator_password,
                role='operator',
                full_name='QC Operator',
                email='operator@magicqc.com'
            )
            operator_user.numeric_password = '0002'
            operator_user.save()
            self.stdout.write(self.style.SUCCESS(
                f'✓ Operator account created: {operator_username} / {operator_password} (PIN: 0002)'
            ))
        else:
            # Update existing operator with numeric password
            operator_user = CustomUser.objects.get(username=operator_username)
            operator_user.numeric_password = '0002'
            operator_user.save()
            self.stdout.write(self.style.WARNING(
                f'Operator account "{operator_username}" already exists (PIN updated to 0002)'
            ))
        
        self.stdout.write(self.style.SUCCESS('\n=== Default Users Ready ==='))
        self.stdout.write(self.style.SUCCESS(f'Admin Login: {admin_username} / {admin_password}'))
        self.stdout.write(self.style.SUCCESS(f'Operator Login: {operator_username} / {operator_password}'))
