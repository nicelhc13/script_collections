import argparse
import os
import typing

parse = argparse.ArgumentParser(description='Parse and extract actual/expected runtime of Vite')
parse.add_argument('-input', metavar='input', type=str, help="Input Directory")
parse.add_argument('-output', metavar='output', type=str, help="Output Directory")
parse.add_argument('-system', metavar='system', type=str, help="System information")
args = parse.parse_args()

def findMaxRSS(ip: str, jobid: str):
  for outfile in os.listdir(ip):
    if not "_" in outfile or not ".out" in outfile or \
      not jobid in outfile:
      continue
    print("Target outfile:", outfile, ", job id:", jobid)
    prefix = os.path.dirname(os.path.abspath(__file__))
    fullpath = os.path.join(prefix, ip+"/"+outfile)
    max_rss = 0
    with open(fullpath) as f:
      lines = f.readlines()
      for line in reversed(lines):
        if "max_mem_gb=" in line:
          rss = float(line.split("max_mem_gb=")[1].split(" mem_gb=")[0])
          if rss > max_rss:
            max_rss = rss
    return max_rss

def parse(ip: str, op: str, system: str):
  total_time_str = "STAT, 0, (NULL), MainLoop, HMAX,"
  compute_time_str = "STAT, 0, (NULL), Computation, HMAX,"
  comm_time_str= "STAT, 0, (NULL), Communication, HMAX,"

  stat_dic = {}
  for statfile in os.listdir(ip):
    if not "_" in statfile or not ".stats" in statfile:
      print(statfile, " does not fit to our format")
      continue
    statfile_split = statfile.split("_")
    application = statfile_split[0]
    graph_name = statfile_split[1]
    partition = statfile_split[2]
    num_hosts = statfile_split[3]
    job_id = statfile_split[4]

    key = system+"_"+application+"_"+partition+"_"+graph_name+"_"+num_hosts
    if not key in stat_dic.keys():
      stat_dic[key] = {}
      stat_dic[key]["system"] = system
      stat_dic[key]["application"] = application
      stat_dic[key]["partition"] = partition
      stat_dic[key]["graph_name"] = graph_name
      stat_dic[key]["num_hosts"] = num_hosts
      stat_dic[key]["count"] = 0
      stat_dic[key]["compute_time"] = 0
      stat_dic[key]["comm_time"] = 0
      stat_dic[key]["total_time"] = 0
      stat_dic[key]["max_rss"] = 0
      # coarsening is not included in the com 
    max_RSS = findMaxRSS(ip, job_id)
    print("max RSS:", max_RSS)
    stat_dic[key]["max_rss"] = max_RSS
    prefix = os.path.dirname(os.path.abspath(__file__))
    fullpath = os.path.join(prefix, ip+"/"+statfile)
    if not os.path.exists(fullpath):
      print("Failed to open a file:", fullpath)
      continue
    with open(fullpath) as f:
      lines = f.readlines()
      compute_exist = 0
      comm_exist = 0
      total_exist = 0
      for line in lines:
        if compute_time_str in line:
          compute_exist = 1
          stat_dic[key]["compute_time"] += float(line.split(compute_time_str)[1])
        if comm_time_str in line:
          comm_exist = 1
          stat_dic[key]["comm_time"] += float(line.split(comm_time_str)[1])
        if total_time_str in line:
          total_exist = 1
          stat_dic[key]["total_time"] += float(line.split(total_time_str)[1])
      if compute_exist == 0 or comm_exist == 0 or total_exist == 0:
        print(fullpath, " failed; rerunning is required")
        continue
      stat_dic[key]["count"] += 1
  for key, val in stat_dic.items():
    count = float(val["count"])
    if count != 0:
#if count < 3:
#print(key+" requires more repeats:"+str(count))
#else:
      print(val["system"]+","+val["application"]+","+val["graph_name"]+","+val["partition"]+","+
            val["num_hosts"]+","+str(val["compute_time"]/count)+","+str(val["comm_time"]/count)+
            ","+str(val["total_time"]/count)+","+str(val["max_rss"]))
    else:
      print(key+" failed; rerunning is required")
 
if __name__ == '__main__':
  print("Input directory:", args.input)
  print("Output directory:", args.output)
  print("Target system:", args.system)
  parse(args.input, args.output, args.system)
