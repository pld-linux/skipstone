#
# Conditional build:
# _with_gtk1	- use gtk+ 1.2 instead of 2.x
#
%define		minmozver	4:1.5a
%define		gtkv		gtk%{?_with_gtk1:1}%{!?_with_gtk1:2}
Summary:	SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko engine
Summary(pl):	Przegl±darka oparta o Gtk+, korzystaj±ca z engine'u Mozilli (gecko)
Summary(pt_BR):	Browser que usa o toolkit GTK+ e o engine gecko do Mozilla para renderização
Name:		skipstone
Version:	0.8.3
Release:	8
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://www.muhri.net/skipstone/%{name}-%{version}.tar.gz
# Source0-md5:	d44324e3664723c2cbe82ce60464dc51
Source1:	%{name}.desktop
Patch0:		%{name}-dirs.patch
Patch1:		%{name}-pld.patch
Patch2:		%{name}_locale_pl.patch
Patch3:		%{name}-chrome_check.patch
Patch4:		%{name}-mozilla1.1.patch
Patch5:		%{name}-mozilla1.2b.patch
Patch6:		%{name}-mozilla1.4.patch
Patch7:		%{name}-mozilla1.5.patch
Patch8:		%{name}-gtk2.patch
Patch9:		%{name}-po-fixes.patch
URL:		http://www.muhri.net/skipstone/
BuildRequires:	autoconf
%{?_with_gtk1:BuildRequires:	gdk-pixbuf-devel}
BuildRequires:	gettext-devel
%{?_with_gtk1:BuildRequires:	gtk+-devel >= 1.2.6}
%{!?_with_gtk1:BuildRequires:	gtk+2-devel >= 2.2.0}
BuildRequires:	libstdc++-devel
BuildRequires:	mozilla-embedded(%{gtkv}) >= %{minmozver}
BuildRequires:	mozilla-embedded-devel >= %{minmozver}
%{!?_with_gtk1:BuildRequires:	pkgconfig}
Requires:	mozilla-embedded(%{gtkv}) = %(rpm -q --qf '%{EPOCH}:%{VERSION}' --whatprovides mozilla-embedded)
Provides:	%{name}(%{gtkv}) = %{version}
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
Requires:	%{name}(%{gtkv}) = %{version}

%description plugins
Various Skipstone plugins.

%description plugins -l pl
Ró¿ne wtyczki do Skipstone.

%package plugins-gdkpixbuf
Summary:	Skipstone plugins that require gdk-pixbuf library
Summary(pl):	Wtyczki do Skipstone wymagaj±ce biblioteki gdk-pixbuf
Group:		X11/Applications/Networking
Requires:	%{name}(%{gtkv}) = %{version}

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
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%{!?_with_gtk1:%patch8 -p1}
%patch9 -p1 -b .pofixes

# handle gettext 0.10/0.11 incompatibility
if ! msgfmt --version | grep -q '0\.1[12]\.' ; then
	mv -f locale/zh_TW.Big5.po{.pofixes,}
fi

mv -f locale/{zh_CN.GB2312,zh_CN}.po
mv -f locale/{zh_TW.Big5,zh_TW}.po

%build
%if 0%{!?_with_gtk1:1}
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
%endif

%{__autoconf}

CPPFLAGS="-I/usr/include/nspr -DNEW_H=\<new.h\>"
CXXFLAGS="%{rpmcflags} -fno-rtti"
%configure \
	--with-mozilla-includes=/usr/include/mozilla \
	--with-mozilla-libs=/usr/lib/mozilla \
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
%{_applnkdir}/Network/WWW/*
%{_pixmapsdir}/*

%files plugins
%defattr(644,root,root,755)
%{_libdir}/skipstone/plugins/LauncherPix
%attr(755,root,root) %{_libdir}/skipstone/plugins/[AHLSZ]*.so
%attr(755,root,root) %{_libdir}/skipstone/plugins/NewButton.so

%files plugins-gdkpixbuf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/skipstone/plugins/FavIcon.so
