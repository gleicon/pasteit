PasteIT
=======

Pastebin clone using python, gevent, pygments, redis and bottle.
It is intended as a workbench to pluggable storage backends.
Initially a file based backend is ready, a git based backend is almost ready

Edit pasteit.py to change your base domain and run as a normal python app. 
For serious loads you might want to serve css, js and html from a webserver. In this case, map the backend as /pasteit.
For development/testing run with python pasteit.py

There's a file named functions.sh with shortcuts to integrate shell to pasteit. use xpbcopy to create a text file and xpbpaste to retrieve it. The id returned to xpbcopy is the same that can be appended to pasteit url or used as parameter to xpbpaste.
