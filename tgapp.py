from tg import expose, TGController, AppConfig
from tg.util import Bunch
from sqlalchemy.orm import sessionmaker, scoped_session
from wsgiref.simple_server import make_server
import webhelpers2
import webhelpers2.text

class RootController(TGController):
    @expose()
    def index(self):
        return 'Hello, World!'
    
    # http://localhost:8080/hello?person=MyName
    @expose('hello.xhtml')
    def hello(self, person=None):
        return dict(person=person)
    
config = AppConfig(minimal=True, root_controller=RootController())
config.renderers = ['kajiki']
config['helpers'] = webhelpers2
config.serve_static = True
config.paths['static_files'] = 'public'
config['use_sqlalchemy'] = True
config['sqlalchemy.url'] = 'sqlite:///mydatabase.db'

DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))

def init_model(engine):
    DBSession.configure(bind=engine)

config['model'] = Bunch(
    DBSession=DBSession, 
    init_model=init_model
    )
application = config.make_wsgi_app()
server_port = 8080
print(f"Serving on http://localhost:{server_port}")
httpd = make_server('', server_port, application)
httpd.serve_forever()