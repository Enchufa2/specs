Summary: OpenBUGS.
Name: openbugs 
Version: 3.2.2
Release: 1
License: GPL
Group: Applications/Science
Source0: http://www.openbugs.info/w/Downloads/OpenBUGS-%{version}.tar.gz
Patch0: pj-Makefile-4.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildArchitectures: i386 i686 x86_64

%description

OpenBUGS is a program that conducts Bayesian estimation
vi Gibbs Sampling. It is a continuation of the WinBUGS
project, which was a continuation of the BUGS project.
BUGS=Bayesian Updating with Gibbs Sampling 


%prep

%setup -n OpenBUGS-%{version} 
%patch0 -p1

%configure --prefix=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_prefix}

make DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf $RPM_BUILD_ROOT

# basic contains some reasonable 
%files 
%defattr(-, root, root)
%dir %{_bindir}
%dir %{_libdir}
%dir %{_mandir}
%{_bindir}/*
%{_libdir}/*
%{_mandir}/*
%doc doc/*


%changelog
* Fri Jul 27 2012 Paul Johnson <pauljohn32@freefaculty.org> 3.2.2-1
- new version

* Sun Mar 27 2011 Paul Johnson <pauljohn32@freefaculty.org> 3.2.1-1
- update

* Mon Nov 8 2010 Paul Johnson <pauljohn32@freefaculty.org> 3.1.2-1
- new


