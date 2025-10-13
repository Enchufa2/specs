%global project certbot-dns-dinahosting
%global module certbot_dns_dinahosting
%global commit 4f66a5a3c081f030f6eaac658494ffd22728cc28
%global short_commit 4f66a5a

Name:           python-%{project}
Version:        1.0.0
Release:        1%{?dist}%{?buildtag}
Summary:        Dinahosting DNS Authenticator plugin for Certbot

License:        Apache-2.0
URL:            https://github.com/rdrgzlng/%{project}
Source0:        %{url}/archive/%{commit}/%{project}-%{commit}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
This plugin automates the process of completing a dns-01 challenge by
creating, and subsequently removing, TXT records using the Dinahosting API.}

%description %_description

%package -n python3-%{project}
Summary:        %{summary}

%description -n python3-%{project} %_description

%prep
%autosetup -p1 -n %{project}-%{commit}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{module}

%files -n python3-%{project} -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
