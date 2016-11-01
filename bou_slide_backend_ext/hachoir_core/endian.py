"""
Constant values about endian.
"""

from openerp.addons.bou_slide_backend_ext.hachoir_core.i18n import _

BIG_ENDIAN = "ABCD"
LITTLE_ENDIAN = "DCBA"
MIDDLE_ENDIAN = "BADC"
NETWORK_ENDIAN = BIG_ENDIAN

endian_name = {
    BIG_ENDIAN: _("Big endian"),
    LITTLE_ENDIAN: _("Little endian"),
    MIDDLE_ENDIAN: _("Middle endian"),
}
