from tg import expose, TGController, AppConfig
from tg.util import Bunch
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from wsgiref.simple_server import make_server
import webhelpers2
import webhelpers2.text

class RootController(TGController):
    @expose(content_type='text/plain')
    def index(self):
        logs = DBSession.query(Log).order_by(Log.timestamp.desc()).all()
        return 'Past Greetings\n' + '\n'.join([f"{l.person if l.person else 'World'} - {l.timestamp}" for l in logs])
    
    # http://localhost:8080/hello?person=MyName
    @expose('hello.xhtml')
    def hello(self, person=None):
        DBSession.add(Log(person=person or ''))
        DBSession.commit()
        return dict(person=person)


DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))
DeclarativeBase = declarative_base()
class Log(DeclarativeBase):
    __tablename__ = 'logs'

    uid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    person = Column(String(50), nullable=False)

def init_model(engine):
    DBSession.configure(bind=engine)
    DeclarativeBase.metadata.create_all(engine) # Create tables if they do not exist

config = AppConfig(minimal=True, root_controller=RootController())
config.renderers = ['kajiki']
config['helpers'] = webhelpers2
config.serve_static = True
config.paths['static_files'] = 'public'
config['use_sqlalchemy'] = True
config['sqlalchemy.url'] = 'sqlite:///mydatabase.db'
config['model'] = Bunch(
    DBSession=DBSession, 
    init_model=init_model
    )


application = config.make_wsgi_app()
server_port = 8080
print(f"Serving on http://localhost:{server_port}")
httpd = make_server('', server_port, application)
httpd.serve_forever()