from webob import Response
from webob.exc import HTTPNotFound, HTTPMovedPermanently
from repoze.bfg.jinja2 import render_template_to_response
from repoze.bfg.view import bfg_view
from repoze.bfg.interfaces import IRootFactory
from zope.component import getUtility, getGlobalSiteManager

import mint.repoze
from mint.repoze.root import Root
from mint.repoze.models import Video
from mint.repoze.interfaces import IVideoContainer

@bfg_view(name='', for_=Root)
def index(context, request):
    return render_template_to_response('templates/index.html', context=context)

@bfg_view(name='index.html', for_=Root)
def index_page(context, request):
    return render_template_to_response('templates/index.html', context=context)

@bfg_view(name='video_redirect')
def video_redirect(context, request):
    return HTTPMovedPermanently(location = '/videos/' + context.video_name)

@bfg_view(for_=Video)
def video(context, request):
    return render_template_to_response('templates/real_video.html', context=context)

@bfg_view(name='tag')
def tag(context, request):
    gsm = getGlobalSiteManager()
    videos = gsm.getUtility(IVideoContainer).get_videos_by_tag_as_html(context.tag)
    return render_template_to_response('templates/tag.html', context=context, videos=videos)

@bfg_view(name='static', for_=Root)
def static_view(context, request):
    from mint.repoze.urldispatch import static
    return static('mint/repoze/static')(context, request)

