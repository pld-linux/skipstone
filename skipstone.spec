Summary:	SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko engine
Summary(pl):	Przegl±darka oparta o gtk+, korzystaj±ca z engine'u Mozilli (gecko)
Name:		skipstone
Version:	0.7.3
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	http://www.muhri.net/skipstone/%{name}-%{version}.tar.gz
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-dirs.patch
URL:		http://www.muhri.net/skipstone/
Requires:	mozilla-embedded >= 0.9.2-4
BuildRequires:	gtk+-devel >= 1.2.6
BuildRequires:	mozilla-devel >= 0.9.2-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
SkipStone is a simple Gtk+ web browser that utilizes Mozilla's gecko
engine.

%description -l pl
SkipStone jest prost± przegl±dark± www opart± na Gtk+, korzystaj±c± z
engine'u Mozilli - gecko.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} OPT="%{rpmcflags} -DSKIPSTONE_SYSTEM_THEME_DIR=\"\\\"%{_datadir}/%{name}/pixmaps\\\"\"" \
	cookie_support=1

%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_bindir}

%{__make} install PREFIX=$RPM_BUILD_ROOT%{_prefix}

gzip -9nf README* AUTHORS ChangeLog

%post
umask 022
rm -f %{_libdir}/mozilla/component.reg
MOZILLA_FIVE_HOME=%{_libdir}/mozilla regxpcom

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz *.pl
%attr(755,root,root) %{_bindir}/skipstone-bin
%attr(755,root,root) %{_bindir}/skipstone
%attr(755,root,root) %{_bindir}/skipdownload
%{_datadir}/skipstone
