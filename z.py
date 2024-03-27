#!/usr/bin/python3

import json,os,sys,hashlib,argparse

circuit={}
circuitTime={}
circuitOp={}
timeline=None

terms_store=None
reverse_store=None

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, required=False, default='test', nargs='?', help="name of the JSON source file, in FEATHER format (defaut name: test.json)")
parser.add_argument("--debug", type=bool, nargs='?', default=False, help="toggles debug mode (default: False")
parser.add_argument("--canonical", nargs='?', default=False, type=bool, help="generates partition in canonical form (default: False)")
parser.add_argument("--name", type=str, required=True, nargs='?', help="name of the series in the source file")
parser.add_argument("--origin", type=str, required=True, nargs='?', help="origin of the equivalence to be proved")
parser.add_argument("--endpoint", type=str, required=True, nargs='?', help="endpoint of the equivalence to be proved")
args = parser.parse_args()

debug=args.debug
canonical=args.canonical
filename=args.filename
scope=args.name
source=args.origin
destination=args.endpoint

def load_file(filename):
  global timeline
  try:
    with open(f"{filename}", 'r') as f:
      timeline = json.load(f)
  except:
    print("cannot load input file.")
    sys.exit(1)

def sort_by_first_term(l):
  return l[0]

def contents_addressable(json_obj):
  json_string = json.dumps(json_obj, sort_keys=True)
  return hashlib.sha256(json_string.encode()).hexdigest()

def build_canonical_partition(scope):
  global terms_store
  global reverse_store
  found=False
  maxId=-1
  origClasses=None
  terms=set()
  canonical_classes=[]
  for aT in timeline:
    if aT['name']==scope:
      found=True
      timeseries=aT['history']
      break
  if not found:
    return None
  found=False
  for aS in timeseries:
    if aS['id']>maxId:
      maxId=aS['id']
      origClasses=aS['classes']
      found=True
  if not found:
    return None
  for aO in origClasses:
    for aT in aO:
      if aT not in terms:
        terms.add(aT)
  sorted_terms=sorted(list(terms))
  terms_store = {"TERM"+str(i): sorted_terms[i] for i in range(len(sorted_terms))}
  reverse_store = {string: "TERM"+str(index) for index, string in enumerate(sorted_terms)}
  for aO in origClasses:
    canonical_terms=set()
    for aT in aO:
      canonical_terms.add(reverse_store[aT])
    canonical_class=sorted(list(canonical_terms))
    canonical_classes.append(canonical_class)
  canonical_partition=sorted(canonical_classes,key=sort_by_first_term)
  return canonical_partition,contents_addressable(canonical_partition)

def find_last_common_class(source, destination, scope):
  found=False
  for aT in timeline:
    if aT['name']==scope:
      found=True
      break
  if not found:
    print(f"series {scope} not found in source file")
    sys.exit(1)
    return None,None,None,None
  equality=None
  operation=None
  LHS=None
  RHS=None
  timeseries=aT['history']
  for step in timeseries:
    found=False
    for ec in step['classes']:
      if source in ec and destination in ec:
        found=True
        LHS=step['equality']['LHS']
        RHS=step['equality']['RHS']
        op=step['op']
        time=step['id']
        break
    if found:
      break
  if found:
    return time,op,LHS,RHS
  else:
    print(source,"and",destination,"are not equivalent")
    print("(common class not found)")
    sys.exit(1)
    return None,None,None,None

