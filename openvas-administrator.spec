
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Open Vulnerability Assessment System administrator
Name:		openvas-administrator
Version:	1.3.2
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://wald.intevation.org/frs/download.php/1442/%{name}-%{version}.tar.gz
# Source0-md5:	0410287e899f6b57c8674c0fe7b6fb1b
URL:		http://www.openvas.org/
BuildRequires:	cmake
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gnutls-devel > 2.8
BuildRequires:	libuuid-devel
BuildRequires:	openvas-libraries-devel >= 6.0.0
BuildRequires:	pkgconfig
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	graphviz
#BuildRequires:	sqlfairy
#BuildRequires:	xmltoman
%endif
BuildConflicts:	openvas-libraries-devel >= 7.0
Requires:	openvas-common >= 6.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the administrator module for the Open Vulnerability Assessment
System (OpenVAS). This module can for example manage OpenVAS users and
the Feed service for a OpenVAS installation. The administator can be
used as a command line utility as well as a service using the
XML-based and SSL-secured OpenVAS Adminstration Protocol (OAP).

The Open Vulnerability Assessment System (OpenVAS) is a framework of
several services and tools offering a comprehensive and powerful
vulnerability scanning and vulnerability management solution.

%package apidocs
Summary:	OpenVAS administrator API documentation
Group:		Documentation

%description apidocs
OpenVAS administrator API documentation.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DLOCALSTATEDIR=/var \
	..
%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog README
%doc doc/{*.html,*.rnc,*.conf}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openvas/openvasad_log.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openvas/pwpolicy.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*
%{_datadir}/openvas/openvasad
