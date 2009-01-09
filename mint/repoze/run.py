from repoze.bfg.router import make_app
from repoze.bfg.registry import get_options
from repoze.bfg.urldispatch import RoutesMapper

class MintApp:
    def __init__(self, **kw):
        self.options = get_options(kw)
    
    def get_root(self):
        from mint.repoze.models import get_root as fallback_get_root
        root = RoutesMapper(fallback_get_root)
        root = self.connect_routes(root)
        return root
    
    def connect_routes(self, root):
        root.connect('/', controller='index')
        root.connect('/:video_name', controller='video')
        root.connect('/tags/:tag', controller='tag')
        return root
    
    @property
    def app(self):
        import mint.repoze
        return make_app(self.get_root(), mint.repoze)
    
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
    


# def application(environ, start_response):
#     from mint.repoze.models import get_root as fallback_get_root
#     import mint.repoze
#     
#     get_root = RoutesMapper(fallback_get_root)
#     get_root.connect('/', controller='index')
#     get_root.connect('/:video_name', controller='video')
#     
#     return make_app(get_root, mint.repoze)(environ, start_response)
# 
def app(global_config, **kw):
    """ This function returns a repoze.bfg.router.Router object.  It
    is usually called by the PasteDeploy framework during ``paster
    serve``"""
    # paster app config callback
    return MintApp(**kw)

