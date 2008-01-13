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

from util.persistence import Persistent, PersistentProperty


class Jokebook(object):
  __metaclass__ = Persistent 
  
  @PersistentProperty
  def id():
    '''object id'''
    def default(self): return 0
    def get(self): return self.__id
    def set(self, value): self.__id = value

  @PersistentProperty
  def title():
    '''the title of this jokebook'''
    def get(self): return self.__title
    def set(self, value): self.__title = value
    
  @PersistentProperty
  def image():
    '''the cover image of this jokebook'''
    def get(self): return self.__image
    def set(self, value): self.__image = value

  @PersistentProperty
  def image_blob():
    '''raw image data'''
    def get(self): return self.__image_blob
    def set(self, value): self.__image_blob = value
    
  @PersistentProperty
  def sound():
    '''the sound we must play on punchline'''
    def get(self): return self.__sound
    def set(self, value): self.__sound = value

  @PersistentProperty
  def sound_blob():
    '''raw data for the sound'''
    def get(self): return self.__sound_blob
    def set(self, value): self.__sound_blob = value    

  @PersistentProperty
  def owner():
    '''the owner of this jokebook'''
    def get(self): return self.__owner
    def set(self, value): self.__owner = value

  @PersistentProperty
  def jokes():
    '''the jokes in the jokebook'''
    def default(self): return []
    def get(self): return self.__jokes

  @PersistentProperty
  def submissions():
    '''jokes submitted to this jokebook pending approval'''
    def default(self): return []
    def get(self): return self.__submissions

  @PersistentProperty
  def show():
    '''should this jokebook be visible to others'''
    def default(self): return False
    def get(self): return self.__show
    def set(self, value): self.__show = value
    
  # TODO - this should really be transparent
  @property
  def next_joke_id(self):
    if len(self.jokes) == 0:
      return 1
    return max([joke.id for joke in self.jokes]) + 1
  
  
