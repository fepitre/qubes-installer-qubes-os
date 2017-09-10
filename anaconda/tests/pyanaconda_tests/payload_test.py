#
# Authors: Jiri Konecny <jkonecny@redhat.com>
#
## Copyright (C) 2017  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from pyanaconda.payload import dnfpayload
from blivet.size import Size
import unittest
import tempfile
import os
import hashlib
import shutil

from pyanaconda.payload.dnfpayload import RepoMDMetaHash


class PickLocation(unittest.TestCase):
    def pick_download_location_test(self):
        """Take the biggest mountpoint which can be used for download"""
        df_map = {"/mnt/sysimage/not_used" : Size("20 G"),
                  "/mnt/sysimage/home"     : Size("2 G"),
                  "/mnt/sysimage/"         : Size("5 G")}
        download_size = Size("1.5 G")
        install_size = Size("1.8 G")

        mpoint = dnfpayload._pick_mpoint(df_map, download_size, install_size, True)

        self.assertEqual(mpoint, "/mnt/sysimage/home")

    def pick_download_root_test(self):
        """Take the root for download because there are no other available mountpoints
           even when the root isn't big enough.

           This is required when user skipped the space check.
        """
        df_map = {"/mnt/sysimage/not_used" : Size("20 G"),
                  "/mnt/sysimage/home"     : Size("2 G"),
                  "/mnt/sysimage"         : Size("5 G")}
        download_size = Size("2.5 G")
        install_size = Size("3.0 G")

        mpoint = dnfpayload._pick_mpoint(df_map, download_size, install_size, True)

        self.assertEqual(mpoint, "/mnt/sysimage")

    def pick_install_location_test(self):
        """Take the root for download and install."""
        df_map = {"/mnt/sysimage/not_used" : Size("20 G"),
                  "/mnt/sysimage/home"     : Size("2 G"),
                  "/mnt/sysimage"         : Size("6 G")}
        download_size = Size("1.5 G")
        install_size = Size("3.0 G")

        mpoint = dnfpayload._pick_mpoint(df_map, download_size, install_size, False)

        self.assertEqual(mpoint, "/mnt/sysimage")

    def pick_install_location_error_test(self):
        """No suitable location is found."""
        df_map = {"/mnt/sysimage/not_used" : Size("20 G"),
                  "/mnt/sysimage/home"     : Size("1 G"),
                  "/mnt/sysimage"         : Size("4 G")}
        download_size = Size("1.5 G")
        install_size = Size("3.0 G")

        mpoint = dnfpayload._pick_mpoint(df_map, download_size, install_size, False)

        self.assertEqual(mpoint, None)


class DummyRepo(object):
    def __init__(self):
        self.id = "anaconda"
        self.baseurl = []


class DummyPayload(object):
    def __init__(self):
        class DummyMethod(object):
            def __init__(self):
                self.method = None

        class DummyData(object):
            def __init__(self):
                self.method = DummyMethod()

        self.data = DummyData()


class DNFPayloadMDCheckTests(unittest.TestCase):
    def setUp(self):
        self._content_repomd = """
Content of the repomd.xml file

or it should be. Nah it's just a test!
"""
        self._temp_dir = tempfile.mkdtemp(suffix="pyanaconda_tests")
        os.makedirs(os.path.join(self._temp_dir, "repodata"))
        self._md_file = os.path.join(self._temp_dir, "repodata", "repomd.xml")
        with open(self._md_file, 'w') as f:
            f.write(self._content_repomd)
        self._dummyRepo = DummyRepo()
        self._dummyRepo.baseurl = ["file://" + self._temp_dir]

    def tearDown(self):
        # remove the testing directory
        shutil.rmtree(self._temp_dir)

    def download_file_repomd_test(self):
        """Test if we can download repomd.xml with file:// successfully."""
        m = hashlib.md5()
        m.update(self._content_repomd.encode('ascii', 'backslashreplace'))
        reference_digest = m.digest()

        r = RepoMDMetaHash(DummyPayload(), self._dummyRepo)
        r.store_repoMD_hash()

        self.assertEqual(r.repoMD_hash, reference_digest)

    def verify_repo_test(self):
        """Test verification method."""
        r = RepoMDMetaHash(DummyPayload(), self._dummyRepo)
        r.store_repoMD_hash()

        # test if repomd comparision works properly
        self.assertTrue(r.verify_repoMD())

        # test if repomd change will be detected
        with open(self._md_file, 'a') as f:
            f.write("This should not be here!")
        self.assertFalse(r.verify_repoMD())

        # test correct behavior when the repo file won't be available
        os.remove(self._md_file)
        self.assertFalse(r.verify_repoMD())
