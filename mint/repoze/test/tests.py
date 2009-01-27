from nose.tools import assert_true, assert_equals, assert_raises, with_setup
from webtest import TestApp, AppError
from mint.repoze.run import MintApp
from mint.repoze.test.data import users

from os.path import abspath, dirname, join

app = TestApp('config:' + join(dirname(__file__), 'testing.ini'))

def login(user=users[u'admin'], url=u'/login.html', app=app):
    u"This is not a test!  It is a utility for other tests"
    res = app.get(url)
    form = res.forms[u'login']
    form[u'login'] = user[u'id']
    form[u'password'] = user[u'password']
    res = form.submit()
    res = res.follow()
    res = res.follow()
    assert_true(
        user[u'user'] in res.body,
        u'Should be logged in.'
    )
    assert_true(
        u'logout' in res.body,
        u'Should be a link to logout.'
    )


def test_valid_root():
    """root returns a `200` status code"""
    res = app.get('/')
    assert "200" in res.status

def test_root_not_404():
    """root does not return Not Found"""
    res = app.get('/')
    assert "404" not in res.status

def test_index_page():
    """root page contains `home`"""
    res = app.get('/')
    assert_true(
        'home' in res.body,
        '`home` should be within the page returned by `/`'
    )

def test_root_equals_index():
    """`/` equals `/index.html`"""
    res1 = app.get('/')
    res2 = app.get('/index.html')
    assert_true(
        res1.body == res2.body,
        '`/` should be the same as `index.html`'
    )

def test_ads_on_index():
    """Ad section on homepage"""
    res = app.get('/')
    assert_true(
        'ad-section' in res.body,
        'ad-section should be in the `index.html` page'
    )

def test_video_page():
    """video page contains video name"""
    res = app.get('/videos/intro')
    assert_true(
        'intro' in res.body,
        u'video name should be within the video page'
    )

def test_intro_video_on_root():
    """root has a `intro` video"""
    res = app.get('/')
    assert 'div class="videoplayer" id="intro"' in res.body

def test_intro_video_page():
    """`/video/intro` has a `intro` video"""
    res = app.get('/videos/intro')
    assert 'div class="videoplayer" id="intro"' in res.body
    res = res.click('feature')
    test_tag_page(res)

def test_flibble_page_returns_404():
    """`/flibble` isn't a page"""
    assert_raises(
        AppError,
        app.get,
        '/videos/flibble'
    )
    print u'who the hell called their video `flibble`'

def test_oil_on_ice_video(res=None):
    """`/oil_on_ice` video exists and has tags"""
    if not res:
        res = app.get('/videos/oil_on_ice')
    assert_true(
     'div class="videoplayer" id="oil_on_ice"' in res.body,
     "Oil on Ice video should be there"
    )
    assert_true(
     'div id="tags"' in res.body,
     "Tags div should be there"
    )
    
    for tag in ['feature', 'arctic', 'water']:
        assert_true(
            tag in res.body,
            "%s tag should be in body" % tag
        )

def test_legacy_video_redirect():
    """/[video_name] redirects to /videos/[video_name]"""
    res = app.get('/intro')
    assert_true(
        '301' in res.status,
        u'response should be a 301 response, not %s' % res.status
    )

def test_tag_page(res=None):
    """check contents of a tag page | check links on page return real video pages"""
    if res == None:
        res = app.get('/tags/feature')
    assert_true(
        '200' in res.status,
        u'Server should return OK'
    )
    print res
    assert_true(
        'feature' in res.body,
        u'correct tag should be in body'
    )
    assert_true(
        'intro' in res.body,
        u'intro should be a featured video'
    )
    
    res = res.click('oil_on_ice')
    test_oil_on_ice_video(res)

def test_reachable_static():
    """Static files are accessible at `/static/`"""
    res = app.get('/static/css/screen.css')
    assert_true(
        '200' in res.status,
        u'`200` not in response'
    )

def test_reachable_zopish_static():
    """Static files are accessible via zope syntax (/@@static/)"""
    res = app.get('/@@static/css/screen.css')
    assert_true(
        '200' in res.status,
        u'`200` not in response'
    )

@with_setup(login)
def test_add_video():
    """Publish a new video through the web interface"""
    res = app.get('/videos/add_video.html')
    assert_true(
        '200' in res.status,
        u'add video url not available'
    )
    
    res = app.post(
        '/videos/add_video.html', 
        {
            'video.name': 'testvid1',
            'video.description': 'A test video for our tests',
            'video.tags': 'foo,bar,baz'
        }
    )
    print res
    assert_true(
        'successful' in res.body,
        u'post not successful'
    )
    
    res = app.get('/videos/testvid1')
    assert_true(
        '200' in res.status,
        u'new video not live'
    )
    
    res = app.get('/tags/foo')
    assert_true(
        'testvid1' in res.body,
        u'video not searchable by tags'
    )
    

def test_rules_the_world():
    """This app rules the world"""
    print u'well done you broke the mould'
    assert True

