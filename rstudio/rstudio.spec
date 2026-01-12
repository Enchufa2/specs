%global bundled_gwt_version         2.12.2
%global bundled_websockets_version  1.0.4
%global bundled_gin_version         2.1.2
%global bundled_guava_version       32.1.3
%global bundled_jakartaiapi_version 2.0.1
%global bundled_errorpa_version     2.23.0
%global bundled_failureacc_version  1.0.2
%global bundled_elemental2_version  1.2.3
%global bundled_junit_version       4.9b3
%global bundled_guice_version       6.0.0
%global bundled_aopalliance_version 1.0
%global bundled_hunspell_version    1.7.2
%global bundled_rapidjson_version   24b5e7a
%global bundled_treehh_version      2.81
%global bundled_sundown_version     1.16.0
%global bundled_synctex_version     1.17
%global bundled_ace_version         1.32.5
%global bundled_datatables_version  1.10.4
%global bundled_jquery_version      3.5.1
%global bundled_pdfjs_version       1.3.158
%global bundled_revealjs_version    2.4.0
%global bundled_jsbn_version        1.1
%global bundled_highlightjs_version c589dcc
%global bundled_qunitjs_version     1.18.0
%global bundled_xtermjs_version     3.14.5
%global bundled_jsyaml_version      5.0.2
%global bundled_jsdiff_version      8.0.2
%global mathjax_short               27
%global rstudio_node_version        22
%global rstudio_version_major       2026
%global rstudio_version_minor       01
%global rstudio_version_patch       0
%global rstudio_version_suffix      392
%global rstudio_git_revision_hash   49fbea7a09a468fc4d1993ca376fd5b971cb58e3
%global quarto_git_revision_hash    591b3520eafbb4da7b26b9f31aac6948801f19d8
%global rstudio_version             %{rstudio_version_major}.%{rstudio_version_minor}.%{rstudio_version_patch}
%global rstudio_flags \
    export RSTUDIO_VERSION_MAJOR=%{rstudio_version_major} ; \
    export RSTUDIO_VERSION_MINOR=%{rstudio_version_minor} ; \
    export RSTUDIO_VERSION_PATCH=%{rstudio_version_patch} ; \
    export RSTUDIO_VERSION_SUFFIX=+%{rstudio_version_suffix} ; \
    export RSTUDIO_GIT_REVISION_HASH=%{rstudio_git_revision_hash} ; \
    export GIT_COMMIT=%{rstudio_git_revision_hash} ; \
    export PACKAGE_OS=$(cat /etc/redhat-release)

# Disable deprecated openssl engine
%global _preprocessor_defines %{_preprocessor_defines} -DOPENSSL_NO_ENGINE
# Do not build non-lto objects, as that may result in
# memory exhaustion by the linker.
%global optflags %(echo '%{optflags}' | sed -e 's!-ffat-lto-objects!-fno-fat-lto-objects!g')

Name:           rstudio
Version:        %{rstudio_version}+%{rstudio_version_suffix}
Release:        1%{?dist}
Summary:        RStudio base package
ExclusiveArch:  %{java_arches}

# See NOTICE file
License:        AGPL-3.0-or-later AND LGPL-2.1-or-later AND Apache-2.0 AND MIT AND BSD-3-Clause AND ISC AND W3C AND MPL-1.1 AND CPL-1.0 AND CC-BY-SA-4.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/%{rstudio_git_revision_hash}/%{name}-%{version}.tar.gz
Source1:        https://github.com/quarto-dev/quarto/archive/%{quarto_git_revision_hash}/quarto-%{quarto_git_revision_hash}.tar.gz
Source2:        %{name}.metainfo.xml
# Unbundle mathjax, pandoc, hunspell dictionaries
Patch0:         0000-unbundle-dependencies-common.patch
# Move resources/app to the root
Patch1:         0001-flatten-tree.patch
# Use system-provided nodejs binary
Patch4:         0004-use-system-node.patch

