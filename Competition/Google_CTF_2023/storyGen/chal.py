import time
import os

time.sleep(0.1)

print("Welcome to a story generator.")
print("Answer a few questions to get started.")
print()

name = input("What's your name?\n")
where = input("Where are you from?\n")

def sanitize(s):
  return s.replace("'", '').replace("\n", "")

#name = sanitize(name)
#where = sanitize(where)

STORY = """

#@NAME's story

NAME='@NAME'
WHERE='@WHERE'

echo "$NAME came from $WHERE. They always liked living there."
"""


open("/tmp/script.sh", "w").write(STORY.replace("@NAME", name).replace("@WHERE", where).strip())
os.chmod("/tmp/script.sh", 0o777)

while True:
  s = input("Do you want to hear the personalized, procedurally-generated story?\n")
  if s.lower() == "no":
    break
  print()
  print()
  os.system("/tmp/script.sh")
  print()
  print()

print("Bye!")
