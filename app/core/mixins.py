from django.http import JsonResponse
from django.views.generic.base import TemplateResponseMixin


class JSONResponseMixin(TemplateResponseMixin):
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_json_data(context), **response_kwargs)

    def get_json_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        raise NotImplemented()
