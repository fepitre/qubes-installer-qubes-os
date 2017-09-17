%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/pungi
%endif

Name:           pungi
Version:        4.1.18
Release:        2%{?dist}
Epoch:          1000
Summary:        Distribution compose tool

Group:          Development/Tools
License:        GPLv2
URL:            https://pagure.io/pungi
Source0:        https://pagure.io/releases/%{name}/%{name}-%{version}.tar.bz2
Patch1:         0001-Set-repository-gpgkey-option.patch
Patch2:         0002-Verify-downloaded-packages.patch
Patch3:         disable-efi.patch
Patch4:         Hacky-way-to-pass-gpgkey-to-lorax.patch
#Patch5:         fix-recursive-partition-table-on-iso-image.patch
#Patch6:         disable-upgrade.patch
BuildRequires:  python-nose, python-mock
BuildRequires:  python-devel, python-setuptools, python2-productmd
BuildRequires:  python-lockfile, kobo, kobo-rpmlib, python-kickstart, createrepo_c
BuildRequires:  python-lxml, libselinux-python, yum-utils, lorax
BuildRequires:  yum => 3.4.3-28, createrepo >= 0.4.11
BuildRequires:  gettext, git-core, cvs
BuildRequires:  python-jsonschema
BuildRequires:  python-enum34
BuildRequires:  python2-dnf
BuildRequires:  python2-multilib
BuildRequires:  python2-libcomps

#deps for doc building
BuildRequires:  latexmk
BuildRequires:  python-sphinx, texlive-latex-bin-bin, texlive-collection-fontsrecommended
BuildRequires:  texlive-times, texlive-cmap, texlive-babel-english, texlive-fancyhdr
BuildRequires:  texlive-fancybox, texlive-titlesec, texlive-framed, texlive-threeparttable
BuildRequires:  texlive-mdwtools, texlive-wrapfig, texlive-parskip, texlive-upquote
BuildRequires:  texlive-multirow, texlive-capt-of, texlive-eqparbox, tex(color.cfg)
BuildRequires:	texlive-needspace
BuildRequires:  tex(fncychap.sty)
BuildRequires:  tex(tabulary.sty)

Requires:       createrepo >= 0.4.11
Requires:       yum => 3.4.3-28
Requires:       lorax >= 22.1
Requires:       repoview
Requires:       python-lockfile
Requires:       kobo
Requires:       kobo-rpmlib
Requires:       python-productmd
Requires:       python-kickstart
Requires:       libselinux-python
Requires:       createrepo_c
Requires:       python-lxml
Requires:       koji >= 1.10.1-13
# This is optional do not Require it
#Requires:       jigdo
Requires:       cvs
Requires:       yum-utils
Requires:       isomd5sum
Requires:       genisoimage
Requires:       gettext
# this is x86 only 
#Requires:       syslinux
Requires:       git
Requires:       python-jsonschema
Requires:       libguestfs-tools-c
Requires:       python-enum34
Requires:       python2-dnf
Requires:       python2-multilib
Requires:       python2-libcomps

BuildArch:      noarch

%description
A tool to create anaconda based installation trees/isos of a set of rpms.

%package utils
Summary:    Utilities for working with finished composes
Requires:   pungi = %{version}-%{release}

%description utils
These utilities work with finished composes produced by Pungi. They can be used
for creating unified ISO images, validating config file or sending progress
notification to Fedora Message Bus.


%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%%patch5 -p1
#%%patch6 -p1

%build
%{__python} setup.py build
cd doc
make latexpdf
make epub
make text
make man
gzip _build/man/pungi.1

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -d %{buildroot}/var/cache/pungi
%{__install} -d %{buildroot}/%{_mandir}/man8

%files
%defattr(-,root,root,-)
%license COPYING GPL
%doc AUTHORS
%{python_sitelib}/%{name}
%{python_sitelib}/%{name}-%{version}-py?.?.egg-info
%{_bindir}/%{name}
%{_bindir}/%{name}-koji
%{_bindir}/%{name}-gather
%{_bindir}/comps_filter
%{_bindir}/%{name}-make-ostree
%{_datadir}/%{name}
/var/cache/%{name}

%files utils
%{python_sitelib}/%{name}_utils
%{_bindir}/%{name}-create-unified-isos
%{_bindir}/%{name}-config-validate
%{_bindir}/%{name}-fedmsg-notification
%{_bindir}/%{name}-patch-iso
%{_bindir}/%{name}-compare-depsolving
%{_bindir}/%{name}-wait-for-signed-ostree-handler

%check
nosetests --exe
./tests/data/specs/build.sh
cd tests && ./test_compose.sh

%changelog
* Mon Aug 21 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.18-1
- KojiWrapper: include serverca in session_opts (otaylor)
- Report warning when config sections are not used (lsedlar)
- pkgset: Download packages with dnf (lsedlar)
- gather: Fix duplicated log line (lsedlar)
- gather: Add fulltree-exclude flag to DNF backend (lsedlar)
- checks: Stop looking for imports (lsedlar)
- ostree: Simplify configuration (lsedlar)
- config: Reduce duplication in schema (lsedlar)
- config: Add option for dumping config schema (lsedlar)
- scm: Accept unicode as local path (lsedlar)
- docs: Add documentation for scm_dict (lsedlar)
- scm-wrapper: Allow running command after git clone (lsedlar)
- scm-wrapper: Test correct file lists are returned (lsedlar)
- tests: Fix test_compose.sh paths (lsedlar)
- gather: Only parse pungi log once (lsedlar)
- gather: Report missing comps packages (lsedlar)
- gather: Avoid reading whole log into memory (lsedlar)
- repoclosure: Allow aborting compose when repoclosure fails (lsedlar)
- repoclosure: Fix logging errors (lsedlar)
- tests: Make test-compose cwd independent (lsedlar)
- Make strict the only option. (rbean)
- Raise a ValueError with details if module not found in PDC. (rbean)
- unified-iso: Only link to non-empty variants (lsedlar)
- gather: Fix excluding debugsource packages from input list (lsedlar)
- gather: Add debugsource package to tests (lsedlar)
- Use only one list of patterns/rules for debug packages (opensource)
- Do not match "*-debugsource-*" as debuginfo package (opensource)
- Use pungi.util.pkg_is_debug() instead of pungi.gather.is_debug() (opensource)
- remove the dependency of rpmUtils (qwan)
- Add support for debugsource packages (lsedlar)
- gather: Don't pull multiple debuginfo packages (lsedlar)
- GatherSourceModule: return rpm_obj instead of the rpm_obj.name (jkaluza)
- gather: Stop requiring comps file in nodeps (lsedlar)

