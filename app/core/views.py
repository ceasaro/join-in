from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from core.models import JoinIn
from core.utils.datetime_utils import utc_now

User = get_user_model()


# Create your views here.
class HomeView(TemplateView):
    template_name = "join_in/home.html"


class JoinView(TemplateView):
    template_name = "join_in/join.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.join_in = None

    def get(self, request, *args, slug=None, **kwargs):
        if slug is None:
            self.join_in = JoinIn.objects.filter().get()
        else:
            self.join_in = JoinIn.objects.get(slug=slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['join_in'] = self.join_in
        for_datetime = utc_now()
        users = self.join_in.get_users(for_datetime)
        for user in users:
            user.joined_period = user.loans.filter(join_in=self.join_in, created__day=for_datetime.day).exists()
            user.balance = self.join_in.balance(user)
        context['users'] = users
        # context['users'] = User.objects.all()
        return context
