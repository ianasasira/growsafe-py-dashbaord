class NotificationService:
    def notify_expiring_batch(self, batch):
        from apps.notifications.models import Notification
        from apps.accounts.models import User
        
        admins = User.objects.filter(company=batch.company, role__in=['company_admin', 'company_staff'])
        
        for admin in admins:
            Notification.objects.create(
                user=admin,
                company=batch.company,
                notification_type='warning',
                title='Batch Expiring Soon',
                message=f'Batch {batch.batch_number} will expire on {batch.expiry_date}.',
                link=f'/dashboard/batches/{batch.id}/',
            )
    
    def notify_recall(self, recall):
        from apps.notifications.models import Notification
        from apps.accounts.models import User
        
        admins = User.objects.filter(company=recall.company, role__in=['company_admin', 'company_staff'])
        
        for admin in admins:
            Notification.objects.create(
                user=admin,
                company=recall.company,
                notification_type='alert',
                title='Product Recall Initiated',
                message=f'Recall initiated for batch {recall.batch.batch_number}.',
                link=f'/dashboard/recalls/{recall.id}/',
            )
