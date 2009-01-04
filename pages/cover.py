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

import pages.joke


class Cover(Page):
  
  def __init__(self, jokebook):
    Page.__init__(self)

    # title
    self.append(hippo.CanvasText(text='"' + jokebook.title + '" ' + _('started by') + ' ' + jokebook.owner,
                                 xalign=hippo.ALIGNMENT_CENTER,
                                 padding_top=10))
    self.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL))      

    # cover picture 
    cover_picture = self.make_imagebox(jokebook, 'image', 480, 360, False)    
    self.append(cover_picture, hippo.PACK_EXPAND)
    self.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL))
    
    # open button 
    button = gtk.Button(_('Open'))
    button.connect('clicked', self.__do_clicked_open, jokebook)
    button.set_size_request(50, -1)
    self.append(hippo.CanvasWidget(widget=theme.theme_widget(button),
                                   box_width=50))

  
  def __do_clicked_open(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.joke.Joke, jokebook)
 
 
 
