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

from util.persistence import Persistent, PersistentProperty


class Joke(object):
  __metaclass__ = Persistent
  
  @PersistentProperty
  def id():
    '''some doc string'''
    def default(self): return 0
    def get(self): return self.__id
    def set(self, value): self.__id = value

  @PersistentProperty
  def image():
    '''the image for the joke'''
    def get(self): return self.__image
    def set(self, value): self.__image = value

  @PersistentProperty
  def image_blob():
    '''raw image data'''
    def get(self): return self.__image_blob
    def set(self, value): self.__image_blob = value
    
  @PersistentProperty
  def text():
    '''the joke question'''
    def get(self): return self.__text
    def set(self, value): self.__text = value

  @PersistentProperty
  def answer():
    '''the joke answer'''
    def get(self): return self.__answer
    def set(self, value): self.__answer = value

  @PersistentProperty
  def joker():
    '''the author of the joke'''
    def get(self): return self.__joker
    def set(self, value): self.__joker = value

  @PersistentProperty
  def joker_location():
    '''the location of the author'''
    def get(self): return self.__joker_location
    def set(self, value): self.__joker_location = value
    
  @PersistentProperty
  def joker_country():
    '''the country of the author'''
    def get(self): return self.__joker_country
    def set(self, value): self.__joker_country = value
 
  def test_data(self):
    #self.image = 'resources/knockknock.png'
    self.text = '''Knock, knock
Who's there ?
Alex.
Alex who?'''
    self.answer = 'Alex plain later, just let me in!'
    self.joker = 'hummingbird'
    self.joker_location = 'Cape Town'
    self.joker_country = 'South Africa'
    
    return self
  
  
  