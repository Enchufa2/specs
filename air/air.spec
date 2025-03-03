%bcond_without check

Name:           air
Version:        0.4.1
Release:        1%{?dist}
Summary:        An R formatter and language server

# SourceLicense:  MIT
License:        MIT
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/posit-dev/%{name}
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gcc-c++

%description
An R formatter and language server, written in Rust.

%prep
%autosetup -p1 -n %{name}-%{version}
%cargo_prep -N
sed -i '/offline/d' .cargo/config.toml

%build
%cargo_build
#%%{cargo_license_summary}
#%%{cargo_license} > LICENSE.dependencies

%install
#%%cargo_install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 target/rpm/%{name} %{buildroot}%{_bindir}/%{name}
#find .cargo/registry -type f -name "*.rs" -exec chmod -x {} \;

#%%if %{with check}
#%%check
#%%cargo_test
#%%endif

%files
%license LICENSE
#%%license LICENSE.dependencies
%doc CHANGELOG.md
%doc README.md
%{_bindir}/%{name}

%changelog
