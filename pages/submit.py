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

from persistence.joke import Joke

import pages.joke
import pages.choose


class JokeEditor(Page):
  
  def __init__(self, joke):
    Page.__init__(self, 
                  spacing=8,
                  padding=4,
                  border_color=theme.COLOR_RED.get_int(),
                  border=0,
                  xalign=hippo.ALIGNMENT_START,
                  orientation=hippo.ORIENTATION_HORIZONTAL)
    
     # left column 
    self.left = hippo.CanvasBox(border=0,
                                border_color=theme.COLOR_RED.get_int(),
                                box_width=450,
                                xalign=hippo.ALIGNMENT_START,
                                orientation=hippo.ORIENTATION_VERTICAL,
                                padding=theme.BORDER_WIDTH_CONTROL/2)
    joke_image = self.make_imagebox(joke, 'image', 320, 240, True)
    self.left.append(joke_image)
    
    # right column 
    self.right = hippo.CanvasBox(border=0,
                                 border_color=theme.COLOR_RED.get_int(),
                                 box_width=350,
                                 xalign=hippo.ALIGNMENT_START,
                                 orientation=hippo.ORIENTATION_VERTICAL,
                                 padding_bottom=theme.BORDER_WIDTH_CONTROL/2,
                                 spacing=theme.BORDER_WIDTH_CONTROL/2)
    self.right.append(hippo.CanvasText(text=_('Question'),
                                  xalign=hippo.ALIGNMENT_START,
                                  color=theme.COLOR_DARK_GREEN.get_int(),
                                  font_desc=theme.FONT_BODY.get_pango_desc()))
    self.right.append(self.make_textbox(joke, 'text'))

    self.right.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL)) 
    
    self.right.append(hippo.CanvasText(text=_('Answer'),
                                  xalign=hippo.ALIGNMENT_START,
                                  color=theme.COLOR_DARK_GREEN.get_int(),
                                  font_desc=theme.FONT_BODY.get_pango_desc()))
    self.right.append(self.make_textbox(joke, 'answer'))
    
    self.append(self.left)
    self.append(self.right)


class Submit(Page):
  
  def __init__(self, jokebook, last_joke=0): # last_joke is for 'back' button
    Page.__init__(self, spacing=10)

    # create a new joke
    joke = Joke() 
    joke.id = jokebook.next_joke_id
    logging.info('Created new joke with id: %d' % joke.id)
    joke.joker = Globals.nickname

    # info
    self.append(self.make_field(_('Submission For:'), 250, jokebook, 'title', 300, False))
    self.append(self.make_field(_('Your Name:'),  250, joke, 'joker', 300, True))
    
    self.append(hippo.CanvasBox(box_height=theme.SPACER_VERTICAL)) # spacer

    # joke editor
    jokebox = JokeEditor(joke)        
    nav = hippo.CanvasBox(
      padding_right=8,
      padding_top=8,
      spacing=18,
      orientation=hippo.ORIENTATION_HORIZONTAL)
    button = gtk.Button(_('Submit'))
    button.connect('clicked', self.__do_clicked_submit, jokebook, joke)    
    nav.append(hippo.CanvasWidget(widget=theme.theme_widget(button), padding_right=10, padding_top=20))
    button = gtk.Button(_('Back'))
    button.connect('clicked', self.__do_clicked_back, jokebook, last_joke)    
    nav.append(hippo.CanvasWidget(widget=theme.theme_widget(button), padding_top=20))
    jokebox.right.append(nav)
    self.append(jokebox)


  def __do_clicked_back(self, button, jokebook, last_joke):
    joke_page = Globals.JokeMachineActivity.set_page(pages.joke.Joke, jokebook, last_joke)
    joke_page.force_answer(jokebook, last_joke) # force joke into answered state


  def __do_clicked_submit(self, button, jokebook, joke):

    Globals.JokeMachineActivity.set_page(pages.choose.Choose)
    
    # TODO -> Factor out of the page ? Should be transparent to UI layer ?
    if not Globals.JokeMachineActivity.is_shared:
      logging.error('pages.submit.Submit -> CANNOT SUBMIT WITHOUT A TUBE')
      return
    
    logging.debug('Submitting joke to remote')
    pickle = joke.dumps()
    Globals.JokeMachineActivity.tube.Submit(jokebook.id, pickle)
    logging.debug('Submitted joke to remote')
    
    
    
    

