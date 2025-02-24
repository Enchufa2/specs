%bcond_without check
%global upname ark

Name:           %{upname}-kernel
Version:        0.1.166
Release:        1%{?dist}
Summary:        Ark, an R Kernel

# SourceLicense:  MIT
License:        MIT
# LICENSE.dependencies contains a full license breakdown

URL:            https://github.com/posit-dev/%{upname}
Source:         %{url}/archive/%{version}/%{upname}-%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel
Requires:       R-core

%description
Ark is an R kernel for Jupyter applications. It was created to serve as
the interface between R and the Positron IDE and is compatible with all
frontends implementing the Jupyter protocol.

%prep
%autosetup -p1 -n %{upname}-%{version}
%cargo_prep -N
sed -i '/offline/d' .cargo/config.toml

%build
%cargo_build
#%%{cargo_license_summary}
#%%{cargo_license} > LICENSE.dependencies

%install
#%%cargo_install
install -d -m 0755 %{buildroot}%{_libexecdir}/%{name}/bin
install -m 0755 target/rpm/{%{upname},echo} %{buildroot}%{_libexecdir}/%{name}/bin
find .cargo/registry -type f -name "*.rs" -exec chmod -x {} \;

#%%if %{with check}
#%%check
#%%cargo_test
#%%endif

%files
%license LICENSE
%license crates/%{upname}/NOTICE
#%%license LICENSE.dependencies
%doc BUILDING.md
%doc CHANGELOG.md
%doc README.md
%{_libexecdir}/%{name}

%changelog
