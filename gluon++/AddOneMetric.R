library("optparse")
library("data.table")

target_column <- "Timer_Clustering_Kernel"

ParseStat <- function(input, output) {
  log_data <- read.csv(input, stringsAsFactors=F, strip.white=T)
  target_row <- subset(log_data, STAT_TYPE == "STAT" & CATEGORY == target_column)  
  target_data <- substring(target_row[6], 0)
  target_data <- as.numeric(target_data) / 1000000
#print(target_data)

  input_split <- strsplit(input, "/|\\\\")[[1]]
  input_split <- input_split[length(input_split)]
  input_split <- strsplit(input_split, '\\.')[[1]]
  graph <- input_split[1]
  app <- input_split[2]
  algo <- input_split[3]
  info <- paste("Graph:", graph, " app:", app, " algo:", algo)
  print(info)

  return_list <- list("Graph" = graph, "App" = app, "Algo" = algo,
                      "Time" = target_data)
  if (!file.exists(output)) {
    write.csv(as.data.frame(return_list), row.names=T,
              file=output, quote=F) 
  } else {
    write.table(as.data.frame(return_list), file=output,
                row.names=T, col.names=F, quote=F,
                append=T, sep=",")
  }
}

opt_list = list(make_option(c("-i", "--input"),
                            action="store", default=NA, type="character",
                            help="name of the input file to parse"),
                make_option(c("-o", "--output"),
                            action="store", default=NA, type="character",
                            help="name of the output file to store output")
                )

opt_parser <- OptionParser(usage = "%prog [options] -i input.log -o output.csv",
                           option_list=opt_list)
opt <- parse_args(opt_parser)

if (is.na(opt$i)) {
  print_help(opt_parser)
  stop("At least one argument must be spplied (input file)", call.=FALSE)
}

if (is.na(opt$o)) {
  print_help(opt_parser)
  stop("At least one argument must be supplied (output file)", call.=FALSE)
}

ParseStat(opt$i, opt$o)
