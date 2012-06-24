Summary:	phpWebFileManager - file management PHP tool
Summary:	phpWebFileManager - narz�dzie w PHP do zarz�dzania plikami
Name:		phpWebFileManager
Version:	0.7
Release:	0.1
License:	GPL
Group:		Applications/WWW
Source0:	http://platon.sk/upload/_projects/00004/%{name}-%{version}.tar.gz
# Source0-md5:	1057eed9fbb6dca9de7d6b62c3ff7f47
Source1:	%{name}.conf
URL:		http://platon.sk/projects/phpWebFileManager/
Requires:	php
Requires:	php-pcre
Requires:	webserver = apache
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

%description -l pl
phpWebFileManager to narz�dzie w PHP do zarz�dzania plikami. Zosta�o
zaprojektowane do w��czania do du�ych projekt�w przy u�yciu
odpowiednich mechanizm�w PHP, na przyk�ad require() lub podobnej
funkcji. Mo�e by� jednak u�ywane tak�e jako samodzielna aplikacja WWW.

Najwa�niejsze mo�liwo�ci oferowane przez phpWebFileManagera to:
- �atwa i prosta instalacja
- bezpieczne przegl�danie katalog�w
- tworzenie, zmiana nazw i usuwanie katalog�w
- tworzenie, umieszczanie, zmiana nazw, usuwanie i ogl�danie plik�w
- edycja i zapisywanie plik�w
- du�e mo�liwo�ci konfiguracji w celu umo�liwienia/zabronienia
  poszczeg�lnych operacji
- kompatybilno�� z modu�em PostNuke
- obs�uga wielu j�zyk�w.

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
%doc doc/{AUTHOR,ChangeLog,COPYING,PN-MODULE-HOWTO,README,TODO}
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/icons
%{_appdir}/lang
%{_appdir}/plugins

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/%{name}.conf
