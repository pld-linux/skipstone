
%define		minmozver	0.9.7

Summary:	SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko engine
Summary(pl):	Przegl±darka oparta o Gtk+, korzystaj±ca z engine'u Mozilli (gecko)
Name:		skipstone
Version:	0.7.9
Release:	2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.muhri.net/skipstone/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-dirs.patch
Patch2:		%{name}-pld.patch
URL:		http://www.muhri.net/skipstone/
BuildRequires:	gdk-pixbuf-devel
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
Requires:	mozilla-embedded = %(rpm -q --qf '%{VERSION}' --whatprovides mozilla-embedded)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libplds4.so libplc4.so libnspr4.so libgtksuperwin.so libxpcom.so

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko
engine.

%description -l pl
SkipStone jest prost± przegl±dark± www opart± na Gtk+, korzystaj±c± z
engine'u Mozilli - gecko.

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
%patch2 -p1

%build
%{__make} OPT="%{rpmcflags} -DSKIPSTONE_SYSTEM_THEME_DIR=\"\\\"%{_datadir}/%{name}/pixmaps\\\"\"" \
	cookie_support=1

for d in AutoComplete HistorySideBar Launcher NewButton SearchToolBar Zoomer \
	FavIcon ; do
	%{__make} -C plugins/$d \
		OPT="%{rpmcflags}" \
		LDFLAGS="%{rpmldflags} -shared"
done

# these plugins require imlib2:
#NewButtonImlib Throbber

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_applnkdir}/Network/WWW,%{_pixmapsdir},%{_libdir}/skipstone/plugins}

%{__make} install PREFIX=$RPM_BUILD_ROOT%{_prefix}
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Network/WWW
cp -f icons/skipstone-desktop.png $RPM_BUILD_ROOT%{_pixmapsdir}/

install plugins/*/*.so $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins
cp -rf plugins/Launcher/LauncherPix $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins


gzip -9nf README* AUTHORS ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%files
%defattr(644,root,root,755)
%doc *.gz *.pl
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