def find_circuit(source, destination, scope):
  global circuit
  global circuitTime
  global circuitOp
  if source==destination:
    return
  time,op,LHS,RHS=find_last_common_class(source,destination,scope)
  if op=='M':
    if (source==LHS or source==RHS) and (destination==LHS or destination==RHS):
      if source==LHS:
        circuit[source]=RHS
        circuitTime[source]=time
        circuitOp[source]='M'
      elif source==RHS:
        circuit[source]=LHS
        circuitTime[source]=time
        circuitOp[source]='M'
      if destination==LHS:
        circuit[RHS]=destination
        circuitTime[RHS]=time
        circuitOp[RHS]='M'
      elif destinaion==RHS:
        circuit[LHS]=destination
        circuitTime[LHS]=time
        circuitOp[LHS]='M'
      return
    if source==LHS or source==RHS:
      if source==LHS:
        circuit[source]=RHS
        circuitTime[source]=time
        circuitOp[source]='M'
        time2,op2,LHS2,RHS2=find_last_common_class(RHS,destination,scope)
        if time2!=time:
          find_circuit(RHS,destination,scope)
      elif source==RHS:
        circuit[source]=LHS
        circuitTime[source]=time
        circuitOp[source]='M'
        time3,op3,LHS3,RHS3=find_last_common_class(LHS,destination,scope)
        if time3!=time:
          find_circuit(LHS,destination,scope)
    elif destination==LHS or destination==RHS:
      if destination==LHS:
        circuit[RHS]=destination
        circuitTime[RHS]=time
        circuitOp[RHS]='M'
        time2,op2,LHS2,RHS2=find_last_common_class(source,RHS,scope)
        if time2!=time:
          find_circuit(source,RHS,scope)
      elif destination==RHS:
        circuit[LHS]=destination
        circuitTime[LHS]=time
        circuitOp[LHS]='M'
        time3,op3,LHS3,RHS3=find_last_common_class(source,LHS,scope)
        if time3!=time:
          find_circuit(source,LHS,scope)
    if (source!=LHS and source!=RHS and destination!=LHS and destination!=RHS):
      circuit[LHS]=RHS
      circuitTime[LHS]=time
      circuitOp[LHS]='M'
      time2,op2,LHS2,RHS2=find_last_common_class(RHS,destination,scope)
      if time2!=time:
        find_circuit(RHS,destination,scope)
      time2,op2,LHS2,RHS2=find_last_common_class(LHS,destination,scope)
      if time2!=time:
        find_circuit(LHS,destination,scope)
      time2,op2,LHS2,RHS2=find_last_common_class(source,RHS,scope)
      if time2!=time:
        find_circuit(source,RHS,scope)
      time2,op2,LHS2,RHS2=find_last_common_class(source,LHS,scope)
      if time2!=time:
        find_circuit(source,LHS,scope)
  elif op=='G':
    if (source==LHS or source==RHS) and (destination==LHS or destination==RHS):
      circuit[source]=destination
      circuitTime[source]=time
      circuitOp[source]='G'
      return
    if (source==LHS or source==RHS):
      if source==LHS:
        circuit[source]=RHS
        circuitTime[source]=time
        circuitOp[source]='G'
        find_circuit(RHS,destination,scope)
      elif source==RHS:
        circuit[source]=LHS
        circuitTime[source]=time
        circuitOp[source]='G'
        find_circuit(LHS,destination,scope)
      return
    elif (destination==LHS or destination==RHS):
      if destination==LHS:
        circuit[RHS]=destination
        circuitTime[RHS]=time
        circuitOp[RHS]='G'
        find_circuit(source,RHS,scope)
      elif destination==RHS:
        circuit[LHS]=destination
        circuitTime[LHS]=time
        circuitOp[LHS]='G'
        find_circuit(source,LHS,scope)
      return
  else:
    return

load_file(filename)
#source='a'
#destination='b'
#scope='RG0'

find_circuit(source,destination,scope)
if canonical:
  cp,hx=build_canonical_partition(scope)
  jo={}
#  jo['terms']={}
  jo['partition']={}
  jo['partition']['classes']=cp
  jo['partition']['address']=hx
#  print(len(terms_store))
#  for ts in terms_store:
#    jo['terms'][ts]=terms_store[ts]
  with open(f"{hx}.json", 'w') as f:
    json.dump(jo,f, sort_keys=True,indent=2)
  print("")
  print("Canonical partition:",hx)
  print("  number of classes:",len(cp))
  print("  number of terms:",len(terms_store))
cnt=-1
done=False
if source in circuit:
  curr=source
else:
  print(source,"and",destination,"are not equivalent")
  print("(origin not found in partition)")
  sys.exit(1)
proof=''

while not done and cnt<100000:
  cnt+=1
  proof+="("+str(circuitTime[curr])+") "+curr+" -["+circuitOp[curr]+"]-> "+circuit[curr]+"\n"
  curr=circuit[curr]
  done=curr not in circuit
if cnt>=100000:
  print("too many attempts.")
  sys.exit(1)
if not done:
  print(source,"and",destination,"are not equivalent")
  sys.exit(1)
else:
  print("")
  print("*** Proof Of Equivalence between",source,"and",destination,"***")
  print("")
  print(proof)
  sys.exit(0)
