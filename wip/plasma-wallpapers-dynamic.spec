%global component wallpapers-dynamic

Name:           plasma-%{component}
Version:        3.3.5
Release:        1%{?dist}%{?buildtag}
Summary:        Dynamic wallpaper plugin for KDE Plasma

License:        GPLv3 and LGPLv3 and MIT
URL:            https://github.com/zzag/plasma5-%{component}
Source0:        %{url}/archive/%{version}/plasma5-%{component}-%{version}.tar.gz

BuildRequires:  cmake, extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtlocation-devel
BuildRequires:  kf5-kpackage-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  libexif-devel
BuildRequires:  libheif-devel
BuildRequires:  desktop-file-utils
Recommends:     dynamicwallpaper-lakeside-louis-coyle

%description
A simple dynamic wallpaper plugin for KDE Plasma.

%prep
%autosetup -p1

%build
%cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DBUILD_TESTING=OFF
%make_build -C build

%install
%make_install -C build
%find_lang plasma_wallpaper_com.github.zzag.wallpaper
desktop-file-validate %{buildroot}/%{_datadir}/kservices5/plasma-wallpaper-com.github.zzag.wallpaper.desktop

%files -f plasma_wallpaper_com.github.zzag.wallpaper.lang
%license LICENSES/*
%{_libdir}/qt5/plugins/kpackage/packagestructure/packagestructure_dynamicwallpaper.so
%{_libdir}/qt5/qml/com/github/zzag
%{_datadir}/dynamicwallpapers
%{_datadir}/kservices5/plasma-wallpaper-com.github.zzag.wallpaper.desktop
%{_datadir}/metainfo/com.github.zzag.wallpaper.appdata.xml
%{_datadir}/plasma/wallpapers/com.github.zzag.wallpaper

%changelog
