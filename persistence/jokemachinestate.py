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

from persistence.jokebook import Jokebook
from persistence.joke import Joke

class JokeMachineState(object):
  __metaclass__ = Persistent 
  
  @PersistentProperty 
  def id():
    '''object id'''
    def default(self): return 0
    def get(self): return self.__id
    def set(self, value): self.__id = value

  @PersistentProperty
  def jokebooks():
    '''the jokebooks in this jokemachine'''
    def default(self): return []
    def get(self): return self.__jokebooks

  @PersistentProperty
  def version():
    '''The activity version used to create this Jokebook'''
    def default(self): return 1  # TODO - pull from activity/activity.info
    def get(self): return self.__version
    
    
  @property
  def next_jokebook_id(self):
    if len(self.jokebooks) == 0:
      return 1
    return max([jokebook.id for jokebook in self.jokebooks]) + 1


  def jokebook(self, id):
    for jokebook in self.jokebooks:
      if jokebook.id == id:
        return jokebook
    logging.error('Could not find jokebook with id %d' % d)
    return None

  def test_data(self):
    self.id = 1

    # add some jokebooks with jokes
    num_jokebooks = 0
    num_jokes = 2
    num_submissions = 2
    for jokebook_id in range(1, num_jokebooks + 1):
      jokebook = Jokebook()
      jokebook.id = jokebook_id
      jokebook.owner = 'hummingbird'
      jokebook.title = 'Jokebook ' + str(jokebook.id)
      #jokebook.image = 'images/smile-big.png'
      for joke_id in range(1, num_jokes + 1):
        joke = Joke().test_data()
        joke.id = joke_id
        jokebook.jokes.append(joke)
      for joke_id in range(1, num_submissions + 1):
        joke = Joke().test_data()
        joke.id = joke_id
        jokebook.submissions.append(joke)
      self.jokebooks.append(jokebook)

    return self
  