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

import pickle 


class JournalPickler:
  '''Works with util.Persistence to persist objects to the Sugar Journal'''
  
  def __init__(self, obj = None):
    pass

  def __set_dirty(self, obj, is_dirty):
    obj.__dirty__ = False 
    for name, prop in obj.__properties__:
      if prop.fget(obj).__class__ is list:
        for item in prop.fget(obj):
          if hasattr(item, '__dirty__'):
            self.__set_dirty(item, is_dirty)


  def dumps(self, obj, deep_dump):
    self.__set_dirty(obj, False)
    pickled = pickle.dumps(obj)
    return pickled

  
  def loads(self, pickled):
    obj = pickle.loads(pickled)
    self.__set_dirty(obj, False)
    return obj


dumps = lambda obj, deep=False : JournalPickler(obj).dumps(obj, deep)
loads = JournalPickler().loads
