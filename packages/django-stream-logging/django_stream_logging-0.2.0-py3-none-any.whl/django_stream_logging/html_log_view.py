from ..message_log_stream import MessageLogStream
from django.http import HttpResponse
from django.views.generic.base import View


class HtmlLogView(View, MessageLogStream):

    content_log = []

    def write_default(self, message):
        self.content_log.append(message)

    def start_stream(self):
        self.content_log = []
        self.write_info("Se ha iniciado el registro")

    def finish_stream(self):
        self.write_info("Se ha finalizado el registro")

    def write_warning(self, message):
        self._add_to_log(message, "text-warning")

    def write_danger(self, message):
        self._add_to_log(message, "text-danger")

    def write_info(self, message):
        self._add_to_log(message, "text-info")

    def write_success(self, message):
        self._add_to_log(message, "text-success")

    def write_error(self, message):
        self._add_to_log(message, "text-danger")

    def write_notice(self, message):
        self._add_to_log(message, "text-primary")

    def _add_to_log(self, message, type_class=None):
        if type_class:
            message = f"<span class=\"{type_class}\">{message}</span>"
        self.content_log.append(message)

    def _get_content_html(self):
        return "<br>".join(self.content_log)

    def get_html_http_response(self):
        response = HttpResponse(self._get_content_html())
        response['Content-Type'] = 'text/html'
        response['Cache-Control'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs):
        return self.get_html_http_response()
