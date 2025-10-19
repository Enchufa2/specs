%global commit 29499edd20ef021e7942cdc993f6520febdf5454
%global short_commit 29499ed

Name:           dinaip
Version:        0^1.git%{short_commit}
Release:        1%{?dist}%{?buildtag}
Summary:        Haz que tu dominio resuelva en una IP dinámica

License:        LGPL-3.0-or-later
URL:            https://github.com/dinahosting/%{name}-linux-shell
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        %{name}.service
Source2:        logrotate
Source3:        environment
Patch:          %{name}-grep.patch

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Requires:       perl-libwww-perl
Requires:       curl
Requires:       logrotate
%{?systemd_requires}

%description
dinaIP es una aplicación que se encarga de monitorizar la IP del equipo
en el que se está ejecutando y actualizar la información de las zonas
según vaya cambiando la misma. Así, permite que todas aquellas zonas
que están apuntando a dicho equipo estén siempre actualizadas con los
cambios que se van dando.

%prep
%autosetup -p1 -n %{name}-linux-shell-%{commit}
rm source/install.sh
sed -i 's@/var/run@/run@' source/Demonio.pm

%build

%install
install -d -m 0755  %{buildroot}%{_libdir}/%{name} \
                    %{buildroot}%{_bindir} \
                    %{buildroot}%{_unitdir} \
                    %{buildroot}%{_sysconfdir}/logrotate.d
cp -a source/* %{buildroot}%{_libdir}/%{name}/
ln -s %{_libdir}/%{name}/%{name}.pl %{buildroot}%{_bindir}/%{name}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 0600 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE
%doc README.md
%{_libdir}/%{name}
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}

%changelog
%autochangelog
