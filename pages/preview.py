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
    
    preview_box = CanvasListBox(1028, theme.PREVIEW_HEIGHT) # TODO - really shouldn't be hardcoded
    for joke in jokebook.jokes:
      list_row = self.make_listrow(JokeViewer(joke, jokebook.title))
      preview_box.append(list_row)
    self.append(preview_box)
    
    self.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL))
    
    button = gtk.Button(_('Edit'))
    button.connect('clicked', self.__do_clicked_edit, jokebook)    
    self.append(hippo.CanvasWidget(widget=theme.theme_widget(button)))

  
  def __do_clicked_edit(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
 
 
 