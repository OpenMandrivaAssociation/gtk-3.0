# enable_gtkdoc: Toggle if gtk-doc files should be rebuilt.
#      0 = no
#      1 = yes
%define enable_gtkdoc 1

# enable_bootstrap: Toggle if bootstrapping package
#      0 = no
#      1 = yes
%define enable_bootstrap 0

# enable_tests: Run test suite in build
#      0 = no
#      1 = yes
%define enable_tests 0

%{?_without_gtkdoc: %{expand: %%define enable_gtkdoc 0}}
%{?_without_bootstrap: %{expand: %%define enable_bootstrap 0}}
%{?_without_tests: %{expand: %%define enable_tests 0}}

%{?_with_gtkdoc: %{expand: %%define enable_gtkdoc 1}}
%{?_with_bootstrap: %{expand: %%define enable_bootstrap 1}}
%{?_with_tests: %{expand: %%define enable_tests 1}}


# required version of various libraries
%define req_glib_version		2.28.0
%define req_pango_version		1.24.0
%define req_atk_version			1.30
%define req_cairo_version		1.10.0
%define req_gdk_pixbuf_version		2.22.0

%define pkgname			gtk+
%define api_version		3.0
%define binary_version	3.0
%define lib_major		0
%define libname			%mklibname %{pkgname} %{api_version} %{lib_major}
%define libname_x11		%mklibname %{pkgname}-x11- %{api_version} %{lib_major}
%define develname		%mklibname -d %pkgname %api_version

%define gail_major 0
%define gail_libname %mklibname gail %api_version %gail_major
%define gaildevelname %mklibname -d gail %api_version

%define git_url git://git.gnome.org/gtk+

Summary:	The GIMP ToolKit (GTK+), a library for creating GUIs
Name:		%{pkgname}%{api_version}
Version:	3.0.4
Release:        %mkrel 1
License:	LGPLv2+
Group:		System/Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%pkgname/%{pkgname}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
URL:		http://www.gtk.org
Requires:	common-licenses
BuildRequires:	gettext-devel
BuildRequires:  libglib2.0-devel >= %{req_glib_version}
BuildRequires:	libatk1.0-devel >= %{req_atk_version}
BuildRequires:  cairo-devel >= %{req_cairo_version}
BuildRequires:	pango-devel >= %{req_pango_version}
BuildRequires:	libgdk_pixbuf2.0-devel >= %req_gdk_pixbuf_version
BuildRequires:  gobject-introspection-devel >= 0.10.1
BuildRequires:  X11-devel
BuildRequires:  cups-devel
BuildRequires:  fam-devel
%if %enable_tests
BuildRequires:  x11-server-xvfb
%endif
%if %enable_gtkdoc
BuildRequires: gtk-doc >= 0.9 
BuildRequires: sgml-tools
BuildRequires: texinfo
%endif
# gw tests will fail without this
BuildRequires: fonts-ttf-dejavu
%if !%{enable_bootstrap}
Suggests: xdg-user-dirs-gtk
%endif
Requires: %{libname} = %{version}
Provides:	%{pkgname}3 = %{version}-%{release}

%description
The gtk+ package contains the GIMP ToolKit (GTK+), a library for creating
graphical user interfaces for the X Window System.  GTK+ was originally
written for the GIMP (GNU Image Manipulation Program) image processing
program, but is now used by several other programs as well.  

If you are planning on using the GIMP or another program that uses GTK+,
you'll need to have the gtk+ package installed.

%package -n %{libname}
Summary: %{summary}
Group:	 %{group}
Provides:	lib%{pkgname}3 = %{version}-%{release}
Provides:	lib%{name} = %{version}-%{release}
Provides:   gtk3 = %{version}-%{release}
Requires:   libglib2.0 >= %{req_glib_version}
Requires:   libpango1.0 >= %{req_pango_version}
Requires:   libatk1.0 >= %{req_atk_version}
Requires(post): 	%{libname_x11} = %{version}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with gtk+.

