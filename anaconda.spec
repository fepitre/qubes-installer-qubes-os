%define livearches %{ix86} x86_64 ppc ppc64 ppc64le

Summary: Graphical system installer
Name:    anaconda
Version: 26.1
Release: 1%{?dist}
License: GPLv2+ and MIT
Epoch:   1000
Group:   Applications/System
URL:     http://fedoraproject.org/wiki/Anaconda

# To generate Source0 do:
# git clone https://github.com/rhinstaller/anaconda
# git checkout -b archive-branch anaconda-%%{version}-%%{release}
# ./autogen.sh
# make dist
Source0: %{name}-%{version}.tar.bz2

%if 0%{?qubes_builder}
%define _builddir %(pwd)/anaconda
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Versions of required components (done so we make sure the buildrequires
# match the requires versions of things).

%define blivetguiver 2.1.5-2
%define dbusver 1.2.3
%define dnfver 2.2.0
%define dracutver 034-7
%define fcoeutilsver 1.0.12-3.20100323git
%define firewalldver 0.3.5-1
%define gettextver 0.19.8
%define gtk3ver 3.22.17
%define helpver 22.1-1
%define iscsiver 6.2.0.873-26
%define isomd5sum 1.0.10
%define langtablever 0.0.34
%define libarchivever 3.0.4
%define libblockdevver 2.1
%define libtimezonemapver 0.4.1-2
%define libxklavierver 5.4
%define mehver 0.23-1
%define nmver 1.0
%define partedver 1.8.1
%define pykickstartver 2.36-1
%define pypartedver 2.5-2
%define rpmver 4.10.0
%define simplelinever 0.5-1
%define utillinuxver 2.15.1

BuildRequires: audit-libs-devel
BuildRequires: gettext >= %{gettextver}
BuildRequires: gtk3-devel >= %{gtk3ver}
BuildRequires: gtk-doc
BuildRequires: gtk3-devel-docs >= %{gtk3ver}
BuildRequires: glib2-doc
BuildRequires: gobject-introspection-devel
BuildRequires: glade-devel
BuildRequires: libgnomekbd-devel
BuildRequires: libxklavier-devel >= %{libxklavierver}
BuildRequires: pango-devel
BuildRequires: python3-kickstart >= %{pykickstartver}
%if ! 0%{?rhel}
BuildRequires: python3-bugzilla
%endif
BuildRequires: python3-devel
BuildRequires: python3-nose
BuildRequires: systemd
# rpm and libarchive are needed for driver disk handling
BuildRequires: rpm-devel >= %{rpmver}
BuildRequires: libarchive-devel >= %{libarchivever}
%ifarch %livearches
BuildRequires: desktop-file-utils
%endif
%ifarch s390 s390x
BuildRequires: s390utils-devel
%endif
BuildRequires: libtimezonemap-devel >= %{libtimezonemapver}

# Tools used by the widgets resource bundle generation
BuildRequires: gdk-pixbuf2-devel
BuildRequires: libxml2

Requires: anaconda-core = %{epoch}:%{version}-%{release}
Requires: anaconda-gui = %{epoch}:%{version}-%{release}
Requires: anaconda-tui = %{epoch}:%{version}-%{release}

%description
The anaconda package is a metapackage for the Anaconda installer.

%package core
Summary: Core of the Anaconda installer
Requires: python3-libs
Requires: python3-dnf >= %{dnfver}
Requires: python3-blivet >= 1:2.1.9-1
Requires: python3-blockdev >= %{libblockdevver}
Requires: libblockdev-plugins-all >= %{libblockdevver}
Requires: python3-meh >= %{mehver}
Requires: libreport-anaconda >= 2.0.21-1
Requires: libselinux-python3
Requires: rpm-python3 >= %{rpmver}
Requires: parted >= %{partedver}
Requires: python3-pyparted >= %{pypartedver}
Requires: python3-requests
Requires: python3-requests-file
Requires: python3-requests-ftp
Requires: python3-kickstart >= %{pykickstartver}
Requires: langtable-data >= %{langtablever}
Requires: langtable-python3 >= %{langtablever}
Requires: authconfig
Requires: firewalld >= %{firewalldver}
Requires: util-linux >= %{utillinuxver}
Requires: python3-gobject-base
Requires: python3-dbus
Requires: python3-pwquality
Requires: python3-systemd
Requires: python3-pydbus

# pwquality only "recommends" the dictionaries it needs to do anything useful,
# which is apparently great for containers but unhelpful for the rest of us
Requires: cracklib-dicts

Requires: python3-pytz
Requires: realmd
Requires: teamd
%ifarch %livearches
Requires: usermode
%endif
%ifarch s390 s390x
Requires: openssh
%endif
Requires: isomd5sum >= %{isomd5sum}
Requires: createrepo_c
Requires: NetworkManager >= %{nmver}
Requires: NetworkManager-libnm >= %{nmver}
Requires: NetworkManager-team
Requires: dhclient
Requires: kbd
Requires: chrony
Requires: python3-ntplib
Requires: rsync
Requires: systemd
%ifarch %{ix86} x86_64
Requires: fcoe-utils >= %{fcoeutilsver}
%endif
Requires: python3-iscsi-initiator-utils >= %{iscsiver}
%ifarch %{ix86} x86_64
%if ! 0%{?rhel}
Requires: hfsplus-tools
%endif
%endif
Requires: kexec-tools
Requires: python3-pid
Requires: python3-ordered-set >= 2.0.0
Requires: python3-wrapt

Requires: python3-coverage >= 4.0-0.12.b3

# required because of the rescue mode and VNC question
Requires: anaconda-tui = %{epoch}:%{version}-%{release}

# Make sure we get the en locale one way or another
Requires: glibc-langpack-en

Obsoletes: anaconda-images <= 10
Provides: anaconda-images = %{version}-%{release}
Obsoletes: anaconda-runtime < %{version}-%{release}
Provides: anaconda-runtime = %{version}-%{release}
Obsoletes: booty <= 0.107-1

%description core
The anaconda-core package contains the program which was used to install your
system.

%package gui
Summary: Graphical user interface for the Anaconda installer
Requires: anaconda-core = %{version}-%{release}
Requires: anaconda-widgets = %{version}-%{release}
Requires: python3-meh-gui >= %{mehver}
Requires: adwaita-icon-theme
Requires: system-logos
Requires: tigervnc-server-minimal
Requires: libxklavier >= %{libxklavierver}
Requires: libgnomekbd
Requires: libtimezonemap >= %{libtimezonemapver}
Requires: nm-connection-editor
%ifarch %livearches
Requires: zenity
%endif
Requires: keybinder3
%ifnarch s390 s390x
Requires: NetworkManager-wifi
%endif
Requires: anaconda-user-help >= %{helpver}
Requires: yelp
Requires: blivet-gui-runtime >= %{blivetguiver}

# Needed to compile the gsettings files
BuildRequires: gsettings-desktop-schemas
BuildRequires: metacity

%description gui
This package contains graphical user interface for the Anaconda installer.

%package tui
Summary: Textual user interface for the Anaconda installer
Requires: anaconda-core = %{epoch}:%{version}-%{release}
Requires: python3-simpleline >= %{simplelinever}

%description tui
This package contains textual user interface for the Anaconda installer.

%package widgets
Summary: A set of custom GTK+ widgets for use with anaconda
Group: System Environment/Libraries
Requires: python3

%description widgets
This package contains a set of custom GTK+ widgets used by the anaconda installer.

%package widgets-devel
Summary: Development files for anaconda-widgets
Group: Development/Libraries
Requires: glade
Requires: %{name}-widgets%{?_isa} = %{epoch}:%{version}-%{release}

%description widgets-devel
This package contains libraries and header files needed for writing the anaconda
installer.  It also contains Python and Glade support files, as well as
documentation for working with this library.

%package dracut
Summary: The anaconda dracut module
Requires: dracut >= %{dracutver}
Requires: dracut-network
Requires: dracut-live
Requires: xz
Requires: python3-kickstart

%description dracut
The 'anaconda' dracut module handles installer-specific boot tasks and
options. This includes driver disks, kickstarts, and finding the anaconda
runtime on NFS/HTTP/FTP servers or local disks.

%prep
%if ! 0%{?qubes_builder}
%setup -q
%endif


%build
./autogen.sh
%configure
%{__make} %{?_smp_mflags}

%install
%{make_install}
find %{buildroot} -type f -name "*.la" | xargs %{__rm}

# Create an empty directory for addons
mkdir %{buildroot}%{_datadir}/anaconda/addons

%ifarch %livearches
desktop-file-install ---dir=%{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/liveinst.desktop
%endif
# NOTE: If you see "error: Installed (but unpackaged) file(s) found" that include liveinst files,
#       check the IS_LIVEINST_ARCH in configure.ac to make sure your architecture is properly defined

# If no langs found, keep going
%find_lang %{name} || :

%post widgets -p /sbin/ldconfig
%postun widgets -p /sbin/ldconfig


%ifarch %livearches
%post
update-desktop-database &> /dev/null || :
%endif

%ifarch %livearches
%postun
update-desktop-database &> /dev/null || :
%endif

%files

# Allow the lang file to be empty
%define _empty_manifest_terminate_build 0

%files core -f %{name}.lang
%license COPYING
%{_unitdir}/*
%{_prefix}/lib/systemd/system-generators/*
%{_bindir}/instperf
%{_bindir}/anaconda-disable-nm-ibft-plugin
%{_sbindir}/anaconda
%{_sbindir}/handle-sshpw
%{_datadir}/anaconda
%{_prefix}/libexec/anaconda
%exclude %{_prefix}/libexec/anaconda/dd_*
%{python3_sitearch}/pyanaconda/*
%exclude %{python3_sitearch}/pyanaconda/rescue.py*
%exclude %{python3_sitearch}/pyanaconda/__pycache__/rescue.*
%exclude %{python3_sitearch}/pyanaconda/ui/gui/*
%exclude %{python3_sitearch}/pyanaconda/ui/tui/*
%{_bindir}/analog
%{_bindir}/anaconda-cleanup
%ifarch %livearches
%{_bindir}/liveinst
%{_sbindir}/liveinst
%config(noreplace) %{_sysconfdir}/pam.d/*
%config(noreplace) %{_sysconfdir}/security/console.apps/*
%{_libexecdir}/liveinst-setup.sh
%{_datadir}/applications/*.desktop
%{_sysconfdir}/xdg/autostart/*.desktop
%endif

%files gui
%{python3_sitearch}/pyanaconda/ui/gui/*
%{_datadir}/themes/Anaconda/*

%files tui
%{python3_sitearch}/pyanaconda/rescue.py
%{python3_sitearch}/pyanaconda/__pycache__/rescue.*
%{python3_sitearch}/pyanaconda/ui/tui/*

%files widgets
%{_libdir}/libAnacondaWidgets.so.*
%{_libdir}/girepository*/AnacondaWidgets*typelib
%{python3_sitearch}/gi/overrides/*

%files widgets-devel
%{_libdir}/libAnacondaWidgets.so
%{_includedir}/*
%{_datadir}/glade/catalogs/AnacondaWidgets.xml
%{_datadir}/gtk-doc

%files dracut
%dir %{_prefix}/lib/dracut/modules.d/80%{name}
%{_prefix}/lib/dracut/modules.d/80%{name}/*
%{_prefix}/libexec/anaconda/dd_*

%changelog
