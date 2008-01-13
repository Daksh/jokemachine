#!/usr/bin/python
#
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
sys.path.append('..')

from persistence.jokemachinestate import JokeMachineState

def dump(obj, indent = '  '):
  print indent + str(obj)
  for name, prop in obj.__properties__:
    value = prop.fget(obj)
    print indent + name, '=', value #, ' "' + prop.__doc__ + '"'
    if value.__class__ is list:
      for item in value:
        dump(item, indent + '  ')

  print indent + 'is_dirty =', obj.__dirty__




state = JokeMachineState().test_data()

print state.jokebooks
print state.next_jokebook_id

#[max(joke.id) for joke in self.__jokes]

#pickle = state.dumps()
#new_state = JokeMachineState.loads(pickle)
#dump(new_state)


