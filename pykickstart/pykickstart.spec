%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/pykickstart
%endif

Name:      pykickstart
Version:   2.38
Release:   3%{?dist}
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
Source0:   %{name}-%{version}.tar.gz
Patch1: 0001-Add-gpgkey-option-to-repo-command.patch
Patch2: 0002-Ignore-errors-from-check-coverage-tests.patch
Patch3: standard-xgettext.patch
BuildArch: noarch


BuildRequires: gettext
BuildRequires: python-coverage
BuildRequires: python-devel
BuildRequires: python-nose
BuildRequires: python-ordered-set
BuildRequires: python-setuptools
BuildRequires: python-requests

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
%package -n python-kickstart
Summary:  Python 2 library for manipulating kickstart files.
Requires: python-six
Requires: python-requests
Requires: python-ordered-set

%description -n python-kickstart
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

%patch1 -p1
%patch2 -p1
%patch3 -p1

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
#make PYTHON=%{__python3} test
popd

%files
%defattr(-,root,root,-)
%license COPYING
%doc README
%doc data/kickstart.vim
%{_bindir}/ksvalidator
%{_bindir}/ksflatten
%{_bindir}/ksverdiff
%{_bindir}/ksshell
%{_mandir}/man1/*

%files -n python-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.rst
%{python2_sitelib}/pykickstart*egg*
%{python2_sitelib}/pykickstart/*py*
%{python2_sitelib}/pykickstart/commands/*py*
%{python2_sitelib}/pykickstart/handlers/*py*
%{python2_sitelib}/pykickstart/locale/

%files -n python3-kickstart
%defattr(-,root,root,-)
%doc docs/2to3
%doc docs/programmers-guide
%doc docs/kickstart-docs.rst
%{python3_sitelib}/pykickstart*egg*
%{python3_sitelib}/pykickstart/*py*
%{python3_sitelib}/pykickstart/commands/*py*
%{python3_sitelib}/pykickstart/handlers/*py*
%{python3_sitelib}/pykickstart/locale/

%changelog
