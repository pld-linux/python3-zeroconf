#
# Conditional build:
%bcond_with	integration	# Integration tests work in mock but fail in Koji with PermissionError
%bcond_with	tests		# unit tests

%define module	zeroconf
Summary:	Pure Python Multicast DNS Service Discovery Library
Summary(pl.UTF-8):	Czysto pythonowa biblioteka Multicast DNS Service Discovery
Name:		python3-%{module}
# 0.40+ uses poetry to build
Version:	0.39.4
Release:	1
License:	LGPL v2
Group:		Libraries/Python
#Source0Download: https://github.com/jstasiak/python-zeroconf/releases
Source0:	https://github.com/jstasiak/python-zeroconf/archive/%{version}/python-%{module}-%{version}.tar.gz
# Source0-md5:	b37ccfaff57368f6fc079676f904c834
URL:		https://github.com/jstasiak/python-zeroconf
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-async_timeout >= 4.0.1
BuildRequires:	python3-ifaddr >= 0.1.7
BuildRequires:	python3-pytest
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

%prep
%setup -q -n python-%{module}-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest \
	%{!?with_integration:-k "not integration"}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/zeroconf
%{py3_sitescriptdir}/zeroconf-%{version}-py*.egg-info
