#!/usr/bin/python
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


import sys
sys.path.append('..')

#import json
import cPickle

from persistence.joke import Joke
from persistence.jokebook import Jokebook
from persistence.jokemachinestate import JokeMachineState

from util.decorators import Property

# ##############################################################################
# test Property decorator
#


from util.audioplayer import AudioPlayer

audio = AudioPlayer()
#audio.uri = '/home/antoine/Projects/dev.laptop.org/sugar-jhbuild/build/share/activities/JokeMachine.activity/resources/laugh_attack.wav'
audio.uri = '/home/antoine/Projects/dev.laptop.org/sugar-jhbuild/source/sugar/data/startup.flac'
audio.play()

sys.exit()

#class Foo(object):
  
  #@Property
  #def all():
    #def get(self): return self.__all
    #def set(self, value): self.__all = value
    #def default(self): return 'this is a default value'
    
  #@Property
  #def onlyget():
    #def get(self): return self.__onlyget
      
  #@Property
  #def nodefault():
    #def get(self): return self.__nodefault
    #def set(self, value): self.__nodefault = value
      
  
#help(Property)
#foo = Foo()

#print foo.all
#Foo.all = 'changed'
#print foo.all

#print foo.nodefault
#foo.nodefault = 'set now'
#print foo.nodefault

#print foo.onlyget
#foo.onlyget = 'cannot set this'


def f(x):
  ret = 0
  counter = x
  while (counter != 0):
    ret = ret + x
    counter = counter - 1
  return ret


buf = []
def g(x):
  if len(buf) <= x:
    curpos = len(buf)
    for i in range(curpos, x + 1):
      buf.insert(i, i * i)
  return buf[x]
  
  

print g(4)
print g(1)
#print g(2)
#print g(3)
print g(8)
print g(6)

sys.exit()

class Plink(object):
  def __init__(self):
    self.b = 'a'

class Plonk(Plink):
  def __init__(self):
    self.b = 'a'

class Foo(Plonk):
  def __init__(self):
    
    self.a = 'a'

class Bar(Foo):
  def plonk(self, value):
    value = 'b'
    
bar = Bar()

def list_bases(c):
  bases = []
  print 'looking at: ', c
  if not hasattr(c, '__bases__'):
    print 'quitting at', c
    print dir(c)
    return bases
  
  for base in c.__bases__:
    print 'Has base: ', base
    bases.append(base)
    if len(base.__bases__) > 0:
      bases.append(list_bases(base.__bases__))
      
  return bases
  
print list_bases(bar.__class__)

sys.exit()


# ##############################################################################
# test PersistentProperty decorator
#

# dump properties on persistent objects
def dump(obj, indent = '  '):
  print indent + str(obj)
  for name, prop in obj.__properties__:
    value = prop.fget(obj)
    print indent + name, '=', value #, ' "' + prop.__doc__ + '"'
    if value.__class__ is list:
      for item in value:
        dump(item, indent + '  ')

  print indent + 'is_dirty =', obj.__dirty__




state = JokeMachineState()
state = state.test_data()
dump(state)
print "\n========================================================================\n"
pickle = state.dumps()
j = JokeMachineState.loads(pickle)
jokebook = j.jokebooks[0]
jokebook.owner = 'new owner'
dump(j)



sys.exit()


joke = Joke()

print 'Joke.id.doc: ', Joke.id.__doc__
print 'Joke.joke_text.doc: ', Joke.text.__doc__
print

print 'joke.id default should be 0 = ', joke.id
print 'joke is dirty = ', joke.__dirty__
print

joke.id = 66
print 'joke.id set to 66 = ', joke.id
print 'joke is dirty = ', joke.__dirty__
print

print 'joke.joke_text has no default:', joke.text
joke.text = 'joke text'
print 'joke.joke_text has been set to \'joke text\' = ', joke.text
print

print 'joke.id is still 66 = ', joke.id
joke.id = 23
print

print 'joke.id set to 23 = ', joke.id
print


jokebook = Jokebook()
dump(jokebook)
print

jokebook.jokes.append(joke)
dump(jokebook)
print 

j = jokebook.jokes[0]
j.id = 991

dump(jokebook)

print "========================================================================\n"

# ##############################################################################
# test Pickling
#
#jokebook.__dirty__ = False
#jokebook.jokes[0].__dirty__ = False

p = cPickle.dumps(jokebook)
#print p
#o = cPickle.loads(p)

#dump(o)
#dump(o.jokes[0])

print 'Persisting...'
print
jokebook.id = 0
dump(jokebook)
print
pickle = jokebook.dumps()
j = Jokebook.loads(pickle)
dump(j)

#print j.jokes.__class__

#print joke
#print joke.__dirty__
#print joke.dirty
#print joke.pdirty


# json
#p = json.write(j.__dict__)
#print p
#d = json.read(p)
#o = Joke()
#o.__dict__ = d
#print o.id

# pickle
#p = cPickle.dumps(j)
#print p
#o = cPickle.loads(p)
#print o.id
#print o.some_prop
#print o.fn()


#meta
#class meta(type):
  #def __init__(cls, name, bases, dct):
    #print 'Init is called: ' + str(cls) + str(name) + str(bases) + str(dct)

    #method_list = []
    #for func in dct.values():
      #try:
        #method_name = func._dbus_method_name()
        #print func, method_name
        #method_list.append(method_name)
      #except:
        #pass 

    #print method_list
    #super(meta, cls).__init__(name, bases, dct)

#def method(func):
  #def decorator(self, *args):
    #func(self, *args)

  #def _dbus_method_name():
    #return 'dbus_' + func.__name__

  #decorator._dbus_method_name = _dbus_method_name
  #return decorator


#class bar:
  #__metaclass__ = meta

  #@method
  #def my_method(self):
    #print 'my_first_method'
    
  #@method
  #def another_method(self):
    #print 'my_other_method'

#x = bar()
#x.my_method()

#print x.my_method._dbus_method_name

