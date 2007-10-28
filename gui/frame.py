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

import gobject
import gtk
import hippo
import logging

from i18n import LanguageComboBox
from gettext import gettext as _

from globals import Globals

from util.decorators import Property
from gui import theme

import pages.choose
import pages.edit

from persistence.jokebook import Jokebook

class Frame(hippo.Canvas):
  
  def __init__(self):
    hippo.Canvas.__init__(self)
    
    # Root Frame ###############################################################
    # Holds: Everything
    self.__root = hippo.CanvasBox(
      orientation=hippo.ORIENTATION_VERTICAL)
    self.set_root(self.__root)
    
    # Application Header #######################################################
    # Holds: App logo, language box, lessons plan box    
    self.__header = self.__make_header()
    self.__root.append(self.__header)    
    
    # Page Container ###########################################################
    # Holds: The currently open UI page
    self.__container = hippo.CanvasBox(
      border=theme.BORDER_WIDTH,
      border_color=theme.COLOR_FRAME.get_int(),
      background_color=theme.COLOR_BACKGROUND.get_int(),
      spacing=4,
      padding_top=20, 
      padding_left=40, 
      padding_right=40,
      padding_bottom=20,
      orientation=hippo.ORIENTATION_VERTICAL)
    self.__root.append(self.__container, hippo.PACK_EXPAND)
    
    self.__page = hippo.CanvasBox(
      box_height=theme.PAGE_HEIGHT,  # TODO -> Pull width/height from theme - and make sure all
                       #         children pull their sizes relative to this box
      background_color=theme.COLOR_PAGE.get_int(),
      border=4,
      border_color=theme.COLOR_PAGE_BORDER.get_int(), 
      spacing=8,      
      padding=20,
      xalign=hippo.ALIGNMENT_CENTER,
      orientation=hippo.ORIENTATION_VERTICAL)
    self.__container.append(self.__page)
    
    self.__page_class = None
    
    # Application Footer #######################################################
    # Holds: Task buttons
    self.__footer = self.__make_footer()
    self.__container.append(self.__footer)



  def __make_header(self):
    ret = hippo.CanvasBox(
      orientation=hippo.ORIENTATION_HORIZONTAL)
    
    # logo
    logo = gtk.Image()
    logo.set_from_file(Globals.logo)
    ret.append(hippo.CanvasWidget(widget=logo))
    
    # language selection box
    language =  hippo.CanvasWidget(
      background_color=theme.COLOR_BACKGROUND.get_int(),
      border_top=theme.BORDER_WIDTH,
      border_left=theme.BORDER_WIDTH,
      border_color=theme.COLOR_FRAME.get_int(),
      padding_top=12, 
      padding_bottom=12,
      padding_left=100, 
      padding_right=100,
      yalign=hippo.ALIGNMENT_CENTER,
      orientation=hippo.ORIENTATION_VERTICAL)
    button = LanguageComboBox()
    button.install()
    language.props.widget = button 
    button.set_name('Fubar')
    ret.append(language, hippo.PACK_EXPAND)
    
    # lesson plans
    lesson_plans =  hippo.CanvasWidget(
      background_color=theme.COLOR_BACKGROUND.get_int(),
      border_top=theme.BORDER_WIDTH,
      border_left=theme.BORDER_WIDTH, 
      border_right=theme.BORDER_WIDTH, 
      border_color=theme.COLOR_FRAME.get_int(),
      padding_top=12, 
      padding_bottom=12,
      padding_left=30, 
      padding_right=30,
      yalign=hippo.ALIGNMENT_CENTER,
      orientation=hippo.ORIENTATION_VERTICAL)
    button = gtk.Button(_('Lesson Plans'))
    lesson_plans.props.widget = theme.theme_widget(button)
    ret.append(lesson_plans, hippo.PACK_EXPAND)
    
    return ret
  
  
  
  def __make_footer(self):
    ret = hippo.CanvasBox(
      padding_right=8,
      padding_top=8,
      padding_bottom=0,
      spacing=8,
      orientation=hippo.ORIENTATION_HORIZONTAL)
    button = gtk.Button(_('Read Jokebooks'))
    button.connect('clicked', self.__do_clicked_read)
    self.__button_read = hippo.CanvasWidget(widget=theme.theme_widget(button))
    ret.append(self.__button_read)
    button = gtk.Button(_('Make Jokebook'))
    button.connect('clicked', self.__do_clicked_make)
    self.__button_make = hippo.CanvasWidget(widget=theme.theme_widget(button))
    ret.append(self.__button_make)
    return ret
 

  
  @property
  def page_class(self):
    if self.__page_class is None:
      # say, for e.g. we're connecting to another activity and we haven't set a
      # default page yet
      self.__page_class = pages.choose.Choose
    return self.__page_class
 
 
  @Property
  def page(): 
    def get(self): return self.__page
    def set(self, value): 
      self.__page_class = type(value)
      self.__page.clear()
      self.__page.append(value)

      # some rules for the buttons in the footer
      if not Globals.JokeMachineActivity.is_initiator \
         and type(value) is pages.choose.Choose:
        self.__button_read.set_visible(False)
        self.__button_make.set_visible(False)      
      elif not Globals.JokeMachineActivity.is_initiator:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)      
      elif type(value) is pages.choose.Choose:
        self.__button_read.set_visible(False)
        self.__button_make.set_visible(True)
      elif type(value) is pages.edit.Edit:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)
      elif type(value) is pages.preview.Preview:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)
      else:
        self.__button_read.set_visible(True)
        self.__button_make.set_visible(False)



  def __do_clicked_read(self, button):
    Globals.JokeMachineActivity.set_page(pages.choose.Choose)



  def __do_clicked_make(self, button):
    # create a new jokebook
    jokebook = Jokebook()
    jokebook.id = Globals.JokeMachineState.next_jokebook_id
    logging.info('Created new jokebook with id: %d' % jokebook.id)
    jokebook.owner = Globals.nickname
    Globals.JokeMachineState.jokebooks.append(jokebook)
    Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
 