BuildRequires:  make, cmake, ant
BuildRequires:  gcc-c++, java-devel, R-core-devel
BuildRequires:  nodejs%{rstudio_node_version}
BuildRequires:  nodejs%{rstudio_node_version}-npm
BuildRequires:  python3dist(setuptools), git-core
BuildRequires:  quarto
BuildRequires:  mathjax
BuildRequires:  lato-fonts, glyphography-newscycle-fonts
BuildRequires:  boost-devel, boost-url
BuildRequires:  soci-postgresql-devel, soci-sqlite3-devel
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  rapidxml-devel
BuildRequires:  cmake(fmt)
BuildRequires:  cmake(gsl-lite)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  cmake(rapidjson)
BuildRequires:  cmake(tl-expected)
BuildRequires:  cmake(websocketpp)
BuildRequires:  cmake(yaml-cpp)
BuildRequires:  zlib-static
BuildRequires:  hicolor-icon-theme
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

%global _description %{expand:
RStudio is an integrated development environment (IDE) for R. It includes a
console, syntax-highlighting editor that supports direct code execution, as
well as tools for plotting, history, debugging and workspace management.
}

%description    %_description

%package        common
Summary:        Common files for RStudio Desktop and Server
# Avoid issues with upstream package provided by Posit
Conflicts:      %{name} > 2024.04.0
# Ease transition (will be removed in a future release)
Obsoletes:      %{name} < 2024.04.0
Suggests:       %{name}-desktop
Suggests:       %{name}-server
Recommends:     git-core
Recommends:     clang-devel
Requires:       hunspell
Requires:       quarto
Requires:       mathjax
Requires:       lato-fonts, glyphography-newscycle-fonts

Provides:       bundled(gwt) = %{bundled_gwt_version}
Provides:       bundled(gwt-websockets) = %{bundled_websockets_version}
Provides:       bundled(gin) = %{bundled_gin_version}
Provides:       bundled(guava) = %{bundled_guava_version}
Provides:       bundled(jakarta-inject-api) = %{bundled_jakartaiapi_version}
Provides:       bundled(error-prone-annotations) = %{bundled_errorpa_version}
Provides:       bundled(failureaccess) = %{bundled_failureacc_version}
Provides:       bundled(elemental2) = %{bundled_elemental2_version}
Provides:       bundled(junit) = %{bundled_junit_version}
Provides:       bundled(guice) = %{bundled_guice_version}
Provides:       bundled(aopalliance) = %{bundled_aopalliance_version}
Provides:       bundled(hunspell) = %{bundled_hunspell_version}
Provides:       bundled(rapidjson) = %{bundled_rapidjson_version}
Provides:       bundled(tree-hh) = %{bundled_treehh_version}
Provides:       bundled(sundown) = %{bundled_sundown_version}
Provides:       bundled(synctex) = %{bundled_synctex_version}
Provides:       bundled(js-ace) = %{bundled_ace_version}
Provides:       bundled(js-datatables) = %{bundled_datatables_version}
Provides:       bundled(js-jquery) = %{bundled_jquery_version}
Provides:       bundled(js-pdf) = %{bundled_pdfjs_version}
Provides:       bundled(js-reveal) = %{bundled_revealjs_version}
Provides:       bundled(js-bn) = %{bundled_jsbn_version}
Provides:       bundled(js-highlight) = %{bundled_highlightjs_version}
Provides:       bundled(js-qunit) = %{bundled_qunitjs_version}
Provides:       bundled(js-xterm) = %{bundled_xtermjs_version}
Provides:       bundled(js-yaml) = %{bundled_jsyaml_version}
Provides:       bundled(js-jsdiff) = %{bundled_jsdiff_version}

%description    common %_description
This package provides common files for %{name}-desktop and %{name}-server.

%package        desktop
Summary:        Integrated development environment for the R programming language
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires:       hicolor-icon-theme, shared-mime-info

%description    desktop %_description
This package provides the Desktop version, to access the RStudio IDE locally.

%package        server
Summary:        Access RStudio via a web browser
Requires:       %{name}-common%{?_isa} = %{version}-%{release}
Requires(pre):  shadow-utils
%{?systemd_requires}

%description    server %_description
This package provides the Server version, a browser-based interface to the RStudio IDE.

%prep
%autosetup -p1 -n %{name}-%{rstudio_git_revision_hash}
tar -xf %{SOURCE1}
mv quarto-%{quarto_git_revision_hash} src/gwt/lib/quarto

