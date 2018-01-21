Summary: Scripts to bring up network interfaces and legacy utilities
Name: initscripts
Version: 9.79
License: GPLv2
Group: System Environment/Base
Release: 1%{?dist}
URL: https://github.com/fedora-sysv/initscripts
Source: https://github.com/fedora-sysv/initscripts/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: %{name}-rpmlintrc
Requires: /bin/awk, sed, coreutils
Requires: grep
Requires: module-init-tools
Requires: util-linux >= 2.16
Requires: bash >= 3.0
Requires: procps-ng >= 3.3.8-16
Requires: ipcalc
Conflicts: systemd < 216-3
Conflicts: lvm2 < 2.02.98-3
Conflicts: dmraid < 1.0.0.rc16-18
Conflicts: policycoreutils < 2.5-6
Requires: systemd
Requires: iproute, /sbin/arping, findutils
Requires: cpio
Requires: hostname
Conflicts: ipsec-tools < 0.8.0-2
Conflicts: NetworkManager < 0.9.9.0-37.git20140131.el7
Conflicts: ppp < 2.4.6-4
Requires(pre): /usr/sbin/groupadd
Requires(post): /sbin/chkconfig, coreutils
Requires(preun): /sbin/chkconfig
%{?systemd_requires}
BuildRequires: glib2-devel popt-devel gettext pkgconfig systemd
Provides: /sbin/service

%description
This package contains the script that activates and deactivates most
network interfaces, some utilities, and other legacy files.

%package network
Summary: Legacy network configuration files

%description network
This package contains the legacy network configuration files.

%prep
%setup -q

%build
make

%install
make ROOT=%{buildroot} SUPERUSER=`id -un` SUPERGROUP=`id -gn` mandir=%{_mandir} install

%find_lang %{name}

%ifnarch s390 s390x
rm -f \
  %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc \
%endif

rm -f %{buildroot}%{_sysconfdir}/rc.d/rc.local %{buildroot}%{_sysconfdir}/rc.local
touch %{buildroot}%{_sysconfdir}/rc.d/rc.local
chmod 755 %{buildroot}%{_sysconfdir}/rc.d/rc.local

mkdir -p %{buildroot}%{_libexecdir}/initscripts
mkdir -p %{buildroot}%{_libexecdir}/initscripts/legacy-actions

%post
%systemd_post fedora-import-state.service fedora-loadmodules.service fedora-readonly.service

/usr/sbin/chkconfig --add network > /dev/null 2>&1 || :
/usr/sbin/chkconfig --add netconsole > /dev/null 2>&1 || :

%preun
%systemd_preun fedora-import-state.service fedora-loadmodules.service fedora-readonly.service

if [ $1 = 0 ]; then
  /usr/sbin/chkconfig --del network > /dev/null 2>&1 || :
  /usr/sbin/chkconfig --del netconsole > /dev/null 2>&1 || :
fi

%postun
%systemd_postun fedora-import-state.service fedora-loadmodules.service fedora-readonly.service

# This should be removed in Rawhide for Fedora 29:
%triggerun -- initscripts < 9.78
if [ $1 -gt 1 ]; then
  systemctl enable fedora-import-state.service fedora-readonly.service &> /dev/null || :
  echo -e "\nUPGRADE: Automatically re-enabling default systemd units: fedora-import-state.service fedora-readonly.service\n" || :
fi

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime
%config(noreplace) %{_sysconfdir}/sysconfig/netconsole
%config(noreplace) %{_sysconfdir}/sysconfig/readonly-root
%{_sbindir}/ifdown
%{_sbindir}/ifup
%dir %{_sysconfdir}/sysconfig/console
%dir %{_sysconfdir}/sysconfig/modules
%config(noreplace) %{_sysconfdir}/networks
%config(noreplace) %{_sysconfdir}/rwtab
%config(noreplace) %{_sysconfdir}/statetab
%dir %{_sysconfdir}/rwtab.d
%dir %{_sysconfdir}/statetab.d
%{_prefix}/lib/systemd/fedora-*
%{_prefix}/lib/systemd/system/*
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/rc[0-9].d
%{_sysconfdir}/rc[0-9].d
%dir %{_sysconfdir}/rc.d/init.d
%{_sysconfdir}/rc.d/init.d/*
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/rc.d/rc.local
%{_sysconfdir}/profile.d/*
%{_sbindir}/sys-unconfig
%{_bindir}/usleep
%attr(755,root,root) %{_sbindir}/usernetctl
%{_sbindir}/consoletype
%{_sbindir}/genhostid
%{_sbindir}/sushell
%attr(755,root,root) %{_sbindir}/netreport
%{_udevrulesdir}/*
%{_prefix}/lib/udev/rename_device
%{_sbindir}/service
%{_mandir}/man*/*
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%{_sysconfdir}/NetworkManager/dispatcher.d/00-netreport
%doc examples
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sharedstatedir}/stateless
%{_tmpfilesdir}/initscripts.conf
%dir %{_libexecdir}/initscripts
%dir %{_libexecdir}/initscripts/legacy-actions

%files network
%doc sysconfig.txt sysvinitfiles static-routes-ipv6 ipv6-tunnel.howto ipv6-6to4.howto changes.ipv6
%dir %{_sysconfdir}/sysconfig/network-scripts
%{_sysconfdir}/sysconfig/network-scripts/ifdown
%{_sysconfdir}/sysconfig/network-scripts/ifdown-post
%{_sysconfdir}/sysconfig/network-scripts/ifup
%{_sysconfdir}/sysconfig/network-scripts/network-functions
%{_sysconfdir}/sysconfig/network-scripts/network-functions-ipv6
%{_sysconfdir}/sysconfig/network-scripts/init.ipv6-global
%config(noreplace) %{_sysconfdir}/sysconfig/network-scripts/ifcfg-lo
%{_sysconfdir}/sysconfig/network-scripts/ifup-post
%{_sysconfdir}/sysconfig/network-scripts/ifup-routes
%{_sysconfdir}/sysconfig/network-scripts/ifdown-routes
%{_sysconfdir}/sysconfig/network-scripts/ifup-plip
%{_sysconfdir}/sysconfig/network-scripts/ifup-plusb
%{_sysconfdir}/sysconfig/network-scripts/ifup-bnep
%{_sysconfdir}/sysconfig/network-scripts/ifdown-bnep
%{_sysconfdir}/sysconfig/network-scripts/ifup-eth
%{_sysconfdir}/sysconfig/network-scripts/ifdown-eth
%{_sysconfdir}/sysconfig/network-scripts/ifup-ipv6
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ipv6
%{_sysconfdir}/sysconfig/network-scripts/ifup-sit
%{_sysconfdir}/sysconfig/network-scripts/ifdown-sit
%{_sysconfdir}/sysconfig/network-scripts/ifup-tunnel
%{_sysconfdir}/sysconfig/network-scripts/ifdown-tunnel
%{_sysconfdir}/sysconfig/network-scripts/ifup-aliases
%{_sysconfdir}/sysconfig/network-scripts/ifup-ippp
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ippp
%{_sysconfdir}/sysconfig/network-scripts/ifup-wireless
%{_sysconfdir}/sysconfig/network-scripts/ifup-isdn
%{_sysconfdir}/sysconfig/network-scripts/ifdown-isdn
%ifarch s390 s390x
%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc
%endif
