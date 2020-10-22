Name:           graphia
Version:        2.0
Release:        1%{?dist}%{?buildtag}
Summary:        A visualisation tool for the creation and analysis of graphs

License:        GPLv3
URL:            https://github.com/%{name}-app/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(Qt5Qml) >= 5.14
BuildRequires:  pkgconfig(Qt5Svg) >= 5.14
BuildRequires:  pkgconfig(Qt5OpenGLExtensions) >= 5.14
#BuildRequires:  blaze-devel
#BuildRequires:  boost-devel
#BuildRequires:  pkgconfig(cryptopp)
#BuildRequires:  pkgconfig(expat)
#BuildRequires:  hdf5-devel
#BuildRequires:  pkgconfig(matio)
#BuildRequires:  pkgconfig(qcustomplot-qt5)
#BuildRequires:  qtlockedfile-qt5-devel
#BuildRequires:  qtsingleapplication-qt5-devel
#BuildRequires:  utf8cpp-devel
#BuildRequires:  pkgconfig(valgrind)
#BuildRequires:  pkgconfig(zlib)
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
Requires:       hicolor-icon-theme
Requires:       qt5-qtwebview

%description
Graphia is a powerful open source visual analytics application developed
to aid the interpretation of large and complex datasets.
Graphia can create and visualise graphs from tables of numeric data and
display the structures that result. It can also be used to visualise and
analyse any data that is already in the form of a graph.

%prep
%autosetup -p1

%build
%cmake -B build -DCMAKE_INSTALL_PREFIX=%{_libexecdir}/%{name}
%make_build -C build

%install
%make_install -C build
# install link to main executable
install -d -m 0755 %{buildroot}%{_bindir}
ln -s %{_libexecdir}/%{name}/bin/Graphia %{buildroot}%{_bindir}/%{name}
# move icons and desktop file to the right place
cp -r %{buildroot}%{_libexecdir}/%{name}/share %{buildroot}%{_datadir}
rm -rf %{buildroot}%{_libexecdir}/%{name}/share
# validate desktop file
desktop-file-validate %{buildroot}/%{_datadir}/applications/Graphia.desktop

%files
%license LICENSE
%{_bindir}/%{name}
%{_libexecdir}/%{name}/bin/Graphia
%{_libexecdir}/%{name}/bin/CrashReporter
%{_libexecdir}/%{name}/bin/MessageBox
%{_libexecdir}/%{name}/bin/Updater
%{_libexecdir}/%{name}/lib/libthirdparty.so
%{_libexecdir}/%{name}/lib/Graphia/plugins/libcorrelation.so
%{_libexecdir}/%{name}/lib/Graphia/plugins/libgeneric.so
%{_libexecdir}/%{name}/lib/Graphia/plugins/libwebsearch.so
%{_datadir}/applications/Graphia.desktop
%{_datadir}/icons/hicolor/*/Graphia.png

%changelog

