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
import gst
import logging

from globals import Globals

from util.decorators import Property


class AudioPlayer(object):

  def __init__(self):
    pass


  @Property
  def uri():
    def get(self): return self.__uri
    def set(self, value): 
      if value is None or not os.path.exists(value):
        logging.error('AudioPlayer - Invalid URI: %r', value)
        return
      self.__uri = value 
      size = os.path.getsize(self.__uri)
      self.pipeline.get_by_name('source').set_property('location', self.__uri)
      self.pipeline.get_by_name('source').set_property('mmapsize', size)


  @Property
  def raw():
    def get(self): 
      if self.uri is None:
        logging.error('AudioPlayer - No data')
        return None
      f = open(self.uri, 'r')
      raw = f.read()
      f.close()
      return raw
    def set(self, value): 
      name = Globals.temporary_filename()
      f = open(name, 'w')
      f.write(value)
      f.close()
      self.uri = name
      logging.debug('AudioPlayer - set_raw wrote %d bytes to %s', len(value), name)


  @Property
  def pipeline():
    def get(self):
      if self.__pipeline is None:
        self.__pipeline = self.__build_pipeline()
      return self.__pipeline


  def play(self):
    logging.debug('AudioPlayer - started playing sound')
    self.pipeline.set_state(gst.STATE_PLAYING)
    logging.debug('AudioPlayer - finished playing sound')



  def __build_pipeline(self):
    # pipeline
    pipeline = gst.Pipeline('pipeline')

    # add source
    source = gst.element_factory_make('filesrc', 'source')
    pipeline.add(source)

    # add decoder
    decoder = gst.element_factory_make('decodebin', 'decoder')
    decoder.connect("new-decoded-pad", self.__new_decoded_pad) #, converter)
    pipeline.add(decoder)
    source.link(decoder)

    # add converter
    converter = gst.element_factory_make("audioconvert", "converter")
    pipeline.add(converter)

    # add output
    sink = gst.element_factory_make('autoaudiosink', 'sink')
    pipeline.add(sink)
    converter.link(sink)

    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect('message', self.__on_audio_message)	

    return pipeline



  # callbacks ##################################################################

  def __new_decoded_pad(self, dbin, pad, islast):  #, converter)
    converter = self.pipeline.get_by_name('converter') # TODO - pass by arg
    pad.link(converter.get_pad("sink"))


  def __on_audio_message(self, bus, message):
    t = message.type
    #logging.debug('message: %r' % t)
    if t == gst.MESSAGE_EOS:
      self.pipeline.set_state(gst.STATE_NULL)
      logging.debug('AudioPlayer - EOS')
    elif t == gst.MESSAGE_ERROR:
      self.pipeline.set_state(gst.STATE_NULL)
      err, debug = message.parse_error()
      logging.debug('AudioPlayer - Error: %r %r', err, debug)


  # Not used
  def __on_source_handoff(self, source, buffer, pad):
    logging.debug('on_source_handoff(%r, %r, %r)', source, buffer, pad)
