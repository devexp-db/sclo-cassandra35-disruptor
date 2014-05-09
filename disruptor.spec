Name:          disruptor
Version:       3.2.1
Release:       1%{?dist}
Summary:       Concurrent Programming Framework
License:       ASL 2.0
URL:           http://lmax-exchange.github.io/disruptor/
Source0:       https://github.com/LMAX-Exchange/disruptor/archive/%{version}.tar.gz
Source1:       http://repo1.maven.org/maven2/com/lmax/%{name}/%{version}/%{name}-%{version}.pom

BuildRequires: java-devel

# test deps
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.jmock:jmock-junit4)
BuildRequires: mvn(org.jmock:jmock-legacy)

%if 0
# Unavailable performance test deps
# lib/test/hdrhistogram-1.0-SNAPSHOT.jar
BuildRequires: mvn(com.google.caliper:caliper:0.5-rc1)
%endif

# NOTE: the project is buildable with gradle by default
BuildRequires: maven-local
BuildRequires: maven-plugin-bundle
BuildRequires: maven-surefire-provider-junit4

BuildArch:     noarch

%description
A High Performance Inter-Thread Messaging Library.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

cp -p %{SOURCE1} pom.xml
%pom_xpath_inject "pom:project" "
<build>

</build>"

%pom_xpath_inject "pom:project/pom:build" '
<plugins>
  <plugin>
    <groupId>org.apache.felix</groupId>
    <artifactId>maven-bundle-plugin</artifactId>
    <version>any</version>
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
    </executions>
  </plugin>
</plugins>'
%pom_add_plugin org.apache.maven.plugins:maven-jar-plugin . '
<configuration>
  <archive>
    <manifestFile>${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
  </archive>
</configuration>'

# fail to compile cause: incompatible hamcrest apis
rm -r src/test/java/com/lmax/disruptor/RingBufferTest.java \
 src/test/java/com/lmax/disruptor/RingBufferEventMatcher.java

%build

%mvn_file :%{name} %{name}
%mvn_build -- -Dproject.build.sourceEncoding=UTF-8

%install
%mvn_install

%files -f .mfiles
%doc LICENCE.txt README.md

%files javadoc -f .mfiles-javadoc
%doc LICENCE.txt

%changelog
* Mon Apr 21 2014 gil cattaneo <puntogil@libero.it> 3.2.1-1
- update to 3.2.1

* Wed Aug 14 2013 gil cattaneo <puntogil@libero.it> 3.2.0-1
- initial rpm
