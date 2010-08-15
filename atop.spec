%define name atop
%define version 1.25
%define release %mkrel 1

Name:      %name
Version:   %version
Release:   %release
Source:    http://www.atcomputing.nl/Tools/atop/packages/%{name}-%{version}.tar.gz
Patch1:	   atop-1.25-initscript_LSB.patch
URL:       http://www.ATComputing.nl/atop
Summary:   AT Computing System and Process Monitor
License:   GPL
Group:     Text tools 
Buildrequires: zlib1-devel ncurses-devel
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
The program atop is an interactive monitor to view the load on
a Linux-system. It shows the occupation of the most critical
hardware-resources (from a performance point of view) on system-level,
i.e. cpu, memory, disk and network. It also shows which processes are
responsible for the indicated load (again cpu-, memory-, disk- and
network-load on process-level).
The program atop can also be used to log system- and process-level
information in raw format for long-term analysis.

The program atopsar can be used to view system-level statistics as
reports, similar to the program sar.

%prep
%setup -q
%patch1 -p1 -b .LSB
sed -i -e "s/CFLAGS  =/CFLAGS +=/" Makefile

%build
CFLAGS="%{optflags}" %make

%install
rm    -rf 			  $RPM_BUILD_ROOT

install -Dp -m 04711 atop 	  $RPM_BUILD_ROOT%{_bindir}/atop
ln -s atop                        $RPM_BUILD_ROOT%{_bindir}/atopsar
install -Dp -m 0644 man/atop.1 	  $RPM_BUILD_ROOT%{_mandir}/man1/atop.1
install -Dp -m 0644 man/atopsar.1 $RPM_BUILD_ROOT%{_mandir}/man1/atopsar.1
install -Dp -m 0755 atop.init 	  $RPM_BUILD_ROOT%{_initrddir}/atop
install -Dp -m 0711 atop.daily	  $RPM_BUILD_ROOT/etc/atop/atop.daily
install -Dp -m 0644 atop.cron 	  $RPM_BUILD_ROOT/etc/cron.d/atop
install -Dp -m 0644 psaccs_atop	  $RPM_BUILD_ROOT/etc/logrotate.d/psaccs_atop
install -Dp -m 0644 psaccu_atop	  $RPM_BUILD_ROOT/etc/logrotate.d/psaccu_atop
install -d  -m 0755 		  $RPM_BUILD_ROOT/var/log/atop

%clean
rm -rf    $RPM_BUILD_ROOT

%post
%_post_service atop

# save today's logfile (format might be incompatible)
mv /var/log/atop/atop_`date +%Y%m%d` /var/log/atop/atop_`date +%Y%m%d`.save \
					2> /dev/null || :

# create dummy files to be rotated
touch /var/log/atop/dummy_before /var/log/atop/dummy_after

# activate daily logging for today
/etc/atop/atop.daily

%preun
%_preun_service atop

%files
%defattr(-,root,root)
%doc README COPYING README AUTHOR ChangeLog
%{_bindir}/atop
%{_bindir}/atopsar
%{_mandir}/man1/atop.1*
%{_mandir}/man1/atopsar.1*
%config %{_initrddir}/atop
%{_sysconfdir}/%{name}/atop.daily
%{_sysconfdir}/cron.d/atop
%{_sysconfdir}/logrotate.d/psaccs_atop
%{_sysconfdir}/logrotate.d/psaccu_atop
%dir /var/log/atop/
