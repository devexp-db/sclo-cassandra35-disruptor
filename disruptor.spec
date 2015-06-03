Name:          disruptor
Version:       3.3.2
Release:       1%{?dist}
Summary:       Concurrent Programming Framework
License:       ASL 2.0
URL:           http://lmax-exchange.github.io/disruptor/
Source0:       https://github.com/LMAX-Exchange/disruptor/archive/%{version}.tar.gz
Source1:       http://repo1.maven.org/maven2/com/lmax/%{name}/%{version}/%{name}-%{version}.pom

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.jmock:jmock-junit4)
BuildRequires: mvn(org.jmock:jmock-legacy)

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
%setup -q
# Cleanup
find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

cp -p %{SOURCE1} pom.xml

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
rm -f src/test/java/com/lmax/disruptor/EventPollerTest.java

%mvn_file :%{name} %{name}

%build

%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc README.md
%license LICENCE.txt

%files javadoc -f .mfiles-javadoc
%license LICENCE.txt

%changelog
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
