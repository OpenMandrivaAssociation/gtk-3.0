%define enable_gtkdoc 0
%define enable_bootstrap 0
%define enable_tests 0

%define pkgname			gtk+
%define api				3
%define api_version		3.0
%define binary_version	3.0.0
%define lib_major		0
# this isnt really a true lib pkg, but a modules/plugin pkg
%define modulesname		%mklibname %{pkgname} %{api}
%define libname			%mklibname %{pkgname} %{api} %{lib_major}
%define develname		%mklibname -d %pkgname %{api_version}

%define gail_major 0
%define libgail %mklibname gail %{api} %gail_major
%define develgail %mklibname -d gail %{api_version}

%define libgir %mklibname gtk-gir %{api_version}

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api_version}
Version:	3.3.4
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%pkgname/%{pkgname}-%{version}.tar.xz

BuildRequires:  cups-devel
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig(atk) >= 1.29.2
BuildRequires:  pkgconfig(cairo) >= 1.6.0
#BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.21.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.25.10
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires:  pkgconfig(pango) >= 1.20.0
BuildRequires:  pkgconfig(pangocairo) >= 1.20.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)

#gw needed for gtk-update-icon-cache in gtk+3.0 3.0.9
BuildRequires:	gtk+2.0

%if %enable_tests
BuildRequires:  x11-server-xvfb
# gw tests will fail without this
BuildRequires: fonts-ttf-dejavu
%endif
%if %enable_gtkdoc
BuildRequires: gtk-doc >= 0.9 
BuildRequires: sgml-tools
BuildRequires: texlive-texinfo
%endif
%if !%{enable_bootstrap}
Suggests: xdg-user-dirs-gtk
%endif
Requires: %{name}-common = %{version}-%{release}
Obsoletes:	gtk-engines3 < 3.0.0
Provides:	%{pkgname}%{api} = %{version}-%{release}

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

If you are planning on using the GIMP or another program that uses GTK+,
you'll need to have the gtk+ package installed.

%package common
Summary:    %{summary}
Group:      %{group}
BuildArch:  noarch
Conflicts:  %{name} <= 3.3.2-1

%description common
This package contains the common files for the GTK+3.0 graphical user interface.

%package -n %{modulesname}
Summary: %{summary}
Group:	 %{group}
Requires:   %{name} = %{version}-%{release}
Obsoletes:	%{_lib}gtk+3.0_0 < 3.0.0
Obsoletes:	%{_lib}gtk+-x11-3.0_0 < 3.0.0
Obsoletes:	%{_lib}gtk-engines3 < 3.0.0

%description -n %{modulesname}
This package contains the immodules, engines and printbackends libraries
for %{name} to function properly.

%package -n %{develname}
Summary:	Development files for GTK+ (GIMP ToolKit) applications
Group:		Development/GNOME and GTK+
Requires:   %{libname} = %{version}-%{release}
Requires:   %{libgir} = %{version}-%{release}
Provides:	%{pkgname}%{api}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
The libgtk+-devel package contains the static libraries and header files
needed for developing GTK+ (GIMP ToolKit) applications. The libgtk+-devel
package contains GDK (the General Drawing Kit, which simplifies the interface
for writing GTK+ widgets and using GTK+ widgets in applications), and GTK+
(the widget set).

%package -n %{libname}
Summary:    Shared libraries of The GIMP ToolKit (GTK+)
Group:      System/Libraries
Conflicts:  %{libname} <= 3.3.2-1

%description -n %{libname}
This package contains the shared libraries needed to run programs dynamically 
linked with gtk+.

%package -n %{libgir}
Summary:    GObject Introspection interface description for %{name}
Group:      System/Libraries
Requires:   %{libname} = %{version}-%{release}
Conflicts:  %{libname} <= 3.3.2-1

%description -n %{libgir}
GObject Introspection interface description for %{name}.

%package -n %{libgail}
Summary:	GNOME Accessibility Implementation Library
Group:		System/Libraries
Obsoletes:	%{_lib}gail3.0_0 < 3.0.0

%description -n %{libgail}
Gail is the GNOME Accessibility Implementation Library

%package -n %{develgail}
Summary:	Development libraries, include files for GAIL
Group:		Development/GNOME and GTK+
Provides:	libgail-%{api_version}-devel = %{version}-%{release}
Requires:	%{libgail} = %{version}

