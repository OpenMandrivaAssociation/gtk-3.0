# gtk-3.0 is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define url_ver %(echo %{version}|cut -d. -f1,2)

%define enable_gtkdoc 1
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
%bcond_without	colord

%define lib32gdk	%mklib32name gdk %{api} %{major}
%define lib32gtk	%mklib32name gtk %{api} %{major}
%define dev32name	%mklib32name -d %{pkgname} %{api_version}
%define lib32gail	%mklib32name gail %{api} %{gailmaj}
%define dev32gail	%mklib32name -d gail %{api_version}

%global optflags %{optflags} -O3

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api_version}
Version:	3.24.49
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.gtk.org
# Upstream change source name, it is not longer in "gtk+" but with "gtk", also in same dir as gtk4.
Source0:	https://download.gnome.org/sources/gtk/%{url_ver}/gtk-%{version}.tar.xz
#Source0:	https://ftp.gnome.org/pub/GNOME/sources/gtk+/%{url_ver}/%{pkgname}-%{version}.tar.xz
# Dropped because causing problems on COSMIC, Wayfire, Sway, Hyprland etc.
#Patch0:		gtk+-defaulttheme.patch
# Default to using KDE file dialogs etc.
#Patch1:		gtk-use-kde-file-dialogs-by-default.patch
Patch2:		gtk-3.24.34-default-to-sane-font-rendering.patch
#(tpg) ClearLinux patch
Patch3:		madvise.patch
#Patch4:		grap-fix-build-without-introspection.patch
BuildRequires:	cups-devel
BuildRequires:	libxml2-utils
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(atk) >= 1.29.2
BuildRequires:	pkgconfig(cairo) >= 1.6.0
%if %{with colord}
BuildRequires:	pkgconfig(colord)
%endif
BuildRequires:	pkgconfig(epoxy)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0) >= 2.26
BuildRequires:	pkgconfig(glib-2.0) >= 2.25.10
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:	pkgconfig(pango) >= 1.30
BuildRequires:	pkgconfig(pangocairo) >= 1.30
BuildRequires:	pkgconfig(atk-bridge-2.0) >= 2.6.0
BuildRequires:	pkgconfig(tinysparql-3.0)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xcursor)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xkbcommon) >= 0.2.0
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(wayland-protocols)
BuildRequires:	pkgconfig(wayland-client) >= 1.9.91
BuildRequires:	pkgconfig(wayland-cursor) >= 1.9.91
BuildRequires:	pkgconfig(wayland-egl)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(com_err)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(rest-0.7)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(lzo2)
BuildRequires:  glibc-static-devel
BuildRequires:	pkgconfig(harfbuzz-gobject)
BuildRequires:  %{_lib}harfbuzz-gir-devel
BuildRequires:  sassc
#gw needed for gtk-update-icon-cache in gtk+3.0 3.0.9
BuildRequires:	gtk+2.0
BuildRequires:	meson

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
Requires:	gtk-update-icon-cache
%if !%{enable_bootstrap}
Suggests:	xdg-user-dirs-gtk
%endif
# MD to pull in all the orphaned module loaders
Requires:	fontconfig
Requires:	gdk-pixbuf2.0
Requires:	gio2.0
Requires:	glib2.0-common
Requires:	pango-modules

Obsoletes:	gtk-engines3 < 3.0.0
Provides:	%{pkgname}%{api} = %{version}-%{release}
# Both gstreamer plugins needed for many GTK apps like totem to works/launch. Due gst package splitting (I HATE SPLITTING) no longer pulled by default from gst package.
# Make it recommends to avoild dependencies problem at bootsreap builds.
Recommends:	gstreamer1.0-gtk
Recommends:	gstreamer1.0-gtk-wayland

