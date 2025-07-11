Name:		zapping
Summary:	A TV viewer for GNOME
Version:	0.10
Release:	%mkrel 0.0.cvs6.10
License:	GPL
URL:		https://sourceforge.net/projects/zapping/
Group:		Video
#Source0:	http://osdn.dl.sourceforge.net/sourceforge/zapping/%{name}-%{version}.tar.bz2
Source0:	zapping-0.10cvs6.tar.bz2
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}.png
Patch1:		zapping-0.7.1-lib64.patch
Patch2:		zapping-automake-1.13.patch
Patch3:         zapping-0.9.6-pam.patch
# taken from debian package
# http://bugs.debian.org/424502
Patch4:         zapping-0.9.6-shift.patch
Patch5:		zapping-0.10cvs6-libtool_fixes.diff
Patch6:		zapping-0.10cvs6-linkage.patch
Patch7:         zapping-0.10cvs6.libpng15.patch
Patch9:         zapping-0.10cvs6.zvbi.patch
Patch10:        zapping-0.10cvs6.lXext.patch
BuildRequires:	autoconf2.5
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	libglade2.0-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libtool
BuildRequires:	perl-XML-Parser
BuildRequires:	python-devel
BuildRequires:	scrollkeeper
BuildRequires:	usermode-consoleonly
BuildRequires:	zvbi-devel
BuildRequires:	libxmu-devel
Requires:	usermode 
Requires:	usermode-consoleonly

%description
Zapping is a TV viewer for GNOME that supports both Video4Linux 
and Video4Linux2. It's extensible through plugins based on GTK.

%prep

%setup -q -n %{name}-%{version}cvs6
%patch1 -p0 -b .lib64
%patch2 -p1 -b .automake13~
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .libtool_fixes
%patch6 -p0
%patch7 -p1
%patch9 -p1
%patch10 -p1

%build
sed -i -e 's,configure.in,configure.ac,g' configure.in
autoreconf -fi

%configure2_5x --disable-schemas-install
%make

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} plugindir=%{_libdir}/zapping/plugins

perl -pi -e 's,zapping/gnome-television.png,gnome-television,g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="Multimedia" \
  --remove-key="Version" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/zapping_setup_fb
ln -sf zapping $RPM_BUILD_ROOT%{_bindir}/zapzilla

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%endif
  
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-,root,root)
%doc AUTHORS THANKS ChangeLog README README.plugins TODO BUGS
%doc plugins/alirc/README.alirc
%config(noreplace) %{_sysconfdir}/pam.d/zapping_setup_fb
%config(noreplace) %{_sysconfdir}/security/console.apps/zapping_setup_fb
%config(noreplace) %{_sysconfdir}/gconf/schemas/zapping.schemas
      #/home/tv/rpm/tmp/zapping-0.9.6-1mdk-buildroot/etc/pam.d/zapping_setup_fb
	   #  /home/tv/rpm/tmp/zapping-0.9.6-1mdk-buildroot/etc/security/console.apps/zapping_setup_fb

%{_bindir}/*
%{_sbindir}/*
%{_libdir}/zapping
%{_datadir}/applications/zapping.desktop
%{_datadir}/gnome/help/zapping
%{_datadir}/omf/zapping/zapping-C.omf
%{_datadir}/pixmaps/zapping
%{_datadir}/zapping
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_mandir}/*/*




%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 0.10-0.0.cvs6.6mdv2011.0
+ Revision: 671952
- mass rebuild

