from tg.controllers import TGController
from tg import expose, request

class ErrorController(TGController):

    @expose('json')
    def error(self, *args, **kwargs):
        return {
            'status': 'error',
            'path': request.path,
        }

    @expose()
    def document(self, *args, **kwargs):
        return 'Not Found'

    @expose()
    def index(self, *args, **kwargs):
        return 'An error occurred'
