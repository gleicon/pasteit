from bottle import post, get, run, request, response, abort, template, debug, static_file, redirect
import datetime
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import datastore
import idgenerator 
from base62 import base62_encode

BASE_URL = "http://localhost:8080"

ds = datastore.DataStore('file:///tmp/pasteit/')
idgen = idgenerator.IdGenerator()

@get('/')
@get('/index.html')
def index():
    return static_file('index.html', root='./static/')

@get('/css/:f')
def css(f):
    return static_file('%s' % f, root='./static/css/')

@get('/js/:f')
def css(f):
    return static_file('%s' % f, root='./static/js/')

@get('/images/:f')
def css(f):
    return static_file('%s' % f, root='./static/images/')


@post('/pasteit')
def pasteit():
    codebody = request.POST['codebody']
    if codebody == None: abort(500, 'Empty request')
    a = idgen.request()
    id = base62_encode(a)
    r = ds.save("pasteit-%s" % id, codebody)
    if r == False: abort(503, 'Internal error saving id %s (%d)' % (id, a))
    redirect("%s/%s" %(BASE_URL, id))

@get('/:id')
def getdoc(id):
    codebody = ds.load("pasteit-%s" % id)
    if codebody == None: abort(404, 'id not found')
    cc = highlight(codebody, PythonLexer(), HtmlFormatter(style = "colorful")) 
    return template('tpl/pasted.tpl', code=cc, id=id, base_url=BASE_URL)

@get('/raw/:id')
def getdoc(id):
    response.content_type = 'text/plain'
    codebody = ds.load("pasteit-%s" % id)
    if codebody == None: abort(404, 'id not found')
    return codebody

debug(True)
run()