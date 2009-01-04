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


import os
import gtk
import hippo
import pango
import logging
from gettext import gettext as _

from globals import Globals
from gui.page import Page
from gui import theme
from gui.canvaslistbox import CanvasListBox

from pages.joke import JokeViewer

import pages.edit


class Preview(Page):
  
  def __init__(self, jokebook):
    Page.__init__(self, xalign=hippo.ALIGNMENT_CENTER)
    
    preview_box = CanvasListBox()
    
    # cover
    cover = self.make_listrow()
    cover.props.orientation=hippo.ORIENTATION_VERTICAL
    cover.append(hippo.CanvasText(text='"' + jokebook.title + '" ' + _('started by') + ' ' + jokebook.owner,
                                 xalign=hippo.ALIGNMENT_CENTER,
                                 padding_top=10))
    cover.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL))      
    cover_picture = self.make_imagebox(jokebook, 'image', 480, 360, False)    
    cover.append(cover_picture)
    cover.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL))
    preview_box.append(cover)
    
    # jokes
    for joke in jokebook.jokes:
      list_row = self.make_listrow(JokeViewer(joke, jokebook.title))
      preview_box.append(list_row)
    self.append(preview_box, hippo.PACK_EXPAND)
    
    self.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL))
    
    button = gtk.Button(_('Edit'))
    button.connect('clicked', self.__do_clicked_edit, jokebook)    
    self.append(hippo.CanvasWidget(widget=theme.theme_widget(button)))

  
  def __do_clicked_edit(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
 
 
 
