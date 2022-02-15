#! /usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import csv
import re
import random

parser = argparse.ArgumentParser(
  description='Transform C++ committee poll comments from CSV to Markdown.'
)
parser.add_argument(
  'input', metavar='file', type=str,
  help='input CSV file'
)
parser.add_argument(
  '-p', '--poll', metavar='N', type=int, default=0,
  help='poll number to output comments for (0 means all)'
)
args = parser.parse_args()

def key_from_position(vote):
  if vote[0] == 'Strongly Favor':
    return 0
  elif vote[0] == 'Weakly Favor':
    return 1
  elif vote[0] == 'Neutral':
    return 2
  elif vote[0] == 'Did Not Participate':
    return 3
  elif vote[0] == 'Weakly Against':
    return 4
  elif vote[0] == 'Strongly Against':
    return 5
  else:
    return -1

with open(args.input) as csvfile:
  reader = csv.reader(csvfile)

  columns = len(next(reader)) # Skip header row.

  # We have two columns that are not poll results, so `columns / 2` is one
  # greater than the number of polls. That works out nicely, because `range`'s
  # second argument is 1 past the end.
  polls = [args.poll] if args.poll != 0 else range(1, int(columns / 2))

  votes = {poll: [] for poll in polls}

  for row in reader:
    for poll in polls:
      position = row[2 * poll]
      comment  = row[2 * poll + 1]

      position = re.sub(r"I do not want to participate in this poll", "Did Not Participate", position)

      votes[poll].append([position, comment])

      # Sort by position and randomize order of votes for each position.
      random.shuffle(votes[poll])
      votes[poll].sort(key = key_from_position)

  for poll in polls:
    print('## Poll {0} ## {{#poll-{0}}}'.format(poll))
    print()

    for [position, comment] in votes[poll]:
      position = re.sub(r"^", ">\n> — ", position)

      comment = re.sub(r"^", "> ", comment)
      comment = re.sub(r"\n", "\n> ", comment)

      print(comment)
      print(position)
      print('')

