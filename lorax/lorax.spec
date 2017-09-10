# NOTE: This specfile is generated from upstream at https://github.com/rhinstaller/lorax
# NOTE: Please submit changes as a pull request
%define debug_package %{nil}

%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/lorax
%endif

Name:           lorax
Version:        26.9
Release:        1%{?dist}
Epoch:          1000
Summary:        Tool for creating the anaconda install images

Group:          Applications/System
License:        GPLv2+
URL:            https://github.com/rhinstaller/lorax
# To generate Source0 do:
# git clone https://github.com/rhinstaller/lorax
# git checkout -b archive-branch lorax-%%{version}-%%{release}
# tito build --tgz
Source0:        %{name}-%{version}.tar.gz
Patch1:         0001-Allow-specify-gpg-key-for-a-repository.patch
Patch2:         0002-verify-packages-signature.patch
Patch3:         0003-Update-package-verification-for-dnf-API.patch
Patch4:         0004-Remove-branding-code.patch

BuildRequires:  python3-devel

Requires:       lorax-templates

Requires:       GConf2
Requires:       cpio
Requires:       device-mapper
Requires:       dosfstools
Requires:       e2fsprogs
Requires:       findutils
Requires:       gawk
Requires:       genisoimage
Requires:       glib2
Requires:       glibc
Requires:       glibc-common
Requires:       gzip
Requires:       isomd5sum
Requires:       module-init-tools
Requires:       parted
Requires:       squashfs-tools >= 4.2
Requires:       util-linux
Requires:       xz
Requires:       pigz
Requires:       dracut >= 030
Requires:       kpartx

# Python modules
Requires:       libselinux-python3
Requires:       python3-mako
Requires:       python3-kickstart
Requires:       python3-dnf >= 1.1.7


%if 0%{?fedora}
# Fedora specific deps
%ifarch x86_64
Requires:       hfsplus-tools
%endif
%endif

%ifarch %{ix86} x86_64
Requires:       syslinux >= 6.02-4
%endif

%ifarch ppc ppc64 ppc64le
Requires:       kernel-bootwrapper
Requires:       grub2
Requires:       grub2-tools
%endif

%ifarch s390 s390x
Requires:       openssh
%endif

%ifarch %{arm}
Requires:       uboot-tools
%endif

# Moved image-minimizer tool to lorax
Provides:       appliance-tools-minimizer
Obsoletes:      appliance-tools-minimizer < 007.7-3

%description
Lorax is a tool for creating the anaconda install images.

It also includes livemedia-creator which is used to create bootable livemedia,
including live isos and disk images. It can use libvirtd for the install, or
Anaconda's image install feature.

%package lmc-virt
Summary:  livemedia-creator libvirt dependencies
Requires: lorax = %{epoch}:%{version}-%{release}
Requires: qemu
Requires: edk2-ovmf
Recommends: qemu-kvm

%description lmc-virt
Additional dependencies required by livemedia-creator when using it with qemu.

%package lmc-novirt
Summary:  livemedia-creator no-virt dependencies
Requires: lorax = %{epoch}:%{version}-%{release}
Requires: anaconda-core
Requires: anaconda-tui

%description lmc-novirt
Additional dependencies required by livemedia-creator when using it with --no-virt
to run Anaconda.

%package templates-generic
Summary:  Generic build templates for lorax and livemedia-creator
Requires: lorax = %{epoch}:%{version}-%{release}
Provides: lorax-templates

%description templates-generic
Lorax templates for creating the boot.iso and live isos are placed in
/usr/share/lorax/templates.d/99-generic

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} install

%files
%defattr(-,root,root,-)
%license COPYING
%doc AUTHORS docs/livemedia-creator.rst docs/product-images.rst
%doc docs/*ks
%{python3_sitelib}/pylorax
%{python3_sitelib}/*.egg-info
%{_sbindir}/lorax
%{_sbindir}/mkefiboot
%{_sbindir}/livemedia-creator
%{_bindir}/image-minimizer
%dir %{_sysconfdir}/lorax
%config(noreplace) %{_sysconfdir}/lorax/lorax.conf
%dir %{_datadir}/lorax
%{_mandir}/man1/*.1*

%files lmc-virt

%files lmc-novirt

%files templates-generic
%{_datadir}/lorax/templates.d/*


%changelog
