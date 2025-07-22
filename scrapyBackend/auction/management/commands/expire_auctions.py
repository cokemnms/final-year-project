# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from auction.models import Auction

# class Command(BaseCommand):
#     help = 'Expires auctions whose time has passed'

#     def handle(self, *args, **kwargs):
#         now = timezone.now()
#         expired_auctions = Auction.objects.filter(is_active=True, expires_at__lte=now)

#         count = expired_auctions.count()
#         for auction in expired_auctions:
#             auction.is_active = False
#             auction.save()
#             self.stdout.write(self.style.SUCCESS(f'Expired: {auction.title}'))

#         if count == 0:
#             self.stdout.write('No auctions to expire.')
#         else:
#             self.stdout.write(self.style.SUCCESS(f'{count} auctions expired.'))
