library("optparse")
library("data.table")
library(ggplot2)

DrawChart <- function(input, output) {
  log_data <- read.csv(input, stringsAsFactors=F, strip.white=T)
#log_data <- log_data[order(log_data$Time),]
  print(">>> Draw chart")
  print(log_data)

  print(">>> Refined chart")
  log_data <- aggregate(Time~Graph + Algo, data = log_data, mean)
  print(log_data)
  p <- ggplot(log_data, aes(x = reorder(Algo, Time), y = Time, fill=Time)) +
       ylab("Time (s)") + xlab("Algorithm") +
       geom_bar(stat = "identity") +
#geom_text(aes(label = Time), color="black") +
       geom_text(aes(label = Time), alpha=1) +
       theme(text = element_text(size=20),
             axis.text.x = element_text(angle=90), legend.position="none")
  ggsave(gsub(" ", "", paste(output,".pdf")))
}

opt_list = list(make_option(c("-i", "--input"),
                            action="store", default=NA, type="character",
                            help="name of the input file to draw a chart"),
                make_option(c("-o", "--output"),
                            action="store", default=NA, type="character",
                            help="name of the output plot file to store output chart")
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

DrawChart(opt$i, opt$o)