%package -n %{develname}
Summary:	Development files for GTK+ (GIMP ToolKit) applications
Group:		Development/GNOME and GTK+
Provides:   %{libname_x11}-devel = %{version}-%{release}
Provides:	%{pkgname}3-devel = %{version}-%{release}
Provides:	lib%{pkgname}3-devel = %{version}-%{release}
Provides:	lib%{pkgname}%{api_version}-devel = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	lib%{pkgname}-x11-%{api_version}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Requires:	%{libname_x11} = %{version}
Requires:	libgdk_pixbuf2.0-devel >= %req_gdk_pixbuf_version
Requires:	libatk1.0-devel >= %{req_atk_version}
Requires:	libpango1.0-devel >= %{req_pango_version}

%description -n %{develname}
The libgtk+-devel package contains the static libraries and header files
needed for developing GTK+ (GIMP ToolKit) applications. The libgtk+-devel
package contains GDK (the General Drawing Kit, which simplifies the interface
for writing GTK+ widgets and using GTK+ widgets in applications), and GTK+
(the widget set).


%package -n %{libname_x11}
Summary:	X11 backend of The GIMP ToolKit (GTK+)
Group:		System/Libraries
Provides:	lib%{pkgname}-x11-%{api_version} = %{version}-%{release}
Provides:	%{name}-backend = %{version}-%{release}
Requires: 	%{libname} = %{version}
Requires:	%{name} >= %{version}-%{release}

%description -n %{libname_x11}
This package contains the X11 version of library needed to run
programs dynamically linked with gtk+.


%package -n %{gail_libname}
Summary:	GNOME Accessibility Implementation Library
Group:		System/Libraries
Provides:	libgail = %{version}-%{release}

%description -n %{gail_libname}
Gail is the GNOME Accessibility Implementation Library

%package -n %gaildevelname
Summary:	Static libraries, include files for GAIL
Group:		Development/GNOME and GTK+
Provides:	libgail-%{api_version}-devel = %{version}-%{release}
Requires:	%{gail_libname} = %{version}

%description -n %gaildevelname
Gail is the GNOME Accessibility Implementation Library

%prep
%setup -n %{pkgname}-%{version} -q
%apply_patches

%build
%ifarch ppc64
export CFLAGS="$RPM_OPT_FLAGS -mminimal-toc"
%endif

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/-fomit-frame-pointer//g'`

export CPPFLAGS="-DGTK_COMPILATION"
%configure2_5x --enable-xinerama \
%if !%enable_gtkdoc
	--enable-gtk-doc=no
%endif

%make

%check
%if %enable_tests
XDISPLAY=$(i=1; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
%if %mdkversion <= 200600
%{_prefix}/X11R6/bin/Xvfb :$XDISPLAY &
%else
%{_bindir}/Xvfb :$XDISPLAY &
%endif
export DISPLAY=:$XDISPLAY
make check
kill $(cat /tmp/.X$XDISPLAY-lock) ||:
%endif

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std mandir=%{_mandir} RUN_QUERY_IMMODULES_TEST=false RUN_QUERY_LOADER_TEST=false

touch $RPM_BUILD_ROOT%_libdir/gtk-%{api_version}/3.0.0/immodules.cache
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/modules

# handle biarch packages
progs="gtk-query-immodules-%{api_version}"
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/bin
for f in $progs; do
  mv -f $RPM_BUILD_ROOT%{_bindir}/$f $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/bin/
  cat > $RPM_BUILD_ROOT%{_bindir}/$f << EOF
#!/bin/sh
lib=%{_lib}
case ":\$1:" in
:lib*:) lib="\$1"; shift 1;;
esac
exec %{_prefix}/\$lib/gtk-%{api_version}/bin/$f \${1+"\$@"}
EOF
  chmod +x $RPM_BUILD_ROOT%{_bindir}/$f
done

%{find_lang} gtk30
%find_lang gtk30-properties
cat gtk30-properties.lang >> gtk30.lang

#remove not packaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/loaders/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/%{binary_version}.*/printbackends/*.la \
  $RPM_BUILD_ROOT%{_libdir}/gtk-%{api_version}/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%postun -n %{libname_pixbuf} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname_x11} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname_x11} -p /sbin/ldconfig
%endif

