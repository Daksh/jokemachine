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

from util.decorators import Property

from pages.submit import JokeEditor
from pages.joke   import JokeViewer

import pages.preview
import persistence.joke



class PageSelector(hippo.CanvasBox):
  
  def __init__(self, parent, **kwargs):
    hippo.CanvasBox.__init__(self, **kwargs)
    self.__parent = parent

    control_width = 1024 # TODO -> Figure this out from parent size
    self.props.border = 1
    self.props.border_color=theme.COLOR_TAB_ACTIVE.get_int()
    self.props.background_color=theme.COLOR_PAGE.get_int()
    self.props.orientation=hippo.ORIENTATION_VERTICAL
    
    # button box -> # TODO -> Make into generic control
    tab_width = control_width / 3.0
    tab_box = hippo.CanvasBox(background_color=theme.COLOR_TAB_SEPERATOR.get_int(),
                                 spacing=2,
                                 orientation=hippo.ORIENTATION_HORIZONTAL)
    self.__tab_1 = hippo.CanvasText(text=_('Edit Jokebook Cover'),
                                box_width=tab_width,
                                padding=theme.PADDING_TAB,
                                xalign=hippo.ALIGNMENT_START,
                                background_color=theme.COLOR_TAB_ACTIVE.get_int(),
                                color=theme.COLOR_TAB_TEXT.get_int(),
                                font_desc=theme.FONT_TABS.get_pango_desc())
    self.__tab_1.page = EditInfo
    self.__tab_1.connect('button-press-event', self.__do_clicked_tab)    
    tab_box.append(self.__tab_1)
    self.__tab_2 = hippo.CanvasText(text=_('Edit My Jokes'),
                                box_width=tab_width,
                                padding=theme.PADDING_TAB,
                                xalign=hippo.ALIGNMENT_START,
                                background_color=theme.COLOR_TAB_INACTIVE.get_int(),
                                color=theme.COLOR_TAB_TEXT.get_int(),
                                font_desc=theme.FONT_TABS.get_pango_desc())
    self.__tab_2.page = EditJokes
    self.__tab_2.connect('button-press-event', self.__do_clicked_tab)    
    tab_box.append(self.__tab_2)
    self.__tab_3 = hippo.CanvasText(text=_('Review Submitted Jokes'),
                                box_width=tab_width,
                                padding=theme.PADDING_TAB,
                                xalign=hippo.ALIGNMENT_START,
                                background_color=theme.COLOR_TAB_INACTIVE.get_int(),
                                color=theme.COLOR_TAB_TEXT.get_int(),
                                font_desc=theme.FONT_TABS.get_pango_desc())
    self.__tab_3.page = EditReview
    self.__tab_3.connect('button-press-event', self.__do_clicked_tab)    
    tab_box.append(self.__tab_3)
    self.append(tab_box)
    
    self.__page = hippo.CanvasBox(background_color=theme.COLOR_PAGE.get_int(),
                                orientation=hippo.ORIENTATION_VERTICAL)
    self.append(self.__page)
    
    
  @Property
  def page(): 
    def get(self): return self.__page.the_page
    def set(self, value): 
      self.__page.clear()
      self.__page.append(value)
      self.__page.the_page = value
    
    
  def __do_clicked_tab(self, control, event):
    self.__tab_1.props.background_color=theme.COLOR_TAB_INACTIVE.get_int()
    self.__tab_2.props.background_color=theme.COLOR_TAB_INACTIVE.get_int()
    self.__tab_3.props.background_color=theme.COLOR_TAB_INACTIVE.get_int()
    control.props.background_color=theme.COLOR_TAB_ACTIVE.get_int()
    self.__parent.do_tab_clicked(control.page)



class Edit(Page):

  def __init__(self, jokebook):
    Page.__init__(self, xalign=hippo.ALIGNMENT_CENTER)
    
    self.__jokebook = jokebook    
    
    self.__page_selector = PageSelector(self)
    self.append(self.__page_selector)
    self.__page_selector.page = EditInfo(jokebook, self)
    
    button = gtk.Button(_('Preview'))
    button.connect('clicked', self.__do_clicked_preview, jokebook)    
    self.append(hippo.CanvasWidget(widget=theme.theme_widget(button), padding_top=theme.SPACER_VERTICAL))


  def __do_clicked_preview(self, button, jokebook):
    Globals.JokeMachineActivity.set_page(pages.preview.Preview, jokebook)
  

  def do_tab_clicked(self, page_class):
    print page_class
    self.__page_selector.page = page_class(self.__jokebook, self)
    return self.__page_selector.page


class EditInfo(Page): # TODO -> gui.Page should follow this pattern rather
  def __init__(self, jokebook, parent):
    Page.__init__(self, xalign=hippo.ALIGNMENT_CENTER,
                        orientation=hippo.ORIENTATION_VERTICAL,
                        padding=20, 
                        spacing=20,
                        box_height=theme.TABS_HEIGHT)
    
    self.__parent = parent
    
    # page title
    self.append(self.make_field(_('Title of Jokebook:'), 250, jokebook, 'title', 300, True))
    #field = self.make_field(_('Sound Effect:'), 250, None, '', 300, False)
    
    sound_effect = hippo.CanvasBox(orientation=hippo.ORIENTATION_HORIZONTAL, spacing=10)
    sound_effect.append(self.make_bodytext(_('Sound Effect:'), 250, hippo.ALIGNMENT_START, theme.COLOR_DARK_GREEN))
    sound_effect.append(self.make_audiobox(jokebook, 'sound', 316))
    self.append(sound_effect)
    

    # cover picture
    cover_image = self.make_imagebox(jokebook, 'image', 320, 240, True)
    self.append(cover_image)
    
    # punchline sound
    #self.append(self.make_audiobox(jokebook, 'sound'))
    
    
  