* Mon Jul 17 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.17-1
- checksum: Checksum each image only once (lsedlar)
- checksum: Refactor creating checksum files (lsedlar)
- createrepo: Don't use existing metadata with deltas (lsedlar)
- util: Fix finding older compose (lsedlar)
- createrepo: Use correct paths for old package dirs (lsedlar)
- spec: Add missing ostree signature waiting handler (lsedlar)
- docs: Minor improvements to documentation (lsedlar)
- ostree: Add notification handler to wait for signature (lsedlar)
- ostree: Add URL to repo to message (lsedlar)
- gather: nodeps should take packages from comps groups (lsedlar)
- unified-iso: handle empty arch (kdreyer)
- createrepo: handle missing product ids scm dir (kdreyer)
- comps_wrapper: Code clean up (lsedlar)
- comps_filter: Filter environments by arch (pholica)
- notification: Allow specifying multiple scripts (lsedlar)
- pkgset: Allow populating packages from multiple koji tags (qwan)
- pungi: Port to argparse (lsedlar)
- comps_filter: Port to argparse (lsedlar)
- variants-wrapper: Remove main() function (lsedlar)
- multilib_yum: Remove main() function (lsedlar)
- pungi-koji: Port to argparse (lsedlar)
- ostree: Update tests for no ostree init (lsedlar)
- ostree: Don't automatically create a repo (walters)
- osbs: Config validation should accept a list (lsedlar)
- pkgset: Use release number of a module (mcurlej)
- docs: Add a basic info about gathering packages (lsedlar)
- docs: Kobo can be installed via pip now (lsedlar)
- docs: Add overview of what each phase does (lsedlar)
- gather: Log tag from which we pulled a package (lsedlar)
- docs: Document config file format (lsedlar)
- docs: Move logo to _static subdir (lsedlar)
- Add dropped livemedia phase (lsedlar)
- gather: Display source repo of packages (lsedlar)
- pkgset: Use descriptive name for log file (lsedlar)
- ostree-installer: Clean up output dir (lsedlar)
- Ignore more pycodestyle warnings (lsedlar)
- Allow gather source classes to return SimpleRpmWrapper objects from pkgset
  phase directly. (jkaluza)
- tests: use unittest2 if available (lsedlar)
- koji-wrapper: Handle failed subtasks (lsedlar)

* Fri Jun 09 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.16-1
- Fix changelog generator script (lsedlar)
- util: Retry resolving git branches (lsedlar)
- arch: Move exclu(de|sive)arch check to a function (lsedlar)
- gather-source: Check arch in module source (jkaluza)
- koji-wrapper: Stop mangling env variables (lsedlar)
- Ensure all phases are stopped (lsedlar)
- comps-wrapper: Report unknown package types (lsedlar)
- Generate proper modular metadata when there are different versions of the
  same package in the variant (jkaluza)
- checks: Make gpgkey a boolean option (lsedlar)
- ostree: Refactor writing repo file (lsedlar)
- iso-wrapper: Capture debug information for mounting (lsedlar)
- comps-wrapper: Fix crash on conditional packages (lsedlar)
- gather: Don't resolve dependencies in lookaside (lsedlar)
- koji-wrapper: Run all blocking commands with fresh ccache (lsedlar)
- Add @retry decorator and use it to retry connection on PDC on IOError and in
  SCM's retry_run. (jkaluza)
- Remove shebang from non-executable files (lsedlar)

* Thu May 04 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.15-1
- pkgset: Remove use of undefined variable (lsedlar)
- Store RPM artifacts in resulting repository in modulemd metadata. (jkaluza)
- variants: Remove redundant check (lsedlar)
- compose: Stop duplicating variant types (lsedlar)
- gather: Remove handling of impossible state (lsedlar)
- gather: Clean up code (lsedlar)
- gather: Add tests for gather phase (lsedlar)
- scm-wrapper: Remove unused arguments (lsedlar)
- tests: Avoid creating unused temporary files (lsedlar)
- tests: Clean up persistent temporary data (lsedlar)
- docs: Add a logo on the About page (lsedlar)
- docs: Document origin of the name (lsedlar)
- gather-dnf: Log exact Requires pulling a package in (lsedlar)
- gather: Print specific Requires which pulls a package in (lsedlar)
- gather: Process dependencies sorted (lsedlar)
- koji-wrapper: Run koji runroot with fresh credentials cache (lsedlar)
- util: Move get_buildroot_rpms to koji wrapper (lsedlar)
- osbs: Make git_branch required option (lsedlar)
- docs: Update createrepo_checksum allowed values (lsedlar)
- extra-files: Allow configuring used checksums (lsedlar)
- doc: Document options for media checksums (lsedlar)
- config: Add sha512 as valid createrepo checksum (lsedlar)
- util: Report better error on resolving non-existing branch (lsedlar)
- util: Show choices for volid if all are too long (lsedlar)
- checks: Fix anyOf validator yield ValidationError on ConfigOptionWarning
  (qwan)
- comps-wrapper: Reduce duplication in code (lsedlar)
- comps-wrapper: Port to libcomps (lsedlar)
- comps-wrapper: Sort langpacks by name (lsedlar)
- comps-wrapper: Minor code cleanup (lsedlar)
- comps-wrapper: Add tests (lsedlar)
- comps-wrapper: Fix uservisible not being modifiable (lsedlar)
- comps-wrapper: Return IDs instead of yum.comps.Group (lsedlar)
- comps-wrapper: Remove unused code (lsedlar)
- Be explicit about generating release for images (lsedlar)
- docs: Add examples for generated versions (lsedlar)
- ostree: Autogenerate a version (lsedlar)
- Expand compatible arches when gathering from modules. (rbean)
- gather: Clean up method deps (lsedlar)
- gather: Report error if there is no input (lsedlar)
- init: Warn when variants mentions non-existing comps group (lsedlar)
- Fix createrepo issue for modular compose when multiple threads tried to use
  the same tmp directory. (jkaluza)
