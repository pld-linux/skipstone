Summary:	SkipStone - a simple GTK+ web browser that utilizes Mozilla's gecko engine
Summary(pl.UTF-8):	Przeglądarka oparta o GTK+, korzystająca z silnika Mozilli (gecko)
Summary(pt_BR.UTF-8):	Browser que usa o toolkit GTK+ e o engine gecko do Mozilla para renderização
Name:		skipstone
Version:	1.0.1
Release:	0.2
License:	GPL
Group:		X11/Applications/Networking
#Source0Download: http://www.muhri.net/skipstone/page.php3?node=download
Source0:	http://www.muhri.net/skipstone/%{name}-%{version}.tar.gz
# Source0-md5:	c46548d52b16a809e707a1410566fa0a
Source1:	%{name}.desktop
Patch0:		%{name}-dirs.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}_locale_pl.patch
Patch3:		%{name}-gtk2.patch
Patch4:		%{name}-po-fixes.patch
Patch5:		%{name}-xulrunner.patch
URL:		http://www.muhri.net/skipstone/
BuildRequires:	autoconf
BuildRequires:	gettext-devel >= 0.11
BuildRequires:	gtk+2-devel >= 2:2.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	xulrunner-devel >= 1.9
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.167
BuildRequires:	sed >= 4.0
%requires_eq_to	xulrunner xulrunner-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localedir	/usr/share/locale

%description
SkipStone is a simple GTK+ web browser that utilizes Mozilla's gecko
engine.

%description -l pl.UTF-8
SkipStone jest prostą przeglądarką WWW opartą na GTK+, korzystającą z
silnika Mozilli - gecko.

%description -l pt_BR.UTF-8
SkipStone é um Web Browser que usa o toolkit GTK+ e o engine gecko do
Mozilla para renderização.

%package plugins
Summary:	Various Skipstone plugins
Summary(pl.UTF-8):	Różne wtyczki do Skipstone
Group:		X11/Applications/Networking
Requires:	%{name} = %{version}-%{release}
Obsoletes:	skipstone-plugins-gdkpixbuf

%description plugins
Various Skipstone plugins.

%description plugins -l pl.UTF-8
Różne wtyczki do Skipstone.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

sed -i -e 's@/usr/share/skipstone/plugins@%{_libdir}/skipstone/plugins@' \
	src/skipstone.h

# kill precompiled x86_64 binaries
rm -f plugins/ThumbSideBar/*.{o,so}

%build
# not really needed (gettext can handle ->UTF-8 conversion at runtime)
# but it's better to do conversion once at build time
conv() {
iconv -f ${2} -t UTF-8 locale/${1}.po | sed -e "s/\(charset=\)${2}/\1UTF-8/" > ${1}.tmp
mv -f ${1}.tmp locale/${1}.po
}
conv bg CP1251
conv da ISO-8859-1
conv de iso-8859-1
conv es iso-8859-1
conv fr iso-8859-1
conv it iso-8859-1
conv ja EUC-JP
conv nl iso-8859-15
conv pl iso-8859-2
conv pt iso-8859-1

%{__autoconf}
%{__autoheader}
CXXFLAGS="%{rpmcxxflags} -fshort-wchar"
%configure \
	--enable-nls \
	--with-mozilla-includes=/usr/include/xulrunner \
	--with-mozilla-libs=/usr/%{_lib}/xulrunner

%{__make}

%{__make} -C plugins

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_desktopdir},%{_pixmapsdir},%{_libdir}/skipstone/plugins}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	LOCALEDIR=$RPM_BUILD_ROOT%{_localedir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -f icons/skipstone-desktop.png $RPM_BUILD_ROOT%{_pixmapsdir}

install plugins/*/*.so $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins
cp -rf plugins/Launcher/LauncherPix $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins
cp -rf plugins/Throbber/pacspin $RPM_BUILD_ROOT%{_libdir}/skipstone/plugins

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README* convert_bookmarks.pl
%attr(755,root,root) %{_bindir}/skipstone-bin
%attr(755,root,root) %{_bindir}/skipstone
%attr(755,root,root) %{_bindir}/skipdownload
%{_datadir}/skipstone
%dir %{_libdir}/skipstone
%dir %{_libdir}/skipstone/plugins
%{_desktopdir}/skipstone.desktop
%{_pixmapsdir}/skipstone-desktop.png

%files plugins
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/skipstone/plugins/*.so
%{_libdir}/skipstone/plugins/LauncherPix
%{_libdir}/skipstone/plugins/pacspin
