
%define		minmozver	1.0

Summary:	SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko engine
Summary(pl):	Przegl±darka oparta o Gtk+, korzystaj±ca z engine'u Mozilli (gecko)
Summary(pt_BR):	Browser que usa o toolkit GTK+ e o engine gecko do Mozilla para renderização.
Name:		skipstone
Version:	0.8.3
Release:	3
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.muhri.net/skipstone/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Patch0:		%{name}-dirs.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}_locale_pl.patch
Patch3:		%{name}-chrome_check.patch
URL:		http://www.muhri.net/skipstone/
BuildRequires:	autoconf
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	nspr-devel
Requires(post):	mozilla-embedded
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_localedir	/usr/share/locale

%description
SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko
engine.

%description -l pl
SkipStone jest prost± przegl±dark± www opart± na Gtk+, korzystaj±c± z
engine'u Mozilli - gecko.

%description -l pt_BR
SkipStone é um Web Browser que usa o toolkit GTK+ e o engine gecko do
Mozilla para renderização.

%package plugins
Summary:	Various Skipstone plugins
Summary(pl):	Ró¿ne wtyczki do Skipstone
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}

%description plugins
Various Skipstone plugins.

%description plugins -l pl
Ró¿ne wtyczki do Skipstone.

%package plugins-gdkpixbuf
Summary:	Skipstone plugins that require gdk-pixbuf library
Summary(pl):	Wtyczki do Skipstone wymagaj±ce biblioteki gdk-pixbuf
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}

%description plugins-gdkpixbuf
Skipstone plugins that require gdk-pixbuf library. Currently only
FavIcon.

%description plugins-gdkpixbuf -l pl
Wtyczki do SkipStone wymagaj±ce biblioteki gdk-pixbuf. Na razie tylko
FavIcon.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1

%build
%{__autoconf}

CPPFLAGS="-I/usr/include/nspr"
export CPPFLAGS

%configure \
	--with-mozilla-includes=/usr/X11R6/include/mozilla \
	--with-mozilla-libs=/usr/X11R6/lib/mozilla \
	--enable-nls

%{__make}

cd plugins
echo all: > Throbber/Makefile # it requires imlib2, let's skip it for a while
echo all: > NewButtonImlib/Makefile # it requires imlib2, let's skip it for a while
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_applnkdir}/Network/WWW,%{_pixmapsdir},%{_libdir}/skipstone/plugins}

%{__make} install \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LOCALEDIR=$RPM_BUILD_ROOT%{_localedir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
cp -f icons/skipstone-desktop.png $RPM_BUILD_ROOT%{_pixmapsdir}/

install plugins/*/*.so $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins
cp -rf plugins/Launcher/LauncherPix $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* AUTHORS ChangeLog *.pl
%attr(755,root,root) %{_bindir}/skipstone-bin
%attr(755,root,root) %{_bindir}/skipstone
%attr(755,root,root) %{_bindir}/skipdownload
%{_datadir}/skipstone
%dir %{_libdir}/skipstone
%dir %{_libdir}/skipstone/plugins
%dir %{_applnkdir}/Network/WWW/*
%{_pixmapsdir}/*

%files plugins
%defattr(644,root,root,755)
%{_libdir}/skipstone/plugins/LauncherPix
%attr(755,root,root) %{_libdir}/skipstone/plugins/[AHLSZ]*.so
%attr(755,root,root) %{_libdir}/skipstone/plugins/NewButton.so

%files plugins-gdkpixbuf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/skipstone/plugins/FavIcon.so
