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
import logging
import tempfile
from sugar.activity import activity
try:
  from hashlib import sha1
except ImportError:
  # Python < 2.5
  from sha import new as sha1

from persistence.jokemachinestate import JokeMachineState


class __globals(object):
  '''All applications have code that affects global state. These are the
  globals for Jokemachine'''
  
  def __init__(self):
    self.__pwd = activity.get_bundle_path()
    self.__root = None
    self.__logo = 'resources/GameLogoCharacter.png'
    self.__laugh = 'resources/laugh_attack.au'
    self.__activity_state = None
    self.__activity = None
    
    # owner
    self.__owner = None
    self.__owner_sha1 = None
    
    self.__temporary_filenames = []
    

  # convert all of these to @Property
  def set_activity_instance(self, activity_instance):
    logging.debug('setting actifity %r' % activity_instance)    
    self.__root = activity_instance.get_activity_root()        
    self.__activity = activity_instance
    
  # TODO -> Should we refresh the GUI for this one ?
  def set_activity_state(self, activity_state):
    self.__activity_state = activity_state
    
  def set_owner(self, owner):
    logging.debug('Owner is %s' % owner.props.nick)
    self.__owner = owner
    self.__owner_sha1 = sha1(owner.props.nick).hexdigest()

  @property
  def pwd(self):
    return self.__pwd
  
  @property
  def root(self):
    return self.__root
      
  @property
  def tmpdir(self):
    '''Temporary directory - currently this exists for the sole purpose of
    having a place to dump sounds and images into so we don't have to keep
    them in memory - don't know if this will still be valid under bitfrost,
    don't know if sounds and images can be pulled directly out of the journal
    when needing to be (dis)played'''
    logging.debug('Temp dir is %s' % os.path.join(self.__root, 'tmp'))
    return os.path.join(self.__root, 'tmp')
  
  @property
  def logo(self):
    return os.path.join(self.pwd, self.__logo)
  
  @property
  def laugh_uri(self):
    return os.path.join(self.pwd, self.__laugh)
  
  @property
  def JokeMachineState(self):
    if not self.__activity_state:
      # Okay - When app is not run from Journal activity.read_file() is never
      # called, which means we never call Globals.set_activity_state so we
      # create a default state here:
      logging.debug('Globals.JokeMachineState() - creating default data')
      self.__activity_state = JokeMachineState().test_data() # TODO - implement JokeMachineState.new()
    return self.__activity_state
  
  @property
  def JokeMachineActivity(self):
    if not self.__activity:
      # todo log this!!
      logging.debug('no activity set! - use Globals.set_activity_instance to register activity with Global manager')
      return None
    return self.__activity
  
  @property
  def nickname(self):
    return self.__owner.props.nick  
  
  
  # utility functions with global state
  
  def temporary_filename(self):
    (fd, name) = tempfile.mkstemp(prefix='jokemachine_') 
    self.__temporary_filenames.append(name)
    return name

  
  def shutdown(self):
    for filename in self.__temporary_filenames:
      if os.path.exists(filename):
        logging.info('  deleting temporary file: %s' % filename)
        os.remove(filename)


Globals = __globals()
 
 
