from bottle import post, get, run, request, response, abort, template, debug, static_file, redirect
import datetime
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import datastore
import idgenerator 
import throttle
from base62 import base62_encode
import gevent
from gevent import monkey
monkey.patch_all()

BASE_URL = "http://localhost:14100"
STATIC_FILES = "./static"
TEMPLATE_FILES = "./tpl"

ds = datastore.DataStore('file:///tmp/pasteit/')
idgen = idgenerator.IdGenerator("pasteit")
throttle = throttle.ThrottleControl("pasteit")


@get('/')
@get('/index.html')
def index():
    return static_file('index.html', root='%s' % STATIC_FILES)

@get('/shell.html')
def shell():
    return static_file('shell.html', root='%s' % STATIC_FILES)

@get('/css/:f')
def css(f):
    return static_file('%s' % f, root='%s/css' % STATIC_FILES)


@get('/js/:f')
def js(f):
    return static_file('%s' % f, root='%s/js' % STATIC_FILES)


@get('/images/:f')
def imgs(f):
    return static_file('%s' % f, root='%s/images' % STATIC_FILES)


@post('/pasteit')
def pasteit():
    ip = get_real_ip(request)
    r = throttle.check(ip)

    if r is False:
        abort(401, "Not authorized")

    codebody = request.POST['codebody']
    raw = request.POST.get('raw', None)
    if codebody is None:
        abort(500, 'Empty request')

    a = idgen.request()
    id = base62_encode(a)
    r = ds.save("pasteit-%s" % id, codebody)
    if r is False:
        abort(503, 'Internal error saving id %s (%d)' % (id, a))

    if raw is None:
        redirect("%s/%s" % (BASE_URL, id))
    else:
        return id

@get('/:id')
def getdoc(id):
    codebody = ds.load("pasteit-%s" % id)
    if codebody == None: abort(404, 'id not found')
    cc = highlight(codebody, PythonLexer(), HtmlFormatter(style = "colorful")) 
    return template('%s/pasted.tpl' % TEMPLATE_FILES, code=cc, id=id, base_url=BASE_URL)

@get('/raw/:id')
def getdoc(id):
    response.content_type = 'text/plain'
    codebody = ds.load("pasteit-%s" % id)
    if codebody == None: abort(404, 'id not found')
    return codebody

def get_real_ip(req):
    c = req.environ.get("X-Forwarded-For", None)
    if c is None:
        return req.remote_addr
run(host='localhost', port=14100, server='gevent')
