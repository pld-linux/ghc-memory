#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	memory
Summary:	Memory and related abstraction stuff
Name:		ghc-%{pkgname}
Version:	0.15.0
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/memory
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	f763e1781a843e53b75f9944dd546cb5
URL:		http://hackage.haskell.org/package/memory
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-basement >= 0.0.7
BuildRequires:	ghc-deepseq >= 1.1
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-basement-prof >= 0.0.7
BuildRequires:	ghc-deepseq-prof >= 1.1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-basement >= 0.0.7
Requires:	ghc-deepseq >= 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Chunk of memory, polymorphic byte array management and manipulation:

- A polymorphic byte array abstraction and function similar to strict
  ByteString.
- Different type of byte array abstraction.
- Raw memory IO operations (memory set, memory copy, ..)
- Aliasing with endianness support.
- Encoding : Base16, Base32, Base64.
- Hashing : FNV, SipHash

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-basement-prof >= 0.0.7
Requires:	ghc-deepseq-prof >= 1.1

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/Pack
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/Pack/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/Pack/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Encoding
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Encoding/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Encoding/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Hash
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Hash/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Hash/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/MemMap
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/MemMap/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/MemMap/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/ByteArray/Pack/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Encoding/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Hash/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Memory/MemMap/*.p_hi
%endif
