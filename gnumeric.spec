Name:             gnumeric
Epoch:            1
Version:          1.12.34
Release:          1%{?dist}
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
BuildRequires:    bison
BuildRequires:    desktop-file-utils
BuildRequires:    docbook-dtds
BuildRequires:    goffice-devel >= 0.10.28
BuildRequires:    intltool
BuildRequires:    itstool
BuildRequires:    libgda-ui-devel
BuildRequires:    perl-devel
BuildRequires:    perl-generators
BuildRequires:    perl(ExtUtils::Embed)
BuildRequires:    perl(Getopt::Long)
BuildRequires:    perl(IO::Compress::Gzip)
BuildRequires:    psiconv-devel
BuildRequires:    pygobject3-devel
BuildRequires:    pygtk2-devel
BuildRequires:    zlib-devel
BuildRequires:    libappstream-glib
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
%autosetup
chmod -x plugins/excel/rc4.?


%build
%configure --disable-silent-rules
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
%make_install

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/gnumeric.appdata.xml \
  "https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/gnumeric/Screenshot from 2013-10-10 14:19:50.png"

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
%doc HACKING AUTHORS ChangeLog NEWS BUGS README
%license COPYING
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
* Mon Mar 27 2017 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.34-1
- Updated to 1.12.34
- Dropped upstreamed patches

* Tue Jan 31 2017 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.33-1
- Updated to 1.12.33
- Fixed missing $DESTDIR in doc/Makefile.{in,am}
- Added docbook-dtds and itstool to BuildRequires, removed rarian-compat
- Patched to use xml-dtd-4.5 instead of xmlcharent

* Sat Aug 27 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.32-1
- Updated to 1.12.32

* Mon Jul 04 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.31-1
- Updated to 1.12.31

* Mon Jun 20 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.30-1
- Updated to 1.12.30
- Dropped upstreamed patches
- Spec file cleanups

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.12.29-3
- Perl 5.24 rebuild

* Sun May 15 2016 Hans de Goede <hdegoede@redhat.com> - 1:1.12.29-2
- Fix "usage of MIME type "zz-application/zz-winassoc-xls" is discouraged"
  warning showing every time a rpm transaction runs update-desktop-database
- Prune spec-file changelog

* Sat May 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.29-1
- Updated to 1.12.29

* Wed Mar 23 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.28-1
- Updated to 1.12.28

* Sun Feb 07 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.27-1
- Updated to 1.12.27
- Added bison to BuildRequires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.12.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 31 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.26-1
- Updated to 1.12.26

* Mon Dec 28 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.25-1
- Updated to 1.12.25

* Mon Oct 26 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.24-1
- Updated to 1.12.24

* Thu Jul 30 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.23-1
- Updated to 1.12.23

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.12.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.12.22-2
- Perl 5.22 rebuild

* Thu May 28 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.22-1
- Updated to 1.12.22

* Tue Apr 07 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.21-1
- Updated to 1.12.21

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 1:1.12.20-2
- Use better AppData screenshots

* Fri Feb 06 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.20-1
- Updated to 1.12.20

* Thu Jan 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.19-1
- Updated to 1.12.19

* Sat Sep 27 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1:1.12.18-1
- Updated to 1.12.18

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
