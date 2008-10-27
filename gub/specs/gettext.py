from gub import mirrors
from gub import targetbuild
from gub import toolsbuild

class Gettext (targetbuild.AutoBuild):
    # 0.16.1 makes gcc barf on ICE.
    source = 'ftp://ftp.gnu.org/pub/gnu/gettext/gettext-0.15.tar.gz'

    def get_build_dependencies (self):
        return ['libtool']

    def configure_command (self):
        return (targetbuild.AutoBuild.configure_command (self)
                + ' --disable-threads --disable-csharp --disable-java ')

    def configure (self):
        targetbuild.AutoBuild.configure (self)

        ## FIXME: libtool too old for cross compile
        self.update_libtool ()
        self.file_sub ([
                ('(SUBDIRS *=.*)examples', r'\1 '),
                ],
                       '%(builddir)s/gettext-tools/Makefile')

class Gettext__freebsd (Gettext):
    def get_dependency_dict (self):
        d = Gettext.get_dependency_dict (self)
        if self.settings.target_architecture == 'i686-freebsd4':
            d[''].append ('libgnugetopt')
        return d

    def get_build_dependencies (self):
        if self.settings.target_architecture == 'i686-freebsd4':
            return ['libgnugetopt'] + Gettext.get_build_dependencies (self)
        return Gettext.get_build_dependencies (self)

'''
mingw: 0.17
	sed_extract_major='/^[0-9]/{'${nl}'s/^\([0-9]*\).*/\1/p'${nl}q${nl}'}'${nl}'c\'${nl}0${nl}q; \
	sed_extract_minor='/^[0-9][0-9]*[.][0-9]/{'${nl}'s/^[0-9]*[.]\([0-9]*\).*/\1/p'${nl}q${nl}'}'${nl}'c\'${nl}0${nl}q; \
	sed_extract_subminor='/^[0-9][0-9]*[.][0-9][0-9]*[.][0-9]/{'${nl}'s/^[0-9]*[.][0-9]*[.]\([0-9]*\).*/\1/p'${nl}q${nl}'}'${nl}'c\'${nl}0${nl}q; \
	i686-mingw32-windres \
	  "-DPACKAGE_VERSION_STRING=\\\"0.17\\\"" \
	  "-DPACKAGE_VERSION_MAJOR="`echo '0.17' | sed -n -e "$sed_extract_major"` \
	  "-DPACKAGE_VERSION_MINOR="`echo '0.17' | sed -n -e "$sed_extract_minor"` \
	  "-DPACKAGE_VERSION_SUBMINOR="`echo '0.17' | sed -n -e "$sed_extract_subminor"` \
	  -i /home/janneke/vc/gub/target/mingw/src/gettext-0.17/gettext-runtime/intl/libintl.rc -o libintl.res --output-format=coff
sed: expressie #1, teken 11: onbekende opdracht: '\'
sed: expressie #1, teken 25: onbekende opdracht: '\'
sed: expressie #1, teken 39: onbekende opdracht: '\'
'''

class Gettext__mingw (Gettext):

    #source = mirrors.with_template (name='gettext', version='0.17', mirror=mirrors.gnu, format='gz')
    source = Gettext.source
    patches = ['gettext-0.15-mingw.patch']
 
    def config_cache_overrides (self, str):
        return (re.sub ('ac_cv_func_select=yes', 'ac_cv_func_select=no',
               str)
            + '''
# only in additional library -- do not feel like patching right now
gl_cv_func_mbrtowc=${gl_cv_func_mbrtowc=no}
jm_cv_func_mbrtowc=${jm_cv_func_mbrtowc=no}
''')

    def configure_command (self):
        return Gettext.configure_command (self) + ' --disable-libasprintf'

    def configure (self):
        Gettext.configure (self)
        self.file_sub ( [(' gettext-tools ', ' ')],
                        '%(builddir)s/Makefile')

    def install (self):
        ## compile of gettext triggers configure in between.  (hgwurgh.)
        self.update_libtool ()
        Gettext.install (self)

class Gettext__tools (toolsbuild.AutoBuild):
    def get_build_dependencies (self):
        return ['libtool']
    def configure (self):
        toolsbuild.AutoBuild.configure (self)
        self.file_sub ([
                ('(SUBDIRS *=.*)examples', r'\1 '),
                ],
                       '%(builddir)s/gettext-tools/Makefile')
