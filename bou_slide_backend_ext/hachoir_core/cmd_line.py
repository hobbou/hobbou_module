from optparse import OptionGroup
from openerp.addons.bou_slide_backend_ext.hachoir_core.log import log
from openerp.addons.bou_slide_backend_ext.hachoir_core.i18n import _, getTerminalCharset
from openerp.addons.bou_slide_backend_ext.hachoir_core.tools import makePrintable
from openerp.addons.bou_slide_backend_ext.hachoir_core import config

def getHachoirOptions(parser):
    """
    Create an option group (type optparse.OptionGroup) of Hachoir
    library options.
    """
    def setLogFilename(*args):
        log.setFilename(args[2])

    common = OptionGroup(parser, _("Hachoir library"), \
        "Configure Hachoir library")
    common.add_option("--verbose", help=_("Verbose mode"),
        default=False, action="store_true")
    common.add_option("--log", help=_("Write log in a file"),
        type="string", action="callback", callback=setLogFilename)
    common.add_option("--quiet", help=_("Quiet mode (don't display warning)"),
        default=False, action="store_true")
    common.add_option("--debug", help=_("Debug mode"),
        default=False, action="store_true")
    return common

def configureHachoir(option):
    # Configure Hachoir using "option" (value from optparse)
    if option.quiet:
      config.quiet = True
    if option.verbose:
      config.verbose = True
    if option.debug:
      config.debug = True

def unicodeFilename(filename, charset=None):
    if not charset:
        charset = getTerminalCharset()
    try:
        return unicode(filename, charset)
    except UnicodeDecodeError:
        return makePrintable(filename, charset, to_unicode=True)

