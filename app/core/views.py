from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = "join_in/home.html"


class JoinView(TemplateView):
    template_name = "join_in/join.html"
