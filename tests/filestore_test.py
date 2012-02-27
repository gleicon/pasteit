import os
import sys

sys.path.append('..')

import datastore

ds = datastore.DataStore(conn="file:///tmp/anewds")

try:
    assert(ds.load("salsichas") == None)
    assert(ds.exists("salsichas") == False)
    assert(ds.save("salsichas", "feitas de papel") == None)
    assert(ds.save("salsonas", "nao feitas de papel") == None)
    assert(ds.load("salsichas") == 'feitas de papel')
    assert(ds.exists("salsichas") == True)
    assert(ds.remove("salsichas") == True)
    assert(ds.exists("salsichas") == False)
    assert(ds.load("salsichas") == None)
    assert(ds.exists("salsonas") == True)
    assert(ds.remove("salsonas") == True)
    assert(ds.exists("salsonas") == False)
    assert(os.path.exists('/tmp/anewds/s/a') == False)
    assert(ds.load("salsichas") == 'nothing') # must fail

except AssertionError, e:
    print "One or more assertions failed. Check your head: ", e
