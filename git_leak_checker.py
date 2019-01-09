#!/usr/bin/env python
# Author: infosecravindra

import argparse                        # For CLI arguments
import certifi                         # For HTTPS support
import pycurl                          # For making network requests
import random                          # For choosing random UA
import sys                             # For unexpected exit
from io import BytesIO                 # For buffering curl data


# Argument stuff
parser = argparse.ArgumentParser(description='Check .git leaks on domains')
parser.add_argument('input_file', help="Name of file contains domain list")
parser.add_argument('output_file', help="This file will be written on positive find")
args = parser.parse_args()


# Global variables
user_agents = set()             # Empty UA set
input_file = args.input_file
output_file = args.output_file
num_lines = sum(1 for line in open(input_file))
total = 0
success = 0

def read_ua():                  # Read all UA
  try:
    with open('user-agents.txt') as user_agents_file:
      for user_agent in user_agents_file:
        user_agents.add(user_agent.strip())

  except KeyboardInterrupt:
    print ("Ctrl-c pressed ...")
    sys.exit(1)

  except Exception as e:
    print('Error: %s' % e)
    sys.exit(1)


def random_ua():                # Get Random UA
  return random.sample((user_agents),1)[0]


def check_domain(final_url):    # Network call
  try:
    buffer = BytesIO()

    c = pycurl.Curl()    
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(pycurl.ACCEPT_ENCODING, 'identity')
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.TIMEOUT, 10)
    c.setopt(pycurl.URL, final_url)
    c.setopt(pycurl.USERAGENT, random_ua())
    c.perform()
    c.close()

    body = buffer.getvalue().decode('iso-8859-1')
    buffer.close()
    return body

  except pycurl.error:
    return ""

  except KeyboardInterrupt:
    print ("Ctrl-c pressed ...")
    sys.exit(1)

  except Exception as e:
    print('Error: %s' % e)
    sys.exit(1)


def write_domain(url):          # Write vulnerables domains to output file
  try:
    fout =  open(output_file, 'a')
    fout.write("\n" + url)
    fout.close()

  except KeyboardInterrupt:
    print ("Ctrl-c pressed ...")
    sys.exit(1)

  except Exception as e:
    print('Error: %s' % e)
    sys.exit(1)


if __name__ == "__main__":      # Main
  read_ua()
  try:
    with open(input_file) as urls:
      for raw_url in urls:
        if raw_url != "":
          url = raw_url.strip()
          total = total + 1
          print("Progress:", total, "/", num_lines, ", Success:", success, "\r", end="")
          final_url = url + "/.git/HEAD"
          body = check_domain(final_url)

          if "ref: refs" in body:
            write_domain(url)
            success = success + 1

  except KeyboardInterrupt:
    print ("Ctrl-c pressed ...")
    sys.exit(1)

  except Exception as e:
    print('Error: %s' % e)
    sys.exit(1)
