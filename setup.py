#!/usr/bin/env python
try:
  from sugar.activity import bundlebuilder
  bundlebuilder.start("JokeMachine")
except ImportError:
  print 'Cannot find a working sugar environment'