- unified-iso: Use different type for debuginfo iso (lsedlar)
- unified-iso: Handle missing paths in metadata (lsedlar)
- unify repo and repo_from options (qwan)
- Fix some PEP8 errors in util.py (qwan)
- move translate_path from paths.py to util.py (qwan)
- checks.py: support 'append' option (qwan)
- checks.py: show warning message for alias option (qwan)

* Mon Mar 27 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.14-1
- Not create empty skeleton dirs for empty variants (qwan)
- Query only active modules in PDC. (jkaluza)
- Save modules metadata as full yaml object (jkaluza)
- Implement DNF based depsolving (dmach, mmraka, lsedlar)
- Add support for modular composes (jkaluza)
- Add a script for modifying ISO images (lsedlar)
- iso-wrapper: Add utility for mounting images (lsedlar)
- buildinstall: Move tweaking configs into a function (lsedlar)
- image-build: Correctly write can_fail option (lsedlar)
- pungi-koji: new cmd option '--latest-link-status' (qwan)
- Print task ID for successful tasks (lsedlar)
- ostree-installer: Fix logging directory (lsedlar)
- buildinstall: Print debug info if unmount fails (lsedlar)
- pkgset: report all unsigned packages (qwan)
- default createrepo_checksum to sha256 (qwan)
- unified-iso: Log better error when linking fails (lsedlar)
- unified-iso: Blacklist extra files metadata (lsedlar)
- buildinstall: Retry unmounting image (lsedlar)
- Remove indices from documentation (lsedlar)
- iso-wrapper: Handle wrong implant md5 (lsedlar)
- image-build: Remove check for number of images (lsedlar)
- Extract only first version from specfile (lsedlar)
- consolidate repo option names (qwan)
- checks: extend validator with 'alias' (qwan)
- osbs: write manifest for scratch osbs (qwan)

* Fri Mar 03 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.13-1
- Make MANIFEST.in stricter (qwan)
- Remove one line of log print (qwan)
- gather: Filter comps group on depsolving input of optional (lsedlar)
- Enable customizing runroot task weight (lsedlar)
- comps: Filter comps groups for optional variants (lsedlar)
- Rename main logger (lsedlar)
- ostree: Silence logger in tests (lsedlar)
- ostree: Fix crash when extra repos are missing (lsedlar)
- util: Add a utility for managing temporary files (lsedlar)
- Add --quiet option to pungi-koji (qwan)
- handle opening empty images.json while re-running pungi-koji in debug mode
  (qwan)
- minor change: remove an always true condition (qwan)
- Refactor depsolving tests (lsedlar)
- multilib: Remove FileMultilibMethod class (lsedlar)
- pkgset: Use additional packages for initial pull (lsedlar)
- metadata: Fix .treeinfo paths for addons (lsedlar)
- koji_wrapper: Always use --profile option with koji (lsedlar)
- add missing koji_profile from test compose setting (dennis)
- use koji --profile when calling koji for livemedia (dennis)
- repoclosure: Don't run build deps check (lsedlar)
- repoclosure: add option to use dnf backend (lsedlar)
- repoclosure: Add test for repoclosure in test phase (lsedlar)
- repoclosure: Remove duplicated code (lsedlar)
- repoclosure: Remove useless wrapper class (lsedlar)
- repoclosure: Remove unused code (lsedlar)
- repoclosure: Add a test for the wrapper (lsedlar)
- image-build: Pass arches around as a list (lsedlar)
- image-build: Expand arches for can_fail (lsedlar)
- image_checksum: add file sizes to checksum files (qwan)
- Add documentation and example for greedy_method (lsedlar)
- replace ${basearch} when updating the ref (dennis)
- Add some debugging about ref updating (puiterwijk)

* Tue Jan 17 2017 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.12-1
- unified-iso: Fall back to default config (lsedlar)
- osbs: optionally check GPG signatures (qwan)
- ostree-installer:  Allow multiple repos in ostree installer (qwan)
- Update tox.ini (lsedlar)
- unified-iso: Create isos with debuginfo packages (lsedlar)
- Create temporary dirs under compose's workdir (qwan)
- spec: Update upstream and source URL (lsedlar)
- unified-iso: Create work/ dir if missing (lsedlar)
- spec: Copy %%check section from Fedora (lsedlar)
- Update MANIFEST.in to include test data (lsedlar)
- osbs: Add better example to documentation (lsedlar)
- metadata: Correctly parse lorax .treeinfo (lsedlar)
- spec: Add a separate subpackage for extra utils (lsedlar)
- Add script to generate unified ISOs (lsedlar)
- osbs: Validate config in tests (lsedlar)
- osbs: Verify the .repo files contain correct URL (lsedlar)
- osbs: Enable specifying extra repos (lsedlar)
- pungi-make-ostree: change 'tree' command '--log-dir' arg to be required
  (qwan)
- Add test for krb_login with principal and keytab (puiterwijk)
- Make sure that the profile name is parsed correctly (puiterwijk)
- Make KojiWrapper support krb_login with keytab (puiterwijk)
- Make KojiWrapper parse krb_rdns (puiterwijk)
- Update documentation (lsedlar)
- image-build: Allow failure only on some arches (lsedlar)
- live-media: Allow some arches to fail (lsedlar)
- image-build: Use install_tree from parent for nested variants (lsedlar)
- config: Report unknown options as warnings (lsedlar)
- pungi: Fix --nosource option (lsedlar)
- pungi: Handle missing SRPM (lsedlar)
- ostree-installer: Add 'installer' sub-command to pungi-make-ostree (qwan)
- ostree: Add 'tree' sub-command to pungi-make-ostree script (qwan)
- metadata: Allow creating internal releases (lsedlar)
- Add CLI option to create ci compose (lsedlar)
- Fix PhaseLoggerMixin in case of compose has _logger = None (qwan)
- ostree-installer: Use dvd-ostree as type in metadata (lsedlar)
- image-build: Reduce duplication (lsedlar)
- createrepo: Add tests for adding product certificates (lsedlar)
- createrepo: Add tests for retrieving product certificates (lsedlar)
- Include phase name in log for some phases (qwan)
- Expose lorax's --rootfs-size argument (walters)
- pungi: Include noarch debuginfo (lsedlar)
- media-split: Print sensible message for unlimited size (lsedlar)

