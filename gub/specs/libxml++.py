from gub import mirrors
from gub import repository
from gub import targetbuild

url='http://ftp.gnome.org/pub/GNOME/sources/libxml++/2.18/libxml++-2.18.1.tar.gz'

class Libxml_xx_ (targetbuild.AutoBuild):
    source = mirrors.with_vc (repository.TarBall (self.settings.downloads, url))
    def _get_build_dependencies (self):
        return ['glibmm']
    def get_build_dependencies (self):
        return self._get_build_dependencies ()
    def get_dependency_dict (self):
        return {'': self._get_build_dependencies ()}