%description -n %{develgail}
Gail is the GNOME Accessibility Implementation Library

%prep
%setup -qn %{pkgname}-%{version}
%apply_patches

%build
# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fomit-frame-pointer//g'`

export CPPFLAGS="-DGTK_COMPILATION"
%configure2_5x \
	--disable-static \
	--enable-xinerama \
	--enable-gtk2-dependency

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
rm -rf %{buildroot}

%makeinstall_std RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false

touch %{buildroot}%{_libdir}/gtk-%{api_version}/%{binary_version}/immodules.cache
mkdir -p %{buildroot}%{_libdir}/gtk-%{api_version}/modules

%if %_lib != lib
 mv %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version} %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version}-64
%else
 mv %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version} %{buildroot}%{_bindir}/gtk-query-immodules-%{api_version}-32
%endif

%find_lang gtk30 gtk30-properties gtk30.lang

#remove not packaged files
rm -f %{buildroot}%{_mandir}/man1/gtk-update-icon-cache.1*
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -n %{modulesname}
if [ "$1" = "2" ]; then
  if [ -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules ]; then
    rm -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules
  fi
fi
%if %_lib != lib
 %{_bindir}/gtk-query-immodules-%{api_version}-64 --update-cache
%else
 %{_bindir}/gtk-query-immodules-%{api_version}-32 --update-cache
%endif

%triggerin -n %{modulesname} -- %{_libdir}/gtk-%{api_version}/%{binary_version}/immodules/*.so
%if %_lib != lib
 %{_bindir}/gtk-query-immodules-%{api_version}-64 --update-cache
%else
 %{_bindir}/gtk-query-immodules-%{api_version}-32 --update-cache
%endif

%triggerpostun -n %{modulesname} -- %{_libdir}/gtk-%{api_version}/%{binary_version}/immodules/*.so
%if %_lib != lib
 %{_bindir}/gtk-query-immodules-%{api_version}-64 --update-cache
%else
 %{_bindir}/gtk-query-immodules-%{api_version}-32 --update-cache
%endif

%files
%doc README
%{_bindir}/gtk-query-immodules-%{api_version}-*

%files common -f gtk30.lang
%dir %{_sysconfdir}/gtk-%{api_version}
%config(noreplace) %{_sysconfdir}/gtk-%{api_version}/im-multipress.conf
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/themes
%{_mandir}/man1/gtk-query-immodules-%{api_version}.1*

%files -n %{modulesname}
%ghost %verify (not md5 mtime size) %{_libdir}/gtk-%{api_version}/3.0.0/immodules.cache
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/modules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}/immodules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}/printbackends
%{_libdir}/gtk-%{api_version}/%{binary_version}/immodules/*.so
%{_libdir}/gtk-%{api_version}/%{binary_version}/printbackends/*.so

%files -n %{libname}
%{_libdir}/libgtk-3.so.%{lib_major}*
%{_libdir}/libgdk-3.so.%{lib_major}*

%files -n %{libgir}
%{_libdir}/girepository-1.0/Gdk-%{api_version}.typelib
%{_libdir}/girepository-1.0/GdkX11-%{api_version}.typelib
%{_libdir}/girepository-1.0/Gtk-%{api_version}.typelib

%files -n %{develname}
%doc docs/*.txt AUTHORS ChangeLog NEWS* README*
%{_bindir}/gtk3-demo
%{_includedir}/gtk-%{api_version}
%{_libdir}/libgtk-%{api}.so
%{_libdir}/libgdk-%{api}.so
%{_libdir}/pkgconfig/gdk-*%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-*%{api_version}.pc
%{_datadir}/aclocal/*
%{_datadir}/gtk-%{api_version}
%{_datadir}/gir-1.0/Gdk-%{api_version}.gir
%{_datadir}/gir-1.0/GdkX11-%{api_version}.gir
%{_datadir}/gir-1.0/Gtk-%{api_version}.gir
%doc %{_datadir}/gtk-doc/html/gdk3
%doc %{_datadir}/gtk-doc/html/gtk3

%files -n %{libgail}
%{_libdir}/libgailutil-%{api}.so.%{gail_major}*

%files -n %{develgail}
%{_includedir}/gail-%{api_version}
%{_libdir}/libgailutil-%{api}.so
%{_libdir}/pkgconfig/gail-%{api_version}.pc
%{_datadir}/gtk-doc/html/gail-libgail-util3

