Name:           duckdb
Version:        1.4.1
Release:        1%{?dist}
Summary:        An analytical in-process SQL database management system

License:        MIT
URL:            https://github.com/%{name}/%{name}
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  openssl-devel

%description
DuckDB is a high-performance analytical database system. It is designed to be
fast, reliable, portable, and easy to use. DuckDB provides a rich SQL dialect,
with support far beyond basic SQL. DuckDB supports arbitrary and nested
correlated subqueries, window functions, collations, complex types (arrays,
structs, maps), and several extensions designed to make SQL easier to use.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1
sed -i '26i #include <cstdint>' third_party/thrift/thrift/transport/TTransport.h

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DOVERRIDE_GIT_DESCRIBE=v%{version} \
    -DDUCKDB_EXTENSION_CONFIGS=".github/config/bundled_extensions.cmake" \
    -DSET_DUCKDB_LIBRARY_VERSION=true \
    -DINSTALL_BIN_DIR=%{_bindir} \
    -DINSTALL_LIB_DIR=%{_libdir} \
    -DINSTALL_INCLUDE_DIR=%{_includedir} \
    -DINSTALL_CMAKE_DIR=%{_libdir}/cmake/%{name}
%cmake_build

%install
%cmake_install

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}_*.a
%{_libdir}/lib*_extension.a
%{_includedir}/%{name}
%{_includedir}/%{name}.h*
%{_libdir}/cmake/%{name}

%changelog
