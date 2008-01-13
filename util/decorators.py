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

import sys


# Courtesy of: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/465427
DecoratorWithArgs = \
  lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)



def Property(function):
  '''Property Decorator
     Adapted from: http://wiki.python.org/moin/PythonDecoratorLibrary

     Example: 
      
        class Foo(object):
          @Property
          def my_property():
            def get(self): return self.__my_property
            def set(self, value): self.__my_property = value  # (optional)
            def default(self): return 'some default value'    # (optional)
  '''
  
  keys = 'set', 'del'
  func_locals = {'doc':function.__doc__}
  
  def fgetter(obj, name, getter, fdef):
    attr_name = '_' + obj.__class__.__name__ + '__' + name
    if not hasattr(obj, attr_name):
      setattr(obj, attr_name, fdef(obj))
    return getter(obj)
  
  def introspect(frame, event, arg):
    if event == 'return':
      locals = frame.f_locals
      func_locals.update(dict(('f' + k,locals.get(k)) for k in keys))
      if locals.has_key('default'):
        func_locals['fget'] = lambda obj : fgetter(obj, function.__name__, locals['get'], locals['default'])
      else:
        func_locals['fget'] = lambda obj : fgetter(obj, function.__name__, locals['get'], lambda x : None)
      
      sys.settrace(None)
    return introspect
  
  sys.settrace(introspect)
  function()
  
  return property(**func_locals)

