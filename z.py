#!/usr/bin/python3

import json,os,sys,argparse

circuit={}
circuitTime={}
circuitOp={}
timeline=None

parser = argparse.ArgumentParser()
parser.add_argument("--filename", type=str, required=False, default='test', nargs='?', help="name of the JSON source file, in FEATHER format (defaut name: test.json)")
parser.add_argument("--debug", type=bool, nargs='?', default=False, help="toggles debug mode (default: False")
parser.add_argument("--name", type=str, required=True, nargs='?', help="name of the series in the source file")
parser.add_argument("--origin", type=str, required=True, nargs='?', help="origin of the equivalence to be proved")
parser.add_argument("--endpoint", type=str, required=True, nargs='?', help="endpoint of the equivalence to be proved")
args = parser.parse_args()

debug=args.debug
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
  run_pass(source, destination, scope, 'G')
  run_pass(source, destination, scope, 'M')

def run_pass(source, destination, scope, pss):
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
#    if (source!=LHS and source!=RHS and destination!=LHS and destination!=RHS):
    else:
      if pss=='M':
        if LHS not in circuit and RHS in circuit:
          circuit[LHS]=RHS
          circuitTime[LHS]=time
          circuitOp[LHS]='M'
        if RHS not in circuit and LHS in circuit:
          circuit[RHS]=LHS
          circuitTime[RHS]=time
          circuitOp[RHS]='M'
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

if source==destination:
  print("ERROR: source and destination must not be identical")
  sys.exit(1)

find_circuit(source,destination,scope)

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
