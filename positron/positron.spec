%global debug_package %{nil}
%global positron_arch %[ "%{_arch}" == "x86_64" ? "x64" : "arm64" ]
%global positron_node 20

Name:           positron
Version:        2024.07.0+17
Release:        1%{?dist}
Summary:        A next-generation data science IDE

%global positron_version %gsub %{version} + -
%global positron_flags \
    export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 ; \
    export ELECTRON_SKIP_BINARY_DOWNLOAD=1 ; \
    export POSITRON_BUILD_NUMBER=%gsub %{version} .*%+(.*) %1

License:        Elastic-2.0
URL:            https://github.com/posit-dev/%{name}
Source0:        %{url}/archive/%{positron_version}/%{name}-%{positron_version}.tar.gz

#BuildRequires:  yarnpkg, nodejs-npm
BuildRequires:  nodejs%{positron_node}-npm
BuildRequires:  make, cmake, gcc-c++
BuildRequires:  python3-pip, python3dist(setuptools), git-core
BuildRequires:  krb5-devel
BuildRequires:  libsecret-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  zeromq-devel
BuildRequires:  ark-kernel
BuildRequires:  pandoc
BuildRequires:  hicolor-icon-theme
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
#Requires:       nodejs%%{positron_node}
Requires:       ark-kernel, python3-ipykernel
Requires:       pandoc
Requires:       hicolor-icon-theme, shared-mime-info

%description
A next-generation data science IDE built by Posit PBC.
An extensible, polyglot tool for writing code and exploring data.
A familiar environment for reproducible authoring and publishing.

%prep
%autosetup -p1 -n %{name}-%{positron_version}
mkdir -p ../ark/target/release
ln -sf %{_libexecdir}/ark-kernel/bin/ark ../ark/target/release
git init # they use git apply in extensions/positron-python/scripts/vendor.py

%build
%{positron_flags}
mkdir -p ~/.local/bin && export PATH=~/.local/bin:$PATH
ln -sf %{_bindir}/node-%{positron_node} ~/.local/bin/node
ln -sf %{_bindir}/npm-%{positron_node} ~/.local/bin/npm
npm config set prefix "~/.local"
npm install --global yarn
yarn global add node-gyp
yarn --immutable --network-timeout 120000
yarn gulp vscode-linux-%{positron_arch}
yarn gulp vscode-linux-%{positron_arch}-prepare-rpm

%install
pushd .build/linux/rpm/$(uname -m)/rpmbuild/BUILD/%{_datadir}
    # install app
    install -d -m 0755 %{buildroot}%{_libexecdir}
    mv %{name} %{buildroot}%{_libexecdir}
    # install desktop and appdata files
    install -d -m 0755 %{buildroot}%{_datadir}
    mv applications mime pixmaps %{buildroot}%{_datadir}
    install -d -m 0755 %{buildroot}%{_metainfodir}
    install -m 0644 appdata/%{name}.appdata.xml %{buildroot}%{_metainfodir}
    # install completions
    install -d -m 0755 %{buildroot}%{bash_completions_dir}
    ln -sf %{_libexecdir}/%{name}/resources/completions/bash/%{name} \
        %{buildroot}%{bash_completions_dir}
    install -d -m 0755 %{buildroot}%{zsh_completions_dir}
    ln -sf %{_libexecdir}/%{name}/resources/completions/zsh/_%{name} \
        %{buildroot}%{zsh_completions_dir}
popd

# install symlink to binary
install -d -m 0755 %{buildroot}%{_bindir}
ln -sf %{_libexecdir}/%{name}/bin/%{name} %{buildroot}%{_bindir}
# use system tools
ln -sf %{_bindir}/pandoc %{buildroot}%{_libexecdir}/%{name}/bin/pandoc
ln -sf %{_libexecdir}/ark-kernel/bin/ark \
    %{buildroot}%{_libexecdir}/%{name}/resources/app/extensions/%{name}-r/resources/ark

# cleanup prebuilds
for PREB in $(find %{buildroot}%{_libexecdir}/%{name} -name prebuilds); do
pushd $PREB
    rm -rf $(ls | grep -xv linux-%{positron_arch})
    find . -name "*musl*" -delete
popd
done

# validate desktop and appdata files
sed -i 's@%{_datadir}@%{_libexecdir}@g' %{buildroot}/%{_datadir}/applications/%{name}*.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-url-handler.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%files
%{_bindir}/%{name}
%dir %{_libexecdir}/%{name}
%license %{_libexecdir}/%{name}/LICENSES.chromium.html
%{_libexecdir}/%{name}/bin
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
%{_libexecdir}/%{name}/%{name}
%{_libexecdir}/%{name}/resources.pak
%{_libexecdir}/%{name}/resources
%{_libexecdir}/%{name}/snapshot_blob.bin
%{_libexecdir}/%{name}/v8_context_snapshot.bin
%{_libexecdir}/%{name}/vk_swiftshader_icd.json
%dir %{bash_completions_dir}
%{bash_completions_dir}/%{name}
%dir %{zsh_completions_dir}
%{zsh_completions_dir}/_%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-url-handler.desktop
%{_datadir}/mime/packages/%{name}-workspace.xml
%{_datadir}/pixmaps/com.visualstudio.code.oss.png
%{_metainfodir}/%{name}.appdata.xml

%changelog
