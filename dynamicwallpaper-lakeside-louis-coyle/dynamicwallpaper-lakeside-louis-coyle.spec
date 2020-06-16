%global git_date 20191105
%global git_commit 2b8f7e6cccded0968fd43cc86fd4eda773388971
%global git_short %(echo %{git_commit} | cut -c1-7)

Name:           dynamicwallpaper-lakeside-louis-coyle
Version:        0
Release:        2.%{git_date}git%{git_short}%{?dist}
Summary:        Dynamic wallpaper for KDE Plasma
BuildArch:      noarch

License:        Public Domain
URL:            https://github.com/hugotrsd/%{name}
Source0:        %{url}/archive/%{git_commit}/%{name}-%{git_commit}.tar.gz

BuildRequires:  plasma5-wallpapers-dynamic
Requires:       plasma5-wallpapers-dynamic

%description
Wallpaper based on Louis Coyle's dynamic wallpaper for MacOS.

%prep
%autosetup -p1 -n %{name}-%{git_commit}

%build

%install
install -d -m 0755 %{buildroot}%{_datadir}/dynamicwallpapers/lakeside
sed -i '/"Id":/c\        "Id": "lakeside",' metadata.json
cp -r metadata.json contents %{buildroot}%{_datadir}/dynamicwallpapers/lakeside

%files
%{_datadir}/dynamicwallpapers/lakeside

%changelog
