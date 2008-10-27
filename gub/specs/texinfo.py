from gub import toolsbuild

class Texinfo__tools (toolsbuild.AutoBuild):
    source = 'ftp://ftp.gnu.org/pub/gnu/texinfo/texinfo-4.11.tar.bz2'
    def patch (self):
        # for 4.11
        self.system ('cd %(srcdir)s/build-aux && chmod +x install-sh config.sub config.guess missing')
    def get_build_dependencies (self):
        return ['ncurses']
