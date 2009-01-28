from mint.repoze.models import Video, VideoContainer

videos = dict(
        intro = Video(u'intro', u'', [u'feature', u'intro',]),
        oil_on_ice = Video(u'oil_on_ice', u'', [u'feature', u'arctic', u'water',]),
        toxic_sperm = Video(u'toxic_sperm', u'', [u'feature', u'greenpeace',]),
)

video_container = VideoContainer(**videos)


users = {
    'admin': {
        'id': 'admin',
        'email': 'admin@mint.com',
        'password': 'test'
    }
}