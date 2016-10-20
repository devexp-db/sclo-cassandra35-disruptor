%{?scl:%scl_package disruptor}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}disruptor
Version:	3.3.4
Release:	3%{?dist}
Summary:	Concurrent Programming Framework
License:	ASL 2.0
URL:		http://lmax-exchange.github.io/%{pkg_name}/
Source0:	https://github.com/LMAX-Exchange/%{pkg_name}/archive/%{version}.tar.gz
Source1:	http://repo1.maven.org/maven2/com/lmax/%{pkg_name}/%{version}/%{pkg_name}-%{version}.pom
# see http://www.jmock.org/threading-synchroniser.html
Patch0:		%{pkg_name}-3.3.2-jmock.patch

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix_maven}maven-plugin-bundle
BuildRequires:	%{?scl_prefix_java_common}hamcrest
# test dependency
BuildRequires:	%{?scl_prefix_java_common}junit
# test dependencies not needed in SCL package
%{!?scl:BuildRequires: mvn(org.jmock:jmock-junit4)
scl:BuildRequires: mvn(org.jmock:jmock-legacy)}
%{?scl:Requires: %scl_runtime}

%if 0
# Unavailable performance test deps
# lib/test/hdrhistogram-1.0-SNAPSHOT.jar
BuildRequires: mvn(com.google.caliper:caliper:0.5-rc1)
%endif

BuildArch:     noarch

%description
A High Performance Inter-Thread Messaging Library.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -qn %{pkg_name}-%{version}
# Cleanup
find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

%patch0 -p1

cp -p %{SOURCE1} pom.xml

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
# Add OSGi support
%pom_xpath_inject "pom:project" "<packaging>bundle</packaging>"
%pom_add_plugin org.apache.felix:maven-bundle-plugin:2.3.7 . '
<extensions>true</extensions>
<configuration>
  <instructions>
    <Bundle-DocURL>%{url}</Bundle-DocURL>
    <Bundle-Name>${project.name}</Bundle-Name>
    <Bundle-Vendor>LMAX Disruptor Development Team</Bundle-Vendor>
  </instructions>
</configuration>
<executions>
  <execution>
    <id>bundle-manifest</id>
    <phase>process-classes</phase>
    <goals>
      <goal>manifest</goal>
    </goals>
  </execution>
</executions>'

# fail to compile cause: incompatible hamcrest apis
rm -r src/test/java/com/lmax/disruptor/RingBufferTest.java \
 src/test/java/com/lmax/disruptor/RingBufferEventMatcher.java
# Failed to stop thread: Thread[com.lmax.disruptor.BatchEventProcessor@1d057a39,5,main]
rm -r src/test/java/com/lmax/disruptor/dsl/DisruptorTest.java
# Test fails due to incompatible jmock version
#rm -f src/test/java/com/lmax/disruptor/EventPollerTest.java

# remove unneeded test dependencies for SCL package
%{?scl:%pom_remove_dep org.jmock:jmock-junit4
%pom_remove_dep org.jmock:jmock-legacy
rm -rf src/test}

%mvn_file :%{pkg_name} %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md
%license LICENCE.txt

%files javadoc -f .mfiles-javadoc
%license LICENCE.txt

%changelog
* Thu Oct 20 2016 Tomas Repik <trepik@redhat.com> - 3.3.4-3
- use standard SCL macros

* Tue Aug 09 2016 Tomas Repik <trepik@redhat.com> - 3.3.4-2
- scl conversion

* Thu Jun 23 2016 gil cattaneo <puntogil@libero.it> 3.3.4-1
- update to 3.3.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 gil cattaneo <puntogil@libero.it> 3.3.2-2
- build fix for jmock 2.8.1

* Wed Jun  3 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.2-1
- Update to upstream version 3.3.2

* Sun Feb 01 2015 gil cattaneo <puntogil@libero.it> 3.2.1-3
- introduce license macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 gil cattaneo <puntogil@libero.it> 3.2.1-1
- update to 3.2.1

* Wed Aug 14 2013 gil cattaneo <puntogil@libero.it> 3.2.0-1
- initial rpm
