# NOTE: obsolete, for 3rd generation cluster see cluster.spec
Summary:	Shared-disk cluster file system
Summary(pl.UTF-8):	Klastrowy system plików na współdzielonym dysku
Name:		gfs
Version:	2.03.11
Release:	1
Epoch:		1
License:	GPL v2+
Group:		Applications/System
Source0:	ftp://sources.redhat.com/pub/cluster/releases/cluster-%{version}.tar.gz
# Source0-md5:	712b9f583472d1de614641bc0f4a0aaf
Patch0:		%{name}-blkid.patch
Patch1:		cluster-kernel.patch
URL:		http://sources.redhat.com/cluster/gfs/
BuildRequires:	libblkid-devel >= 2.16
BuildRequires:	ncurses-devel
BuildRequires:	perl-base
# some parts point to gfs2 components
Requires:	gfs2 = %{epoch}:%{version}
Requires:	libblkid >= 2.16
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

%description -l pl.UTF-8
GFS (Global File System) to klastrowy system plików. Pozwala klastrowi
komputerów na jednoczesne korzystanie z urządzenia blokowego
dzielonego między nimi (poprzez FC, iSCSI, NBD itp.). GFS odczytuje i
zapisuje urządzenie blokowe jak lokalny system plików, ale używa
dodatkowo modułu blokującego, aby umożliwić komputerom koordynowanie
ich operacji I/O w celu zachowania spójności systemu plików. Jedną z
szykownych możliwości GFS-a jest idealna spójność - zmiany wykonane w
systemie plików na jednej maszynie natychmiast pokazują się na
wszystkich innych maszynach w klastrze.

%prep
%setup -q -n cluster-%{version}
%patch0 -p1
%patch1 -p1

%build
./configure \
	--cc="%{__cc}" \
	--cflags="%{rpmcflags} -Wall" \
	--ldflags="%{rpmldflags}" \
	--incdir=%{_includedir} \
	--ncursesincdir=%{_includedir}/ncurses \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--sbindir=%{_sbindir} \
	--without_gfs2 \
	--without_gnbd \
	--without_kernel_modules
%{__make} -C %{name}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C %{name} install \
	DESTDIR=$RPM_BUILD_ROOT

# fake for man pages links check
touch $RPM_BUILD_ROOT%{_mandir}/man8/gfs2_edit.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/fsck.gfs
%attr(755,root,root) %{_sbindir}/gfs_debug
%attr(755,root,root) %{_sbindir}/gfs_fsck
%attr(755,root,root) %{_sbindir}/gfs_grow
%attr(755,root,root) %{_sbindir}/gfs_jadd
%attr(755,root,root) %{_sbindir}/gfs_mkfs
%attr(755,root,root) %{_sbindir}/gfs_quota
%attr(755,root,root) %{_sbindir}/gfs_tool
%attr(755,root,root) %{_sbindir}/mkfs.gfs
# TODO: PLDify
#%attr(754,root,root) /etc/rc.d/init.d/gfs
%{_mandir}/man8/gfs.8*
%{_mandir}/man8/gfs_fsck.8*
%{_mandir}/man8/gfs_grow.8*
%{_mandir}/man8/gfs_jadd.8*
%{_mandir}/man8/gfs_mkfs.8*
%{_mandir}/man8/gfs_mount.8*
%{_mandir}/man8/gfs_quota.8*
%{_mandir}/man8/gfs_tool.8*
# links to gfs2
%attr(755,root,root) %{_sbindir}/gfs_edit
%attr(755,root,root) %{_sbindir}/mount.gfs
%attr(755,root,root) %{_sbindir}/umount.gfs
%{_mandir}/man8/gfs_edit.8*
