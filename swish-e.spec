%define	major	2
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname %{name} -d

Summary:	Simple Web Indexing System for Humans - Enhanced
Name: 		swish-e
Version: 	2.4.7
Release:	3
License: 	GPL
Group: 		Networking/Other
URL: 		http://swish-e.org/
Source0: 	http://swish-e.org/distribution/%{name}-%{version}.tar.gz
Patch0:		%{name}-2.4.7-fix-str-fmt.patch
BuildRequires:	perl-devel
BuildRequires:	libxml2-devel
BuildRequires:	pcre-devel
BuildRequires:	zlib-devel
BuildRequires:	chrpath
# (oe) require perl-SWISH-API just to play safe
Requires:	perl-SWISH-API >= %{version}

%description
Swish-e key features are :
    * Emacs/Gnus mail index in cooordination with nnir.el
    * Fast - many factors that affect speed, but a search on this server 
	that returns a thousand documents takes only a few seconds.
    * Flexible - a number of configuration options provide you a high degree 
	of control over what is indexed and how.
    * Powerful - the AND, OR and NOT operators are supported, words can be 
	truncated (using *), and searches can be limited to particular fields 
	(META tag fields, TITLEs, etc.)
    * Free - nothing, zip, zero.
    * It's made for Web sites - In indexing HTML files, SWISH-E can ignore 
	data in most tags while giving higher relevance to information in 
	header and title tags. Titles are extracted from HTML files and appear 
	in the search results. SWISH can automatically search your whole Web 
	site for you in one pass, if it's under one directory. You can also 
	limit your search to words in HTML titles, comments, emphasized tags, 
	and META tags. In addition, 8-bit HTML characters can be indexed, 
	converted, and searched.
    * It creates portable indexes - Index files consist of only one file, 
	so they can be transported around and easily maintained.
    * You can fix the source - We encourage people to send in patches and 
	suggestions on how to make SWISH-E better. You may want to join 
	the SWISH-E Discussion.

%package -n	%{libname}
Summary:	Swish-e libraries
Group:		System/Libraries

%description -n	%{libname}
Swish-e libraries

%package -n	%{devname}
Summary:	Swish-e devel files
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel
Provides:	lib%{name}-devel
Obsoletes:	%{mklibname %{name} 2 -d}

%description -n	%{devname}
Devel files for swish-e

%package -n	perl-SWISH-API
Summary:	SWISH::API - Perl interface to the Swish-e C Library
Group:		Development/Perl

%description -n	perl-SWISH-API
PERL SWISH-E language bindings and scripts.

SWISH::API provides a Perl interface to the Swish-e search engine.
SWISH::API allows embedding the swish-e search code into your
application avoiding the need to fork to run the swish-e binary
and to keep an index file open when running multiple queries. This
results in increased search performance.

%prep
%setup -q
%patch0 -p0

%build
%configure2_5x	--with-libxml2=%{_prefix} \
		--with-zlib=%{_prefix}

%make

pushd perl
	perl Makefile.PL SWISHBINDIR=$(readlink -f ../src) SWISHINC="-I$(readlink -f ../src)" SWISHLIBS="-L$(readlink -f ../src/.libs) -lswish-e" SWISHVERSION="%{version}"
        %make
	LD_LIBRARY_PATH=../src/.libs make test
popd

make test

%install
%makeinstall_std

install -m0755 swish-config %{buildroot}%{_bindir}/swish-config

%makeinstall_std -C perl

# nuke rpath
find %{buildroot}%{perl_vendorlib} -type f -name "*.so" | xargs chrpath -d
chrpath -d %{buildroot}%{_bindir}/swish-e

%files
%doc %{_docdir}/%{name}
%{_bindir}/swish-e
%{_datadir}/%{name}
%{_mandir}/man1/*

%files -n %{libname}
%multiarch %{_libdir}/*.so.*

%files -n %{devname}
%{_bindir}/swish-config
%multiarch %{_libdir}/*.so
%multiarch %{_libdir}/*.*a
%{_includedir}/*.h
%multiarch %{_libdir}/pkgconfig/*

%files -n perl-SWISH-API
%doc perl/Changes perl/README
%{_bindir}/swish-filter-test
%{_prefix}/lib/%{name} 
%{perl_vendorlib}/*/auto/SWISH/API/API.so
%{perl_vendorlib}/*/SWISH/API.pm
%{_mandir}/man3/SWISH::API.3pm*
