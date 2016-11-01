from openerp.addons.bou_slide_backend_ext.hachoir_metadata.version import VERSION as __version__
from openerp.addons.bou_slide_backend_ext.hachoir_metadata.metadata import extractMetadata

# Just import the module,
# each module use registerExtractor() method
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import archive
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import audio
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import file_system
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import image
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import jpeg
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import misc
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import program
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import riff
from openerp.addons.bou_slide_backend_ext.hachoir_metadata import video

