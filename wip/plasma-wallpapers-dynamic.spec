%global component wallpapers-dynamic

Name:           plasma-%{component}
Version:        3.3.9
Release:        1%{?dist}
Summary:        Dynamic wallpaper plugin for KDE Plasma

License:        GPLv3 and LGPLv3 and BSD and CC0 and CC-BY-SA
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
Recommends:     %{name}-builder

%description
A simple dynamic wallpaper plugin for KDE Plasma.

%package        devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains the development headers and libraries.

%package        builder
Summary:        Wallpaper builder for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    builder
Command-line utility to build dynamic wallpapers.

%package        builder-bash-completion
Summary:        Bash completion support for %{name}-builder
BuildArch:      noarch
Requires:       %{name}-builder%{?_isa} = %{version}-%{release}
Requires:       bash bash-completion

%description    builder-bash-completion
Files needed to support bash completion.

%package        builder-fish-completion
Summary:        Fish completion support for %{name}-builder
BuildArch:      noarch
Requires:       %{name}-builder%{?_isa} = %{version}-%{release}
Requires:       fish

%description    builder-fish-completion
Files needed to support fish completion.

%package        builder-zsh-completion
Summary:        Zsh completion support for %{name}-builder
BuildArch:      noarch
Requires:       %{name}-builder%{?_isa} = %{version}-%{release}
Requires:       zsh

%description    builder-zsh-completion
Files needed to support zsh completion.

%prep
%autosetup -n plasma5-%{component}-%{version}

%build
%cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DBUILD_TESTING=OFF
%make_build -C build

%install
%make_install -C build
%find_lang plasma_wallpaper_com.github.zzag.dynamic
desktop-file-validate %{buildroot}/%{_datadir}/kservices5/plasma-wallpaper-com.github.zzag.dynamic.desktop

%files -f plasma_wallpaper_com.github.zzag.dynamic.lang
%license LICENSES/*
%{_datadir}/plasma/wallpapers/com.github.zzag.dynamic
%{_datadir}/metainfo/com.github.zzag.dynamic.appdata.xml
%{_datadir}/kservices5/plasma-wallpaper-com.github.zzag.dynamic.desktop
%{_libdir}/qt5/qml/com/github/zzag/plasma/wallpapers/dynamic
%{_libdir}/qt5/plugins/kpackage/packagestructure/packagestructure_dynamicwallpaper.so
%{_libdir}/libkdynamicwallpaper.so.1.0.0
%{_libdir}/libkdynamicwallpaper.so.1
"%{_datadir}/wallpapers/Dynamic Numbers"

%files devel
%{_includedir}/KDynamicWallpaper
%{_libdir}/libkdynamicwallpaper.so
%{_libdir}/cmake/KDynamicWallpaper

%files builder
%{_bindir}/kdynamicwallpaperbuilder

%files builder-bash-completion
%{_datadir}/bash-completion/completions/kdynamicwallpaperbuilder

%files builder-fish-completion
%{_datadir}/fish/completions/kdynamicwallpaperbuilder.fish

%files builder-zsh-completion
%{_datadir}/zsh/site-functions/_kdynamicwallpaperbuilder

%changelog
* Sat Jun 05 2021 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.9-1
- Update to v3.3.9

* Sat Nov 14 2020 Iñaki Úcar <iucar@fedoraproject.org> - 3.3.5-1
- Initial packaging for Fedora
