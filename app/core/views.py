from dateutil.parser import ParserError
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from core.mixins import JSONResponseMixin
from core.models import JoinIn
from core.utils.datetime_utils import utc_now, str_to_datetime, datetime_to_millis, \
    millis_to_datetime

User = get_user_model()


# Create your views here.
class HomeView(TemplateView):
    template_name = "join_in/home.html"


class JoinInBaseView(TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.join_in: JoinIn | None = None

    def get(self, request, *args, slug=None, **kwargs):
        self.get_join_in(slug)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, slug=None, **kwargs):
        self.get_join_in(slug)
        return super().get(request, *args, **kwargs)

    def get_join_in(self, slug):
        if slug is None:
            self.join_in = JoinIn.objects.filter().get()
        else:
            self.join_in = JoinIn.objects.get(slug=slug)
        return self.join_in

    def get_for_datetime(self):
        try:
            for_datetime = millis_to_datetime(int(self.request.GET.get('for_timestamp')))
        except (ParserError, TypeError, ValueError):
            for_datetime = utc_now()
        return for_datetime


class JoinView(JoinInBaseView):
    template_name = "join_in/join.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for_datetime = self.get_for_datetime()
        context['join_in'] = self.join_in
        context['for_timestamp'] = datetime_to_millis(for_datetime)
        users = self.join_in.get_users(for_datetime)
        for user in users:
            user.joined_period = user.has_joined(self.join_in, for_datetime)
            user.balance = self.join_in.balance(for_datetime, user)
        context['users'] = users
        return context


class UserJoinJSONView(JSONResponseMixin, JoinInBaseView):

    def get_user(self):
        user_email = self.kwargs.get('user_email')
        return User.objects.get(email=user_email)

    def get_json_data(self, context):
        user = self.get_user()
        for_datetime = self.get_for_datetime()
        self.join_in.toggle_fee(user, for_datetime)
        return {
            'user': {
                'email': user.email,
                'balance': self.join_in.balance(for_datetime, user),
                'joined_period': user.has_joined(self.join_in, for_datetime)
            }
        }
