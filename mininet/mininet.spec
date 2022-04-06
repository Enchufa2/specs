Name:           mininet
Version:        2.3.0
Release:        2%{?dist}
Summary:        Emulator for rapid prototyping of Software Defined Networks

License:        MIT
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  help2man

# mininet can use openvswitch or other OpenFlow switches for packet forwarding
Requires:       openvswitch
# mininet relies on cgroups and network namespaces to emulate network nodes
Requires:       libcgroup-tools
# tools required for managing processes
Requires:       which, psmisc, procps-ng
# tools required for accessing and operate emulated nodes
Requires:       xterm, socat, openssh-clients
# tools required for managing network interfaces at emulated nodes
Requires:       iproute, ethtool, net-tools
# tools required for connectivity testing at emulated nodes
Requires:       telnet, iperf

%description
Mininet emulates a complete network of hosts, links, and switches on a single
machine. To create a sample two-host, one-switch network, just run: 'sudo mn'

Mininet is useful for interactive development, testing, and demos, especially
those using OpenFlow and SDN. OpenFlow-based network controllers prototyped
in Mininet can usually be transferred to hardware with minimal changes for
full line-rate execution.


%prep
%autosetup -p1

# remove shebangs to make rpmlint happy
sed -i '/#\!\/usr\/bin\/env python$/d' mininet/topo.py examples/*.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel
export PYTHON=%{python3}
%make_build man
%make_build mnexec


%install
install -p -D mnexec %{buildroot}%{_bindir}/mnexec
install -p -D -m 644 -t %{buildroot}%{_mandir}/man1 mn.1 mnexec.1
%pyproject_install
%pyproject_save_files %{name}


%check
%pyproject_check_import -t


%files -f %{pyproject_files}
%doc README.* CONTRIBUTORS
%license LICENSE
%{_bindir}/mn
%{_bindir}/mnexec
%{_mandir}/man1/mn.1*
%{_mandir}/man1/mnexec.1*


%changelog
* Wed Apr 06 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2.3.0-2
- Remove explicit compilation flags
- Preserve timestamps in install
- Add comments to Requires
- Remove shebangs from mininet/topo.py and examples

* Fri Mar 18 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2.3.0-1
- Initial packaging for Fedora
