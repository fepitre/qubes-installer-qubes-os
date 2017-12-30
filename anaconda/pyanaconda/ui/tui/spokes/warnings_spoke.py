# Ask vnc text spoke
#
# Copyright (C) 2013  Red Hat, Inc.
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

from pyanaconda.ui.tui.spokes import StandaloneTUISpoke
from pyanaconda.ui.tui.simpleline import TextWidget
from pyanaconda.ui.tui.hubs.summary import SummaryHub
from pyanaconda.i18n import N_, _

from pyanaconda.iutil import is_unsupported_hw
from pyanaconda.product import productName

import logging
log = logging.getLogger("anaconda")

__all__ = ["WarningsSpoke"]

class WarningsSpoke(StandaloneTUISpoke):
    """
       .. inheritance-diagram:: WarningsSpoke
          :parts: 3
    """
    title = N_("Warnings")

    preForHub = SummaryHub
    priority = 0

    def __init__(self, *args, **kwargs):
        StandaloneTUISpoke.__init__(self, *args, **kwargs)

        self._message = _("This hardware lack features required by Qubes OS. "
                          "Missing features: %(features)s. "
                          "For more information on supported hardware, "
                          "please refer to https://www.qubes-os.org/system-requirements/")
        # Does anything need to be displayed?
        # pylint: disable=no-member
        #   self._unsupported = not self.data.unsupportedhardware.unsupported_hardware \
        #                       and is_unsupported_hw()
        self._unsupported = is_unsupported_hw()

    @property
    def completed(self):
        return not self._unsupported

    def refresh(self, args=None):
        StandaloneTUISpoke.refresh(self, args)

        self._window += [TextWidget(self._message % {'features': self._unsupported}), ""]

        return True

    # Override Spoke.apply
    def apply(self):
        pass
