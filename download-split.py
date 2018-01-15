#!/usr/bin/python3
import urllib.request
import yaml
import itertools
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='specify yaml-file (default: download.split.yml)')
args = parser.parse_args()



if (args.file):
   stream=args.file
else:
   stream = open('download-split.yml','r')

all = yaml.load_all(stream)
data = next(all)

url_pattern = data['url']
print (url_pattern)

size = data['placeholders']

print(size[0])

def tryset(x):
    try:
       return x['set']
    except:
       return []
	   

iter = list(map(lambda x: x['start'], size))
min =  list(map(lambda x: x['start'], size))

print(iter)
max = list(map(lambda x: x['end'], size))

set = list(map(lambda x: tryset(x), size))
type = list(map(lambda x: x['type'], size))

have_output = False

try:
   output = data['output']
   f = open(output, 'wb')
   have_output = True
except:
   print("Nothing")
   # Nothing to do
  
print(set)


def chain(it):
    r = []
    for dim in range(0,len(it)):
      if type[dim] == ['range']:
        r.append(it[dim])
      elif type[dim] == ['range', 'set']:
        r.append(it[dim])
        r.append(set[dim][it[dim]-min[dim]])
      elif type[dim] == ['set', 'range']:
        r.append(set[dim][it[dim]-min[dim]])
        r.append(it[dim])
      elif type[dim] == ['set']:
        r.append(set[dim][it[dim-min[dim]]])
       
    print(r)
    return (r)
  
finished = False

while not finished:
    my_iter = chain(iter)
    url = url_pattern.format(*my_iter)
    print (url)

    file_name = url.split('/')[-1]
	
    try:
       pos = file_name.index('?')
       file_name = file_name[:pos]
    except:
       print("Nothing found")
       # Nothin to do
	
    try:	
       u = urllib.request.urlopen(url)
       if not have_output:
          f = open(file_name, 'wb')
       meta = u.info()
       file_size = int(u.getheader("Content-Length"))
       print ("Downloading: %s Bytes: %s" % (file_name, file_size))

       file_size_dl = 0
       block_sz = 8192
       while True:
         buffer = u.read(block_sz)
         if not buffer:
            break

         file_size_dl += len(buffer)
         f.write(buffer)
         status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
         status = status + chr(8)*(len(status)+1)
         sys.stdout.write ("\r%s" % status)
         sys.stdout.flush()

       if not have_output:
         f.close()
    except:
       print("Nothing")
	   # Do Nothing
	   

    print('Ready')
	
    for dim in range(len(iter)-1, -1,-1):
      if iter[dim] < max[dim]:
        iter[dim] += 1
        break;
      iter[dim]=min[dim]
      if dim==0:
        finished = True;

if have_output:
    f.close()