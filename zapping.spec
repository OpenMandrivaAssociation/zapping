Name:		zapping
Summary:	A TV viewer for GNOME
Version:	0.9.6
Release:	%mkrel 7
License:	GPL
URL:		http://sourceforge.net/projects/zapping/
Group:		Video
Source0:	http://osdn.dl.sourceforge.net/sourceforge/zapping/%{name}-%{version}.tar.bz2
Source11:	%{name}-16.png
Source12:	%{name}-32.png
Source13:	%{name}.png
Patch1:		zapping-0.7.1-lib64.patch
Patch2:		zapping-0.9.6-ppc.patch
Patch3:         zapping-0.9.6-pam.patch
# taken from debian package
# http://bugs.debian.org/424502
Patch4:         zapping-0.9.6-shift.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	autoconf2.5 arts-devel libglade2.0-devel libgnomeui2-devel
BuildRequires:	python-devel scrollkeeper perl-XML-Parser
BuildRequires:	zvbi-devel usermode-consoleonly desktop-file-utils
Requires:	usermode 
Requires:	usermode-consoleonly
Requires(pre):	info-install

%description
Zapping is a TV viewer for GNOME that supports both Video4Linux 
and Video4Linux2. It's extensible through plugins based on GTK.

%prep
%setup -q
%patch1 -p1 -b .lib64
%patch2 -p1 -b .ppc
%patch3 -p1
%patch4 -p1
autoconf

%build
%configure2_5x
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

%{find_lang} %{name}

%post
%update_menus
  
%postun
%clean_menus

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
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


