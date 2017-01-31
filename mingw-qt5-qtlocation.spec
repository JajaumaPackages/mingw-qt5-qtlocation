%?mingw_package_header

%global qt_module qtlocation
#%%global pre rc1

#%%global snapshot_date 20130510
#%%global snapshot_rev f2840834

%if 0%{?snapshot_date}
%global source_folder qt-%{qt_module}
%else
%global source_folder %{qt_module}-opensource-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-%{qt_module}
Version:        5.6.0
Release:        1%{?pre:.%{pre}}%{?snapshot_date:.git%{snapshot_date}.%{snapshot_rev}}%{?dist}
Summary:        Qt5 for Windows - QtLocation component

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries
URL:            http://www.qtsoftware.com/

%if 0%{?snapshot_date}
# To regenerate:
# wget http://qt.gitorious.org/qt/%{qt_module}/archive-tarball/%{snapshot_rev} -O qt5-%{qt_module}-%{snapshot_rev}.tar.gz
Source0:        qt5-%{qt_module}-%{snapshot_rev}.tar.gz
%else
%if "%{?pre}" != ""
Source0:        http://download.qt-project.org/development_releases/qt/%{release_version}/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0:        http://download.qt-project.org/official_releases/qt/%{release_version}/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

BuildArch:      noarch

# NOTE: The mingw{32,64}-qt5-qtquick1 requirements are unversioned due to
# a circular dependency where qtquick1 depends on qtwebkit, but qtwebkit
# depends on qtlocation which itself depends on qtquick1
BuildRequires:  mingw32-filesystem >= 96
BuildRequires:  mingw32-qt5-qtbase >= 5.6.0
BuildRequires:  mingw32-qt5-qtquick1

BuildRequires:  mingw64-filesystem >= 96
BuildRequires:  mingw64-qt5-qtbase >= 5.6.0
BuildRequires:  mingw64-qt5-qtquick1


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtLocation component

%description -n mingw32-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win64
%package -n mingw64-qt5-%{qt_module}
Summary:        Qt5 for Windows - QtLocation component

%description -n mingw64-qt5-%{qt_module}
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%?mingw_debug_package


%prep
%setup -q -n %{source_folder}

%if 0%{?snapshot_date}
# Make sure the syncqt tool is run because we're using a git snapshot
# Otherwise the build fails against Qt 5.1
mkdir .git
%endif


%build
%mingw_qmake_qt5 ../%{qt_module}.pro
%mingw_make %{?_smp_mflags}


%install
%mingw_make install INSTALL_ROOT=$RPM_BUILD_ROOT

# .prl files aren't interesting for us
find $RPM_BUILD_ROOT -name "*.prl" -delete

# Create a list of .dll.debug files which need to be excluded from the main packages
# We do this to keep the %%files section as clean/readable as possible (otherwise every
# single file and directory would have to be mentioned individually in the %%files section)
# Note: the .dll.debug files aren't created yet at this point (as it happens after
# the %%install section). Therefore we have to assume that all .dll files will
# eventually get a .dll.debug counterpart
find $RPM_BUILD_ROOT%{mingw32_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw32-qt5-%{qt_module}.excludes
find $RPM_BUILD_ROOT%{mingw64_prefix} | grep .dll | grep -v .dll.a | sed s@"^$RPM_BUILD_ROOT"@"%%exclude "@ | sed s/".dll\$"/".dll.debug"/ > mingw64-qt5-%{qt_module}.excludes


# Win32
%files -n mingw32-qt5-%{qt_module} -f mingw32-qt5-%{qt_module}.excludes
%{mingw32_bindir}/Qt5Location.dll
%{mingw32_bindir}/Qt5Positioning.dll
%{mingw32_includedir}/qt5/QtLocation/
%{mingw32_includedir}/qt5/QtPositioning/
%{mingw32_libdir}/libQt5Location.dll.a
%{mingw32_libdir}/libQt5Positioning.dll.a
%{mingw32_libdir}/cmake/Qt5Location/
%{mingw32_libdir}/cmake/Qt5Positioning/
%{mingw32_libdir}/pkgconfig/Qt5Location.pc
%{mingw32_libdir}/pkgconfig/Qt5Positioning.pc
%{mingw32_libdir}/qt5/plugins/geoservices/
%{mingw32_libdir}/qt5/plugins/position/
%{mingw32_datadir}/qt5/qml/QtLocation/
%{mingw32_datadir}/qt5/qml/QtPositioning/
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_location.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_location_private.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_positioning.pri
%{mingw32_datadir}/qt5/mkspecs/modules/qt_lib_positioning_private.pri

# Win64
%files -n mingw64-qt5-%{qt_module} -f mingw64-qt5-%{qt_module}.excludes
%{mingw64_bindir}/Qt5Location.dll
%{mingw64_bindir}/Qt5Positioning.dll
%{mingw64_includedir}/qt5/QtLocation/
%{mingw64_includedir}/qt5/QtPositioning/
%{mingw64_libdir}/libQt5Location.dll.a
%{mingw64_libdir}/libQt5Positioning.dll.a
%{mingw64_libdir}/cmake/Qt5Location/
%{mingw64_libdir}/cmake/Qt5Positioning/
%{mingw64_libdir}/pkgconfig/Qt5Location.pc
%{mingw64_libdir}/pkgconfig/Qt5Positioning.pc
%{mingw64_libdir}/qt5/plugins/geoservices/
%{mingw64_libdir}/qt5/plugins/position/
%{mingw64_datadir}/qt5/qml/QtLocation/
%{mingw64_datadir}/qt5/qml/QtPositioning/
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_location.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_location_private.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_positioning.pri
%{mingw64_datadir}/qt5/mkspecs/modules/qt_lib_positioning_private.pri


%changelog
* Thu Apr  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 30 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1

* Fri Aug  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0
- Removed BR: mingw{32,64}-qt5-qt3d as it is unneeded
- Added BR: mingw{32,64}-qt5-qtquick1 which in fact is needed

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 22 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1

* Tue Dec 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0

* Sat Sep 20 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Tue Jul  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0

* Sun Mar 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-2
- Make sure we're built against mingw-qt5-qtbase >= 5.2.1 (RHBZ 1077213)

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-4
- Previous commit caused .dll.a files to disappear

* Sun Jan 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-3
- Don't carry .dll.debug files in main package

* Wed Jan  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-2
- Dropped manual rename of import libraries

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.rc1
- Update to 5.2.0 RC1

* Fri Aug  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.6.git20130510.f2840834
- Dropped reference to unused patch
- Don't bundle .dll.debug files in the main packages

* Thu Jul 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.5.git20130510.f2840834
- Make sure the syncqt tool is run because we're using a git snapshot

* Fri May 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.4.git20130510.f2840834
- Update to 20130510 snapshot (rev f2840834)

* Fri Jan 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.3.git20121112.ac83b242
- Update to ac83b242 snapshot (fixes compatibility with Qt 5.0.0 Final)

* Mon Nov 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1.git20121112.8e6b5b08
- Update to 20121112 snapshot (rev 8e6b5b08)
- Rebuild against latest mingw-qt5-qtbase
- Dropped pkg-config rename hack as it's unneeded now

* Wed Sep 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial release

