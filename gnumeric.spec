Name:             gnumeric
Epoch:            1
Version:          1.12.17
Release:          3%{?dist}
Summary:          Spreadsheet program for GNOME
#LGPLv2+:
#plugins/gda/plugin-gda.c
#plugins/fn-financial/sc-fin.c
#plugins/plan-perfect/charset.c
#src/widgets/gnumeric-lazy-list.h
#GPLv3+:
#src/parser.c
License:          GPLv2+ and GPLv3+ and LGPLv2+
URL:              http://projects.gnome.org/gnumeric/
Source:           ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/1.12/%{name}-%{version}.tar.xz
#BuildRequires:    libgnomedb-devel >= 3.0.0
BuildRequires:    desktop-file-utils
BuildRequires:    goffice-devel >= 0.9.2
BuildRequires:    intltool
BuildRequires:    libgda-ui-devel
BuildRequires:    perl(ExtUtils::Embed)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(IO::Compress::Gzip)
BuildRequires:    psiconv-devel
BuildRequires:    pygobject3-devel
BuildRequires:    pygtk2-devel
BuildRequires:    rarian-compat
BuildRequires:    zlib-devel
Requires:         hicolor-icon-theme
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Gnumeric is a spreadsheet program for the GNOME GUI desktop
environment.


%package devel
Summary:          Files necessary to develop gnumeric-based applications
Requires:         %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Gnumeric is a spreadsheet program for the GNOME GUI desktop
environment. The gnumeric-devel package includes files necessary to
develop gnumeric-based applications.


%package plugins-extras
Summary:          Files necessary to develop gnumeric-based applications
Requires:         %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description plugins-extras
This package contains the following additional plugins for gnumeric:
* gda and gnomedb plugins:
  Database functions for retrieval of data from a database.
* perl plugin:
  This plugin allows writing of plugins in perl


%prep
%setup -q

chmod -x plugins/excel/rc4.?


%build
%configure --enable-ssindex
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --all-name --with-gnome

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --delete-original                                  \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
  --vendor fedora                                                       \
%endif
  --dir $RPM_BUILD_ROOT%{_datadir}/applications                         \
  --add-category Office                                                 \
  --add-category Spreadsheet                                            \
  --remove-category Education                                           \
  --remove-category Science                                             \
  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

#remove unused mime type icons
rm $RPM_BUILD_ROOT/%{_datadir}/pixmaps/gnome-application-*.png
rm $RPM_BUILD_ROOT/%{_datadir}/pixmaps/%{name}/gnome-application-*.png

#remove spurious .ico thing
rm $RPM_BUILD_ROOT/usr/share/pixmaps/win32-%{name}.ico
rm $RPM_BUILD_ROOT/usr/share/pixmaps/%{name}/win32-%{name}.ico

#remove .la files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
     glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc HACKING AUTHORS ChangeLog NEWS BUGS README COPYING