# system libraries
ln -sf %{_includedir}/rapidxml.h src/cpp/core/include/core/rapidxml/rapidxml.hpp
sed -i 's/"${${_PREFIX}_VERSION}" //g' src/cpp/ext/CMakeLists.txt # rm version requirement
sed -i 's/::fmt//g' src/cpp/core/CMakeLists.txt
sed -i 's/::yaml-cpp//g' src/cpp/core/CMakeLists.txt

# additional dependencies
export RSTUDIO_TOOLS_ROOT=$PWD/dependencies/common && pushd $RSTUDIO_TOOLS_ROOT
    ./install-gwt
    ./install-copilot-language-server
    platform=$([ "%{_arch}" = "x86_64" ] && echo "arm64" || echo "x64")
    for f in darwin win32 $platform; do find . -name $f -exec rm -rf {} +; done
popd

# fix error: ‘make_unique’ is not a member of ‘boost’
sed -i '30i #include <boost/make_unique.hpp>' src/cpp/session/modules/rmarkdown/NotebookExec.cpp

%build
mkdir -p dependencies/common/node/%{rstudio_node_version}/bin
export PATH="$PWD/dependencies/common/node/%{rstudio_node_version}/bin:$PATH"
pushd dependencies/common/node/%{rstudio_node_version}
    ln -s %{_bindir}/node-%{rstudio_node_version} bin/node
    ln -s %{_bindir}/npm-%{rstudio_node_version} bin/npm
    ln -s %{_bindir}/npx-%{rstudio_node_version} bin/npx
    ./bin/npm install yarn && ln -s $PWD/node_modules/yarn/bin/yarn bin/yarn
popd
%{rstudio_flags}
%cmake -Wno-dev -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_libexecdir}/%{name} \
    -DRSTUDIO_DISABLE_CHECK_FOR_UPDATES=1 \
    -DRSTUDIO_TARGET=Electron \
    -DRSTUDIO_ELECTRON=TRUE \
    -DRSTUDIO_SERVER=TRUE \
    -DQUARTO_ENABLED=FALSE \
    -DRSTUDIO_USE_SYSTEM_TL_EXPECTED=Yes \
    -DRSTUDIO_USE_SYSTEM_FMT=Yes \
    -DRSTUDIO_USE_SYSTEM_GSL_LITE=No \
    -DRSTUDIO_USE_SYSTEM_HUNSPELL=No \
    -DRSTUDIO_USE_SYSTEM_RAPIDJSON=No \
    -DRSTUDIO_USE_SYSTEM_WEBSOCKETPP=Yes \
    -DRSTUDIO_USE_SYSTEM_YAML_CPP=Yes \
    -DRSTUDIO_USE_SYSTEM_ZLIB=Yes \
    -DRSTUDIO_USE_SYSTEM_SOCI=Yes \
    -DRSTUDIO_USE_SYSTEM_BOOST=Yes \
    -DBOOST_ROOT=%{_prefix} -DBOOST_LIBRARYDIR=%{_lib} \
    -DRSTUDIO_BOOST_REQUESTED_VERSION=1.83.0 \
    -DRSTUDIO_NODE_VERSION=%{rstudio_node_version}
%make_build -C build # ALL

%install
%{rstudio_flags}
%make_install -C build
# expose symlinks in /usr/bin
install -d -m 0755 %{buildroot}%{_bindir}
ln -s %{_libexecdir}/%{name}/{%{name},bin/%{name}-server} %{buildroot}%{_bindir}

# validate .desktop and .metainfo.xml files
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
mkdir -p %{buildroot}%{_metainfodir}
install -m 0644 %{SOURCE2} %{buildroot}%{_metainfodir}/
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.metainfo.xml

# create required directories for rstudio-server (according to INSTALL)
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}-server

# install the systemd service file and change /var/run -> /run
install -D -m 0644 \
    %{buildroot}%{_libexecdir}/%{name}/extras/systemd/%{name}-server.service \
    %{buildroot}%{_unitdir}/%{name}-server.service
sed -i 's@/var/run@/run@g' %{buildroot}%{_unitdir}/%{name}-server.service

# install the PAM module
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 0644 \
    %{buildroot}%{_libexecdir}/%{name}/extras/pam/%{name} \
    %{buildroot}%{_sysconfdir}/pam.d/%{name}

