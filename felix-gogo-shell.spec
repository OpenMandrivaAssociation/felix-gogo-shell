%{?_javapackages_macros:%_javapackages_macros}
%global project   felix
%global bundle    org.apache.felix.gogo.shell

%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package %{project}-gogo-shell}

Name:             %{?scl_prefix}%{project}-gogo-shell
Version:          0.10.0
Release:          9.0%{?dist}
Summary:          Community OSGi R4 Service Platform Implementation - Basic Commands

License:          ASL 2.0
URL:              http://felix.apache.org/site/apache-felix-gogo.html

Source0:          http://mirror.catn.com/pub/apache//felix/org.apache.felix.gogo.shell-0.10.0-project.tar.gz
  
# Changed GroupID from osgi to felix
Patch0:           %{pkg_name}-groupid.patch

Patch1:           ignoreActivatorException.patch

BuildArch:        noarch

BuildRequires:    java-devel >= 1.7.0
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    xmvn
BuildRequires:    maven-plugin-bundle
BuildRequires:    maven-surefire-provider-junit4
BuildRequires:    %{?scl_prefix}felix-gogo-parent
BuildRequires:    %{?scl_prefix}felix-gogo-runtime
BuildRequires:    felix-osgi-compendium
BuildRequires:    maven-install-plugin
BuildRequires:    mockito

%{?scl:BuildRequires:	  %{?scl_prefix}build}

Requires:         java 
Requires:         jpackage-utils
%{?scl:Requires: %scl_runtime}

%description
Apache Felix is a community effort to implement the OSGi R4 Service Platform
and other interesting OSGi-related technologies under the Apache license. The
OSGi specifications originally targeted embedded devices and home services
gateways, but they are ideally suited for any project interested in the
principles of modularity, component-orientation, and/or service-orientation.
OSGi technology combines aspects of these aforementioned principles to define a
dynamic service deployment framework that is amenable to remote management.

%package javadoc

Summary:          Javadoc for %{pkg_name}
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{bundle}-%{version}
%patch0 -p1 -F3
%patch1

%build
%{?scl:%scl_maven_opts}
mvn-rpmbuild install javadoc:aggregate 

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}/%{project}
install -pm 644 target/%{bundle}-%{version}.jar %{buildroot}%{_javadir}/%{project}/%{bundle}.jar

# pom
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP.%{project}-%{bundle}.pom
%add_maven_depmap JPP.%{project}-%{bundle}.pom %{project}/%{bundle}.jar

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{pkg_name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{pkg_name}


%files
%doc DEPENDENCIES LICENSE NOTICE
%{_javadir}/*
%{_mavenpomdir}/JPP.%{project}-%{bundle}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE
%{_javadocdir}/%{pkg_name}

%changelog
* Mon Aug 5 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.10.0-9
- Fix FTBFS.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Krzysztof Daniel <kdaniel@redhat.com> 0.10.0-7
- Initial SCLization.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.10.0-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Krzysztof Daniel <kdaniel@redhat.com> 0.10.0-3
- Temporary fix for bug 786041

* Wed Jan 18 2012 Tomas Radej <tradej@redhat.com> - 0.10.0-2
- Changed jar path

* Mon Jan 09 2012 Tomas Radej <tradej@redhat.com> - 0.10.0-1
- Initial packaging