* Tue Nov 15 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.11-1
- [ostree] Allow extra repos to get packages for composing OSTree repository
  (qwan)
- pungi: Run in-process for testing (lsedlar)
- pungi: Only add logger once (lsedlar)
- pungi: Connect yum callback to logger (lsedlar)
- extra-files: Nice error message on missing RPM (lsedlar)
- compose: Drop unused argument (lsedlar)
- compose: Search all nested variants (lsedlar)
- ostree-installer: Capture all lorax logs (lsedlar)
- lorax-wrapper: Put all log files into compose logs (lsedlar)
- pungi: Fix reading multilib config files (lsedlar)
- pungi: Fulltree should not apply for input multilib package (lsedlar)
- pungi: Add tests for depsolving (lsedlar)
- Update ostree phase documentation (lsedlar)
- [ostree] Allow adding versioning metadata (qwan)
  (lubomir.sedlar)
- [ostree] New option to enable generating ostree summary file (qwan)
- pungi: Avoid removing from list (lsedlar)
- pungi: Allow globs in %%multilib-whitelist (dmach)
- pungi: Exclude RPMs that are in lookaside (dmach)
- pungi: Fix excluding SRPMs (dmach)
- pungi: Speed up blacklist processing (dmach)
- Update tests to use ostree write-commit-id (puiterwijk)
- ostree: Use the write-commitid-to feature rather than parsing ostree logs
  (puiterwijk)
- checks: Check for createrepo_c (lsedlar)
- checks: Update tests to not require python modules (lsedlar)
- Remove executable permissions on test scripts (puiterwijk)
- Add more require checks (puiterwijk)
- Fix package name for createrepo and mergerepo (puiterwijk)
- not using 'git -C path' which is not supported by git 1.x (qwan)
- pungi-koji: add option for not creating latest symbol link (qwan)
- Replace mount/umount with guestfsmount and 'fusermount -u' (qwan)
- config: Don't abort on deprecated options (lsedlar)
- metadata: Treeinfo should point to packages and repo (lsedlar)
- Send notification when compose fails to start (lsedlar)
- metadata: Stop crashing for non-bootable products (lsedlar)
- createiso: Do not split bootable media (lsedlar)
- doc: Fix a typo in progress notification example (lsedlar)
- Dump images.json after checksumming (lsedlar)
- metadata: Correctly clone buildinstall .treeinfo (lsedlar)
- createiso: Include layered product name in iso name (lsedlar)
- buildinstall: Only transform arch for lorax (lsedlar)
- iso-wrapper: Remove the class (lsedlar)
- config: Validate variant regular expressions (lsedlar)

* Sat Oct 08 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.10-1
- pungi: Replace kickstart repo url (mark)
- ostree-installer: Reduce duplication in tests (lsedlar)
- ostree-installer: Generate correct volume ID (lsedlar)
- ostree-installer: Use ostree as type in filename (lsedlar)
- ostree: Use $basearch in repo file (lsedlar)
- config: Accept empty branch in SCM dict (lsedlar)
- Remove duplicated version from pungi script (lsedlar)
- use --new-chroot when making ostree's (dennis)
- Create git tags without release (lsedlar)
- Translate paths without double slash (lsedlar)
- Remove shebangs from non-executable files (lsedlar)
- Remove FSF address from comments (lsedlar)
- Update contributing guide (lsedlar)
- init: Remove keep_original_comps option (lsedlar)
- tests: Use unittest2 consistently (lsedlar)

* Wed Sep 21 2016 Lubomír Sedlář <lsedlar@redhat.com> - 4.1.9-1
- ostree_installer: Add --isfinal lorax argument (lsedlar)
- Recreate JSON dump of configuration (lsedlar)
- Merge #385 `Test and clean up pungi.linker` (dennis)
- Merge #390 `checksums: Never skip checksumming phase` (dennis)
- variants: Allow multiple explicit optional variants (lsedlar)
- checksums: Never skip checksumming phase (lsedlar)
- [linker] Remove dead code (lsedlar)
- [linker] Add tests (lsedlar)
- Dump original pungi conf (cqi)
- ostree: Add tests for sending ostree messages (lsedlar)
- Send fedmsg message on ostree compose finishg (puiterwijk)
- createrepo: Add option to use xz compression (lsedlar)
- Allow user to set a ~/.pungirc for some defaults (riehecky)
- metadata: Improve error reporting on failed checksum (lsedlar)
- extra-files: Write a metadata file enumerating extra files (jeremy)
- Merge #381 `Automatically generate missing image version` (dennis)
- Automatically generate missing image version (lsedlar)
- Add JSON Schema for configuration (lsedlar)
- Allow arbitrary arguments in make test (lsedlar)
- createiso: Report nice error when tag does not exist (lsedlar)
- Fix test data build script (lsedlar)
- [osbs] Add NVRA of created image into main log (lsedlar)
- [createiso] Remove unused script (lsedlar)
- Update doc about generating release value (lsedlar)
- Use label to populate image release (lsedlar)
- doc: Fix example for image_build (lsedlar)
- Ignore module imports not at top of file (lsedlar)
- Merge #367 `Remove unused imports` (dennis)
- [buildinstall] Fix cleaning output dir (lsedlar)
- Remove unused imports (lsedlar)
- Merge #360 `[osbs] Convert build_id to int` (dennis)
- Merge #361 `Fix config validation script` (dennis)
- Merge #365 `Make image test at end of compose less strict` (dennis)
- [test] Make image test at end of compose less strict (lsedlar)
- [iso] Fix check on failable ISO (lsedlar)
- Add full Pungi version to log output (lsedlar)
- Fix config validation script (lsedlar)
- [osbs] Convert build_id to int (lsedlar)
- [image-build] Get failable config from correct place (lsedlar)

