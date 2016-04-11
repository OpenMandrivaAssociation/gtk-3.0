%define url_ver %(echo %{version}|cut -d. -f1,2)

%define enable_gtkdoc 0
%define enable_bootstrap 0
%define enable_tests 0

%define pkgname		gtk+
%define api		3
%define api_version	3.0
%define binary_version	3.0.0
%define major	0
%define libgdk	%mklibname gdk %{api} %{major}
%define libgtk	%mklibname gtk %{api} %{major}
%define girgdk	%mklibname gdk-gir %{api_version}
%define girgdkx11 %mklibname gdkx11-gir %{api_version}
%define girname	%mklibname gtk-gir %{api_version}
%define devname	%mklibname -d %{pkgname} %{api_version}
# this isnt really a true lib pkg, but a modules/plugin pkg
%define modules	%mklibname gtk-modules %{api_version}

%define gailmaj	0
%define libgail	%mklibname gail %{api} %{gailmaj}
%define devgail	%mklibname -d gail %{api_version}
%bcond_with	crossstrap


Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api_version}
Version:	3.18.9
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gtk+/%{url_ver}/%{pkgname}-%{version}.tar.xz
Patch0:		gtk+-defaulttheme.patch

BuildRequires:	cups-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(atk) >= 1.29.2
BuildRequires:	pkgconfig(cairo) >= 1.6.0
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.26
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.10
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:	pkgconfig(pango) >= 1.30
BuildRequires:	pkgconfig(pangocairo) >= 1.30
BuildRequires:	pkgconfig(atk-bridge-2.0) >= 2.6.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
#gw needed for gtk-update-icon-cache in gtk+3.0 3.0.9
BuildRequires:	gtk+2.0

%if %{enable_tests}
BuildRequires:	x11-server-xvfb
# gw tests will fail without this
BuildRequires	fonts-ttf-dejavu
%endif
%if %{enable_gtkdoc}
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	sgml-tools
BuildRequires:	texlive-texinfo
%endif
%if !%{enable_bootstrap}
Suggests:	xdg-user-dirs-gtk
%endif
Requires:	%{name}-common = %{version}-%{release}
# MD to pull in all the orphaned module loaders
Requires:	fontconfig
Requires:	gdk-pixbuf2.0
Requires:	gio2.0
Requires:	glib2.0-common
Requires:	pango-modules

Obsoletes:	gtk-engines3 < 3.0.0
Provides:	%{pkgname}%{api} = %{version}-%{release}
Suggests:	breeze-gtk

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

If you are planning on using the GIMP or another program that uses GTK+,
you'll need to have the gtk+ package installed.

%package common
Summary:	%{summary}
Group:		%{group}
BuildArch:	noarch
Conflicts:	%{name} < 3.3.2-2

%description common
This package contains the common files for the GTK+3.0 graphical user
interface.

%package -n %{modules}
Summary:	%{summary}
Group:		%{group}
Requires:	%{name} = %{version}-%{release}
Provides:	gtk%{api}-modules = %{version}-%{release}
Obsoletes:	%{_lib}gtk+3 < 3.3.4-2
Obsoletes:	%{_lib}gtk+3.0_0 < 3.0.0
Obsoletes:	%{_lib}gtk+-x11-3.0_0 < 3.0.0
Obsoletes:	%{_lib}gtk-engines3 < 3.0.0

%description -n %{modules}
This package contains the immodules, engines and printbackends libraries
for %{name} to function properly.

%package -n %{libgdk}
Summary:	Shared libraries of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Conflicts:	%{_lib}gtk+3_0 < 3.8.1-2

%description -n %{libgdk}
This package contains a shared library for %{name}.

%package -n %{libgtk}
Summary:	Shared libraries of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Obsoletes:	%{_lib}gtk+3_0 < 3.8.1-6

%description -n %{libgtk}
This package contains a shared library for %{name}.

%if !%{with crossstrap}
%package -n %{girgdk}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}gtk+3_0 < 3.3.2-2
Conflicts:	%{_lib}gtk-gir3.0 < 3.8.1-2

%description -n %{girgdk}
GObject Introspection interface description for %{name}.

%package -n %{girgdkx11}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}gtk+3_0 < 3.3.2-2
Conflicts:	%{_lib}gtk-gir3.0 < 3.8.1-2

%description -n %{girgdkx11}
GObject Introspection interface description for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}gtk+3_0 < 3.3.2-2

%description -n %{girname}
GObject Introspection interface description for %{name}.
%endif

%package -n %{devname}
Summary:	Development files for GTK+ (GIMP ToolKit) applications
Group:		Development/GNOME and GTK+
Requires:	%{libgdk} = %{version}-%{release}
Requires:	%{libgtk} = %{version}-%{release}
%if !%{with crossstrap}
Requires:	%{girgdk} = %{version}-%{release}
Requires:	%{girgdkx11} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
%endif
Provides:	%{pkgname}%{api}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%package -n %{libgail}
Summary:	GNOME Accessibility Implementation Library
Group:		System/Libraries
Obsoletes:	%{_lib}gail3.0_0 < 3.0.0

%description -n %{libgail}
Gail is the GNOME Accessibility Implementation Library

%package -n %{devgail}
Summary:	Development libraries, include files for GAIL
Group:		Development/GNOME and GTK+
Provides:	libgail-%{api_version}-devel = %{version}-%{release}
Requires:	%{libgail} = %{version}

%description -n %{devgail}
Gail is the GNOME Accessibility Implementation Library

%prep
%setup -qn %{pkgname}-%{version}
%apply_patches

%build
# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo %{optflags} | sed -e 's/-fomit-frame-pointer//g'`

