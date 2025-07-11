%global debug_package %{nil}

Name:           quarto
Version:        1.7.32
Release:        1%{?dist}
Summary:        An open-source scientific and technical publishing system

License:        MIT
URL:            https://github.com/%{name}-dev/%{name}-cli
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Provides:       bundled(deno)      = 1.46.3
Provides:       bundled(deno-dom)  = 0.1.41
Provides:       bundled(pandoc)    = 3.6.3
Provides:       bundled(dart-sass) = 1.85.1
Provides:       bundled(esbuild)   = 0.19.12
Provides:       bundled(typst)     = 0.13.0

%description
Author using Jupyter notebooks or with plain text markdown in your favorite
editor. Create dynamic content with Python, R, Julia, and Observable. Publish
reproducible, production quality articles, presentations, dashboards, websites,
blogs, and books in HTML, PDF, MS Word, ePub, and more. Share knowledge and
insights organization-wide by publishing to Posit Connect, Confluence, or
other publishing systems. Write using Pandoc markdown, including equations,
citations, crossrefs, figure panels, callouts, advanced layout, and more.

%prep
%autosetup -p1 -n %{name}-cli-%{version}

%build
./configure.sh
pushd package/src
    ./quarto-bld prepare-dist --set-version %{version} --arch $(uname -m) --log-level info
popd

%install
# install files
install -d -m 0755 %{buildroot}%{_libexecdir}
mv package/pkg-working %{buildroot}%{_libexecdir}/%{name}
# install symlink to binary
install -d -m 0755 %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/%{name}/bin/%{name} %{buildroot}%{_bindir}
# install man pages
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -D -m 0644 \
    %{buildroot}%{_libexecdir}/%{name}/share/man/%{name}-man.man \
    %{buildroot}%{_mandir}/man1/%{name}.1
rm -rf %{buildroot}%{_libexecdir}/%{name}/share/man

%files
%{_bindir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/bin
%{_libexecdir}/%{name}/share
%{_mandir}/man1/%{name}.1*

%changelog