# symlink the location where the bundled dependencies should be
mv dependencies/common/copilot-language-server-js %{buildroot}%{_libexecdir}/%{name}/bin
pushd %{buildroot}%{_libexecdir}/%{name}/bin
    mkdir -p pandoc
    ln -sf %{_libexecdir}/quarto/bin/tools/%{_arch}/pandoc pandoc/pandoc
popd
pushd %{buildroot}%{_libexecdir}/%{name}/resources
    mv app/{.,}* .. && rm -rf app && ln -s .. app
    ln -sf %{_datadir}/hunspell dictionaries
    ln -sf %{_datadir}/javascript/mathjax mathjax-%{mathjax_short}
    pushd presentation/revealjs/fonts
        for fnt in Lato*.ttf; do
            ln -sf %{_datadir}/fonts/lato-fonts/${fnt} ${fnt}
        done
        for fnt in News*.ttf; do
            ln -sf %{_datadir}/fonts/glyphography-newscycle-fonts/${fnt,,} ${fnt}
        done
    popd
    # move and symlink bundled libraries
    mv grid/datatables grid/datatables.bundled
    ln -sf ./datatables.bundled grid/datatables
    mv pdfjs pdfjs.bundled
    ln -sf ./pdfjs.bundled pdfjs
    mv presentation/revealjs presentation/revealjs.bundled
    ln -sf ./revealjs.bundled presentation/revealjs
popd

# clean up
pushd %{buildroot}%{_libexecdir}/%{name}
    for f in .gitignore .Rbuildignore LICENSE README; do
        find . -name ${f} -delete
    done
    rm -rf extras COPYING INSTALL NOTICE README.md SOURCE VERSION
    rm -rf clang_x64_v8_arm64
popd

# add user rstudio-server
%pre server
getent group %{name}-server >/dev/null || groupadd -r %{name}-server
getent passwd %{name}-server >/dev/null || \
    useradd -r -g %{name}-server -d %{_sharedstatedir}/%{name}-server -s /sbin/nologin \
    -c "User for %{name}-server" %{name}-server
exit 0

%post server
%systemd_post %{name}-server.service

%preun server
%systemd_preun %{name}-server.service

%postun server
%systemd_postun_with_restart %{name}-server.service

%triggerun server -- %{name}-server
chown -R %{name}-server:%{name}-server %{_sharedstatedir}/%{name}-server

%files common
%license COPYING NOTICE
%doc README.md
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/bin
%{_libexecdir}/%{name}/bin/debuginfo
%{_libexecdir}/%{name}/bin/pandoc
%{_libexecdir}/%{name}/bin/copilot-language-server-js
%{_libexecdir}/%{name}/bin/postback
%{_libexecdir}/%{name}/bin/r-ldpath
%{_libexecdir}/%{name}/bin/rpostback
%{_libexecdir}/%{name}/bin/rsession
%{_libexecdir}/%{name}/R
%{_libexecdir}/%{name}/resources
%{_libexecdir}/%{name}/www
%{_libexecdir}/%{name}/www-symbolmaps

%files desktop
%license %{_libexecdir}/%{name}/LICENSES.chromium.html
%{_bindir}/%{name}
%{_libexecdir}/%{name}/.webpack
%{_libexecdir}/%{name}/bin/diagnostics
%{_libexecdir}/%{name}/bin/%{name}-backtrace.sh
%{_libexecdir}/%{name}/chrome-sandbox
%{_libexecdir}/%{name}/chrome_100_percent.pak
%{_libexecdir}/%{name}/chrome_200_percent.pak
%{_libexecdir}/%{name}/chrome_crashpad_handler
%{_libexecdir}/%{name}/icudtl.dat
%{_libexecdir}/%{name}/libEGL.so
%{_libexecdir}/%{name}/libGLESv2.so
%{_libexecdir}/%{name}/libffmpeg.so
%{_libexecdir}/%{name}/libvk_swiftshader.so
%{_libexecdir}/%{name}/libvulkan.so.1
%{_libexecdir}/%{name}/locales
%{_libexecdir}/%{name}/resources.pak
%{_libexecdir}/%{name}/%{name}
%{_libexecdir}/%{name}/%{name}.png
%{_libexecdir}/%{name}/package.json
%{_libexecdir}/%{name}/snapshot_blob.bin
%{_libexecdir}/%{name}/v8_context_snapshot.bin
%{_libexecdir}/%{name}/version
%{_libexecdir}/%{name}/vk_swiftshader_icd.json
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png
%{_metainfodir}/%{name}.metainfo.xml

