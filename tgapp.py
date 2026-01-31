from tg import expose, TGController, AppConfig
from wsgiref.simple_server import make_server

class RootController(TGController):
    @expose()
    def index(self):
        return "Hello, World!"
    
    # http://localhost:8080/hello?person=MyName
    @expose()
    def hello(self, person):
        return f"Hello, {person}!"
    
config = AppConfig(minimal=True, root_controller=RootController())
application = config.make_wsgi_app()

print("Serving on http://localhost:8080")
httpd = make_server('', 8080, application)
httpd.serve_forever()