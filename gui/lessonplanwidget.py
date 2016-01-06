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
import locale
import gtk
import logging
from gettext import gettext as _
#from gi.repository import Gtk

class LessonPlanWidget(gtk.Notebook):
  
  def __init__ (self, basepath):
    """Create a Notebook widget for displaying lesson plans in tabs.

        basepath -- string, path of directory containing lesson plans.
        """
    super(LessonPlanWidget, self).__init__()
    lessons = filter(lambda x: os.path.isdir(os.path.join(basepath, 'lessons', x)),
                               os.listdir(os.path.join(basepath, 'lessons')))
    lessons.sort()
    for lesson in lessons:
      self._load_lesson(os.path.join(basepath, 'lessons', lesson),
                        _(lesson))


  def _load_lesson (self, path, name):
    """Load the lesson content from a .txt, taking l10n into account.

        path -- string, path of lesson plan file, e.g. lessons/Introduction
        lesson -- string, name of lesson
        """
    code, encoding = locale.getdefaultlocale()
    logging.debug('Locale code: %r' % code)
    if code is None or encoding is None:
      locale.setlocale(locale.LC_ALL, 'en_US')
      code, encoding = locale.getlocale()
    #canvas = Gtk.TextView()
    canvas = gtk.TextView()
    canvas.show()
    canvas.set_wrap_mode(gtk.WRAP_WORD)

    files = map(lambda x: os.path.join(path, '%s.txt' % x),
                ('_'+code.lower(), '_'+code.split('_')[0].lower(), 
                 'default'))
    files = filter(lambda x: os.path.exists(x), files)

    with open(files[0],'r') as f:
      text = f.read()
      canvas.get_buffer().set_text(text)

    self.append_page(canvas, gtk.Label(name))
