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
from gettext import gettext as _

from globals import Globals
from gui.page import Page
from gui import theme
from util.audioplayer import AudioPlayer

import pages.submit

import persistence.joke

class JokeViewer(Page):

  def __init__(self, joke, jokebook_title=''):
    Page.__init__(self, 
                  spacing=8,
                  #background_color=theme.COLOR_PAGE.get_int(),
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
                                orientation=hippo.ORIENTATION_VERTICAL)
    joke_image = self.make_imagebox(joke, 'image', 320, 240, False)
    self.left.append(joke_image)
    self.left.append(hippo.CanvasText(text=jokebook_title,
                                      xalign=hippo.ALIGNMENT_START,
                                      color=theme.COLOR_DARK_GREEN.get_int(),
                                      font_desc=theme.FONT_BODY_BOLD.get_pango_desc()))
    self.left.append(hippo.CanvasText(text=_('Joke') + ' ' + str(joke.id),
                                      xalign=hippo.ALIGNMENT_START,
                                      font_desc=theme.FONT_BODY.get_pango_desc()))
    self.left.append(hippo.CanvasText(text=_('By') + ' ' + str(joke.joker),
                                      xalign=hippo.ALIGNMENT_START,
                                      font_desc=theme.FONT_BODY.get_pango_desc()))

    # right column 
    self.right = hippo.CanvasBox(border=0,
                                 border_color=theme.COLOR_RED.get_int(),
                                 box_width=350,
                                 xalign=hippo.ALIGNMENT_START,
                                 orientation=hippo.ORIENTATION_VERTICAL)
    self.right.append(hippo.CanvasText(text=_('Question'),
                                       xalign=hippo.ALIGNMENT_START,
                                       color=theme.COLOR_DARK_GREEN.get_int(),
                                       font_desc=theme.FONT_BODY.get_pango_desc()))
    self.right.append(self.make_bodytext(joke.text))

    self.right.append(hippo.CanvasBox(box_height=30)) # spacer

    self.answer_box = hippo.CanvasBox()
    self.answer_box.append(hippo.CanvasText(text=_('Answer'),
                                       xalign=hippo.ALIGNMENT_START,
                                       color=theme.COLOR_DARK_GREEN.get_int(),
                                       font_desc=theme.FONT_BODY.get_pango_desc()))
    self.answer_box.append(self.make_bodytext(joke.answer))    
    self.right.append(self.answer_box)

    self.append(self.left)
    self.append(self.right)



class Joke(Page):

  def __init__(self, jokebook, joke_id = 0):
    Page.__init__(self)

    # handle empty jokebook
    if len(jokebook.jokes) <= joke_id:
      self.append(self.make_bodytext(_('This Jokebook is empty')))
      if not Globals.JokeMachineActivity.is_initiator:
        button = gtk.Button(_('Submit a Joke'))
        button.connect('clicked', self.__do_clicked_submit, jokebook, joke_id)        
        self.append(hippo.CanvasWidget(widget=theme.theme_widget(button), 
                                       padding_top=20))
      else:
        button = gtk.Button(_('Add Jokes'))
        button.connect('clicked', self.__do_clicked_add, jokebook, joke_id)        
        self.append(hippo.CanvasWidget(widget=theme.theme_widget(button), 
                                       padding_top=20))
      return
      
    # the joke box
    joke = jokebook.jokes[joke_id]
    self.joke_box = JokeViewer(joke, jokebook.title)
    self.joke_box.answer_box.set_visible(False)

    # the navigation box
    self.navigation_box = hippo.CanvasBox(
      padding_right=8,
      padding_top=8,
      spacing=18,
      orientation=hippo.ORIENTATION_HORIZONTAL)

    # the answer button
    button = gtk.Button(_('Answer'))
    button.connect('clicked', self.__do_clicked_answer, jokebook, joke_id)        
    self.navigation_box.append(hippo.CanvasWidget(widget=theme.theme_widget(button), padding_top=20))
    self.joke_box.right.append(self.navigation_box)
    self.append(self.joke_box)


  # for forcing the joke into the answered state from page.submit
  def force_answer(self, jokebook, joke_id):
    self.__do_clicked_answer(None, jokebook, joke_id)


  def __do_clicked_answer(self, button, jokebook, joke_id):
    # play a sound if the jokebook has one
    if jokebook.sound_blob != None:
      player = AudioPlayer()
      player.raw = jokebook.sound_blob
      player.play()
        
    # show the answer
    self.joke_box.answer_box.set_visible(True)
    
    # reconfigure navigation box
    self.navigation_box.clear()
    
    # check if there are any more jokes left
    if len(jokebook.jokes) > joke_id + 1:
      button = gtk.Button(_('Next'))
      button.connect('clicked', self.__do_clicked_next, jokebook, joke_id + 1)        
      self.navigation_box.append(hippo.CanvasWidget(widget=theme.theme_widget(button), padding_right=10, padding_top=20))
    
    # only allow submitting a joke if activity is shared and you are the one joining
    if not Globals.JokeMachineActivity.is_initiator:
      button = gtk.Button(_('Submit a Joke'))
      button.connect('clicked', self.__do_clicked_submit, jokebook, joke_id)        
      self.navigation_box.append(hippo.CanvasWidget(widget=theme.theme_widget(button), 
                                                    padding_top=20))
      
    
  def __do_clicked_add(self, button, jokebook, joke_id):
    page = Globals.JokeMachineActivity.set_page(pages.edit.Edit, jokebook)
    tab = page.do_tab_clicked(pages.edit.EditJokes)
    tab.do_clicked_add_joke(None, jokebook)

  def __do_clicked_submit(self, button, jokebook, joke_id):
    Globals.JokeMachineActivity.set_page(pages.submit.Submit, jokebook, joke_id)


  def __do_clicked_next(self, button, jokebook, joke_id):
    Globals.JokeMachineActivity.set_page(pages.joke.Joke, jokebook, joke_id)
    
  
