Summary:	Shared-disk cluster file system
Summary(pl):	Klastrowy system plików na wspó³dzielonym dysku
Name:		gfs
Version:	1.02.00
Release:	1
Epoch:		1
License:	GPL v2
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	131c34c8b66d8d7d74384839ed4091d0
URL:		http://sources.redhat.com/cluster/gfs/
BuildRequires:	iddev
BuildRequires:	perl-base
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
GFS (Global File System) to klastrowy system plików. Pozwala klastrowi
komputerów na jednoczesne korzystanie z urz±dzenia blokowego
dzielonego miêdzy nimi (poprzez FC, iSCSI, NBD itp.). GFS odczytuje i
zapisuje urz±dzenie blokowe jak lokalny system plików, ale u¿ywa
dodatkowo modu³u blokuj±cego, aby umo¿liwiæ komputerom koordynowanie
ich operacji I/O w celu zachowania spójno¶ci systemu plików. Jedn± z
szykownych mo¿liwo¶ci GFS-a jest idealna spójno¶æ - zmiany wykonane w
systemie plików na jednej maszynie natychmiast pokazuj± siê na
wszystkich innych maszynach w klastrze.

%prep
%setup -q -n cluster-%{version}
install -d %{name}/include/linux
install %{name}-kernel/src/gfs/{gfs_ioctl.h,gfs_ondisk.h} %{name}/include/linux
install %{name}-kernel/src/harness/lm_interface.h %{name}/include/linux
cd %{name}

%{__perl} -pi -e 's/-Wall/%{rpmcflags} -Wall/' make/defines.mk.input
%{__perl} -pi -e 's/-O2 //' gfs_{mkfs,quota,tool}/Makefile

%build
cd %{name}
./configure \
	--incdir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir}
%{__make} \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
cd %{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
#%attr(754,root,root) /etc/rc.d/init.d/gfs
%{_mandir}/man?/*
