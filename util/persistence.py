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


class Persistent(type):
  '''Metaclass providing object persistence'''
  def __init__(cls, name, bases, dct):
    super(Persistent, cls).__init__(name, bases, dct)
    
    setattr(cls, '__dirty__', False)
    setattr(cls, '__properties__', filter(_is_persistent, dct.iteritems()))

    from util.journalpickler import dumps, loads
    setattr(cls, 'dumps', dumps)
    setattr(cls, 'loads', loads)



def PersistentProperty(function):
  '''Decorator to set up persistent properties
     Adapted from: http://wiki.python.org/moin/PythonDecoratorLibrary
  '''
  
  func_locals = {'doc':function.__doc__}

  def fgetter(obj, name, getter, fdef):
    attr_name = '_' + obj.__class__.__name__ + '__' + name
    if not hasattr(obj, attr_name):
      setattr(obj, attr_name, fdef(obj))
    return getter(obj)
  
  def fsetter(obj, name, setter, value):
    setattr(obj, '__dirty__', True) # TODO -> Propogate dirty flag up to any
                                    #         parent objects ?
    return setter(obj, value)
  
  def introspect(frame, event, arg):
    if event == 'return':
      locals = frame.f_locals
      if locals.has_key('delete'):
        func_locals['fdel'] = locals['delete']
      if locals.has_key('set'):
        func_locals['fset'] = \
          lambda obj, value : fsetter(obj, function.__name__, locals['set'], value)
      if locals.has_key('default'):
        get_function = lambda obj : fgetter(obj, function.__name__, locals['get'], locals['default'])
      else:
        get_function = lambda obj : fgetter(obj, function.__name__, locals['get'], lambda x : None)
      get_function.__decorator__ = PersistentProperty # tag the getter so we can id the
                                                      # decorator. Yeah, it's ugly.
      func_locals['fget'] = get_function
      sys.settrace(None)
    return introspect
  sys.settrace(introspect)
  function()
  return property(**func_locals)


# a wee bit ugly
def _is_persistent(item):
  '''check if property is decorated with PersistentProperty decorator'''
  prop = item[1]
  return type(prop) is property and \
         hasattr(prop.fget, '__decorator__') and \
         prop.fget.__decorator__ is PersistentProperty


