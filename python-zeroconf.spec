#
# Conditional build:
%bcond_with	integration	# Integration tests work in mock but fail in Koji with PermissionError
%bcond_with	tests		# unit tests
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module

%define module	zeroconf
Summary:	Pure Python Multicast DNS Service Discovery Library
Summary(pl.UTF-8):	Czysto pythonowa biblioteka Multicast DNS Service Discovery
Name:		python-%{module}
# keep 0.19.x here for python2 support
Version:	0.19.1
Release:	1
License:	LGPL v2
Group:		Libraries/Python
#Source0Download: https://github.com/jstasiak/python-zeroconf/releases
Source0:	https://github.com/jstasiak/python-zeroconf/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	bda83913df1669610ba3c09f8133614e
Patch0:		%{name}-mock.patch
URL:		https://github.com/jstasiak/python-zeroconf
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-enum34
BuildRequires:	python-mock
BuildRequires:	python-netifaces >= 0.10.6
BuildRequires:	python-pytest
BuildRequires:	python-six
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-netifaces >= 0.10.6
BuildRequires:	python3-pytest
BuildRequires:	python3-six
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A pure Python implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%description -l pl.UTF-8
Czysto pythonowa implementacja wykrywania usług multicastowych DNS
przy użyciu Bonjour/Avahi.

%package -n python3-%{module}
Summary:	Pure Python Multicast DNS Service Discovery Library
Summary(pl.UTF-8):	Czysto pythonowa biblioteka Multicast DNS Service Discovery
Group:		Libraries/Python

%description -n python3-%{module}
A pure Python implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%description -n python3-%{module} -l pl.UTF-8
Czysto pythonowa implementacja wykrywania usług multicastowych DNS
przy użyciu Bonjour/Avahi.

%prep
%setup -q
%patch0 -p1

# Remove enum-compat from install_requires
# See https://bugzilla.redhat.com/show_bug.cgi?id=1432165
sed -i '/enum-compat/d' setup.py

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest \
	%{!?with_integration:-k "not integration"}
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest \
	%{!?with_integration:-k "not integration"}
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst
%{py_sitescriptdir}/zeroconf.py[co]
%{py_sitescriptdir}/zeroconf-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/__pycache__/zeroconf.cpython-*.py[co]
%{py3_sitescriptdir}/zeroconf.py
%{py3_sitescriptdir}/zeroconf-%{version}-py*.egg-info
%endif
