# Modified by Dan Green 2022, Based on script by:
# Copyright (C) 2019 Matthew Lai
#
# This file is part of JLC Kicad Tools.
#
# JLC Kicad Tools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# JLC Kicad Tools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with JLC Kicad Tools.  If not, see <https://www.gnu.org/licenses/>.

import csv
import re

def ReadDB(filename):
  db = {}
  with open(filename) as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      if row[0] == "Footprint pattern":
        continue
      else:
        db[re.compile(row[0])] = int(row[1])
  return db

def FixRotation(side, posx, rot, package, db):
  rotation = float(rot)
  if side.strip() == "bottom":
    posx = "{0:.6f}".format(-float(posx))
  for pattern, correction in db.items():
    if pattern.match(package):
      print("Footprint {} matched {}. Applying {} deg correction"
          .format(package, pattern.pattern, correction))
      if side.strip() == "bottom":
          rotation = (rotation - correction) % 360
      else:
          rotation = (rotation + correction) % 360
      rot = "{0:.6f}".format(rotation)
      break
  return (posx, rot)

