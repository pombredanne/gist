#!/usr/bin/env python

from optparse import OptionParser
import os, sys, string, pprint
from cStringIO import StringIO
import urllib2, urllib


optparser = OptionParser("usage: %prog inputdir [options] inputdir")
optparser.set_defaults(secret="")
optparser.add_option( "-p", "--private",
        action="store_true", dest="private",
        help="The private secret." )


(opts, filenames) = optparser.parse_args()


def write(filenames):
    out = {}
    counter = 1

    for i in filenames:
        if os.path.isfile(i):
            info = os.path.splitext(i)
            f = open(i)
            fileStr = StringIO(f.read()).getvalue()
            ext_key = "file_ext[gistfile%s]" % counter
            name_key = "file_name[gistfile%s]" % counter
            content_key = "file_contents[gistfile%s]" % counter
            out[ext_key] = info[1]
            out[name_key] = i
            out[content_key] = fileStr
            counter = counter + 1
        
    if opts.private:
        out['private'] = 'on'

    out['login'] = os.popen('git config --global github.user').read().strip()
    out['token'] = os.popen('git config --global github.token').read().strip()


    pp = pprint.PrettyPrinter(indent=4)

    url = 'http://gist.github.com/gists'
    data = urllib.urlencode(out)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)


    print(response.geturl())


if len(filenames) == 0:
    print "No args given.."
    sys.exit(1)

write(filenames)
