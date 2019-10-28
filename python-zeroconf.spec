#
# Conditional build:
%bcond_with	integration	# Integration tests work in mock but fail in Koji with PermissionError
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define pypi_name zeroconf
Summary:	Pure Python Multicast DNS Service Discovery Library
Name:		python-%{pypi_name}
Version:	0.18.0
Release:	4
License:	LGPLv2
Group:		Libraries/Python
Source0:	https://github.com/jstasiak/%{name}/archive/%{version}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	f40e133a2cec3087761e5230cdf8637c
URL:		https://github.com/jstasiak/python-%{pypi_name}
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-enum34
BuildRequires:	python-mock
BuildRequires:	python-netifaces
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
BuildRequires:	python-six
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-mock
BuildRequires:	python3-netifaces
BuildRequires:	python3-pytest
BuildRequires:	python3-setuptools
BuildRequires:	python3-six
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A pure Python implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%package -n     python3-%{pypi_name}
Summary:	Pure Python 3 Multicast DNS Service Discovery Library
Group:		Libraries/Python
Requires:	python3-netifaces
Requires:	python3-six

%description -n python3-%{pypi_name}
A pure Python 3 implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%prep
%setup -q

# Remove enum-compat from install_requires
# See https://bugzilla.redhat.com/show_bug.cgi?id=1432165
sed -i '/enum-compat/d' setup.py

%build
%if %{with python2}
%py_build
%if %{with tests}
%{__python} -m pytest \
	%{!?with_integartion:-k "not integration"}
%endif
%endif

%if %{with python3}
%py3_build %{?with_tests:test}

%if %{with tests}
%{__python3} -m pytest \
	%{!?with_integartion:-k "not integration"}
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

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
%{py_sitescriptdir}/%{pypi_name}.py[co]
%{py_sitescriptdir}/%{pypi_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/__pycache__/*
%{py3_sitescriptdir}/%{pypi_name}.py
%{py3_sitescriptdir}/%{pypi_name}-%{version}-py*.egg-info
%endif