%files server
%{_bindir}/%{name}-server
%{_libexecdir}/%{name}/bin/rserver
%{_libexecdir}/%{name}/bin/rserver-pam
%{_libexecdir}/%{name}/bin/rserver-url
%{_libexecdir}/%{name}/bin/%{name}-server
%{_libexecdir}/%{name}/db
%dir %{_sharedstatedir}/%{name}-server
%{_unitdir}/%{name}-server.service
%config(noreplace) %{_sysconfdir}/pam.d/%{name}

%changelog
* Mon Jan 12 2026 Iñaki Úcar <iucar@fedoraproject.org> - 2026.01.0+392-1
- Update to 2026.01.0+392

* Mon Nov 03 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2025.09.2+418-1
- Update to 2025.09.2+418

* Mon Oct 06 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2025.09.1+401-1
- Update to 2025.09.1+401

* Mon Sep 15 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2025.09.0+387-1
- Update to 2025.09.0+387

* Mon Jun 09 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2025.05.1+513-1
- Update to 2025.05.1+513

* Wed May 07 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2025.05.0+496-2
- Unbundle some stuff back

* Tue May 06 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2025.05.0+496-1
- Update to  2025.05.0+496

* Sun Apr 27 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2024.12.1+563-3
- Rebuild for SOCI 4.1

* Thu Mar 06 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2024.12.1+563-2
- Link to quarto's pandoc version

* Mon Feb 17 2025 Iñaki Úcar <iucar@fedoraproject.org> - 2024.12.1+563-1
- Update to 2024.12.1+563

* Mon Dec 23 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.12.0+467-1
- Update to 2024.12.0+467

* Mon Nov 11 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.09.1+394-2
- Update to 2024.09.1+394
- Add upstream patch to fix font issues

* Tue Sep 24 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.09.0+375-1
- Update to 2024.09.0+375

* Tue Jul 02 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.04.2+764-2
- Define OPENSSL_NO_ENGINE to avoid deprecated API

* Tue Jun 11 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.04.2+764-1
- Update to 2024.04.2+764

* Wed May 29 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.04.0+735-3
- Fix Lato fonts link

* Thu May 02 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.04.0+735-2
- Version conflict and obsolete the previous versions to ease transition

* Wed May 01 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2024.04.0+735-1
- Update to 2024.04.0+735
- Rename rstudio as rstudio-common, set conflicts with upstream package

* Thu Apr 25 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2023.12.1+402-3
- R-maint-sig mass rebuild

* Tue Feb 27 2024 Jiri Vanek <jvanek@redhat.com> - 2023.12.1+402-2
- Rebuilt for java-21-openjdk as system jdk

* Fri Feb 02 2024 Iñaki Úcar <iucar@fedoraproject.org> - 2023.12.1+402-1
- Update to 2023.12.1+402

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.12.0+369-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2023.12.0+369-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 2023.12.0+369-2
- Rebuilt for Boost 1.83

* Wed Dec 20 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.12.0+369-1
- Update to 2023.12.0+369

* Tue Oct 31 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.09.1+494-2
- Fix Copilot's node path resolution

* Thu Oct 19 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.09.1+494-1
- Update to 2023.09.1+494

* Thu Sep 28 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.09.0+463-1
- Update to 2023.09.0+463

* Fri Aug 25 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.06.2+561-1
- Update to 2023.06.2+561

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.06.1+524-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.06.1+524-1
- Update to 2023.06.1+524

* Wed Jul 05 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.06.0+421-3
- Add RSTUDIO_DISABLE_CHECK_FOR_UPDATES=1 to the desktop file
- Drop QT_QPA_PLATFORM=xcb from the desktop file
- Drop dependency on orphaned esbuild

* Wed Jun 28 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 2023.06.0+421-2
- Rebuilt due to fmt 10 update.

* Thu Jun 08 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.06.0+421-1
- Update to 2023.06.0+421

* Fri May 12 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.03.1+446-1
- Update to 2023.03.1+446

* Mon Apr 24 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.03.0+386-4
- Fix visual editor mode bz#2189205

* Fri Apr 21 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.03.0+386-3
- R-maint-sig mass rebuild

* Sat Apr 08 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.03.0+386-2
- Fix yarn path