%if %{with compat32}
BuildRequires:	gio2.0-32
BuildRequires:	devel(libgdk_pixbuf-2.0)
BuildRequires:	devel(libfontconfig)
BuildRequires:	devel(libfreetype)
BuildRequires:	devel(libz)
BuildRequires:	devel(libbz2)
BuildRequires:	devel(liblzma)
BuildRequires:	devel(libgmodule-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libpango-1.0)
BuildRequires:	devel(libatk-1.0)
BuildRequires:	devel(libatk-bridge-2.0)
BuildRequires:	devel(libuuid)
BuildRequires:	devel(libcairo)
%if %{with colord}
BuildRequires:	pkgconfig(colord)
%endif
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(liblzo2)
BuildRequires:	devel(libepoxy)
BuildRequires:	devel(libgdk_pixbuf-2.0)
BuildRequires:	devel(libpangocairo-1.0)
BuildRequires:	devel(libatk-bridge-2.0)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXcomposite)
BuildRequires:	devel(libXcursor)
BuildRequires:	devel(libXdamage)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libXtst)
BuildRequires:	devel(libXfixes)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXinerama)
BuildRequires:	devel(libXrandr)
BuildRequires:	devel(libxkbcommon)
BuildRequires:	devel(libwayland-client)
BuildRequires:	devel(libwayland-cursor)
BuildRequires:	devel(libwayland-egl)
BuildRequires:	devel(libXrender)
BuildRequires:	devel(libharfbuzz)
BuildRequires:  devel(libkrb5)
BuildRequires:  devel(libcom_err)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(rest-0.7)
BuildRequires:  glibc-static-devel
BuildRequires:	devel(libfribidi)
BuildRequires:	devel(libXft)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libffi)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libxcb-shm)
BuildRequires:	devel(libxcb-render)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libpixman-1)
BuildRequires:	devel(libexpat)
BuildRequires:	devel(libGL)
BuildRequires:	devel(libEGL)
BuildRequires:	devel(libpangoft2-1.0)
BuildRequires:	devel(libdbus-1)
BuildRequires:	devel(libatspi)
BuildRequires:	devel(libcups)
%endif

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
Conflicts:	%{name} < 3.18.9-4

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
Requires:	%{name}-common = %{version}-%{release}
# For native file dialogs
%ifnarch %{riscv}
Requires:	xdg-desktop-portal-implementation
%endif

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
# Not needed but used as sanity workaround after harfuzz gir splitting.
Requires:       %{_lib}harfbuzz-gir-devel
Provides:	%{pkgname}%{api}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%package -n gtk-update-icon-cache
Summary:	Icon theme caching utility
Group:		System/Libraries

%description -n gtk-update-icon-cache
GTK+ can use the cache files created by gtk-update-icon-cache to avoid a lot of
system call and disk seek overhead when the application starts. Since the
format of the cache files allows them to be mmap()ed shared between multiple
applications, the overall memory consumption is reduced as well.


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

%if %{with compat32}
%package -n %{lib32gdk}
Summary:	Shared libraries of The GIMP ToolKit (GTK+) (32-bit)
Group:		System/Libraries

%description -n %{lib32gdk}
This package contains a shared library for %{name}.

%package -n %{lib32gtk}
Summary:	Shared libraries of The GIMP ToolKit (GTK+) (32-bit)
Group:		System/Libraries
# For native file dialogs
%ifnarch %{riscv}
Requires:	xdg-desktop-portal-implementation
%endif

%description -n %{lib32gtk}
This package contains a shared library for %{name}.

%package -n %{dev32name}
Summary:	Development files for GTK+ (GIMP ToolKit) applications (32-bit)
Group:		Development/GNOME and GTK+
Requires:	%{lib32gdk} = %{version}-%{release}
Requires:	%{lib32gtk} = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}

%description -n %{dev32name}
This package contains the development files for %{name}.

%package -n %{lib32gail}
Summary:	GNOME Accessibility Implementation Library (32-bit)
Group:		System/Libraries

%description -n %{lib32gail}
Gail is the GNOME Accessibility Implementation Library

%package -n %{dev32gail}
Summary:	Development libraries, include files for GAIL (32-bit)
Group:		Development/GNOME and GTK+
Requires:	%{devgail} = %{version}
Requires:	%{lib32gail} = %{version}

%description -n %{dev32gail}
Gail is the GNOME Accessibility Implementation Library
%endif

%prep
%autosetup -n gtk-%{version} -p1
# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=$(echo %{optflags} | sed -e 's/-fomit-frame-pointer//g')

%if %{with compat32}
%meson32 \
	 -Dx11_backend=true \
	 -Dwayland_backend=true \
	 -Dbroadway_backend=true \
         -Dintrospection=false \
	 -Dxinerama=yes
