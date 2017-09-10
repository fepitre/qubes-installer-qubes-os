%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/pungi
%endif

Name:           pungi
Version:        4.1.18
Release:        2%{?dist}
Epoch:          1000
Summary:        Distribution compose tool

Group:          Development/Tools
License:        GPLv2
URL:            https://pagure.io/pungi
Source0:        https://pagure.io/releases/%{name}/%{name}-%{version}.tar.bz2
Patch1:         0001-Set-repository-gpgkey-option.patch
Patch2:         0002-Verify-downloaded-packages.patch
Patch3:         disable-efi.patch
Patch4:         Hacky-way-to-pass-gpgkey-to-lorax.patch
#Patch5:         fix-recursive-partition-table-on-iso-image.patch
#Patch6:         disable-upgrade.patch
BuildRequires:  python-nose, python-mock
BuildRequires:  python-devel, python-setuptools, python2-productmd >= 1.3
BuildRequires:  python-lockfile, kobo, kobo-rpmlib, python-kickstart, createrepo_c
BuildRequires:  python-lxml, libselinux-python, yum-utils, lorax, python-rpm
BuildRequires:  yum => 3.4.3-28, createrepo >= 0.4.11
BuildRequires:  gettext, git-core, cvs
BuildRequires:  python-jsonschema
BuildRequires:  python-enum34
BuildRequires:  python2-dnf
BuildRequires:  python2-multilib

#deps for doc building
BuildRequires:  latexmk
BuildRequires:  python-sphinx, texlive-latex-bin-bin, texlive-collection-fontsrecommended
BuildRequires:  texlive-times, texlive-cmap, texlive-babel-english, texlive-fancyhdr
BuildRequires:  texlive-fancybox, texlive-titlesec, texlive-framed, texlive-threeparttable
BuildRequires:  texlive-mdwtools, texlive-wrapfig, texlive-parskip, texlive-upquote
BuildRequires:  texlive-multirow, texlive-capt-of, texlive-eqparbox, tex(color.cfg)
BuildRequires:	texlive-needspace
BuildRequires:  tex(fncychap.sty)
BuildRequires:  tex(tabulary.sty)

Requires:       createrepo >= 0.4.11
Requires:       yum => 3.4.3-28
Requires:       lorax >= 22.1
Requires:       repoview
Requires:       python-lockfile
Requires:       kobo
Requires:       kobo-rpmlib
Requires:       python-productmd >= 1.3
Requires:       python-kickstart
Requires:       libselinux-python
Requires:       createrepo_c
Requires:       python-lxml
Requires:       koji >= 1.10.1-13
# This is optional do not Require it
#eRquires:       jigdo
Requires:       cvs
Requires:       yum-utils
Requires:       isomd5sum
Requires:       genisoimage
Requires:       gettext
# this is x86 only 
#Requires:       syslinux
Requires:       git
Requires:       python-jsonschema
Requires:       python-enum34
Requires:       python2-dnf
Requires:       python2-multilib

BuildArch:      noarch

%description
A tool to create anaconda based installation trees/isos of a set of rpms.

%package utils
Summary:    Utilities for working with finished composes
Requires:   pungi = %{version}-%{release}

%description utils
These utilities work with finished composes produced by Pungi. They can be used
for creating unified ISO images, validating config file or sending progress
notification to Fedora Message Bus.


%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%%patch5 -p1
#%%patch6 -p1

%build
%{__python} setup.py build
cd doc
make latexpdf
make epub
make text
make man
gzip _build/man/pungi.1

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -d %{buildroot}/var/cache/pungi
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -m 0644 doc/_build/man/pungi.1.gz %{buildroot}%{_mandir}/man1

%check
nosetests --exe
./tests/data/specs/build.sh
cd tests && ./test_compose.sh

%files
%license COPYING GPL
%doc AUTHORS doc/_build/latex/Pungi.pdf doc/_build/epub/Pungi.epub doc/_build/text/*
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info
%{_bindir}/%{name}
%{_bindir}/%{name}-koji
%{_bindir}/%{name}-gather
%{_bindir}/comps_filter
%{_bindir}/%{name}-make-ostree
%{_mandir}/man1/pungi.1.gz
%{_datadir}/pungi
/var/cache/pungi

%files utils
%{python_sitelib}/%{name}_utils
%{_bindir}/%{name}-create-unified-isos
%{_bindir}/%{name}-config-validate
%{_bindir}/%{name}-fedmsg-notification
%{_bindir}/%{name}-patch-iso
%{_bindir}/%{name}-compare-depsolving
%{_bindir}/%{name}-wait-for-signed-ostree-handler

%changelog
