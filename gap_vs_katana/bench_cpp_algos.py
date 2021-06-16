# from pytest import approx, raises
# import pytest
import argparse
import sys
import os
import time

timer_file=sys.stderr

binary_dir="/home/hlee/benchmarking/katana.binary"
output_dir="/home/hlee/benchmarking/katana.output.0616"
prefix=""

def run_bfs(graph_path, input_args, source_node_file, trial, threads):
    start_node = input_args["source_node"]
    algo = "SyncDO"
    flags = " --noverify"

    if "road" in input_args['name']:
        threads = 16
        algo = "Async"
        flags = ""

    if not source_node_file == "":
        if not os.path.exists(source_node_file):
            print(f"Source node file doesn't exist:", graph_path,
                  file=sys.stderr)
        timer_algo_start = time.time()
        command = f"{binary_dir}/bfs-cpu --algo={algo} -t={threads} "
        command += f"{flags} "
        command += f"-statFile={output_dir}/{prefix}bfs_{input_args['name']}_{trial}.stats {graph_path}"
        command += f" --startNodesFile={source_node_file}"
        os.system(command)
        timer_algo_end = time.time()
        print(f"Commands,", command, file=sys.stderr) 
        print(f"BFS timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)
    else:
        timer_algo_start = time.time()
        command = f"{binary_dir}/bfs-cpu --algo={algo} --startNodes={start_node} -t={threads} "
        command += f"{flags} "
        command += f"-statFile={output_dir}/{prefix}bfs_{input_args['name']}_{trial}.stats {graph_path}"
        os.system(command)
        timer_algo_end = time.time()
        print(f"Commands,", command, file=sys.stderr) 
        print(f"BFS source,", start_node, file=sys.stderr)
        print(f"BFS timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)

def run_sssp(graph_path, input_args, source_node_file, trial, threads):
    start_node = input_args["source_node"]
    edge_prop_name = input_args["edge_wt"]
    algo = "DeltaStep"

    if "kron" in input_args["name"] or "urand" in input_args["name"]:
      algo = "DeltaStepFusion"

    if not source_node_file == "":
        if not os.path.exists(source_node_file):
            print(f"Source node file doesn't exist: ",graph_path,
                  file=sys.stderr)

        timer_algo_start = time.time()
        command = f"{binary_dir}/sssp-cpu --algo={algo} --delta={input_args['sssp_delta']} "
        command += f"--edgePropertyName={edge_prop_name} "
        command += f"--startNodesFile={source_node_file} "
        command += f"-t=96 {graph_path} -statFile={output_dir}/{prefix}sssp_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"SSSP timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)

    else:
        timer_algo_start = time.time()
        command = f"{binary_dir}/sssp-cpu --algo={algo} --delta={input_args['sssp_delta']} "
        command += f"--edgePropertyName={edge_prop_name} --startNodes={start_node} "
        command += f"-t=96 {graph_path} -statFile={output_dir}/{prefix}sssp_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"SSSP source,",start_node, file=sys.stderr)
        print(f"SSSP timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)


def run_jaccard(graph_path, input_args, trial, threads):
    compare_node = input_args["source_node"]

    timer_algo_start = time.time()
    command = f"{binary_dir}/jaccard-cpu --baseNode={compare_node} -t=96"
    command += f" -statFile={output_dir}/{prefix}jaccard_{input_args['name']}_{trial}.stats"
    command += f" {graph_path}"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr) 
    print(f"Jaccard compare node,",compare_node, file=sys.stderr)
    print(f"Jaccard timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_pagerank(graph_path, input_args, trial, threads):
    tolerance = 0.0001
    max_iteration = 1000

    timer_algo_start = time.time()
    command = f"{binary_dir}/pagerank-cpu --algo=PullTopological --maxIterations={max_iteration}"
    command += f" --tolerance={tolerance} -t=96 {graph_path} --transposedGraph"
    command += f" -statFile={output_dir}/{prefix}pagerank_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr) 
    print(f"Page rank timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_bc(graph_path, input_args, source_node_file, trial, threads):
    start_node = input_args["source_node"]
    edge_prop_name = input_args["edge_wt"]

    flags = ""
    if "road" in input_args['name']:
        threads = 16
        flags += "--threadSpin" 

    n = 4
    if not source_node_file == "":
        if not os.path.exists(source_node_file):
            print(f"Source node file doesn't exist: ",graph_path,
                  file=sys.stderr)

        timer_algo_start = time.time()
        command = f"{binary_dir}/{prefix}betweennesscentrality-cpu --algo=Level {graph_path}"
        command += f" --edgePropertyName={edge_prop_name} "
        command += f"--startNodesFile={source_node_file} -t={threads}"
        command += f" --numberOfSources={n}"
        command += f" {flags}"
        command += f" --statFile={output_dir}/{prefix}bc_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"Between centrality timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)
    else:
        sources = [start_node]
        timer_algo_start = time.time()
        command = f"{binary_dir}/{prefix}betweennesscentrality-cpu --algo=Level {graph_path}"
        command += f" --edgePropertyName={edge_prop_name} "
        command += f"--startNodes={sources} -t={threads}"
        command += f" --numberOfSources=1"
        command += f" --statFile={output_dir}/{prefix}bc_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"Between centrality source,",sources, file=sys.stderr)
        print(f"Between centrality timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)


def run_tc(graph_path, input_args, trial, thread):
    timer_algo_start = time.time()
    command = f"{binary_dir}/triangle-counting-cpu --relabel {graph_path}"
    command += f" --algo=orderedCount --symmetricGraph -t=96"
    command += f" --statFile={output_dir}/tc_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr) 
    print(f"Triangle counting timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_cc(graph_path, input_args, trial, threads):
    timer_algo_start = time.time()
    command = f"{binary_dir}/connected-components-cpu --algo=Afforest -t=96"
    command += f" {graph_path} --symmetricGraph "
    command += f"--statFile={output_dir}/cc_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr)
    print(f"Connected components timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_kcore(graph_path, input_args, trial, threads):
    k = 10
    timer_algo_start = time.time()
    command = f"{binary_dir}/k-core-cpu --algo=Synchronous -t=96"
    command += f" {graph_path} --symmetricGraph -kCoreNumber={k}"
    command += f" --statFile={output_dir}/kcore_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr)
    print(f"K-core timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_louvain(graph_path, input_args, trial, threads):
    edge_prop_name = input_args["edge_wt"]

    timer_algo_start = time.time()
    command = f"{binary_dir}/louvain-clustering-cpu --algo=Deterministic -t=96"
    command += f" {graph_path} --symmetricGraph "
    command += f" --statFile={output_dir}/louvain_{input_args['name']}_{trial}.stats"
    command += f" --modularity_threshold_per_round=0.0001 "
    command += f" --modularity_threshold_total=0.0001 --max_iterations=10000 "
    command += f" --min_graph_size=100"
    command += f" --edgePropertyName={edge_prop_name}"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr)
    print(f"Louvain timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_all_gap(args):
    threads=args.threads
    print("Using threads:", threads, file=sys.stderr)
    inputs = [
        {
            "name": "GAP-road",
            "symmetric_input": "GAP-road",
            "symmetric_clean_input": "GAP-road",
            "transpose_input": "GAP-road",
            "source_node": 18944626,
            "edge_wt": "value",
            "sssp_delta": 13,
        },
        {
            "name": "GAP-kron",
            "symmetric_input": "GAP-kron",
            "symmetric_clean_input": "GAP-kron",
            "transpose_input": "GAP-kron",
            "source_node": 71328660,
            "edge_wt": "value",
            "sssp_delta": 1,
        },
        {
            "name": "GAP-twitter",
            "symmetric_input": "GAP-twitter-symmetric",
            "symmetric_clean_input": "GAP-twitter-symmetric_cleaned",
            "transpose_input": "GAP-twitter-transpose",
            "source_node": 19058681,
            "edge_wt": "value",
            "sssp_delta": 1,
        },
        {
            "name": "GAP-web",
            "symmetric_input": "GAP-web-symmetric",
            "symmetric_clean_input": "GAP-web-symmetric_cleaned",
            "transpose_input": "GAP-web-transpose",
            "source_node": 19879527,
            "edge_wt": "value",
            "sssp_delta": 1,
        },
        {
            "name": "GAP-urand",
            "symmetric_input": "GAP-urand",
            "symmetric_clean_input": "GAP-urand",
            "transpose_input": "GAP-urand",
            "source_node": 57337430,
            "edge_wt": "value",
            "sssp_delta": 1,
        },

    ]

    # Load our graph
    input = next(item for item in inputs if item["name"] == args.graph)
    if args.application in ["bfs", "sssp", "bc", "jaccard"]:
        graph_path = f"{args.input_dir}/{input['name']}"
        if not os.path.exists(graph_path):
            print(f"Graph doesn't exist: ",graph_path, file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)

        if args.application == "bfs":
            for t in range(args.trials):
              run_bfs(graph_path, input, args.source_nodes, t, threads)

        if args.application == "sssp":
            for t in range(args.trials):
                run_sssp(graph_path, input, args.source_nodes, t, threads)

        if args.application == "jaccard":
            for t in range(args.trials):
                run_jaccard(graph_path, input, t, threads)

        if args.application == "bc":
            for t in range(args.trials):
                run_bc(graph_path, input, args.source_nodes, t, threads)

    elif args.application in ["tc"]:
        graph_path = f"{args.input_dir}/{input['symmetric_clean_input']}"
        if not os.path.exists(graph_path):
            print(f"Symmetric clean Graph doesn't exist: ",graph_path,
                  file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)

        if args.application == "tc":
            for t in range(args.trials):
                run_tc(graph_path, input, t, threads)

    elif args.application in ["cc", "kcore", "louvain"]:
        graph_path = f"{args.input_dir}/{input['symmetric_input']}"
        if not os.path.exists(graph_path):
            print(f"Symmetric Graph doesn't exist: ",graph_path,
                  file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)

        if args.application == "cc":
            for t in range(args.trials):
                run_cc(graph_path, input, t, threads)

        if args.application == "kcore":
            for t in range(args.trials):
                run_kcore(graph_path, input, t, threads)

        if args.application == "louvain":
            for t in range(args.trials):
                run_louvain(graph_path, input, t, threads)

    elif args.application in ["pagerank"]:
        ## Using transpose file pagerank pull which is expected
        ## to perform better than pagerank push algorithm
        graph_path = f"{args.input_dir}/{input['transpose_input']}"
        if not os.path.exists(graph_path):
            print(f"Symmetric Graph doesn't exist: ",graph_path,
                  file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)
        if args.application == "pagerank":
            for t in range(args.trials):
                run_pagerank(graph_path, input, t, threads)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
             "Benchmark performance of routines")

    parser.add_argument(
        "--input-dir",
        default="./",
        help="Path to the input directory (default: %(default)s)",
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=None,
        help="Number of threads to use (default: query sinfo). "+
             "Should match max threads.",
    )
    parser.add_argument(
        "--graph",
        default="GAP-road",
        choices=["GAP-road", "GAP-kron", "GAP-twitter", "GAP-web", "GAP-urand" ],
        help="Graph name (default: %(default)s)",
    )
    parser.add_argument(
        "--application",
        default="bfs",
        choices=["bfs", "sssp", "cc", "bc", "pagerank",
                 "tc", "jaccard", "kcore", "louvain"],
        help="Application to run (default: %(default)s)",
    )
    parser.add_argument(
        "--source-nodes",
        default="",
        help="Source nodes file(default: %(default)s)",
    )
    parser.add_argument(
        "--trials",
        type=int,
        default=1,
        help="Number of trials (default: %(default))",
    )

    parsed_args = parser.parse_args()

    if not os.path.isdir(parsed_args.input_dir):
        print(f"input directory : ",parsed_args.input_dir," doesn't exist",
              file=sys.stderr)
        sys.exit(1)

    if not parsed_args.threads:
        parsed_args.threads = int(os.cpu_count())

    print(f"Using input directory: ",parsed_args.input_dir," and ",
          "Threads: ",parsed_args.threads, file=sys.stderr)

    threads = parsed_args.threads
    run_all_gap(parsed_args)