%endif

%meson \
	-Dx11_backend=true \
	-Dwayland_backend=true \
	-Dbroadway_backend=true \
	-Dman=true \
	-Dxinerama=yes \
	-Dtracker3=true \
	-Dbuiltin_immodules=backend \
%if %{with crossstrap}
	-Dintrospection=false \
%else
	-Dintrospection=true \
%endif
%if %{with colord}
	-Dcolord=yes
%endif

# fight unused direct deps
#sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%meson_build


%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

touch %{buildroot}%{_libdir}/gtk-%{api_version}/%{binary_version}/immodules.cache
mkdir -p %{buildroot}%{_libdir}/gtk-%{api_version}/modules

%if "%{_lib}" != "lib"
 mv %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version} %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version}-64
%else
 mv %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version} %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version}-32
%endif

%find_lang gtk30 gtk30-properties gtk30.lang

#remove not packaged files
#rm -f %{buildroot}%{_mandir}/man1/gtk-update-icon-cache.1*
#rm -f %{buildroot}%{_bindir}/gtk-update-icon-cache

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
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}
%ghost %verify (not md5 mtime size) %{_libdir}/gtk-%{api_version}/%{binary_version}/immodules.cache
%{_bindir}/gtk-query-immodules-%{api_version}-*
%{_bindir}/gtk-launch
%{_bindir}/broadwayd
%{_bindir}/gtk-query-settings


%files common -f gtk30.lang
%dir %{_sysconfdir}/gtk-%{api_version}
%config(noreplace) %{_sysconfdir}/gtk-%{api_version}/im-multipress.conf
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.EmojiChooser.gschema.xml
%{_datadir}/themes
%{_datadir}/gettext/its/gtkbuilder.*
%{_mandir}/man1/gtk-query-immodules-%{api_version}.1*
%{_mandir}/man1/gtk-launch.1*
%{_mandir}/man1/broadwayd.1*
%{_mandir}/man1/gtk-query-settings.1*

%files -n %{modules}
%dir %{_libdir}/gtk-%{api_version}/modules
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
%doc docs/*.txt NEWS
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
%optional %doc %{_datadir}/gtk-doc/html/gdk3
%optional %doc %{_datadir}/gtk-doc/html/gtk3
%{_mandir}/man1/gtk3-demo*.1*
# in 3.20.2
#%{_mandir}/man1/gtk-query-settings.1.xz
%{_mandir}/man1/gtk3-icon-browser.1*
%{_mandir}/man1/gtk3-widget-factory.1*
%{_mandir}/man1/gtk-encode-symbolic-svg.1*
%{_mandir}/man1/gtk-builder-tool.1*

%files -n gtk-update-icon-cache
%{_bindir}/gtk-update-icon-cache
%{_mandir}/man1/gtk-update-icon-cache.1*


%files -n %{libgail}
%{_libdir}/libgailutil-%{api}.so.%{gailmaj}*

%files -n %{devgail}
%{_includedir}/gail-%{api_version}
%{_libdir}/libgailutil-%{api}.so
%{_libdir}/pkgconfig/gail-%{api_version}.pc
%optional %doc %{_datadir}/gtk-doc/html/gail-libgail-util3

%if %{with compat32}
%files -n %{dev32name}
%{_prefix}/lib/libgtk-%{api}.so
%{_prefix}/lib/libgdk-%{api}.so
%{_prefix}/lib/pkgconfig/gdk-*%{api_version}.pc
%{_prefix}/lib/pkgconfig/gtk+-*%{api_version}.pc

%files -n %{lib32gdk}
%{_prefix}/lib/libgdk-%{api}.so.%{major}*

%files -n %{lib32gtk}
%{_prefix}/lib/libgtk-%{api}.so.%{major}*
%{_prefix}/lib/gtk-%{api_version}

%files -n %{lib32gail}
%{_prefix}/lib/libgailutil-%{api}.so.%{gailmaj}*

%files -n %{dev32gail}
%{_prefix}/lib/libgailutil-%{api}.so
%{_prefix}/lib/pkgconfig/gail-%{api_version}.pc
%endif
