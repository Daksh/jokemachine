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


import logging


from dbus.service import method, signal
from dbus.gobject_service import ExportedGObject


from globals import Globals
from persistence.jokemachinestate import JokeMachineState
from persistence.joke import Joke

MESH_SERVICE = 'org.worldwideworkshop.JokeMachine'
MESH_IFACE = MESH_SERVICE
MESH_PATH = '/org/worldwideworkshop/JokeMachine'



class JokeMachineSession(ExportedGObject):
  """The bit that talks over the TUBES!!!"""

  def __init__(self, tube, is_initiator, get_buddy, activity):
    """Initialise the PollSession.

        tube -- TubeConnection
        is_initiator -- boolean, True = we are sharing, False = we are joining
        get_buddy -- function
        activity -- JokeMachine (sugar.activity.Activity)
        """
    super(JokeMachineSession, self).__init__(tube, MESH_PATH)
    self.tube = tube
    self.is_initiator = is_initiator
    self.entered = False  # Have we set up the tube?
    self._get_buddy = get_buddy  # Converts handle to Buddy object
    self.activity = activity  # JokeMachine
    self.tube.watch_participants(self.participant_change_cb)



  # Signals and signal handlers ################################################

  @signal(dbus_interface=MESH_IFACE, signature='')
  def Hello(self):
    """Signal to request that my UpdatePoll method is called to let me know about
    other known polls."""

  # a -> Say hello to incoming buddy and send him our state
  def hello_cb(self, sender=None):
    '''Tell the newcomer what's going on.'''
    assert sender is not None
    logging.debug('In hello_cb - Newcomer %s has joined and sent Hello', sender)
    # sender is a bus name - check if it's me:
    if sender == self.my_bus_name:
      # then I don't want to respond to my own Hello
      return
    
    logging.debug('Sending %s my state' % sender)
    state_pickle = Globals.JokeMachineState.dumps()
    logging.debug('PICKLE TYPE: %r (hello_cb)' % type(state_pickle))
    #state_pickle = ('This is my tubes message being sent to %s' % sender)
    #logging.debug('PICKLE TYPE: %r (hello_cb)' % type(state_pickle))
    self.tube.get_object(sender, MESH_PATH).PumpActivityState(state_pickle, dbus_interface=MESH_IFACE)
    
    # Ask for other's jokes back
    #self.HelloBack(sender)



  # b -> I am a buddy who be receiving some state
  @method(dbus_interface=MESH_IFACE, 
          in_signature='s', 
          out_signature='')
  def PumpActivityState(self, state_pickle):
    state_pickle = str(state_pickle)
    #logging.info('I JUST RECEIVED PICKLE TYPE: %r - %s (PumpActivityState)', type(state_pickle), state_pickle)
    if len(state_pickle) == 0:
      logging.debug('JokeMachineSession.ReceiveActivityState() -> empty state_pickle - creating empty state')
      activity_state = JokeMachineState().test_data()
    else:
      logging.debug('JokeMachineSession.ReceiveActivityState() -> Unpickling state from remote')
      activity_state = JokeMachineState.loads(state_pickle)
    Globals.set_activity_state(activity_state) 
    
    # refresh activity ui
    Globals.JokeMachineActivity.refresh()
    logging.debug('Finished receiving state')    
    

  # c -> I am the connecting buddy, I can send some state back here if I want
  @signal(dbus_interface=MESH_IFACE, signature='s')
  def HelloBack(self, recipient):
      """Respond to Hello.
      recipient -- string, sender of Hello.
      """

  def helloback_cb(self, recipient, sender):
    """Reply to Hello.

        recipient -- string, the XO who send the original Hello.

        Other XOs should ignore this signal.
        """
    logging.debug('*** In helloback_cb: recipient: %s, sender: %s' %
                       (recipient, sender))
    if sender == self.my_bus_name:
      # Ignore my own signal
      return
    if recipient != self.my_bus_name:
      # This is not for me
      return
    
    # anything ?


  # d -> I am the connecting buddy, I have a joke to submit to you
  @signal (dbus_interface=MESH_IFACE, signature='us')
  def Submit(self, jokebook_id, joke_pickle):
    '''Submit a joke'''
    
  def submit_cb(self, jokebook_id, joke_pickle, sender=None):
    '''Receive someones submission
    jokebook_id -- the jokebook to submit joke to
    joke_pickle -- a pickled joke'''
    if sender == self.my_bus_name: # don't respond to own submit signal
      return
    logging.debug('In submit_cv. sender: %r' % sender)
    
    # 1. unpickle joke
    joke_pickle = str(joke_pickle)
    if len(joke_pickle) == 0:
      logging.debug('JokeMachineSession.submit_cb() -> empty joke_pickle - doing nothing')
      return
    joke = Joke.loads(joke_pickle)
    logging.debug('%s submitted a joke to my jokebook# %d with text: %s and answer %s', joke.joker, jokebook_id, joke.text, joke.answer)
    
    # 2. get the jokebook it belongs to
    jokebook = Globals.JokeMachineState.jokebook(jokebook_id)
    if jokebook is None:
      logging.error('Joke was submitted to non-existent jokebook id %d', jokebook_id)
      return
    
    # 3. add it to submissions in the appropriate jokebook
    jokebook.submissions.append(joke)
  
    # 4. TODO - show some kind of alert - ask on #sugar


  # e -> I am the initiator, I've just accepted a submission, tell everyone!
  @signal (dbus_interface=MESH_IFACE, signature='us')
  def BroadcastJoke(self, jokebook_id, joke_pickle):
    '''broadcast newly accepted submission back to the mesh'''
    
  def broadcast_joke_cb(self, jokebook_id, joke_pickle, sender):
    '''handle a BroadCast Joke by creating a new joke in the local store'''
    if sender == self.my_bus_name:
      # Ignore my own signal
      return

    logging.debug('In broadcast_joke_cb. sender: %r' % sender)
    
    # 1. unpickle joke
    joke_pickle = str(joke_pickle)
    if len(joke_pickle) == 0:
      logging.debug('JokeMachineSession.broadcast_joke_cb() -> empty joke_pickle - doing nothing')
      return
    joke = Joke.loads(joke_pickle)
    logging.debug('%s broadcast a joke to my jokebook# %d with text: %s and answer %s', joke.joker, jokebook_id, joke.text, joke.answer)
    
    # 2. get the jokebook it belongs to
    jokebook = Globals.JokeMachineState.jokebook(jokebook_id)
    if jokebook is None:
      logging.error('Joke was broadcast to non-existent jokebook id %d', jokebook_id)
      return
    
    # 3. add it to jokes in the appropriate jokebook
    jokebook.jokes.append(joke)
    
    # 4. TODO - show some kind of alert - ask on #sugar


  # ############################################################################


  def participant_change_cb(self, added, removed):
    '''Callback when tube participants change.'''
    logging.debug('In participant_change_cb')
    if added:
      logging.debug('Adding participants: %r' % added)
    if removed:
      logging.debug('Removing participants: %r' % removed)
    for handle, bus_name in added:
      buddy = self._get_buddy(handle)
      if buddy is not None:
        logging.debug('Buddy %s was added' % buddy.props.nick)
    for handle in removed:
      buddy = self._get_buddy(handle)
      if buddy is not None:
        logging.debug('Buddy %s was removed' % buddy.props.nick)
        
        # TODO - participant changed
        # Set buddy's polls to not active so I can't vote on them
        #for poll in self.activity._polls:
          #if poll.author == buddy.props.nick:
            #poll.active = False
            #logging.debug(
              #'Closing poll %s of %s who just left.' %
              #(poll.title, poll.author))

    if not self.entered:
      if self.is_initiator:
        logging.debug("I'm initiating the tube")
      else:
        logging.debug('Joining, sending Hello')
        self.Hello()
      self.tube.add_signal_receiver(self.hello_cb, 
                                    'Hello', 
                                    MESH_IFACE,
                                    path=MESH_PATH, 
                                    sender_keyword='sender')
      self.tube.add_signal_receiver(self.helloback_cb, 
                                    'HelloBack',
                                    MESH_IFACE, 
                                    path=MESH_PATH, 
                                    sender_keyword='sender')
      self.tube.add_signal_receiver(self.submit_cb, 
                                    'Submit', 
                                    MESH_IFACE,
                                    path=MESH_PATH, 
                                    sender_keyword='sender')
      self.tube.add_signal_receiver(self.broadcast_joke_cb, 
                                    'BroadcastJoke', 
                                    MESH_IFACE, 
                                    path=MESH_PATH, 
                                    sender_keyword='sender')
      
      self.my_bus_name = self.tube.get_unique_name()
      self.entered = True


