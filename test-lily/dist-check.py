#!/usr/bin/python


import re
import sys
import os
import glob
import optparse


sys.path.insert (0, os.path.split (sys.argv[0])[0] + '/../lib/')

import repository
import tempfile
import misc

def parse_options ():
    p = optparse.OptionParser ()
    p.usage = "dist-check.py BUILD-DIR"
    p.add_option ('--skip',
		  action="store_true",
		  dest="skip",
		  help="return 0 if couldn't get lock.")
    p.add_option ('--repository',
		  action="store",
		  dest="repository",
                  default="",
		  help="CVS repository of lilypond.")
    
    (o,a) = p.parse_args ()
    if len (a) < 1:
	p.print_help()
	sys.exit (2)

    
    o.repository = os.path.abspath (o.repository)
    
    return o,a

def check_cvs ():
    pass

def system (s):
    print s
    if os.system (s):
        raise Exception ('failed')
def popen (s):
    print s
    return os.popen (s)

def get_config_dict (dir):
    d = misc.grok_sh_variables (dir + '/config.make')

    version_dict = misc.grok_sh_variables (d['configure-srcdir'] + '/VERSION')
    d.update (version_dict)

    d['builddir'] = d['configure-builddir']
    d['srcdir'] = d['configure-srcdir']
    
    return d

def check_files (tarball, cvs_repo):
    tarball = os.path.abspath (tarball)

    tarball_dirname = re.sub ('\.tar.*', '', os.path.split (tarball)[1])

    repo = repository.get_repository_proxy (cvs_repo)
    
    dir = tempfile.mkdtemp ()
    print dir
    
    files = popen ('cd %(dir)s && tar xzvf %(tarball)s' % locals ()).readlines ()
    files = [f.strip () for f in files]
    ly_files  = [f for f in files
                 if re.search (r'\.ly$', f)]

    file_dict = dict ((f, 1) for f in files)
    
    entries =  repo.all_cvs_entries ()
    exceptions = ['.cvsignore', 'stepmake/.cvsignore']

    error_found = False
    for e in entries:
        filename = e[0]

        if filename in exceptions:
            continue

        filename = os.path.join (tarball_dirname, filename)
        if not file_dict.has_key (filename):
            print ('file from CVS not distributed: %s' % filename)
            error_found = True

    system ('rm -rf %(dir)s' % locals ())
    if error_found:
        raise Exception ('dist error found')

def main ():
    (options, args) = parse_options ()
    
    builddir = args[0]
    config = get_config_dict (builddir)

    system ('cd %(builddir)s/ && make dist' % locals ())
    tarball = '%(builddir)s/out/lilypond-%(MAJOR_VERSION)s.%(MINOR_VERSION)s.%(PATCH_LEVEL)s.tar.gz' % config
    check_files (tarball, options.repository)

if __name__ == '__main__':
    main ()
