from django.core.management.base import BaseCommand
from django.db.models import Count

from core.models import JoinIn, Loan


class Command(BaseCommand):
    help = "Test command to test some code"

    def add_arguments(self, parser):
        parser.add_argument("--fix", action="store_true",
                            help="If set it will try to fix the found consistency errors.")

    def handle(self, fix, *args, **options):
        self.fix_too_many_fee_per_period(fix)

    def fix_too_many_fee_per_period(self, fix):
        daily_join_ins = JoinIn.objects.filter(membership_period=JoinIn.DAILY)
        loans = Loan.objects.filter(join_in__in=daily_join_ins)
        for loan in (loans
                .values('user_id', 'user__email', 'created__year', 'created__month', 'created__day')
                .annotate(amount=Count('created__day')).filter(amount__gt=1)):
            user_id = loan.get('user_id')
            year = loan.get('created__year')
            month = loan.get('created__month')
            day = loan.get('created__day')
            print(f"{loan.get('user__email')} (id: {user_id}) "
                  f"added {loan.get('amount')} fees on daily join in for day {year}-{month}-{day} ")
            if fix:
                loans_to_delete = loans.filter(user_id=user_id, created__day=day,
                                               created__month=month,
                                               created__year=year).order_by('created')[1:]
                print(f"Deleting membership {loans_to_delete}")
                loans.delete()