%configure \
	--disable-static \
	--enable-xkb \
	--enable-xinerama \
	--enable-xrandr \
	--enable-xfixes \
	--enable-xcomposite \
	--enable-xdamage \
	--enable-x11-backend \
%if %{with crossstrap}
	--enable-introspection=no \
%endif
	--enable-colord

%make

%check
%if %enable_tests
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%{_bindir}/Xvfb :$XDISPLAY &
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock) ||:
%endif

%install
%makeinstall_std RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false

touch %{buildroot}%{_libdir}/gtk-%{api_version}/%{binary_version}/immodules.cache
mkdir -p %{buildroot}%{_libdir}/gtk-%{api_version}/modules

%if "%{_lib}" != "lib"
 mv %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version} %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version}-64
%else
 mv %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version} %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version}-32
%endif

%find_lang gtk30 gtk30-properties gtk30.lang

#remove not packaged files
rm -f %{buildroot}%{_mandir}/man1/gtk-update-icon-cache.1*
rm -f %{buildroot}%{_bindir}/gtk-update-icon-cache

%post -n %{modules}
if [ "$1" = "2" ]; then
  if [ -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules ]; then
    rm -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules
  fi
fi
%if "%{_lib}" != "lib"
 %{_bindir}/gtk-query-immodules-%{api_version}-64 --update-cache
%else
 %{_bindir}/gtk-query-immodules-%{api_version}-32 --update-cache
%endif

%triggerin -n %{modules} -- %{_libdir}/gtk-%{api_version}/%{binary_version}/immodules/*.so
%if "%{_lib}" != "lib"
 %{_bindir}/gtk-query-immodules-%{api_version}-64 --update-cache
%else
 %{_bindir}/gtk-query-immodules-%{api_version}-32 --update-cache
%endif

%triggerpostun -n %{modules} -- %{_libdir}/gtk-%{api_version}/%{binary_version}/immodules/*.so
%if "%{_lib}" != "lib"
 %{_bindir}/gtk-query-immodules-%{api_version}-64 --update-cache
%else
 %{_bindir}/gtk-query-immodules-%{api_version}-32 --update-cache
%endif

%files
%{_bindir}/gtk-query-immodules-%{api_version}-*
%{_bindir}/gtk-launch

%files common -f gtk30.lang
%dir %{_sysconfdir}/gtk-%{api_version}
%config(noreplace) %{_sysconfdir}/gtk-%{api_version}/im-multipress.conf
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/themes
%{_mandir}/man1/gtk-query-immodules-%{api_version}.1*
%{_mandir}/man1/gtk-launch.1*
%{_mandir}/man1/broadwayd.1*

%files -n %{modules}
%ghost %verify (not md5 mtime size) %{_libdir}/gtk-%{api_version}/3.0.0/immodules.cache
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/modules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}
%{_libdir}/gtk-%{api_version}/%{binary_version}/immodules
%{_libdir}/gtk-%{api_version}/%{binary_version}/printbackends

%files -n %{libgdk}
%{_libdir}/libgdk-%{api}.so.%{major}*

%files -n %{libgtk}
%{_libdir}/libgtk-%{api}.so.%{major}*

%if !%{with crossstrap}
%files -n %{girgdk}
%{_libdir}/girepository-1.0/Gdk-%{api_version}.typelib

%files -n %{girgdkx11}
%{_libdir}/girepository-1.0/GdkX11-%{api_version}.typelib

%files -n %{girname}
%{_libdir}/girepository-1.0/Gtk-%{api_version}.typelib
%endif

%files -n %{devname}
%doc README
%doc docs/*.txt AUTHORS ChangeLog NEWS* README*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-icon-browser
%{_bindir}/gtk3-widget-factory
# in 3.20.2
#%{_bindir}/gtk-query-settings
%{_bindir}/gtk-encode-symbolic-svg
%{_bindir}/gtk-builder-tool
%{_includedir}/gtk-%{api_version}
%{_libdir}/libgtk-%{api}.so
%{_libdir}/libgdk-%{api}.so
%{_libdir}/pkgconfig/gdk-*%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-*%{api_version}.pc
# in 3.20.2
#%{_datadir}/gettext/its/*.*
%{_datadir}/aclocal/*
%{_datadir}/gtk-%{api_version}
%if !%{with crossstrap}
%{_datadir}/gir-1.0/Gdk-%{api_version}.gir
%{_datadir}/gir-1.0/GdkX11-%{api_version}.gir
%{_datadir}/gir-1.0/Gtk-%{api_version}.gir
%endif
%{_datadir}/applications/gtk3-demo.desktop
%{_datadir}/applications/gtk3-icon-browser.desktop
%{_datadir}/applications/gtk3-widget-factory.desktop
%{_iconsdir}/*/*/*/gtk3-demo*
%{_iconsdir}/*/*/*/gtk3-widget-factory*
%_datadir/glib-2.0/schemas/org.gtk.Demo.gschema.xml
%doc %{_datadir}/gtk-doc/html/gdk3
%doc %{_datadir}/gtk-doc/html/gtk3
%{_mandir}/man1/gtk3-demo*.1*
# in 3.20.2
#%{_mandir}/man1/gtk-query-settings.1.xz
%{_mandir}/man1/gtk3-icon-browser.1*
%{_mandir}/man1/gtk3-widget-factory.1*
%{_mandir}/man1/gtk-encode-symbolic-svg.1*
%{_mandir}/man1/gtk-builder-tool.1*

%files -n %{libgail}
%{_libdir}/libgailutil-%{api}.so.%{gailmaj}*

%files -n %{devgail}
%{_includedir}/gail-%{api_version}
%{_libdir}/libgailutil-%{api}.so
%{_libdir}/pkgconfig/gail-%{api_version}.pc
%{_datadir}/gtk-doc/html/gail-libgail-util3