%post -n %{libname}
if [ "$1" = "2" ]; then
  if [ -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules ]; then
    rm -f %{_sysconfdir}/gtk-%{api_version}/gtk.immodules
  fi
fi

%{_libdir}/gtk-%{api_version}/bin/gtk-query-immodules-%{api_version} > %_libdir/gtk-%{api_version}/3.0.0/immodules.cache

%post 
if [ -d %{_datadir}/icons ]; then
 for i in `/bin/ls %{_datadir}/icons` ; do 
  [ -d "%{_datadir}/icons/$i" -a -e "%{_datadir}/icons/$i/icon-theme.cache" -a -e "%{_datadir}/icons/$i/index.theme" ] && gtk-update-icon-cache-%{api_version} --force --quiet %{_datadir}/icons/$i
 done
 exit 0
fi

%files -f gtk30.lang
%defattr(-, root, root)
%doc README
%{_bindir}/gtk-query-immodules-%{api_version}
%{_bindir}/gtk-update-icon-cache-%{api_version}
%_mandir/man1/gtk-query-immodules-%{api_version}.1*
%_mandir/man1/gtk-update-icon-cache-%{api_version}.1*
%{_datadir}/themes
%dir %{_sysconfdir}/gtk-%{api_version}
%config(noreplace) %{_sysconfdir}/gtk-%{api_version}/im-multipress.conf

%files -n %{libname}
%defattr(-, root, root)
%doc README
%ghost %verify (not md5 mtime size) %_libdir/gtk-%{api_version}/3.0.0/immodules.cache
%dir %{_libdir}/gtk-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/bin
%{_libdir}/gtk-%{api_version}/bin/gtk-query-immodules-%{api_version}
%dir %{_libdir}/gtk-%{api_version}/modules
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/immodules/*.so
%dir %{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/engines/*.so
%{_libdir}/gtk-%{api_version}/%{binary_version}.*/printbackends/*.so

%files -n %{develname}
%defattr(-, root, root)
%doc docs/*.txt AUTHORS ChangeLog NEWS* README*
%doc %{_datadir}/gtk-doc/html/gdk3
%doc %{_datadir}/gtk-doc/html/gtk3
%{_bindir}/gtk3-demo
%_bindir/gtk-builder-convert-%{api_version}
%_mandir/man1/gtk-builder-convert-%{api_version}.1*
%{_datadir}/aclocal/*
%{_datadir}/gtk-%{api_version}
%{_includedir}/gtk-%{api_version}/gdk
%{_includedir}/gtk-%{api_version}/gtk
%{_includedir}/gtk-%{api_version}/unix-print
%{_libdir}/gtk-%{api_version}/include
%{_libdir}/pkgconfig/gdk-%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-%{api_version}.pc
%{_libdir}/pkgconfig/gtk+-unix-print-%{api_version}.pc
%{_libdir}/*x11*.so
%_datadir/gir-1.0/Gdk-%{api_version}.gir
%_datadir/gir-1.0/GdkX11-%{api_version}.gir
%_datadir/gir-1.0/Gtk-%{api_version}.gir
%attr(644,root,root) %{_libdir}/*x11*.la
%{_libdir}/pkgconfig/*x11*


%files -n %{libname_x11}
%defattr(-, root, root)
%{_libdir}/*x11*.so.*
%_libdir/girepository-1.0/Gdk-%{api_version}.typelib
%_libdir/girepository-1.0/GdkX11-%{api_version}.typelib
%_libdir/girepository-1.0/Gtk-%{api_version}.typelib

%files -n %gail_libname
%defattr(-,root,root)
%{_libdir}/libgailutil-%{api_version}.so.%{gail_major}*
%{_libdir}/gtk-%{api_version}/modules/libferret.so
%{_libdir}/gtk-%{api_version}/modules/libgail.so

%files -n %gaildevelname
%defattr(-,root,root)
%{_datadir}/gtk-doc/html/gail-libgail-util3
%{_libdir}/libgailutil-%{api_version}.so
%attr(644,root,root) %{_libdir}/libgailutil-%{api_version}.la
%{_includedir}/gail-%{api_version}
%{_libdir}/pkgconfig/gail-%{api_version}.pc
