# from pytest import approx, raises
# import pytest
import argparse
import sys
import os
import time

timer_file=sys.stderr


def run_bfs(graph_path, input_args, source_node_file, trial):
    start_node = input_args["source_node"]

    if not source_node_file == "":
        if not os.path.exists(source_node_file):
            print(f"Source node file doesn't exist:", graph_path,
                  file=sys.stderr)
        timer_algo_start = time.time()
#command = f"./bfs-cpu --algo=Sync -t=32 "
        command = f"./bfs-directionopt-cpu --algo=SyncDO -t=32 "
        command += f"-statFile=\"bfs_{input_args['name']}_{trial}.stats\" {graph_path}"
        command += f" --startNodesFile={source_node_file}"
        print(f"Commands,", command, file=sys.stderr) 
        os.system(command)
        timer_algo_end = time.time()
        print(f"BFS timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)
    else:
        timer_algo_start = time.time()
#command = f"./bfs-cpu --algo=Sync --startNodes={start_node} -t=32 "
        command = f"./bfs-directionopt-cpu --algo=SyncDO --startNodes={start_node} -t=32 "
        command += f"-statFile=\"bfs_{input_args['name']}_{trial}.stats\" {graph_path}"
        print(f"Commands,", command, file=sys.stderr) 
        os.system(command)
        timer_algo_end = time.time()
        print(f"BFS source,", start_node, file=sys.stderr)
        print(f"BFS timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)


def run_sssp(graph_path, input_args, source_node_file, trial):
    start_node = input_args["source_node"]
    edge_prop_name = input_args["edge_wt"]

    if not source_node_file == "":
        if not os.path.exists(source_node_file):
            print(f"Source node file doesn't exist: ",graph_path,
                  file=sys.stderr)

        timer_algo_start = time.time()
        command = f"./sssp-cpu --algo=deltaStep --delta={input_args['sssp_delta']} "
        command += f"--startNodesFile=\"{source_node_file}\" "
        command += f"-t=32 {graph_path} -statFile=sssp_{input_args['name']}_{trial}.stats"
        print(f"Commands,", command, file=sys.stderr) 
        os.system(command)
        timer_algo_end = time.time()

        print(f"SSSP timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)

    else:
        timer_algo_start = time.time()
        command = f"./sssp-cpu --algo=deltaStep --delta={input_args['sssp_delta']} "
        command += f" --startNodes=\"{start_node}\" "
        command += f"-t=32 {graph_path} -statFile=sssp_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"SSSP source,",start_node, file=sys.stderr)
        print(f"SSSP timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)


def run_jaccard(graph_path, input_args, trial):
    compare_node = input_args["source_node"]

    timer_algo_start = time.time()
    command = f"./jaccard-cpu --baseNode={compare_node} -t=32"
    command += f" -statFile=jaccard_{input_args['name']}_{trial}.stats"
    command += f" {graph_path}"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr) 
    print(f"Jaccard compare node,",compare_node, file=sys.stderr)
    print(f"Jaccard timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_pagerank(graph_path, input_args, trial):
    tolerance = 0.0001
    max_iteration = 1000

    timer_algo_start = time.time()
    command = f"./pagerank-pull-cpu --algo=Topo --maxIterations={max_iteration}"
    command += f" --tolerance={tolerance} -t=32 {graph_path} --transposedGraph"
    command += f" -statFile=pagerank_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr) 
    print(f"Page rank timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_bc(graph_path, input_args, source_node_file, trial):
    start_node = input_args["source_node"]
    edge_prop_name = input_args["edge_wt"]

    n = 4
    if not source_node_file == "":
        if not os.path.exists(source_node_file):
            print(f"Source node file doesn't exist: ",graph_path,
                  file=sys.stderr)

        timer_algo_start = time.time()
        command = f"./betweennesscentrality-cpu --algo=Level {graph_path}"
        command += f" --sourcesToUse=\"{source_node_file}\" -t=32"
        command += f" --numOfSources={n}"
        command += f" --statFile=bc_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"Between centrality timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)
    else:
        sources = [start_node]
        timer_algo_start = time.time()
        command = f"./betweennesscentrality-cpu --algo=Level {graph_path}"
        command += f" --startNodes=\"{sources}\" -t=32"
        command += f" --numOfSources=1"
        command += f" --statFile=bc_{input_args['name']}_{trial}.stats"
        os.system(command)
        timer_algo_end = time.time()

        print(f"Commands,", command, file=sys.stderr) 
        print(f"Between centrality source,",sources, file=sys.stderr)
        print(f"Between centrality timer (s),",
              round((timer_algo_end - timer_algo_start), 2),
              file=timer_file)


def run_tc(graph_path, input_args, trial):
    timer_algo_start = time.time()
    command = f"./triangle-counting-cpu --relabel {graph_path}"
    command += f" --algo=orderedCount --symmetricGraph -t=32"
    command += f" --statFile=tc_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr) 
    print(f"Triangle counting timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_cc(graph_path, input_args, trial):
    command = f"./connected-components-cpu --algo=Afforest -t=32"
    command += f" {graph_path} --symmetricGraph "
    command += f"--statFile=cc_{input_args['name']}_{trial}.stats"
    print(f"Commands,", command, file=sys.stderr)
    timer_algo_start = time.time()
    os.system(command)
    timer_algo_end = time.time()

    print(f"Connected components timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_kcore(graph_path, input_args, trial):
    k = 10
    timer_algo_start = time.time()
    command = f"./k-core-cpu --algo=Sync -t=32"
    command += f" {graph_path} --symmetricGraph -kcore={k}"
    command += f" --statFile=kcore_{input_args['name']}_{trial}.stats"
    os.system(command)
    timer_algo_end = time.time()

    print(f"Commands,", command, file=sys.stderr)
    print(f"K-core timer (s),",
          round((timer_algo_end - timer_algo_start), 2),
          file=timer_file)


def run_louvain(graph_path, input_args, trial):
    edge_prop_name = input_args["edge_wt"]

    timer_algo_start = time.time()
    command = f"./louvain-clustering-cpu --algo=Deterministic -t=32"
    command += f" {graph_path} --symmetricGraph "
    command += f" --statFile=louvain_{input_args['name']}_{trial}.stats"
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
    print("Using threads:", args.threads, file=sys.stderr)
    inputs = [
        {
            "name": "GAP-road.sgr",
            "symmetric_input": "GAP-road.sgr",
            "symmetric_clean_input": "GAP-road.sgr",
            "transpose_input": "GAP-road.sgr",
            "source_node": 18944626,
            "edge_wt": "value",
            "sssp_delta": 13,
        },
        {
            "name": "GAP-kron.sgr",
            "symmetric_input": "GAP-kron.sgr",
            "symmetric_clean_input": "GAP-kron.sgr",
            "transpose_input": "GAP-kron.sgr",
            "source_node": 71328660,
            "edge_wt": "value",
            "sssp_delta": 1,
        },
        {
            "name": "GAP-twitter.gr",
            "symmetric_input": "GAP-twitter.sgr",
            "symmetric_clean_input": "GAP-twitter.csgr",
            "transpose_input": "GAP-twitter.tgr",
            "source_node": 19058681,
            "edge_wt": "value",
            "sssp_delta": 1,
        },
        {
            "name": "GAP-web.gr",
            "symmetric_input": "GAP-web.sgr",
            "symmetric_clean_input": "GAP-web.csgr",
            "transpose_input": "GAP-web.tgr",
            "source_node": 19879527,
            "edge_wt": "value",
            "sssp_delta": 1,
        },
    ]

    # Load our graph
    input = next(item for item in inputs if args.graph in item["name"])
    if args.application in ["bfs", "sssp", "bc", "jaccard"]:
        graph_path = f"{args.input_dir}/{input['name']}"
        if not os.path.exists(graph_path):
            print(f"Graph doesn't exist: ",graph_path, file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)

        if args.application == "bfs":
            for t in range(args.trials):
                run_bfs(graph_path, input, args.source_nodes, t)

        if args.application == "sssp":
            for t in range(args.trials):
                run_sssp(graph_path, input, args.source_nodes, t)

        if args.application == "jaccard":
            for t in range(args.trials):
                run_jaccard(graph_path, input, t)

        if args.application == "bc":
            for t in range(args.trials):
                run_bc(graph_path, input, args.source_nodes, t)

    elif args.application in ["tc"]:
        graph_path = f"{args.input_dir}/{input['symmetric_clean_input']}"
        if not os.path.exists(graph_path):
            print(f"Symmetric clean Graph doesn't exist: ",graph_path,
                  file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)

        if args.application == "tc":
            for t in range(args.trials):
                run_tc(graph_path, input, t)

    elif args.application in ["cc", "kcore", "louvain"]:
        graph_path = f"{args.input_dir}/{input['symmetric_input']}"
        if not os.path.exists(graph_path):
            print(f"Symmetric Graph doesn't exist: ",graph_path,
                  file=sys.stderr)

        print(f"Running ",args.application," on graph: ",graph_path,
              file=sys.stderr)

        if args.application == "cc":
            for t in range(args.trials):
                run_cc(graph_path, input, t)

        if args.application == "kcore":
            for t in range(args.trials):
                run_kcore(graph_path, input, t)

        if args.application == "louvain":
            for t in range(args.trials):
                run_louvain(graph_path, input, t)

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
                run_pagerank(graph_path, input, t)


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
        choices=["GAP-road", "GAP-kron", "GAP-twitter", "GAP-web"],
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

    run_all_gap(parsed_args)
