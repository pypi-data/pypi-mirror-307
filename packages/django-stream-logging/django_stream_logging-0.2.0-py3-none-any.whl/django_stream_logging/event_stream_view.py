from django.http import StreamingHttpResponse
from django.views.generic.base import View
from abc import abstractmethod
import threading
from queue import Queue


class EventStreamView(View):

    messages_queue = Queue()

    def write_default(self, message):
        self.messages_queue.put(message)

    def finish_stream(self):
        self.messages_queue.put("Stream finalizado")
        self.messages_queue.put(None)

    @abstractmethod
    def event_stream(self):
        self.write_error("Metodo 'event_stream' no implementado")
        self.finish_stream()

    def flush_stream(self):
        threading.Thread(target=self.event_stream).start()
        while True:
            message = self.messages_queue.get()
            if message is None:
                break
            yield f"{message}\n"

    def get_event_stream_response(self):
        response = StreamingHttpResponse(self.flush_stream())
        response['Content-Type'] = 'text/event-stream; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

    def get(self, request, *args, **kwargs):
        return self.get_event_stream_response()
