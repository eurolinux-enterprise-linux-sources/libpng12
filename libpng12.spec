Summary: Old version of libpng, needed to run old binaries
Name: libpng12
Version: 1.2.50
Release: 10%{?dist}
License: zlib
Group: System Environment/Libraries
URL: http://www.libpng.org/pub/png/

# Obsolete old temporary packaging of libpng 1.2
Obsoletes: libpng-compat <= 2:1.5.10

# Note: non-current tarballs get moved to the history/ subdirectory,
# so look there if you fail to retrieve the version you want
Source: ftp://ftp.simplesystems.org/pub/png/src/libpng-%{version}.tar.bz2

Patch0: libpng12-multilib.patch
Patch1: libpng12-pngconf.patch
Patch2: libpng12-CVE-2013-6954.patch
Patch3: libpng12-CVE-2015-7981.patch
Patch4: libpng12-CVE-2015-8126.patch

BuildRequires: zlib-devel, pkgconfig

%description
The libpng12 package provides libpng 1.2, an older version of the libpng
library for manipulating PNG (Portable Network Graphics) image format files.
This version should be used only if you are unable to use the current
version of libpng.

%package devel
Summary: Development files for libpng 1.2
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa} pkgconfig%{?_isa}

%description devel
The libpng12-devel package contains header files and documentation necessary
for developing programs using libpng12.

%prep
%setup -q -n libpng-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure \
  --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

## unpackaged files
# We don't ship .la files.
rm -fv $RPM_BUILD_ROOT%{_libdir}/libpng*.la
# rename man page to avoid conflict with base libpng package
mv $RPM_BUILD_ROOT%{_mandir}/man5/png.5 $RPM_BUILD_ROOT%{_mandir}/man5/png12.5
# omit that conflicts with base libpng-devel package
rm -fv $RPM_BUILD_ROOT%{_bindir}/libpng-config
rm -fv $RPM_BUILD_ROOT%{_includedir}/{png,pngconf}.h
rm -fv $RPM_BUILD_ROOT%{_libdir}/libpng.so
rm -fv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libpng.pc
# rename man pages to avoid conflict with base libpng-devel package
mv $RPM_BUILD_ROOT%{_mandir}/man3/libpng.3 $RPM_BUILD_ROOT%{_mandir}/man3/libpng12.3
mv $RPM_BUILD_ROOT%{_mandir}/man3/libpngpf.3 $RPM_BUILD_ROOT%{_mandir}/man3/libpngpf12.3

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc LICENSE
%doc libpng-%{version}.txt README TODO CHANGES
%{_libdir}/libpng*.so.*
%{_mandir}/man5/*

%files devel
%doc example.c
%{_bindir}/libpng12-config
%{_includedir}/libpng12/
%{_libdir}/libpng12.so
%{_libdir}/pkgconfig/libpng12.pc
%{_mandir}/man3/*

%changelog
* Thu Jun 30 2016 Nikola Forró <nforro@redhat.com> - 1.2.50-10
- Revert removal of libpng compat library
- Related: #1282628

* Wed Jun 29 2016 Nikola Forró <nforro@redhat.com> - 1.2.50-9
- Don't drop man pages, but rename them to avoid conflict
- Resolves: #1285680

* Thu Feb 11 2016 Petr Hracek <phracek@redhat.com> - 1.2.50-8
- libpng12-devel conflicts with libpng-devel
- Resolves: #1282628

* Mon Nov 23 2015 Petr Hracek <phracek@redhat.com> - 1.2.50-7
- Security fix for CVE-2015-7981 and CVE-2015-8126
- Resolves: #1283577

* Wed Jan 29 2014 Petr Hracek <phracek@redhat.com> - 1.2.50-6
- Adding patch CVE-2013-6954
- Resolves: #1056864

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.50-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.50-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Tom Lane <tgl@redhat.com> 1.2.50-2
- Remove unnecessary use of epoch
Related: #850628

* Fri Aug  3 2012 Tom Lane <tgl@redhat.com> 1.2.50-1
- Update to 1.2.50 (just on general principles)
- Add Obsoletes: libpng-compat

* Wed Aug  1 2012 Tom Lane <tgl@redhat.com> 1.2.49-1
- Created from libpng