class EditJokes(Page):
  
  def __init__(self, jokebook, parent):
    Page.__init__(self)
    
    self.__parent = parent
    
    # list of jokes
    jokes_div = CanvasListBox(800, theme.TABS_HEIGHT)  
    jokes_div.props.border=0
    for joke in jokebook.jokes:
      button = gtk.Button(' ' + _('Delete') + ' ')
      button.connect('clicked', self.__do_clicked_delete, jokebook, joke)
      list_row = self.make_listrow(JokeEditor(joke))
      list_row.append(hippo.CanvasWidget(widget=theme.theme_widget(button),
                                         padding=5),
                      hippo.PACK_END)
      jokes_div.append(list_row)
    self.append(jokes_div)
    
    # new joke button
    buttons = hippo.CanvasBox(orientation=hippo.ORIENTATION_HORIZONTAL,
                              xalign=hippo.ALIGNMENT_START)
    button = gtk.Button(_('Add New Joke'))
    button.connect('clicked', self.do_clicked_add_joke, jokebook)    
    buttons.append(hippo.CanvasWidget(widget=theme.theme_widget(button)))    
    jokes_div.append(buttons)
    
    
  def __do_clicked_delete(self, button, jokebook, joke):
    confirm = gtk.MessageDialog(Globals.JokeMachineActivity, 
                                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                gtk.MESSAGE_QUESTION,
                                gtk.BUTTONS_YES_NO,
                                _('Are you sure you want to delete this joke ?'))
    response = confirm.run()
    confirm.hide()
    confirm.destroy()
    del confirm
    if response == gtk.RESPONSE_YES:
      logging.debug('Deleting joke: %s' % joke.id)
      jokebook.jokes.remove(joke)
      self.__parent.do_tab_clicked(EditJokes)
    
    
  def do_clicked_add_joke(self, button, jokebook):
    # create a new joke
    joke = persistence.joke.Joke() 
    joke.id = jokebook.next_joke_id
    logging.info('Created new joke with id: %d' % joke.id)
    joke.joker = Globals.nickname
    jokebook.jokes.append(joke)
    
    # reload tab
    self.__parent.do_tab_clicked(EditJokes)
  
    
    
class EditReview(Page):
  def __init__(self, jokebook, parent):
    Page.__init__(self)
    
    self.__parent = parent
    
    jokes_div = CanvasListBox(800, theme.TABS_HEIGHT)  
    jokes_div.props.border=0
    for joke in jokebook.submissions:
      list_row = self.make_listrow(JokeViewer(joke, jokebook.title))
      list_row.props.orientation=hippo.ORIENTATION_VERTICAL
      
      buttons = hippo.CanvasBox(orientation=hippo.ORIENTATION_HORIZONTAL,
                                xalign=hippo.ALIGNMENT_END,
                                spacing=10,
                                padding=10)
      
      button = gtk.Button(' ' + _('Reject') + ' ')
      button.connect('clicked', self.__do_clicked_reject, jokebook, joke)
      buttons.append(hippo.CanvasWidget(widget=theme.theme_widget(button),
                                        border_color=theme.COLOR_RED.get_int(),
                                        border=0,
                                        xalign=hippo.ALIGNMENT_CENTER))

      button = gtk.Button(' ' + _('Accept') + ' ')
      button.connect('clicked', self.__do_clicked_accept, jokebook, joke)
      buttons.append(hippo.CanvasWidget(widget=theme.theme_widget(button),
                                        border_color=theme.COLOR_RED.get_int(),
                                        border=0,
                                        xalign=hippo.ALIGNMENT_CENTER))
 
      list_row.append(buttons)
      
      #list_row.props.orientation=hippo.ORIENTATION_VERTICAL
      #status_box = hippo.CanvasBox(orientation=hippo.ORIENTATION_HORIZONTAL,
                                   #padding_top=4,
                                   #padding_left=4)
      #status_box.append(hippo.CanvasText(text=_('Status:'),
                                  #color=theme.COLOR_DARK_GREEN.get_int(),
                                  #box_width=100,
                                  #xalign=hippo.ALIGNMENT_START,
                                  #font_desc=theme.FONT_BODY.get_pango_desc()))
      ##button = None
      #button = gtk.RadioButton()
      #button = gtk.RadioButton(button, _('Approved'))
      #button.set_size_request(200, -1)
      #status_box.append(hippo.CanvasWidget(widget = button))
      #button = gtk.RadioButton(button, _('Rejected'))
      #button.set_size_request(200, -1)
      #status_box.append(hippo.CanvasWidget(widget = button))
      #button = gtk.RadioButton(button, _('Not Reviewed'))
      #button.set_size_request(200, -1)
      #button.set_active(True)
      #status_box.append(hippo.CanvasWidget(widget = button))
      #list_row.append(status_box)
      
      jokes_div.append(list_row)
      
    self.append(jokes_div)
    
    
  def __do_clicked_accept(self, button, jokebook, joke):
    jokebook.jokes.append(joke)
    jokebook.submissions.remove(joke)
    self.__parent.do_tab_clicked(EditReview)
    if Globals.JokeMachineActivity.is_shared:
      # broadcast submission onto the mesh
      logging.debug('Broadcasting joke to mesh')
      pickle = joke.dumps()
      Globals.JokeMachineActivity.tube.BroadcastJoke(jokebook.id, pickle, Globals.nickname)
      logging.debug('Broadcasted joke to mesh')

  
  def __do_clicked_reject(self, button, jokebook, joke):
    jokebook.submissions.remove(joke)
    self.__parent.do_tab_clicked(EditReview)
