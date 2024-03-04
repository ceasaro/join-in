from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

User = get_user_model()


# Create your views here.
class HomeView(TemplateView):
    template_name = "join_in/home.html"


class JoinView(TemplateView):
    template_name = "join_in/join.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
