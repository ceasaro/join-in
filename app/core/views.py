from django.contrib.auth import get_user_model
from django.http import Http404
from django.views.generic import TemplateView

from core.models import JoinIn

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
        context['users'] = self.join_in.users
        # context['users'] = User.objects.all()
        return context
