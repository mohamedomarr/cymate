from django.core.management.base import BaseCommand
from django.utils import timezone
from blog.models import EmailVerification


class Command(BaseCommand):
    help = 'Clean up expired email verification codes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Delete codes expired more than this many hours ago (default: 24)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        hours = options['hours']
        dry_run = options['dry_run']

        # Calculate cutoff time
        cutoff_time = timezone.now() - timezone.timedelta(hours=hours)

        # Find expired codes
        expired_codes = EmailVerification.objects.filter(
            expires_at__lt=cutoff_time
        )

        count = expired_codes.count()

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} expired verification codes older than {hours} hours'
                )
            )
            
            if count > 0:
                self.stdout.write('Codes to be deleted:')
                for code in expired_codes[:10]:  # Show first 10
                    self.stdout.write(
                        f'  - {code.email} ({code.verification_type}) - expired {code.expires_at}'
                    )
                if count > 10:
                    self.stdout.write(f'  ... and {count - 10} more')
        else:
            expired_codes.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} expired verification codes'
                )
            )

            # Also clean up used codes older than 7 days
            old_used_codes = EmailVerification.objects.filter(
                is_used=True,
                created_at__lt=timezone.now() - timezone.timedelta(days=7)
            )
            used_count = old_used_codes.count()
            old_used_codes.delete()

            if used_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Also deleted {used_count} old used verification codes'
                    )
                ) 