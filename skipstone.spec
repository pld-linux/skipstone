%define		minmozver	5:1.7
Summary:	SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko engine
Summary(pl):	Przegl±darka oparta o Gtk+, korzystaj±ca z engine'u Mozilli (gecko)
Summary(pt_BR):	Browser que usa o toolkit GTK+ e o engine gecko do Mozilla para renderização
Name:		skipstone
Version:	0.9.3
Release:	2
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.muhri.net/skipstone/%{name}-%{version}.tar.gz
# Source0-md5:	e5f558e474dcaee673edf25877bdba5b
Source1:	%{name}.desktop
Patch0:		%{name}-dirs.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}_locale_pl.patch
Patch3:		%{name}-chrome_check.patch
Patch4:		%{name}-mozilla1.7.patch
Patch5:		%{name}-gtk2.patch
Patch6:		%{name}-po-fixes.patch
Patch7:		%{name}-pic.patch
URL:		http://www.muhri.net/skipstone/
BuildRequires:	autoconf
BuildRequires:	gettext-devel >= 0.11
BuildRequires:	gtk+2-devel >= 2.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-embedded(gtk2) >= %{minmozver}
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
BuildRequires:	pkgconfig
Requires:	mozilla-embedded(gtk2) = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
Provides:	%{name}(gtk2) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# can be provided by mozilla or mozilla-embedded
%define		_noautoreqdep	libgtkembedmoz.so libgtksuperwin.so libxpcom.so

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
Requires:	%{name}(gtk2) = %{version}-%{release}
Obsoletes:	skipstone-plugins-gdkpixbuf

%description plugins
Various Skipstone plugins.

%description plugins -l pl
Ró¿ne wtyczki do Skipstone.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

mv -f locale/{zh_CN.GB2312,zh_CN}.po
mv -f locale/{zh_TW.Big5,zh_TW}.po

%{__perl} -pi -e 's@/usr/share/skipstone/plugins@%{_libdir}/skipstone/plugins@' \
	src/skipstone.h

# kill precompiled x86 binaries
rm -f plugins/Up/*.{o,so}

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
conv ru koi8-r
conv zh_CN GBK
conv zh_TW big5

%{__autoconf}

CPPFLAGS="-I/usr/include/nspr"
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure \
	--enable-cvs-mozilla \
	--enable-nls \
	--with-mozilla-includes=/usr/include/mozilla \
	--with-mozilla-libs=/usr/%{_lib}/mozilla

%{__make}

cd plugins
echo all: > Throbber/Makefile # it requires imlib2, let's skip it for a while
%{__make}

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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* AUTHORS ChangeLog *.pl
%attr(755,root,root) %{_bindir}/skipstone-bin
%attr(755,root,root) %{_bindir}/skipstone
%attr(755,root,root) %{_bindir}/skipdownload
%{_datadir}/skipstone
%dir %{_libdir}/skipstone
%dir %{_libdir}/skipstone/plugins
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png

%files plugins
%defattr(644,root,root,755)
%{_libdir}/skipstone/plugins/LauncherPix
%attr(755,root,root) %{_libdir}/skipstone/plugins/*.so