* Wed Aug 10 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.8-1
- [createiso] Use shell script for runroot (lsedlar)
- Merge #357 `Improve error messages for gathering packages` (dennis)
- [test] Only check bootability for images on x86_64 and i386 (lsedlar)
- Improve error messages for gathering packages (lsedlar)
- Merge #339 `Refactor failables, step 1` (dennis)
- Refactor failables (lsedlar)
- Stop setting release in OSBS phase (lsedlar)
- Merge #351 `Remove ambiguous imports` (dennis)
- [test] Correctly check bootable ISOs (lsedlar)
- Remove ambiguous imports (lsedlar)
- Merge #347 `Remove duplicate definition of find_old_composes.`
  (lubomir.sedlar)
- Merge #342 `Simplify naming format placeholders` (dennis)
- Merge #345 `createrepo: use separate logs for different pkg_type` (dennis)
- Remove duplicate definition of find_old_composes... (rbean)
- [createrepo] fix 'createrepo_deltas' option (qwan)
- createrepo: use separate logs for different pkg_type (lsedlar)
- Simplify naming format placeholders (lsedlar)
- Treat variants without comps groups as having all of them (lsedlar)
- Always generate rpms.json file (lsedlar)

* Thu Jun 23 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.7-1
- [scm] Add logging for exporting local files (lsedlar)
- [extra-files] Only copy files when there is a config (lsedlar)
- [extra-files] Refactoring (lsedlar)
- [extra-files] Skip whole phase if not configured (lsedlar)
- [extra-files] Copy files using existing function (lsedlar)
- [extra-files] Add tests (lsedlar)
- [osbs] Add a phase to build images in OSBS (lsedlar)
- Setup global log file before logging anything (lsedlar)
- [metadata] Correctly save final flag (lsedlar)
- Merge #326 `add missing dependencies` (dennis)
- [createiso] Add test for adding source iso to metadata (lsedlar)
- Merge #325 `Fix checking optional ISO images in test phase` (dennis)
- Merge #321 `Add support for top-level variant IDs with dashes.` (dennis)
- Merge #320 `images.json: Move src images under binary arches.` (dennis)
- add missing dependencies (nils)
- Fix checking optional ISO images in test phase (lsedlar)
- add lxml dependency (nils)
- images.json: Move src images under binary arches. (dmach)
- Add support for top-level variant IDs with dashes. (dmach)
- Fix PYTHONPATH usage in test_compose.sh. (dmach)
- [createiso] Enable customizing media reserve (lsedlar)
- [createiso] Add test for splitting media (lsedlar)
- [media-split] Remove commented-out code (lsedlar)
- [media-split] Simplify code (lsedlar)
- [media-split] Add code documentation (lsedlar)
- [media-split] Add unit tests (lsedlar)
- Add missing documentation (lsedlar)
- [buildinstall] Fix bad error message (lsedlar)
- Merge #309 `Add compatibility for Python 2.6` (dennis)
- Merge #293 `Add tests for generating discinfo and media.repo files` (dennis)
- Merge #287 `Use koji profiles to list RPMs in buildroot` (dennis)
- [ostree-installer] Put images to os/ directory (lsedlar)
- [ostree] Rename duplicated test (lsedlar)
- [util] Use koji profile for getting RPMs from buildroot (lsedlar)
- [util] Add test for getting list of buildroot RPMs (lsedlar)
- pungi-koji: fix up latest symlink creation (dennis)
- Use unittest2 if available (lsedlar)
- Stop using str.format (lsedlar)
- Stop using functools.total_ordering (lsedlar)
- The message attribute on exception is deprecated (lsedlar)
- [ostree] Rename duplicated test (lsedlar)
- [metadata] Simplify writing media.repo (lsedlar)
- [metadata] Add test for writing media.repo (lsedlar)
- [discinfo] Use context manager for file access (lsedlar)
- [metadata] Add tests for discinfo files (lsedlar)

* Tue May 24 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.6-1
- [ostree-installer] Allow using external repos as source (lsedlar)
- [image-build] Allow using external install trees (lsedlar)
- Add type to base product for layered releases (lsedlar)
- Merge #303 `[ostree] Use unique work and log paths` (dennis)
- [ostree] Use unique work and log paths (lsedlar)
- [arch] Add mock rpmUtils module (lsedlar)

* Mon May 16 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.5-1
- [ostree] Put variant name in ostree log dir (lsedlar)
- Merge #294 `[ostree] Initialize empty repo` (dennis)
- [util] Resolve git+https URLs (lsedlar)
- [ostree] Initialize empty repo (lsedlar)
- [test] Add checks for created images (lsedlar)
- Fix caching global ksurl (lsedlar)
- include tests/fixtures in manifest (dennis)

* Fri Apr 29 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.4-1
- Merge #273 `Deduplicate configuration a bit` (dennis)
- Merge #280 `[createrepo] Use more verbose output` (dennis)
- Merge #283 `Pungi should log when it tries to publish notifications.`
  (dennis)
- [createiso] Add back running isohybrid on x86 disk images (dennis)
- [createiso] Remove chdir() (lsedlar)
- [pkgset] Fix caching RPMs (lsedlar)
- [createrepo] Use more verbose output (lsedlar)
- Pungi should log when it tries to publish notifications. (rbean)
- [pkgset] Use context manager for opening file list (lsedlar)
- [pkgset] Add tests for writing filelists (lsedlar)
- [pkgset] Simplify finding RPM in koji buildroot (lsedlar)
- [pkgset] Clean up koji package set (lsedlar)
- [pkgset] Add test for pkgset merging (lsedlar)
- [pkgset] Add tests for KojiPackageSet (lsedlar)
- [pkgset] Clean up Koji source (lsedlar)
- [pkgset] Add tests for Koji source (lsedlar)
- Add common global settings for images (lsedlar)
- Remove duplicated and dead code (lsedlar)
- [live-media] Add check for live_media_version option (lsedlar)
- [scm-wrapper] Remove unused method (lsedlar)
- [scm-wrapper] Report when file wrapper did not match anything (lsedlar)
- [scm-wrapper] Use context manager for managing temp dir (lsedlar)
- [scm-wrapper] Reduce code duplication in RPM wrapper (lsedlar)
- [scm-wrapper] Copy files directly (lsedlar)
- [scm-wrapper] Reduce code duplication (lsedlar)
- [scm-wrapper] Add tests for SCM wrappers (lsedlar)
- [ostree] Set each repo to point to current compose (lsedlar)
- [ostree-installer] Drop filename setting (lsedlar)
- Merge #269 `Improve logging of failable deliverables` (ausil)
- [ostree-installer] Fix example documentation (lsedlar)
- Improve logging of failable deliverables (lsedlar)
- [ostree-installer] Install ostree in runroot (lsedlar)
- [pkgset] Print more detailed logs when rpm is not found (lsedlar)
- [ostree-installer] Clone repo with templates (lsedlar)

