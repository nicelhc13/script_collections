import argparse

parse = argparse.ArgumentParser(description='Parse and extract actual/expected runtime')
parse.add_argument('-actual', metavar='actual', type=str, help='The output file of run.py')
parse.add_argument('-output', metavar='output', type=str, help='The output file of this script')
args = parse.parse_args()

"""
@param ap actual data path
@param op output path of parsing
"""
def parse(ap: str, op: str):
  # Parse time information.
  with open(ap) as f:
    total_time = 0
    total_iter = 0
    for num, line in enumerate(f, 1):
      if "Iteration" in line and "Outer " not in line and "Starting " not in line:
        if "Iteration 0 " in line:
          continue
        print(">>>> ", line)
        iter_time = line.split(' Graph Execution Time: ')[1]
        iter_time = iter_time.split(' seconds')[0]
        print("\t", iter_time)
        total_time += float(iter_time)
        total_iter += 1
        print("\t\t", total_time)
  avg_time = total_time/float(total_iter)

  print("Total time:", total_time)
  print("Total iter:", total_iter)
  print("Average time:", avg_time)

  # Parse file name for labels.
  label = ap.split('/')[-1].split('.out')[0]
  print("Label:", label)

  with open(op, "a+") as f:
    f.write(label+","+str(avg_time)+"\n")


if __name__ == '__main__':
  print("Output of run.py (actual data): ", args.actual)
  print("Output path: ",  args.output)
  parse(args.actual, args.output)
