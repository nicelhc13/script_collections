import argparse

parse = argparse.ArgumentParser(description='Fix result file')
parse.add_argument('-f', metavar='f', type=str, help='The input file')
args = parse.parse_args()

def sorting(fname: str):
  with open(fname) as f:
    lines = f.readlines()
    for target in [ "independent", "serial", "random", "reduce" ]:
      o_str = ""
      for dm_target in [ "lazydm", "eagerdm" ]:
        for sz_target in [ "100KB", "100MB" ]:
          for line in lines:
            if target in line and dm_target in line and sz_target in line:
              t_str = line.split(",")[1]
              o_str += t_str + ","
          o_str += "\n"
      print(o_str)

if __name__ == '__main__':
  print("Input file:", args.f)
  sorting(args.f)
