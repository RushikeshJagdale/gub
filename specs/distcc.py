from toolpackage import Tool_package

class Distcc (Tool_package):
	def patch (self):
		self.system ("cd %(srcdir)s && patch -p1 < %(patchdir)s/distcc-substitute.patch")

	def __init__ (self,s):
		Tool_package.__init__ (self,s)
		self.with (version='2.18.3',
			   mirror="http://distcc.samba.org/ftp/distcc/distcc-%(version)s.tar.bz2"),
