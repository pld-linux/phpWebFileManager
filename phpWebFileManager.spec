# TODO
# - webapps
Summary:	phpWebFileManager - file management PHP tool
Summary(pl.UTF-8):	phpWebFileManager - narzędzie w PHP do zarządzania plikami
Name:		phpWebFileManager
Version:	0.7
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://platon.sk/upload/_projects/00004/%{name}-%{version}.tar.gz
# Source0-md5:	1057eed9fbb6dca9de7d6b62c3ff7f47
Source1:	%{name}.conf
URL:		http://platon.sk/projects/phpWebFileManager/
Requires:	php(pcre)
Requires:	webserver = apache
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir	/usr/share/%{name}

%description
phpWebFileManager is file management PHP tool. It is designed for
inclusion into large projects using appropriate PHP mechanisms, in
example require() or similar function. However, it can be also used as
a standalone web application.

The most important features offered by phpWebFileManager are:
- easy and straightforward installation
- secure directory browsing
- directory creating, renaming and removing
- file creating, uploading, renaming, deleting and viewing
- file edition and saving
- huge configuration ability to allow/deny appropriate actions
- PostNuke module (add-on) compatibility
- multilanguage support.

%description -l pl.UTF-8
phpWebFileManager to narzędzie w PHP do zarządzania plikami. Zostało
zaprojektowane do włączania do dużych projektów przy użyciu
odpowiednich mechanizmów PHP, na przykład require() lub podobnej
funkcji. Może być jednak używane także jako samodzielna aplikacja WWW.

Najważniejsze możliwości oferowane przez phpWebFileManagera to:
- łatwa i prosta instalacja
- bezpieczne przeglądanie katalogów
- tworzenie, zmiana nazw i usuwanie katalogów
- tworzenie, umieszczanie, zmiana nazw, usuwanie i oglądanie plików
- edycja i zapisywanie plików
- duże możliwości konfiguracji w celu umożliwienia/zabronienia
  poszczególnych operacji
- kompatybilność z modułem PostNuke
- obsługa wielu języków.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_appdir} \
	$RPM_BUILD_ROOT%{_appdir}/{icons,lang,plugins} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_sysconfdir}/httpd}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -pR icons/*		$RPM_BUILD_ROOT%{_appdir}/icons
cp -pR lang/*		$RPM_BUILD_ROOT%{_appdir}/lang
cp -pR plugins/*	$RPM_BUILD_ROOT%{_appdir}/plugins

install %{SOURCE1}	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc doc/{AUTHOR,ChangeLog,PN-MODULE-HOWTO,README,TODO}
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/icons
%{_appdir}/lang
%{_appdir}/plugins
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
