import subprocess

from starboard.env import STARBOARD_STATIC

def rebuild_site():
  subprocess.Popen(["./rebuild.sh"], env={
    "STARBOARD_STATIC": STARBOARD_STATIC
  })