%{_bindir}/*
%{_libdir}/libspreadsheet-%{version}.so
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/%{version}
%exclude %{_libdir}/%{name}/%{version}/plugins/perl-*
%exclude %{_libdir}/%{name}/%{version}/plugins/gdaif
%exclude %{_libdir}/%{name}/%{version}/plugins/psiconv
%{_datadir}/glib-2.0/schemas/org.gnome.gnumeric.*
%{_datadir}/pixmaps/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{version}
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
%{_datadir}/applications/fedora-%{name}.desktop
%else
%{_datadir}/applications/%{name}.desktop
%endif
%{_datadir}/appdata/%{name}.appdata.xml
# The actual omf file is in gnumeric.lang, but find-lang doesn't own the dir!
%dir %{_datadir}/omf/%{name}
%{_mandir}/man1/*

%files devel
%{_libdir}/libspreadsheet.so
%{_libdir}/pkgconfig/libspreadsheet-1.12.pc
%{_includedir}/libspreadsheet-1.12

%files plugins-extras
%{_libdir}/%{name}/%{version}/plugins/perl-*
%{_libdir}/%{name}/%{version}/plugins/gdaif
%{_libdir}/%{name}/%{version}/plugins/psiconv
%{_libdir}/goffice/*/plugins/gnumeric/gnumeric.so
%{_libdir}/goffice/*/plugins/gnumeric/plugin.xml


%changelog
* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.12.17-3
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.12.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.17-1
- Updated to 1.12.17

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.12.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.16-1
- Updated to 1.12.16

* Sun May 04 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.15-1
- Updated to 1.12.15

* Mon Apr 21 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.14-1
- Updated to 1.12.14

* Fri Mar 21 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.13-1
- Updated to 1.12.13

* Mon Mar 17 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.12-2
- Fixed crash on strange .xls files (RH #1076912)

* Tue Mar 04 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.12-1
- Updated to 1.12.12

* Wed Feb 19 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.11-1
- Updated to 1.12.11

* Sun Feb 16 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.10-1
- Updated to 1.12.10

* Wed Jan 01 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.9-1
- Updated to 1.12.9

* Tue Oct 15 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.8-1
- Updated to 1.12.8
- Added appdata.xml

* Sat Sep 14 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.7-1
- Updated to 1.12.7

* Sun Aug 25 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.5-1
- Updated to 0.12.5
- Added libgda and psiconv support

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:1.12.4-2
- Perl 5.18 rebuild
- Build-require dependencies for embedder

* Wed Jul 17 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.4-1
- Updated to 1.12.4

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:1.12.3-2
- Perl 5.18 rebuild

* Sun Jun 30 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.3-1
- Updated to 1.12.3
- Corrected incorrect %%changelog dates

* Mon Apr 29 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.2-1
- Updated to 1.12.2

* Sat Mar 09 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.1-1
- Updated to 1.12.1

* Sun Feb 17 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1:1.12.0-3
- De-vendorize desktop file on F19+ (https://fedorahosted.org/fesco/ticket/1077)
- Remove category 'Education' from desktop file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.0-1
- Updated to 1.12.0

* Sun Nov 18 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.90-1
- Updated to 1.11.90

* Mon Sep 10 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.6-2
- Added pygobject3-devel to BuildRequires (RH #849487)

* Sun Sep 09 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.6-1
- Updated to 1.11.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Julian Sikorski <belegdol@fedoraproject.org>- 1:1.11.5-1
- Updated to 1.11.5
- Updated the License tag: gnumeric is now GPLv2+ and GPLv3+ and LGPLv2+

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1:1.11.4-2
- Perl 5.16 rebuild

* Tue Jun 26 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.4-1
- Updated to 1.11.4

* Mon Jun 25 2012 Petr Pisar <ppisar@redhat.com> - 1:1.11.3-4
- Perl 5.16 rebuild

* Tue Jun 19 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1:1.11.3-3
- Remove "Science" category from menu entry (#833321)

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1:1.11.3-2
- Perl 5.16 rebuild

* Sun Apr 22 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.3-1
- Updated to 1.11.3

* Tue Mar 13 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.2-1
- Updated to 1.11.2

* Sat Jan 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.11.1-1
- Updated to 1.11.1 and updated BuildRequires accordingly
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated the scriptlets to the latest spec
- GConf2 is no more

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1:1.10.17-2
- Rebuild for new libpng

* Tue Aug 02 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.17-1
- Updated to 1.10.17
- Dropped the included patch

* Sat Jul 30 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.16-4
- Fixed a parsing crash using a patch from upstream git (RH #726860)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:1.10.16-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1:1.10.16-2
- Perl mass rebuild

* Sat Jun 18 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.16-1
- Updated to 0.8.16
- Switched to .xz sources
- Dropped included patch

* Thu May 26 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.15-2
- Fix crasher (RH #707965)

* Sun May 22 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.15-1
- Updated to 1.10.15
- Updated GSettings scriptlets to the latest version

* Sun Mar 27 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.14-2
- Added missing GSettings scriptlets
- Only use GSettings on Fedora >= 14

* Sat Mar 26 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.14-1
- Updated to 1.10.14
- Added GSettings schemas to %%files

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.13-1
- Updated to 1.10.13

* Thu Dec 02 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.12-1
- Updated to 1.10.12

* Sat Oct 02 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.11-1
- Updated to 1.10.11

* Wed Sep 29 2010 jkeating - 1:1.10.10-3
- Rebuilt for gcc bug 634757

* Thu Sep 16 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.10-2
- Don't overwrite a good icon with an ancient one (RH #634582)

* Mon Sep 06 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1.10.10-1
- Updated to 1.10.10

* Tue Aug 17 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1.10.9-1
- Updated to 1.10.9

* Sat Aug 07 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.8-1
- Updated to 1.10.8
- Dropped scrollkeeper scriptlets since they are no longer needed
- Updated icon cache and gconf scriptlets to the latest spec

* Thu Aug 05 2010 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.10.0-2
- Rebuilt for goffice 0.8.8
- Switched to wildcards for goffice plugin path

* Mon Feb 22 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.10.0-1
- New upstream

* Thu Dec 31 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.9.17-3
- Upstream bump to 1.9.17
- Apply gnome bz patch #605043
- BR goffice-devel >= 1.7.17
- Change goffice plugins to 0.7.17

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.9.16-2
- rebuild against perl 5.10.1

* Mon Nov 30 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.9.16-1
- New upstream

* Wed Oct 21 2009 Robert Scheck <robert@fedoraproject.org> 1:1.8.4-5
- Applied 4 patches from the 1.8 stable branch (#500890, #505001)

* Mon Oct 12 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.8.4-4
- Resolve rhbz #500890

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.8.4-2
- Resolved rhbz #495314

* Tue Apr 07 2009 Robert Scheck <robert@fedoraproject.org> 1:1.8.4-1
- Upgrade to 1.8.4 (#491769)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.8.2-6
- Disable gdaif and gnome-db plugins
- Resolves CVE-2009-5983

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1:1.8.2-5
- Rebuild for Python 2.6

* Mon Nov 17 2008 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.8.2-4
- Version bump

* Mon Nov 17 2008 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1:1.8.2-3
- Changed the desktop patch

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:1.8.2-2
- add Requires for versioned perl (libperl.so)

* Sat Mar  8 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.8.2-1
- New upstream release 1.8.2

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.8.1-2
- Autorebuild for GCC 4.3

* Fri Jan 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.8.1-1
- New upstream release 1.8.1
- Split of perl and libgda/libgnomedb plugins into gnumeric-plugins-extras

* Thu Nov 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-13
- Fix opening of csv files in non-English locales (bz 385441)

* Wed Sep 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-12
- Replace GPL incompatible licensed md5 code with GPL compatible code from
  gnulib

* Fri Aug 31 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-11
- Fix Source0 URL

* Mon Aug  6 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-10
- Update License tag for new Licensing Guidelines compliance
- Don't regenerate all the autoxxx stuff (not needed) this fixes building with
  the latest intltool

* Sun Jun 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-9
- Remove yelp Requires again <sigh> (bz 243361)

* Fri Jun  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-8
- Add yelp Requires so that the help will always work (bz 243361)

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-7
- Build against new libgda + libgnomedb

* Mon Feb 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-6
- Change BuildRequires: libgsf-devel to libgsf-gnome-devel to fix rawhide build

* Sat Sep  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-5
- Various specfile cleanups
- Don't own /usr/share/omf (bug 205667)

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-4
- FE6 Rebuild

* Fri Jul 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-3
- Fix idl file being in both the main and the devel package
- Move libspreadsheet.so symlink to the devel package

* Sun May 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-2
- Add Patch3 fixing gnumeric not finding its help files (bz 192581).

* Tue May  2 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.3-1
- new upstream version 1.6.3

* Sat Apr  8 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.2-3
- drop bogus mc stuff (bz 169332)

* Tue Mar 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.2-2
- rebuild for new libgsf

* Thu Feb 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.2-1
- New upstream version
- Rebuild for new gcc4.1 and glibc
- add %%{?dist} for consistency with my other packages
- Update scripts to match the scriptlets wiki page

* Sat Jan 21 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.1-3
- Cleanup Requires
- Add (missing) call of gtk-update-icon-cache to %%post and %%postun

* Thu Dec  8 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.1-2
- Switch to core version of libgsf now Core has 1.13 instead of using special
  Extras libgsf113 version.

* Sat Nov 26 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.6.1-1
- new upstream stable version 1.6.1
- drop 2 integrated patches
- own dirs /usr/share/mc/templates /usr/share/mc (bug 169332)
- proper use of desktop-file-install (bug 171963)
- put icon in the proper freedesktop.org spec matching icon dir (bug 171964)
- remove unused mime-type icons
- clean up specfile, own all dirs not owned by Required packages.
- add --enable-ssindex (bug 172164)

* Thu Aug 18 2005 Jeremy Katz <katzj@redhat.com> - 1:1.4.3-6
- rebuild for changes in the devel tree

* Fri Aug 5 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.3-5
- gtk2-devel and libart_lgpl-devel where not getting sucked in because
  of a bug in another package this has been fixed now so the buildrequires
  have been removed again.

* Mon Jul 4 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.3-4
- For some reason gtk2-devel no longer gets sucked in by our other
  buildrequires so explicitly add it.
- libart_lgpl-devel is now needed for building, so add this.
- I also noticed in the configure output that gnumeric can
  use pygtk2, so add this.

* Fri Jun 17 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1.4.3-3
- Add patch3: fix excell export with libgsf >= 0.12 (bugzilla #160075),
  Thanks to Caolan McNamara.

* Tue Mar 15 2005 Caolan McNamara <caolanm@redhat.com> 1.4.3-2
- add libgnomedb to extras and gnumeric's requires

* Mon Mar 14 2005 Caolan McNamara <caolanm@redhat.com> 1.4.3-1
- bump to latest, first in extras
- drop helppath

* Fri Feb 18 2005 Caolan McNamara <caolanm@redhat.com> 1.4.2-3
- rh#149005#

* Mon Feb  7 2005 Matthias Clasen <mclasen@redhat.com> 1.4.2-2
- rebuild

* Thu Jan 27 2005 Caolan McNamara <caolanm@redhat.com> 1.4.2-1
- bump to next version

* Wed Dec 22 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-5
- RH#143587# pango-devel >= 1.4.0

* Sun Dec 19 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-4
- libgsf must be >= 1.10.0

* Fri Dec 17 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-3
- dubious "lib" usage from 64bit POV

* Fri Dec 17 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-2
- RH#143161# crash on reading corrupt excel file

* Wed Dec 15 2004 Caolan McNamara <caolanm@redhat.com> 1.4.1-1
- bump to new version
- drop integrated 64bit patch
- drop integrated desktop.in patch
- drop integrated latex patch
- drop disable bonobo patch
- add enable perl configure patch
- add quickfix for help being searched for in wrong place #gnome161404#

* Tue Nov 02 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-9
- #rh137694# backport latex exporter fix
- #rh137692# backport x64 excel fix

* Sat Oct 30 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-7
- #rh137565# Requires libgnomedb

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 1.2.13-6
- Change Requires(post) to PreReq

* Thu Sep 30 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-5
- #rh134250# improve Requires: desktop-file-utils

* Thu Sep 30 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-4
- #rh134175# invalid mime type entry

* Mon Sep 27 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-3
- make a wild stab at #rh133662#

* Mon Sep 6 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13-2
- update .keys to .desktop

* Tue Jul 27 2004 Caolan McNamara <caolanm@redhat.com> 1.2.13
- update to 1.2.13 
- #107278# --without-bonobo, help is fairly nonfunctional otherwise

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 5 2004 Caolan McNamara <caolanm@redhat.com> 1.2.12
- update to 1.2.12 some exported excel workbooks will not work in Excel
with older versions
_ delete unused patches

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 1.2.8-2
- #74034 own plugin dir
- #111112 BR intltool scrollkeeper gettext desktop-file-utils
- some cleanup

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 1.2.8-1
- Update to 1.2.8

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 6 2004 Daniel Reed <dreed@redhat.com> 1:1.2.6-1
- Version bump (1.2.6)

* Tue Oct 14 2003 Jonathan Blandford <jrb@redhat.com> 1:1.2.1-2
- add ssconvert

* Tue Oct 14 2003 Havoc Pennington <hp@redhat.com> 1:1.2.1-1
- add %%post to install schemas
- 1.2.1

* Fri Sep 19 2003 Havoc Pennington <hp@redhat.com> 1:1.2.0-1
- 1.2.0 final

* Mon Aug 25 2003 Jonathan Blandford <jrb@redhat.com>
- new version for GNOME 2.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 29 2003 Tim Powers <timp@redhat.com> 1:1.0.12-5
- rebuild to fix broken libgal dep

* Tue Feb 18 2003 Elliot Lee <sopwith@redhat.com> 1:1.0.12-4
- Put in a fix for the no-python-on-lib64 problem.

* Wed Feb 12 2003 Havoc Pennington <hp@redhat.com> 1:1.0.12-3
- add --without-guile due to crash on 64-bit #82977

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Havoc Pennington <hp@redhat.com>
- 1.0.12
- remove libtoolize/autotools invocations, dunno why they were there

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 1.0.9-6
- Run libtool/auto*
- Rebuild

* Thu Dec 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- also disable python for mainframe, this should be fixed properly
  at some point...
- add guile to filelist

* Wed Nov  6 2002 Bill Nottingham <notting@redhat.com> 1.0.9-4
- rebuild everywhere
- no python on hammer ATM

* Thu Oct 24 2002 Jeremy Katz <katzj@redhat.com>
- rebuild against new gal
- fixup file lists to use correct macros and include all files

* Fri Aug  2 2002 Havoc Pennington <hp@redhat.com>
- desktop file fixage

* Fri Jul 26 2002 Akira TAGOH <tagoh@redhat.com> 1.0.9-1
- update to 1.0.9
- gnumeric-0.67-excel95-ja.patch: we no longer need it. removed. (Bug#62776)

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- update to 1.0.8
- remove exceljpfonts patch that no longer applies

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 10 2002 Havoc Pennington <hp@redhat.com>
- add jp excel reading patch #62776

* Wed Mar 27 2002 Havoc Pennington <hp@redhat.com>
- add multibyte patch #61624

* Mon Mar 11 2002 Havoc Pennington <hp@redhat.com>
- 1.0.5

* Wed Jan 30 2002 Tim Powers <timp@redhat.com>
- update to 1.0.3

* Tue Nov 20 2001 Jonathan Blandford <jrb@redhat.com>
- Version 0.76

* Mon Oct  8 2001 Matt Wilson <msw@redhat.com>
- removed patch4 (gnumeric-0.67-sheet_corruption.patch), in CVS now.
- removed patch8 (gnumeric-0.67-xlsscale.patch), no longer needed.
- removed patch4 (gnumeric-0.67-s390.patch), no longer needed.
- regenerated patch6 (gnumeric-0.67.lengthen-warning.patch) against 0.71
- removed patch2 (gnumeric-0.67-mb.patch), in CVS now.
- removed patch9 (gnumeric-0.67-backspace.patch), came from CVS.
- removed patch5 (gnumeric-0.67-desktop.patch), ditto
- renamed remaining patches:
    patch3 (gnumeric-0.67-excel95-ja.patch) -> patch2
    patch6 (gnumeric-0.71-lengthen-warning.patch) -> patch3
- removed source10, ja.po from upstream is more up to date.
- added files needed for bonobo gnumeric back into file list

* Wed Sep  5 2001 Owen Taylor <otaylor@redhat.com>
- Add patch from CVS to fix backspace (#53062)

* Tue Aug  7 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem with scaling percentage and XLS files (#51054)
- Fix problem where default font for ja and other locales was backwards

* Mon Aug  6 2001 Owen Taylor <otaylor@redhat.com>
- Install all files from the plugins in the main package. Putting .la
  files in the main package didn't make sense, and we were missing
  some files for the gnome-glossary package.

* Fri Aug  3 2001 Owen Taylor <otaylor@redhat.com>
- Add some missing directories to the main package (#50701)

* Tue Jul 31 2001 Than Ngo <than@redhat.com>
- add patch to build on s390, s390x

* Fri Jul 27 2001 Jonathan Blandford <jrb@redhat.com>
- change 'old copy' dialog to popup after 9 months

* Fri Jul 20 2001 Owen Taylor <otaylor@redhat.com>
- Add missing contents of .desktop file from CVS

* Thu Jul 19 2001 Owen Taylor <otaylor@redhat.com>
- Move desktop file to /etc/X11/applnk (#23488)
- Added BuildPrereq on python-devel (#45029)
- Add BuildPrereq on gal-devel (#45027)
- Add <locale.h> include to .mb patch 
  (don't know why it works for me / in the build system, #32388)

* Mon Jul 16 2001 Jonathan Blandford <jrb@redhat.com>
- backport sheet corruption fix

* Tue Jul 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Make devel subpackage depend on main package

* Sat Jul 07 2001 Owen Taylor <otaylor@redhat.com>
- Version 0.67

* Fri Jun 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- support newer gettext version

* Fri Mar  9 2001 Akira TAGOH <tagoh@redhat.com> 0.61-9
- Fixed read excel95's .xls for Japanese.

* Fri Feb 23 2001 Akira TAGOH <tagoh@rehdat.com> 0.61-8
- Fixed jp patch with gnome-print.

* Mon Feb 19 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed jp patch.

* Thu Feb 08 2001 Yukihiro Nakai <ynakai@redhat.com>
- Fix about Japanese translation (ja.po)

* Wed Feb 07 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update Japanese translation.

* Tue Feb 06 2001 Akira TAGOH <tagoh@redhat.com>
- Added Japanese patch.
- Updated Japanese translation.
  Note: Please remove Source10 when the next upstream release.

* Thu Jan 18 2001 Matt Wilson <msw@redhat.com>
- don't use bin:bin for files in devel.

* Wed Jan 03 2001 Preston Brown <pbrown@redhat.com>
- standard file and directory modes/ownership

* Fri Dec 29 2000 Matt Wilson <msw@redhat.com>
- use rpm > 3.0.5 macros
- 0.61

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Tue Jul 18 2000 Owen Taylor <otaylor@redhat.com>
- Fix DocDir:

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild
