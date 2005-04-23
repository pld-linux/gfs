Summary:	Shared-disk cluster file system
Summary(pl):	Klastrowy system plików na wspó³dzielonym dysku
Name:		gfs
Version:	6.1
%define	bver	pre21
Release:	0.%{bver}.1
License:	GPL v2
Group:		Applications/System
Source0:	http://people.redhat.com/cfeist/cluster/tgz/%{name}-%{version}-%{bver}.tar.gz
# Source0-md5:	0b623c83354884e9da498e09130a3214
# from gfs-kernel CVS
Source1:	gfs_ondisk.h
# NoSource1-md5: 772e1801249bff0478b844924c0fdc20 (rev. 1.7; doesn't compile with 1.8)
Source2:	gfs_ioctl.h
# NoSource2-md5: fad0a58f6f39499661704f0d5af3a8c0 (rev. 1.10)
# from gfs-kernel/harness CVS
Source3:	lm_interface.h
# NoSource3-md5: 5b000a3b33af218e1b6b8a7d96b7e356 (rev. 1.7)
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
%setup -q -n %{name}-%{version}-%{bver}

install -d include/linux
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} include/linux

%{__perl} -pi -e 's/-Wall/%{rpmcflags} -Wall/' make/defines.mk.input
%{__perl} -pi -e 's/-O2 //' gfs_{mkfs,quota,tool}/Makefile

%build
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
#%attr(754,root,root) /etc/rc.d/init.d/gfs
%{_mandir}/man?/*