* Fri Apr 08 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.3-1
- enable the compose test (dennis)
- [ostree-installer] Copy all lorax outputs (lsedlar)
- [ostree] Log to stdout as well (lsedlar)
- [ostree-installer] Use separate directory for logs (lsedlar)
- Merge #260 `Maybe fix ostree?` (ausil)
- [ostree-installer] Put lorax output into work dir (lsedlar)
- [ostree] Add test check for modified repo baseurl (lsedlar)
- [ostree] Move cloning repo back to compose box (lsedlar)
- [ostree] Mount ostree directory in koji (lsedlar)

* Tue Apr 05 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.2-1
- Merge #257 `[ostree] Enable marking ostree phase as failable` (ausil)
- [ostree] Enable marking ostree phase as failable (lsedlar)
- [koji-wrapper] Initialize wrappers sequentially (lsedlar)
- [createiso] Simplify code, test phase (lsedlar)
- [createiso] Move runroot work to separate script (lsedlar)
- [ostree] Use explicit work directory (lsedlar)
- [ostree] Rename atomic to ostree (lsedlar)
- [ostree] Move cloning config repo to chroot (lsedlar)
- [ostree] Fix call to kobo.shortcuts.run (lsedlar)
- [atomic] Stop creating the os directory (lsedlar)
- [checksum] Add arch to file name (lsedlar)

* Fri Apr 01 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.1-1
- install scripts (dennis)
- Merge #242 `Fix wrong file permissions` (ausil)
- Add a utility to validate config (lsedlar)
- [variants] Stop printing stuff to stderr unconditionally (lsedlar)
- Fix atomic/ostree config validations (lsedlar)
- [pungi-wrapper] Remove duplicated code (lsedlar)
- [checks] Add a check for too restrictive umask (lsedlar)
- [util] Remove umask manipulation from makedirs (lsedlar)
- Merge #240 `Filter variants and architectures` (ausil)
- Filter variants and architectures (lsedlar)
- Refactor checking for failable deliverables (lsedlar)
- [buildinstall] Do not crash on failure (lsedlar)
- Reuse helper in all tests (lsedlar)
- [atomic] Add atomic_installer phase (lsedlar)
- [ostree] Add ostree phase (lsedlar)
- [atomic] Add a script to create ostree repo (lsedlar)
- Merge #232 `Improve logging by adding subvariants` (ausil)
- Add compose type to release for images (lsedlar)
- [image-build] Add traceback on failure (lsedlar)
- [image-build] Use subvariants in logging output (lsedlar)
- [live-media] Use subvariants in logging (lsedlar)
- Add tracebacks to all failable phases (lsedlar)
- ppc no longer needs magic bits in the iso (pbrobinson)
- [buildinstall] Add more debugging output (lsedlar)
- [metadata] Stop crashing on empty path from .treeinfo (lsedlar)
- [checksums] Add label to file name (lsedlar)
- [buildinstall] Use customized dvd disc type (lsedlar)
- image_build: fix subvariant handling (awilliam)

* Tue Feb 23 2016 Dennis Gilmore <dennis@ausil.us> - 4.1.0-1
- repoint master at 4.1.x and new feature development

* Tue Feb 23 2016 Dennis Gilmore <dennis@ausil.us> - 4.0.5-1
- [tests] Fix wrong checks in buildinstall tests (lsedlar)
- [tests] Use temporary files for buildinstall (lsedlar)
- [tests] Do not mock open for koji wrapper tests (lsedlar)
- Merge #179 `Update makefile targets for testing` (ausil)
- Update makefile targets for testing (lsedlar)
- [live-images] Set type to raw-xz for appliances (lsedlar)
- [live-images] Correctly create format (lsedlar)
- [tests] Dummy compose is no longer private (lsedlar)
- [tests] Move buildinstall tests to new infrastructure (lsedlar)
- [tests] Use real paths module in testing (lsedlar)
- [tests] Move dummy testing compose into separate module (lsedlar)
- [live-images] Create image dir if needed (lsedlar)
- [live-images] Add images to manifest (lsedlar)
- [live-images] Fix path processing (lsedlar)
- [live-images] Move repo calculation to separate method (lsedlar)
- [koji-wrapper] Fix getting results from spin-appliance (lsedlar)
- [live-images] Filter non-image results (lsedlar)
- [live-images] Rename repos_from to repo_from (lsedlar)
- [koji-wrapper] Add test for passing release to image-build (lsedlar)
- [live-images] Automatically populate release with date and respin (lsedlar)
- [live-media] Respect release set in configuration (lsedlar)
- [live-images] Build all images specified in config (lsedlar)
- [live-media] Don't create $basedir arch (lsedlar)
- Update tests (lsedlar)
- do not ad to image build and live tasks the variant if it is empty (dennis)
- when a variant is empty do not add it to the repolist for livemedia (dennis)
- [live-media] Update tests to use $basearch (lsedlar)
- [buildinstall] Don't run lorax for empty variants (lsedlar)
- Merge #159 `use $basearch not $arch in livemedia tasks` (lubomir.sedlar)
- Merge #158 `do not uses pipes.quotes in livemedia tasks` (lubomir.sedlar)
- Add documentation for signing support that was added by previous commit
  (tmlcoch)
