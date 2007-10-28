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

import locale
import gtk

from abiword import Canvas as AbiCanvas


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
    """Load the lesson content from a .abw, taking l10n into account.

        path -- string, path of lesson plan file, e.g. lessons/Introduction
        lesson -- string, name of lesson
        """
    code, encoding = locale.getdefaultlocale()
    canvas = AbiCanvas()
    canvas.show()
    files = map(lambda x: os.path.join(path, '%s.abw' % x),
                ('_'+code.lower(), '_'+code.split('_')[0].lower(), 
                 'default'))
    files = filter(lambda x: os.path.exists(x), files)
    # On jhbuild, the first works, on XO image 432 the second works:
    try:
      canvas.load_file('file://%s' % files[0], 'text/plain')
    except:
      canvas.load_file('file://%s' % files[0])
    canvas.view_online_layout()
    canvas.zoom_width()
    canvas.set_show_margin(False)
    self.append_page(canvas, gtk.Label(name))