* Fri Mar 17 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2023.03.0+386-1
- Update to 2023.03.0+386

* Thu Feb 23 2023 Kalev Lember <klember@redhat.com> - 2022.12.0+353-4
- Rebuilt for Boost 1.81

* Thu Feb 23 2023 Iñaki Úcar <iucar@fedoraproject.org> - 2022.12.0+353-3
- Update license to meet SPDX specification
- Add patch to fix missing headers
- Add dependency on new catch2 compatibility package

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2022.12.0+353-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 18 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.12.0+353-1
- Update to 2022.12.0+353

* Tue Nov 08 2022 Richard Shaw <hobbes1069@gmail.com> - 2022.07.2+576-3
- Rebuild for yaml-cpp 0.7.0.

* Tue Oct 18 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.07.2+576-2
- Add clang-devel to Recommends

* Thu Sep 22 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.07.2+576-1
- Update to 2022.07.2+576

* Tue Jul 26 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.07.1+554-1
- Update to 2022.07.1+554

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2022.07.0+548-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.07.0+548-2
- Unbundle fmt

* Fri Jul 08 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.07.0+548-1
- Update to 2022.07.0+548
- Define rstudio_flags as global macro
- No need to separate gwt_build anymore https://github.com/rstudio/rstudio/pull/9885