- Support signing of rpm wrapped live images (tmlcoch)
- Fix terminology - Koji uses sigkey not level (tmlcoch)
- use $basearch not $arch in livemedia tasks (dennis)
- do not uses pipes.quotes in livemedia tasks (dennis)
- [live-images] Don't tweak kickstarts (lsedlar)
- Allow specifying empty variants (lsedlar)
- [createrepo] Remove dead assignments (lsedlar)
- Keep empty query string in resolved git url (lsedlar)
- [image-build] Use dashes as arch separator in log (lsedlar)
- [buildinstall] Stop parsing task_id (lsedlar)
- [koji-wrapper] Get task id from failed runroot (lsedlar)
- [live-media] Pass ksurl to koji (lsedlar)
- Merge #146 `[live-media] Properly calculate iso dir` (ausil)
- [live-media] Properly calculate iso dir (lsedlar)
- [image-build] Fix tests (lsedlar)
- add image-build sections (lkocman)
- [koji-wrapper] Add tests for get_create_image_cmd (lsedlar)
- [live-images] Add support for spin-appliance (lsedlar)
- [live-media] Koji option is ksfile, not kickstart (lsedlar)
- [live-media] Use install tree from another variant (lsedlar)
- [live-media] Put images into iso dir (lsedlar)
- [image-build] Koji expects arches as a comma separated string (lsedlar)
- Merge #139 `Log more details when any deliverable fails` (ausil)
- [live-media] Version is required argument (lsedlar)
- [koji-wrapper] Only parse output on success (lsedlar)
- [koji-wrapper] Add tests for runroot wrapper (lsedlar)
- [buildinstall] Improve logging (lsedlar)
- Log more details about failed deliverable (lsedlar)
- [image-build] Fix failable tests (lsedlar)
- Merge #135 `Add live media support` (ausil)
- Merge #133 `media_split: add logger support. Helps with debugging space
  issues on dvd media` (ausil)
- [live-media] Add live media phase (lsedlar)
- [koji-wrapper] Add support for spin-livemedia (lsedlar)
- [koji-wrapper] Use more descriptive method names (lsedlar)
- [image-build] Remove dead code (lsedlar)
- media_split: add logger support. Helps with debugging space issues on dvd
  media (lkocman)
- [image-build] Allow running image build scratch tasks (lsedlar)
- [image-build] Allow dynamic release for images (lsedlar)

* Wed Jan 20 2016 Dennis Gilmore <dennis@ausil.us> - 4.0.4-1
- 4.0.4 release (dennis)
- Merge #123 `Live images: add repo from another variant` (ausil)
- Merge #125 `[image-build] Stop creating wrong arch dirs` (ausil)
- Toggle multilib per variant (lsedlar)
- [live-images] Code cleanup (lsedlar)
- [live-images] Add documentation (lsedlar)
- [live-images] Add repos from other variants (lsedlar)
- [image-build] Stop creating wrong arch dirs (lsedlar)
- Enable identifying variants in exception traces (lsedlar)
- Store which deliverables failed (lsedlar)
- scm.py: use git clone instead git archive for http(s):// (lkocman)
- Fix filtering of system release packages (lsedlar)
- Merge #114 `Use install tree/repo from another variant for image build`
  (ausil)
- Make system release package filtering optional (lsedlar)
- [image-build] Optionally do not break whole compose (lsedlar)
- [image-build] Refactoring (lsedlar)
- [image-build] Use repo from another variant (lsedlar)
- [image-build] Take install tree from another variant (lsedlar)
- Add missing formats to volumeid and image name (lsedlar)
- [image-build] Use single koji task per variant (lsedlar)
- Fix image-build modifying config (lsedlar)
- Fix missing checksums in .treeinfo (lsedlar)
- Don't crash on generating volid without variant (lsedlar)
- Merge #99 `Add option to specify non-failing stuff` (ausil)
- Add repo from current compose (lsedlar)
- Fix getting compose topdir in CreateImage build thread (lsedlar)
- Add option to specify non-failing stuff (lsedlar)
- Allow customizing image name and volume id (lsedlar)
- Fix notifier tests (lsedlar)
- Publish a url instead of a file path. (rbean)
- Add 'topdir' to all fedmsg/notifier messages. (rbean)
- Merge #75 `Start of development guide` (ausil)
- Merge #88 `Resolve HEAD in ksurl to actual hash` (ausil)
- Merge #87 `Add support for customizing lorax options` (ausil)
- Update fedmsg notification hook to use appropriate config. (rbean)
- we need to ensure that we send all the tasks to koji on the correct arch
  (dennis)
- Resolve HEAD in ksurl to actual hash (lsedlar)
- Add support for customizing lorax options (lsedlar)
- Run lorax in separate dirs for each variant (lsedlar)
- Merge #84 `Allow specifying --installpkgs for lorax` (ausil)
- Merge #83 `Fix recently discovered bugs` (ausil)
- Merge #82 `indentation fixs correcting dvd creation` (ausil)
- Merge #69 `Move messaging into cli options and simplify it` (ausil)
- Start lorax for each variant separately (lsedlar)
- Update lorax wrapper to use --installpkgs (lsedlar)
- Allow specifying which packages to install in variants xml (lsedlar)
- Add basic tests for buildinstall phase (lsedlar)
- Fix generating checksum files (lsedlar)
- Use lowercase hashed directories (lsedlar)
- indentation fixs correcting dvd creation (dennis)
- remove glibc32 from the runroot tasks (dennis)
- fix up the pungi-fedmesg-notification script name (dennis)
- Add overview of Pungi to documentation (lsedlar)
- Move messaging into cli options (lsedlar)
- Extend contributing guide (lsedlar)
- Load multilib configuration from local dir in development (lsedlar)
- Allow running scripts with any python in PATH (lsedlar)

* Tue Sep 08 2015 Dennis Gilmore <dennis@ausil.us> - 4.0.3-1
- Merge #54 `fix log_info for image_build (fails if image_build is skipped)`
  (lkocman)
- image_build: self.log_info -> self.compose.log_info (lkocman)
- Revert "Added params needed for Atomic compose to LoraxWrapper" (dennis)
- Revert "fix up if/elif in _handle_optional_arg_type" (dennis)
- Add image-build support (lkocman)
- Add translate path support. Useful for passing pungi repos to image-build
  (lkocman)
- import duplicate import of errno from buildinstall (lkocman)
- handle openning missing images.json (image-less compose re-run) (lkocman)
- compose: Add compose_label_major_version(). (lkocman)
- pungi-koji: Don't print traceback if error occurred. (pbabinca)
- More detailed message for unsigned rpms. (tkopecek)
- New config option: product_type (default is 'ga'); Set to 'updates' for
  updates composes. (dmach)
- kojiwrapper: Add get_signed_wrapped_rpms_paths() and get_build_nvrs()
  methods. (tmlcoch)
- live_images: Copy built wrapped rpms from koji into compose. (tmlcoch)
- kojiwrapper: Add get_wrapped_rpm_path() function. (tmlcoch)
- live_images: Allow custom name prefix for live ISOs. (tmlcoch)
- Do not require enabled runroot option for live_images phase. (tmlcoch)
- Support for rpm wrapped live images. (tmlcoch)
- Remove redundant line in variants wrapper. (tmlcoch)
- Merge #36 `Add params needed for Atomic compose to LoraxWrapper` (admiller)
- live_images: replace hardcoded path substition with translate_path() call
  (lkocman)
- live_images fix reference from koji to koji_wrapper (lkocman)
- fix up if/elif in _handle_optional_arg_type (admiller)
- Added params needed for Atomic compose to LoraxWrapper (admiller)
- Merge #24 `Fix empty repodata when hash directories were enabled. ` (dmach)
- createrepo: Fix empty repodata when hash directories were enabled. (dmach)

* Fri Jul 24 2015 Dennis Gilmore <dennis@ausil.us> - 4.0.2-1
- Merge #23 `fix treeinfo checksums` (dmach)
- Fix treeinfo checksums. (dmach)
- add basic setup for making arm iso's (dennis)
- gather: Implement hashed directories. (dmach)
- createiso: Add createiso_skip options to skip createiso on any variant/arch.
  (dmach)
- Fix buildinstall for armhfp. (dmach)
- Fix and document productimg phase. (dmach)
- Add armhfp arch tests. (dmach)
- Document configuration options. (dmach)
- Add dependency of 'runroot' config option on 'koji_profile'. (dmach)
- Rename product_* to release_*. (dmach)
- Implement koji profiles. (dmach)
- Drop repoclosure-%%arch tests. (dmach)
- Config option create_optional_isos now defaults to False. (dmach)
- Change createrepo config options defaults. (dmach)
- Rewrite documentation to Sphinx. (dmach)
- Fix test data, improve Makefile. (dmach)
- Update GPL to latest version from https://www.gnu.org/licenses/gpl-2.0.txt
  (dmach)

* Thu Jun 11 2015 Dennis Gilmore <dennis@ausil.us> - 4.0.1-1
- wrap check for selinux enforcing in a try except (dennis)
- pull in gather.py patches from dmach for test compose (admiller)
- Add some basic testing, dummy rpm creation, and a testing README (admiller)
- pungi-koji: use logger instead of print when it's available (lkocman)
- fix incorrect reference to variable 'product_is_layered' (lkocman)
- pungi-koji: fix bad module path to verify_label() (lkocman)
- update the package Requires to ensure we have everything installed to run
  pungi-koji (dennis)
- update the package to be installed for productmd to python-productmd (dennis)

* Sun Jun 07 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.9
- update docs now devel-4-pungi is merged to master, minor spelling fixes
  (pbrobinson)
- Fix remaining productmd issues. (dmach)
- Revert "refactor metadata.py to use productmd's compose.dump for composeinfo"
  (dmach)
- Fix LoraxTreeInfo class inheritance. (dmach)
- Fix pungi -> pungi_wrapper namespace issue. (dmach)
- fix arg order for checksums.add (admiller)
- update for productmd checksums.add to TreeInfo (admiller)
- fix product -> release namespace change for productmd (admiller)
- update arch manifest.add config order for productmd api call (admiller)
- update for new productmd named args to rpms (admiller)
- fix pungi vs pungi_wrapper namespacing in method_deps.py (admiller)
- add createrepo_c Requires to pungi.spec (admiller)
- add comps_filter (admiller)
- refactor metadata.py to use productmd's compose.dump for composeinfo instead
  of pungi compose_to_composeinfo (admiller)
- Update compose, phases{buildinstall,createiso,gather/__ini__} to use correct
  productmd API calls (admiller)
- Use libselinux-python instead of subprocess (lmacken)
- Add README for contributors (admiller)

* Wed May 20 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.8
- fix up bad += from early test of implementing different iso labels based on
  if there is a variant or not (dennis)

* Wed May 20 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.7
- make sure we treat the isfinal option as a boolean when fetching it (dennis)
- if there is a variant use it in the volume id and shorten it. this will make
  each producst install tree have different volume ids for their isos (dennis)
- fix up productmd import in the executable (dennis)
- fixup productmd imports for changes with open sourcing (dennis)
- tell the scm wrapper to do an absolute import otherwise we hit a circular dep
  issue and things go wonky (dennis)
- include the dtd files in /usr/share/pungi (dennis)
- add missing ) causing a syntax error (dennis)
- fix up the productmd imports to import the function from the common module
  (dennis)
- fix up typo in getting arch for the lorax log file (dennis)

* Sat Mar 14 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.6.20150314.gitd337c34
- update the git snapshot to pick up some fixes

* Fri Mar 13 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.5.git18d4d2e
- update Requires for rename of python-productmd

* Thu Mar 12 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.4.git18d4d2e
- fix up the pungi logging by putting the arch in the log file name (dennis)
- change pypungi imports to pungi (dennis)
- spec file cleanups (dennis)

* Thu Mar 12 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.3.gita3158ec
- rename binaries (dennis)
- Add the option to pass a custom path for the multilib config files (bcl)
- Call lorax as a process not a library (bcl)
- Close child fds when using subprocess (bcl)
- fixup setup.py and MANIFEST.in to make a useable tarball (dennis)
- switch to BSD style hashes for the iso checksums (dennis)
- refactor to get better data into .treeinfo (dennis)
- Initial code merge for Pungi 4.0. (dmach)
- Initial changes for Pungi 4.0. (dmach)
- Add --nomacboot option (csieh)

* Thu Mar 12 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.2.git320724e
- update git snapshot to switch to executing lorax since it is using dnf

* Thu Mar 12 2015 Dennis Gilmore <dennis@ausil.us> - 4.0-0.1.git64b6c80
- update to the pungi 4.0 dev branch

