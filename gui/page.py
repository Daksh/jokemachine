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
import cairo # for getting png for CanvasImage
import pango
import hippo
import logging
import StringIO

from gettext import gettext as _

from sugar.graphics import style
from sugar.graphics.objectchooser import ObjectChooser
from sugar import mime

# argh!
try:
  from sugar.graphics.roundbox import RoundBox 
except ImportError:
  try:
    from sugar.graphics.roundbox import CanvasRoundBox as RoundBox
  except ImportError:
    from sugar.graphics.canvasroundbox import CanvasRoundBox as RoundBox


from util.persistence import Persistent, PersistentProperty

from util.audioplayer import AudioPlayer


from gui import theme
from globals import Globals


THUMB_SIZE = min(gtk.gdk.screen_width(), gtk.gdk.screen_height()) / 2


class Page(hippo.CanvasBox):

  def __init__(self, **kwargs):
    hippo.CanvasBox.__init__(self, **kwargs)
    
    self.__alternate_color_listrows = False
    self.__color_listrow = theme.COLOR_LIST_ROW_ALT.get_int()
    
  
  def append(self, item, *args, **kwargs):
    hippo.CanvasBox.append(self, item, *args, **kwargs)
    
    
  @property
  def color_listrow(self):
    if not self.__alternate_color_listrows:
      return theme.COLOR_LIST_ROW.get_int()
    if self.__color_listrow == theme.COLOR_LIST_ROW_ALT.get_int():
      self.__color_listrow = theme.COLOR_LIST_ROW.get_int()
    else:
      self.__color_listrow = theme.COLOR_LIST_ROW_ALT.get_int()
    return self.__color_listrow


  def make_listrow(self, contents = None, *args):
    list_row = RoundBox()
    list_row.props.border  = 0 # properties not being set properly by constructor
    list_row.props.padding = theme.DEFAULT_PADDING
    #list_row.props.padding_right=0
    list_row.props.background_color = self.color_listrow
    if contents is not None:
      list_row.append(contents, *args)
    return list_row
      
      
  def make_audiobox(self, obj, property, width):
    
    image_file = os.path.join(Globals.pwd, theme.AUDIO_CHOOSE)
    if not os.path.exists(image_file):
      logging.debug('cannot find %s' % image_file)
      return hippo.CanvasBox()
    
    surface = cairo.ImageSurface.create_from_png(image_file)
    preview_sound = hippo.CanvasImage(image=surface,
                                      xalign=hippo.ALIGNMENT_START,
                                      yalign=hippo.ALIGNMENT_CENTER)
    preview_sound.connect('button-press-event', self.__do_clicked_preview_sound, obj, property)
    
    if hasattr(obj, property) and getattr(obj, property) != None:
      sound_name = getattr(obj, property)
    else:
      sound_name = _('Click to choose a sound')
    
    choose_sound = hippo.CanvasText(text=sound_name, 
                                    xalign=hippo.ALIGNMENT_START)
    choose_sound.connect('button-press-event', self.__do_clicked_choose_sound, obj, property)
    
    sound_box = RoundBox()
    sound_box.props.padding = 2
    sound_box.props.spacing = 10
    sound_box.props.box_width = width
    sound_box.props.border=theme.BORDER_WIDTH_CONTROL / 2
    sound_box.props.border_color=theme.COLOR_DARK_GREEN.get_int()
    sound_box.props.background_color = theme.COLOR_WHITE.get_int()
    sound_box.props.orientation=hippo.ORIENTATION_HORIZONTAL
    sound_box.props.xalign=hippo.ALIGNMENT_START
    sound_box.set_clickable(True)
    sound_box.append(preview_sound)
    sound_box.append(choose_sound)
    
    deglitch_box = hippo.CanvasBox(xalign=hippo.ALIGNMENT_START, box_width=width)
    deglitch_box.append(sound_box)
    return deglitch_box
    

  def make_imagebox(self, obj, property = None, width=-1, height=-1, editable=True, padding=0):
    image = self.__get_property_value(obj, property)  
    if image == '' or image == None:
      image = theme.IMAGE_CHOOSE
    file_name = os.path.join(Globals.pwd, image)
    logging.debug('make_imagebox(%r)' % file_name)
    
    # TODO -> handle landscape/portrait properly
    
    # load image - could be cleaner on the whole... :)
    try:
      if hasattr(obj, 'image_blob') and getattr(obj, 'image_blob') is not None:
        image_file = StringIO.StringIO(obj.image_blob)
        surface = cairo.ImageSurface.create_from_png(image_file) 
      else:
        surface = cairo.ImageSurface.create_from_png(file_name) 
    except Exception, e:
      logging.error('Error while loading image: %r' % e)
      
    # set border
    if editable:
      border_width = 0
    else:
      border_width = theme.BORDER_WIDTH_IMAGE
      
    # the image itself
    cover_image = hippo.CanvasImage(image=surface,
                                    border=border_width,
                                    border_color=theme.COLOR_BLACK.get_int(),
                                    xalign=hippo.ALIGNMENT_CENTER,
                                    yalign=hippo.ALIGNMENT_CENTER,
                                    scale_width=width,
                                    scale_height=height)
    if editable:
      cover_image.set_clickable(True)
      cover_image.connect('button-press-event', self.__do_clicked_image, obj, 'image_blob')
      image_box = RoundBox()
      image_box.props.padding = 0
      image_box.props.spacing = 0
      image_box.props.border=theme.BORDER_WIDTH_CONTROL
      image_box.props.border_color=theme.COLOR_DARK_GREEN.get_int()
      image_box.append(cover_image)
    else:
      image_box = cover_image
      
    # Grrr... RoundedBoxes and CanvasImages expand their width to their parent
    # unless they're in a CanvasBox
    deglitch_box = hippo.CanvasBox(xalign=hippo.ALIGNMENT_CENTER, padding=padding)
    deglitch_box.append(image_box)
    return deglitch_box
  

  def make_bodytext(self, text, width=-1, xalign = hippo.ALIGNMENT_START, text_color = theme.COLOR_BLACK):
    return hippo.CanvasText(text=text,
                            size_mode=hippo.CANVAS_SIZE_WRAP_WORD,
                            box_width=width,
                            xalign=xalign,
                            color=text_color.get_int())
  
  
  def make_textbox(self, obj, property, width=300, height=100, editable=True):
    value = self.__get_property_value(obj, property)
    textbox = self.__textview(value, width, height, editable, True)
    textbox.control.get_buffer().connect('changed', self.__do_changed_control, obj, property)        
    return textbox  
 
 
  def make_field(self, label, label_width, obj, property, field_width, editable=True):
    value = self.__get_property_value(obj, property)
    field_box = hippo.CanvasBox(orientation=hippo.ORIENTATION_HORIZONTAL,
                                xalign=hippo.ALIGNMENT_START,
                                spacing=10)
    field_box.append(hippo.CanvasText(text=label,
                                      box_width=label_width,
                                      xalign=hippo.ALIGNMENT_START,
                                      color=theme.COLOR_DARK_GREEN.get_int()))
    #if editable:
    textfield = self.__textview(value, field_width, -1, editable, False) 
    textfield.control.get_buffer().connect('changed', self.__do_changed_control, obj, property)    
    field_box.append(textfield)
    #else: # TODO - move to __textview()
      #glitch_box = CanvasBox(box_width=field_width)
      #glitch_box.append(hippo.CanvasText(text=value,
                                        #size_mode=hippo.CANVAS_SIZE_WRAP_WORD,
                                        #box_width=field_width,
                                        #xalign=hippo.ALIGNMENT_START))
      #field_box.append(glitch_box)
    return field_box


  # Refactor into a CanvasTextView class
  # TODO: Implement editable and multiline
  # TODO: Lose multiline and change height variable to num_lines
  def __textview(self, text, width=300, height=-1, editable=True, multiline=False):
    textview = gtk.TextView()
    textview.get_buffer().set_text(text)

    # control props
    textview.set_wrap_mode(gtk.WRAP_WORD)
    textview.modify_base(gtk.STATE_NORMAL, theme.COLOR_TEXTBOX.get_gdk_color())
    textview.set_editable(editable)
    textview.set_cursor_visible(editable)
    if height == -1:
      context = textview.create_pango_context()
      layout = pango.Layout(context)
      layout.set_text(text[ : text.find('\n')])
      (w, h) = layout.get_pixel_size()
      height = h #+ theme.BORDER_WIDTH_CONTROL / 2 # fudge factor - on the XO-1 hardware all known solutions evaporate
    textview.set_size_request(width, height)
    textview.set_border_window_size(gtk.TEXT_WINDOW_LEFT, 0)
    textview.set_border_window_size(gtk.TEXT_WINDOW_RIGHT, 0)
    textview.set_border_window_size(gtk.TEXT_WINDOW_TOP, 0)
    textview.set_border_window_size(gtk.TEXT_WINDOW_BOTTOM, 0)
    textview.show()
    
    if editable: # because rounded corners are well... pretty
      border_box = RoundBox() 
      border_box.control = textview    
      border_box.props.padding = 2
      border_box.props.spacing = 0
      border_box.props.border=theme.BORDER_WIDTH_CONTROL / 2
      border_box.props.border_color=theme.COLOR_DARK_GREEN.get_int()
      border_box.props.background_color=theme.COLOR_TEXTBOX.get_int()
      border_box.props.xalign=hippo.ALIGNMENT_START
      #border_box.props.box_width = width
      #border_box.props.box_height = height
      
      # TODO - File bug: RoundBox seriously messes with TextView's 
      #                  (and other things) width !!
      deglitch_box = hippo.CanvasBox() 
      deglitch_box.append(hippo.CanvasWidget(widget=textview))
      border_box.append(deglitch_box)
      return border_box

    no_edit_box = hippo.CanvasWidget(widget=textview)
    no_edit_box.control = textview
    return no_edit_box


  def __get_property_value(self, obj, property):
    # TODO - Clean entire Model/View mechanism up so that we're not 
    #        passing objects and text properties around at all
    if obj is None:
      return ''
    if type(obj) is str:
      return obj
    if hasattr(obj, '__metaclass__') and obj.__metaclass__ is Persistent and hasattr(obj, property):
      value = getattr(obj, property)
      if value is None:
        return ''
      return value
    logging.debug('__get_property_value error: Unknown object type %r', type(obj))
    return obj
 
  
  def __do_changed_control(self, control, obj, property):
    '''Update object model with control values'''
    if hasattr(obj, property) and hasattr(control.props, 'text'):
      setattr(obj, property, control.props.text)
    else:
      print 'NO PROPERTY OR TEXT'


  def __do_clicked_image(self, control, event, obj, property):
    if hasattr(mime, 'GENERIC_TYPE_IMAGE'):
      filter = { 'what_filter': mime.GENERIC_TYPE_IMAGE }
    else:
      filter = { }

    # Courtesy of Write.activity - toolbar.py
    chooser = ObjectChooser(title=_('Choose image'), 
                            parent=Globals.JokeMachineActivity, #._parent,
                            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            **filter)
    try:
      result = chooser.run()
      if result == gtk.RESPONSE_ACCEPT:
        logging.debug('ObjectChooser: %r' % chooser.get_selected_object())
        journal_object = chooser.get_selected_object()
        if hasattr(obj, 'image_blob') and journal_object and journal_object.file_path:
          logging.debug('Getting journal object: %r, %s', journal_object, journal_object.file_path)
          # Set the image now
          raw = _load_image(journal_object.file_path)
          obj.image =  str(journal_object.metadata['title'])
          obj.image_blob = raw
          # refresh the image 
          image_file = StringIO.StringIO(obj.image_blob)
          surface = cairo.ImageSurface.create_from_png(image_file) 
          control.props.image = surface
    finally:
      #chooser.hide()
      chooser.destroy()
      del chooser


  def __do_clicked_choose_sound(self, control, event, obj, property):
    if hasattr(mime, 'GENERIC_TYPE_AUDIO'):
      filter = { 'what_filter': mime.GENERIC_TYPE_AUDIO }
    else:
      filter = { }

    logging.debug('choosing sound file') 
    chooser = ObjectChooser(title=_('Choose Sound'), 
                            parent=Globals.JokeMachineActivity, #._parent,
                            flags=gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            **filter)
    try:
      result = chooser.run()
      if result == gtk.RESPONSE_ACCEPT:
        logging.debug('ObjectChooser: %r' % chooser.get_selected_object())
        journal_object = chooser.get_selected_object()
        if hasattr(obj, 'sound_blob') and journal_object and journal_object.file_path:
          logging.debug('Getting journal object: %r, %s, %s', journal_object, journal_object.file_path, journal_object.metadata['title'])
          # Set the sound now
          f = open(journal_object.file_path, 'r')
          raw = f.read()
          f.close()
          obj.sound = str(journal_object.metadata['title'])
          obj.sound_blob = raw
          control.props.text = obj.sound
    finally:
      #chooser.hide()
      chooser.destroy()
      del chooser
  

  def __do_clicked_preview_sound(self, control, event, obj, property):
    
    if not hasattr(obj, 'sound_blob') or getattr(obj, 'sound_blob') == None:
      logging.debug('No sound to preview')
      return
    
    player = AudioPlayer()
    #player.uri = sound_file
    player.raw = obj.sound_blob
    player.play()

def _load_image(file_name):
    pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(file_name,
            THUMB_SIZE, THUMB_SIZE)
    if pixbuf is None:
        return None
    stream = StringIO.StringIO()
    pixbuf.save_to_callback(lambda data: stream.write(data), 'png')
    return stream.getvalue()
