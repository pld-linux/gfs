Summary:	Shared-disk cluster file system
Summary(pl):	Klastrowy system plik�w na wsp�dzielonym dysku
Name:		gfs
%define	snap	20040625
Version:	0.0.0.%{snap}.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	%{name}.tar.gz
# Source0-md5:	2e787a04f4b730b705bbd9d25dbdee72
URL:		http://sources.redhat.com/cluster/gfs/
BuildRequires:	iddev
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
GFS (Global File System) is a cluster file system. It allows a cluster
of computers to simultaneously use a block device that is shared
between them (with FC, iSCSI, NBD, etc...). GFS reads and writes to
the block device like a local filesystem, but also uses a lock module
to allow the computers coordinate their I/O so filesystem consistency
is maintained. One of the nifty features of GFS is perfect consistency
-- changes made to the filesystem on one machine show up immediately
on all other machines in the cluster.

%description -l pl
GFS (Global File System) to klastrowy system plik�w. Pozwala klastrowi
komputer�w na jednoczesne korzystanie z urz�dzenia blokowego
dzielonego mi�dzy nimi (poprzez FC, iSCSI, NBD itp.). GFS odczytuje i
zapisuje urz�dzenie blokowe jak lokalny system plik�w, ale u�ywa
dodatkowo modu�u blokuj�cego, aby umo�liwi� komputerom koordynowanie
ich operacji I/O w celu zachowania sp�jno�ci systemu plik�w. Jedn� z
szykownych mo�liwo�ci GFS-a jest idealna sp�jno�� - zmiany wykonane w
systemie plik�w na jednej maszynie natychmiast pokazuj� si� na
wszystkich innych maszynach w klastrze.

%prep
%setup -q -n %{name}

%build
./configure \
	--incdir=%{_includedir} \
	--kernel_src=%{_kernelsrcdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
