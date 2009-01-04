# Copyright 2007 World Wide Workshop Foundation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# If you find this activity useful or end up using parts of it in one of your
# own creations we would love to hear from you at info@WorldWideWorkshop.org !
#

import gtk
import hippo

from sugar.graphics import style

from gui import theme
from gui import page


# TODO- height seems bust
class CanvasListBox(hippo.CanvasWidget):
  def __init__(self):
    self._entries_div = hippo.CanvasBox() 

    # props not set properly in constructor
    self._entries_div.props.background_color=theme.COLOR_PAGE.get_int() 
    self._entries_div.props.spacing=style.DEFAULT_SPACING    
    self._entries_div.props.padding=10
    self._entries_div.props.orientation=hippo.ORIENTATION_VERTICAL    

    # Munge it all up into something we can stick into a gtk.ScrolledWindow
    canvas = hippo.Canvas() 
    canvas.set_root(self._entries_div)
    canvas.show()
    
    hbox = gtk.HBox()
    hbox.set_flags(gtk.HAS_FOCUS | gtk.CAN_FOCUS)
    hbox.pack_start(canvas)
    hbox.show()

    scroller = gtk.ScrolledWindow()
    scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    viewport = gtk.Viewport()
    viewport.set_shadow_type(gtk.SHADOW_NONE) 
    viewport.add(hbox)
    viewport.show()
    scroller.add(viewport)
    scroller.show()

    hippo.CanvasWidget.__init__(self, 
                                widget=scroller, 
                                padding=0, 
                                spacing=0,
                                border=1,
                                border_color=theme.COLOR_DARK_GREEN.get_int())


  def append(self, entry, *args):
    self._entries_div.append(entry, *args)

