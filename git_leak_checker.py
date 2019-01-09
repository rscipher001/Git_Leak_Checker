#!/usr/bin/env python3
# Author: infosecravindra


import argparse                        # For CLI arguments
import certifi                         # For HTTPS support
import pycurl                          # For making network requests
import random                          # For choosing random UA
import sys                             # For unexpected exit
from io import BytesIO                 # For buffering curl data


# Argument stuff
parser = argparse.ArgumentParser(description='Check .git leaks on domains')
requiredNamed = parser.add_argument_group('required arguments')
requiredNamed.add_argument('-i', help="This file contains all domain list", dest='input_file', required=True)
parser.add_argument('-o', help="This file will contain vulnerable domains", default='vulnerable_domains.txt', dest='output_file')
parser.add_argument('-t', help="Set curl timeout value, default is 10", default=10, type=int, dest='timeout')
args = parser.parse_args()


# Global variables
user_agents = set()             # Empty UA set
input_file = args.input_file
output_file = args.output_file
timeout = args.timeout
success = 0
total = 0
num_lines = sum(1 for line in open(input_file))


def read_ua():                  # Read all UA
  user_agents.add("Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0")
  user_agents.add("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0")
  user_agents.add("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
  user_agents.add("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")


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
    c.setopt(pycurl.TIMEOUT, timeout)             # Refer Global Variable
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

          print("\rProgress: {}/{} | Success: {}".format(total, num_lines, success), end = "")

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
