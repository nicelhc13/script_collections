import argparse
import statistics

parse = argparse.ArgumentParser(description='Parse and extract actual/expected runtime')
parse.add_argument('-actual', metavar='actual', type=str, help='The output file of run.py')
parse.add_argument('-expect', metavar='expect', type=str, help='The output file of viz.py')
parse.add_argument('-output', metavar='output', type=str, help='The output file of this script')
parse.add_argument('-branch', metavar='branch', type=str, help='Git branch used')

args = parse.parse_args()

"""
@param ap actual data path
@param ep expected data path
@param op output path of parsing
"""
def parse(ap: str, ep: str, op: str, branch: str):
  # Parse time information.
  with open(ap) as f:
    actual_summary = f.readlines()
    actual_summary = actual_summary[-4:-3]
  #with open(ep) as f:
    #expect_summary = f.readlines()
    #expect_summary = expect_summary[-3:-2]

  #print(actual_summary)
  actual_median = actual_summary[0].split(' Median = ')[1].split('\n')[0]
  #expect_summary = expect_summary[0].split(': ')[1]
  #expect_summary = expect_summary.split(' seconds')[0]

  #print("Median time:", actual_median)
  #print("Expected summary:", expect_summary)

  # Parse file name for labels.
  label = ap.split('/')[-1].split('.out')[0]
  if "random" in label:
    label = "Random"
  elif "independent" in label:
    label = "Independent"
  elif "serial" in label:
    label = "Serial"
  elif "reduce" in label:
    label = "Reduction"

  dm_type = "Eager"
  if "lazy" in ap:
    dm_type = "Lazy"

  placement_type = "Policy"
  if "user" in ap:
    placement_type = "User"

  comp_ratio="C95%vsD5%"
  if "80%" in ap:
    comp_ratio="C80%vsD20%"

  num_gpus = 1
  if "2g" in ap:
    num_gpus = 2
  elif "4g" in ap:
    num_gpus = 4

  gbranch = branch

  #label = label+"("+placement_type+","+comp_ratio+")"
  sub_label = "("+comp_ratio+")"
  #print("Label:", label)
  print("Synthetic,", label, ",Frontera,Parla,", dm_type, ",", placement_type, ",", num_gpus, ",", gbranch, ",Yes,", actual_median)

  with open(op, "a+") as f:
    if not ("Policy" in placement_type and "Lazy" in dm_type):
      f.write("Synthetic,"+label+",Frontera,Parla,"+gbranch+","+dm_type+","+placement_type+","+str(num_gpus)+","+actual_median+","+sub_label+"\n")
    #f.write(label+","+str(avg_time)+","+expect_summary+"\n")

if __name__ == '__main__':
  #print("Output of run.py (actual data): ", args.actual)
  #print("Output of viz.py (expected data): ", args.expect)
  #print("Output path: ",  args.output)
  #print("Placement policy: ", args.policy)
  #print("Git branch: ", args.branch)
  parse(args.actual, args.expect, args.output, args.branch)
