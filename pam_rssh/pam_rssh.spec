Name:           pam_rssh
Version:        1.2.0
Release:        1%{?dist}
Summary:        PAM module for restricted SSH

SourceLicense:  MIT
License:        Apache-2.0 AND (BSD-2-Clause OR Apache-2.0) AND CC-PDDC AND (MIT OR Apache-2.0) AND (Unlicense OR MIT)
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/z4yx/%{name}
Source:         %{URL}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  pam-devel

%description
This PAM module allows restricting SSH access based on user configuration.

%prep
%autosetup -n %{name}-%{version} -p1
rm -rf dep && sed -i 's/ssh-agent.*/ssh-agent = "0.2.3"/' Cargo.toml
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
mkdir -p %{buildroot}%{_libdir}/security/
install -m 755 target/release/lib%{name}.so %{buildroot}%{_libdir}/security/

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_libdir}/security/lib%{name}.so

%changelog
* Tue Aug 26 2025 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.0-1
- Initial package
