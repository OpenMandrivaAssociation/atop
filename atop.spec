%define _empty_manifest_terminate_build 0

Name:      atop
Version:	2.6.0
Release:	2
Source0:   http://www.atoptool.nl/download/%{name}-%{version}.tar.gz
URL:       http://www.ATComputing.nl/atop
Summary:   AT Computing System and Process Monitor
License:   GPL
Group:     Text tools 
Buildrequires: pkgconfig(zlib)
Buildrequires: pkgconfig(ncurses)

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
%autosetup -p1
sed -i -e "s/CFLAGS  =/CFLAGS +=/" Makefile

%build
CFLAGS="%{optflags}" %make_build

%install
install -Dp -m 04711 atop 	  %{buildroot}%{_bindir}/atop
ln -s atop                        %{buildroot}%{_bindir}/atopsar
install -Dp -m 0644 man/atop.1 	  %{buildroot}%{_mandir}/man1/atop.1
install -Dp -m 0644 man/atopsar.1 %{buildroot}%{_mandir}/man1/atopsar.1
install -Dp -m 0755 atop.init 	  %{buildroot}%{_initrddir}/atop
install -Dp -m 0711 atop.daily	  %{buildroot}/etc/atop/atop.daily
#install -Dp -m 0644 atop.cronsystemd 	  %{buildroot}/etc/cron.d/atop
install -Dp -m 0644 psaccs_atop	  %{buildroot}/etc/logrotate.d/psaccs_atop
install -Dp -m 0644 psaccu_atop	  %{buildroot}/etc/logrotate.d/psaccu_atop
install -d  -m 0755 		  %{buildroot}/var/log/atop

%post
%systemd_post %{name}
%systemd_post atopacct
%systemd_post atop-rotate.timer

%preun
%systemd_preun %{name}
%systemd_preun atopacct
%systemd_preun atop-rotate.timer

%files
%doc README COPYING AUTHOR ChangeLog
%{_bindir}/atop
%{_bindir}/atopsar
%{_mandir}/man1/atop.1*
%{_mandir}/man1/atopsar.1*
%config %{_initrddir}/atop
%{_sysconfdir}/%{name}/atop.daily
#{_sysconfdir}/cron.d/atop
%{_sysconfdir}/logrotate.d/psaccs_atop
%{_sysconfdir}/logrotate.d/psaccu_atop
%dir /var/log/atop/
