#!/usr/bin/env python3
# Author: infosecravindra


import argparse                        # For CLI arguments
import certifi                         # For HTTPS support
import pycurl                          # For making network requests
import random                          # For choosing random UA
import sys                             # For unexpected exit
from io import BytesIO                 # For buffering curl data
from multiprocessing import Pool       # For parallel processing


# Argument stuff
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--inputfile', default='input.txt', help='input file')
ap.add_argument('-o', '--outputfile', default='output.txt', help='output file')
ap.add_argument('-t', '--threads', default=200, help='threads')
args = ap.parse_args()

# Global variables
user_agents = set()             # Empty UA set
inputfile = args.inputfile
outputfile = args.outputfile
max_process = 50
success = 0
timeout = 5
total = 0
num_lines = sum(1 for line in open(inputfile))


def read_ua():                  # Read all UA
  user_agents.add("Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0")
  user_agents.add("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0")
  user_agents.add("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
  user_agents.add("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")


def random_ua():                # Get Random UA
  return random.sample((user_agents),1)[0]


def check_domain(raw_url):    # Network call
  final_url = raw_url.strip()
  if final_url != "":
    final_url = final_url + "/.git/HEAD"

    try:
      buffer = BytesIO()

      c = pycurl.Curl()    
      c.setopt(c.CAINFO, certifi.where())
      c.setopt(c.WRITEDATA, buffer)
      c.setopt(pycurl.ACCEPT_ENCODING, 'identity')
      c.setopt(pycurl.FOLLOWLOCATION, 1)
      c.setopt(pycurl.TIMEOUT, timeout)             # Refer Global Variable
      c.setopt(pycurl.URL, final_url)
      c.setopt(pycurl.USERAGENT, random_ua())
      c.perform()
      c.close()

      body = buffer.getvalue().decode('iso-8859-1')
      buffer.close()

      if "ref: refs" in body:
        write_domain(final_url)

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
    fout =  open(outputfile, 'a')
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
    domains = open(inputfile, "r").readlines()

  except FileNotFoundError as e:
    print(e)
    exit(e.errno)

  print("Scanning...")
  pool = Pool(processes = max_process)
  pool.map(check_domain, domains)
  print("Finished")
