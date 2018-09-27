%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:      pykickstart
Version:   3.16
Release:   4%{?dist}
Epoch: 1000
License:   GPLv2 and MIT
Group:     System Environment/Libraries
Summary:   Python utilities for manipulating kickstart files.
Url:       http://fedoraproject.org/wiki/pykickstart
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

# Qubes: To get the source:
# git clone https://github.com/rhinstaller/pykickstart
# check out the version of interest by its tag (rXX-X)
# sudo dnf install zanata-python-client
# make po-pull && make archive
# The tarball will be in the current directory.
Source0: %{name}-%{version}.tar.gz
Patch0: 0001-Add-gpgkey-option-to-repo-command.patch
BuildArch: noarch


BuildRequires: gettext
BuildRequires: python2-coverage
BuildRequires: python2-devel
BuildRequires: python2-nose
BuildRequires: python2-ordered-set
BuildRequires: python2-setuptools
BuildRequires: python2-requests

BuildRequires: python3-coverage
BuildRequires: python3-devel
BuildRequires: python3-mypy
BuildRequires: python3-nose
BuildRequires: python3-ordered-set
BuildRequires: python3-requests
BuildRequires: python3-setuptools
BuildRequires: python3-six

Requires: python3-kickstart = %{epoch}:%{version}-%{release}

%description
Python utilities for manipulating kickstart files.  The Python 2 and 3 libraries
can be found in the packages python-kickstart and python3-kickstart
respectively.

# Python 2 library
%package -n python2-kickstart
Summary:  Python 2 library for manipulating kickstart files.
Requires: python-six
Requires: python-requests
Requires: python-ordered-set

%description -n python2-kickstart
Python 2 library for manipulating kickstart files.  The binaries are found in
the pykickstart package.

# Python 3 library
%package -n python3-kickstart
Summary:  Python 3 library for manipulating kickstart files.
Requires: python3-six
Requires: python3-requests
Requires: python3-ordered-set

%description -n python3-kickstart
Python 3 library for manipulating kickstart files.  The binaries are found in
the pykickstart package.

%prep
%setup -q

%patch0 -p1

rm -rf %{py3dir}
mkdir %{py3dir}
cp -a . %{py3dir}

%build
make PYTHON=%{__python2}

pushd %{py3dir}
make PYTHON=%{__python3}
popd

%install
rm -rf %{buildroot}
make PYTHON=%{__python2} DESTDIR=%{buildroot} install

pushd %{py3dir}
make PYTHON=%{__python3} DESTDIR=%{buildroot} install
popd

%check
#make PYTHON=%{__python2} test

pushd %{py3dir}
make PYTHON=%{__python3} test
popd

%files
%license COPYING
%doc README.rst
%doc data/kickstart.vim
%{_bindir}/ksvalidator
%{_bindir}/ksflatten
%{_bindir}/ksverdiff
%{_bindir}/ksshell
%{_mandir}/man1/ksflatten.1.gz
%{_mandir}/man1/ksshell.1.gz
%{_mandir}/man1/ksvalidator.1.gz
%{_mandir}/man1/ksverdiff.1.gz

%files -n python2-kickstart
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python2_sitelib}/pykickstart*.egg-info
%{python2_sitelib}/pykickstart

%files -n python3-kickstart
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.txt
%{python3_sitelib}/pykickstart
%{python3_sitelib}/pykickstart*.egg-info

%changelog
