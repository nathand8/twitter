#!/bin/bash

#Submit this script with: sbatch spark_template.slurm

#SBATCH --time=00:10:00   # walltime
#SBATCH --ntasks=10 # number of processor cores (i.e. tasks)
#SBATCH --nodes=2   # number of nodes
#SBATCH --ntasks-per-node=5   # make sure there's 16 processors per node
#SBATCH --mem-per-cpu=4096M   # memory per CPU core
#SBATCH -J "Symptoms (Test)"   # job name

# The script spark-beta.py will initialize a Spark cluster on the nodes given by slurm.
# The PBS_NODEFILE variable is needed for the script to determine the nodelist given by slurm.
# It is a good idea to reserve all of the processors on the node with the parameter
#   --ntasks-per-node as seen above.
# You should also request a minimum of 2 nodes. 

# Compatibility variables for PBS. spark-beta.py uses this variable to determine which nodes should appear in the cluster.
export PBS_NODEFILE=`/fslapps/fslutils/generate_pbs_nodefile`

# These variables are set to shorten the command below, but are also critical for correct behavior.
# If you are trying to use a different value for JAVA_HOME, ***CHANGING IT HERE MAY NOT SUFFICE***
#
export HADOOP_GROUP=/fslgroup/fslg_hadoop/
export SPARK_PATH=/fslgroup/fslg_hadoop/spark-1.5.0/
export JAVA_HOME=/usr/java/latest/

# *****************************************************************************************************************************
# PLEASE NOTE: Java programs must be compiled with Maven, and Scala programs must be compiled with sbt. 
# *****************************************************************************************************************************
#
# spark.py requires five (5) input strings: 
#	[0] CORES_PER_NODE	same as above SBATCH --ntasks-per-node
#	[1] MEM_PER_NODE	same as above SBATCH --mem-per-cpu, ***WITHOUT TRAILING LETTER, MUST BE IN MEGABYTES***
#	[2] TOTAL_EXECS		same as above SBATCH --ntasks
#	[3] entrance class name for Java or Scala program; pass an empty string when not needed for R and Python programs
#	[4] the actual program string ("program <arguments>", like you would with hadoop.py)
#
# When referencing your home directory the variable ${HOME} should be used rather than '~' to ensure proper substitution.
#  If ~ appears in a quoted string, it will not be substituted.  This could cause hadoop to look for a folder called '~'
#  rather than your home directory.
#
# In Spark terminology, there is one Worker running per Node, so we will use Worker and Node (and in the scripts, "slave") 
# interchangably. Each Worker has n Executors to do their work. Deciding how many Executors to have should be a simple distribution
# of available resources. A good rule of thumb would be to use one (1) core per Executor, and (total node memory / cores per node)
# memory per Executor. In future, this script may do this automatically for you; for now, the Seven Deadly Parameters are up to you.
# 
# For parameter [4] you will need to put total Executors, including all Nodes (Workers). Your Executors are using one (1) core
# apiece, so that means this number will equal the SBATCH --ntasks. Here's an example for you:
#
# If you have 2 Nodes with 3 cores and 2048M per Node (so total of 6 cores), the configuration would be:
#
# ...../spark-beta.py 	3 2048 6 "" "/path/to/my/program.py arg0 arg1"
#

# 9769642
$SPARK_PATH/bin/spark.py 5 2048 10 "" "${HOME}/twitter/symptoms/filterBySymptoms.py '${HOME}/compute/hasState/2013/01/*' ${HOME}/twitter/symptoms/output/small_sample.json"

# java example job
# $SPARK_PATH/bin/spark.py 5 4096 10 "SimpleApp" "${HOME}/example-project-1.0.jar ${HOME}/compute/spark-example-java"

# R example job
# $SPARK_PATH/bin/spark.py 5 4096 10 "" "$SPARK_PATH/examples/src/main/r/dataframe.R"

# scala example job
# $SPARK_PATH/bin/spark.py 5 4096 10 "SimpleApp" "${HOME}/example-project-1.0.jar ${HOME}/compute/spark-example-scala"

exit 0