* Wed Jul 06 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.3+492-2
- Add java_arches as ExclusiveArch (#2104098)

* Fri Jun 03 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.3+492-1
- Update to 2022.02.3+492

* Tue May 24 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.2+485-3
- Remove custom stack-protector definition

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 2022.02.2+485-2
- Rebuilt for Boost 1.78

* Thu Apr 28 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.2+485-1
- Update to 2022.02.2+485

* Wed Mar 23 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.1+461-1
- Update to 2022.02.1+461

* Tue Mar 22 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.0+443-2
- Disable Quarto

* Fri Mar 18 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2022.02.0+443-1
- Update to 2022.02.0+443

* Wed Feb 09 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2021.09.2+382-5
- Increase Java stack size for i686

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 2021.09.2+382-4
- Rebuilt for java-17-openjdk as system jdk

* Tue Jan 25 2022 Parag Nemade <pnemade AT redhat DOT com> - 2021.09.2+382-3
- Update hunspell directory path
  F36 Change https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2021.09.2+382-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Iñaki Úcar <iucar@fedoraproject.org> - 2021.09.2+382-1
- Update to 2021.09.2+382

* Thu Dec 02 2021 Iñaki Úcar <iucar@fedoraproject.org> - 2021.09.1+372-2
- Depend specifically on java-11-openjdk-devel
- Export JAVA_HOME to point to java-11

* Thu Nov 11 2021 Iñaki Úcar <iucar@fedoraproject.org> - 2021.09.1+372-1
- Update to 2021.09.1+372

* Wed Oct 13 2021 Björn Esser <besser82@fedoraproject.org> - 2021.09.0+351-2
- Do not build non-lto objects to avoid memory exhaustion by the linker

* Tue Oct 12 2021 Iñaki Úcar <iucar@fedoraproject.org> - 2021.09.0+351-1
- Update to 2021.09.0+351 (new versioning scheme)
- Build with JDK-11

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.4.1717-5
- Rebuilt with OpenSSL 3.0.0

* Wed Aug 11 2021 Iñaki Úcar <iucar@fedoraproject.org> - 1.4.1717-4
- Remove dependency on pandoc-citeproc

* Sat Aug 07 2021 Jonathan Wakely <jwakely@redhat.com> - 1.4.1717-3
- Rebuilt for Boost 1.76

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1717-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 05 2021 Iñaki Úcar <iucar@fedoraproject.org> - 1.4.1717-1
- Update to 1.4.1717

* Wed Mar 31 2021 Jonathan Wakely <jwakely@redhat.com> - 1.4.1106-3
- Rebuilt for removed libstdc++ symbols (#1937698)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.1106-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Sat Feb 27 2021 Iñaki Úcar <iucar@fedoraproject.org> - 1.4.1106-1
- Update to 1.4.1106

* Wed Feb 17 2021 Iñaki Úcar <iucar@fedoraproject.org> - 1.4.1103-4
- Add metainfo.xml file (#1928992)
- Fix /var/lib/rstudio-server ownership

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1103-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 1.4.1103-2
- Rebuilt for Boost 1.75

* Sat Jan 16 2021 Iñaki Úcar <iucar@fedoraproject.org> - 1.4.1103-1
- Update to 1.4.1103

* Mon Nov 30 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.1093-3
- https://fedoraproject.org/wiki/Changes/Remove_make_from_BuildRoot

* Wed Nov 11 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.1093-2
- Fix resources path for release build without RSTUDIO_PACKAGE_BUILD set

* Sat Sep 19 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.1093-1
- Update to 1.3.1093

* Wed Aug 12 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.1073-1
- Update to 1.3.1073

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1056-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1056-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 17 2020 Jiri Vanek <jvanek@redhat.com> - 1.3.1056-2
- Rebuilt for JDK-11, attempt 2. see
  https://fedoraproject.org/wiki/Changes/Java11

* Wed Jul 15 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.1056-1
- Update to 1.3.1056

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 1.3.959-4
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jul 03 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.959-3
- Set PACKAGE_OS env variable
- Move to out-of-source build

* Tue Jun 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.959-2
- Add R-rmarkdown to Recommends
- Fix some bundled versions and licenses

* Sat May 30 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.3.959-1
- Update to 1.3.959
- Bump gwt version; gwt and gin are now included in the main source
- Bump MathJax version (now matches the one shipped in Fedora)
- Provide bundled rapidjson (devel version, not in Fedora); drop json-spirit
- Provide bundled guidelines-support-library-lite
- Provide bundled Ace (it was present before, but missing in Provides)
- Drop patches already merged upstream; rebase other patches
- Add new binary crash-handler-proxy to rstudio-server

* Sat May 30 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5042-5
- Fix compatibility with boost 1.73

* Tue May 12 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5042-4
- More granularity in file ownership under bin, sanitize requires

* Wed May 06 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5042-3
- Depend specifically on java-1.8.0-openjdk-devel
- Export JAVA_HOME to point to java-1.8.0

* Wed Apr 29 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5042-1
- Update to 1.2.5042, which adds support for R 4.0

* Mon Apr 27 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-14
- Use bundled jQuery before js-query is retired

* Mon Apr 06 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-13
- Remove unneeded qt5-devel metapackage dependency

* Thu Mar 19 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-12
- Add QT_QPA_PLATFORM=xcb to the desktop file to workaround Wayland issues

* Mon Mar 09 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-11
- Cleanup some old dependencies

* Fri Feb 28 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-10
- Do not remove NOTICE from resources dir (displayed in the help menu)

* Thu Feb 27 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-9
- Unbundle NewsCycle font
- Make unzip quiet
- Simplify description

* Tue Feb 25 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-8
- Explicitly list gcc-c++ and java-devel as BuildRequires
- Change Source0 URL to include the package name
- Add isa flag to subpackages
- Require hicolor-icon-theme and shared-mimo-info in -desktop
- Mark config file as noreplace in -server
- Add comments to justify patches
- Unbundle Lato font
- Some refactoring

* Sun Feb 23 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-7
- Downgrade to gwt version 2.8.1 to fix notebook issues
- Rebase patches

* Fri Feb 21 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-6
- Declare bundled hunspell, synctex (RStudio relies on an old APIs)

* Thu Feb 20 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-5
- Declare bundled gwt-websockets, guice, aopalliance, json-spirit, sundown,
  datatables, pdfjs, revealjs, jsbn, highlightjs, qunitjs
- Move and symlink bundled libraries included as-is: datatables, pdfjs, revealjs
- Unbundle qtsingleapplication, websocketpp, hunspell, dictionaries, rapidxml,
  synctex, jQuery
- Validate .desktop file
- Expose rstudio-server script in /usr/bin
- Mark NOTICE as license, clean up more files
- Rebase patches

* Mon Feb 17 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-4
- Increase Java stack size for s390x
- Call target gwt_build manually

* Sun Feb 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-3
- Move PNG file to rstudio-desktop sub-package

* Sun Feb 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-2
- Exclude rstudio-desktop from arches not supported by QtWebEngine
- Add 0004-fix-STL-access-undefined-behaviour.patch

* Sun Feb 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.2.5033-1
- Initial packaging for Fedora
- Most of the work ported from Dan Čermák's SPEC for openSUSE
