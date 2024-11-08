#!/bin/bash

# Check if a directory is passed as an argument
if [ -z "$1" ]; then
  echo "Error: No directory provided."
  echo "Usage: ./script.sh /path/to/directory [partition] [memory]"
  exit 1
fi

directory=$1
partition=${2:-tamirQ}
mem=${3:-3G}
port=${4:-8888}

# Submit the job to PBS
qsub -q $partition -l mem=$mem <<EOT
#!/bin/bash
# Source bashrc to initialize conda
source ~/.bashrc

# Initialize conda (if necessary)
eval "\$(conda shell.bash hook)"

#PBS -N test_job
#PBS -l walltime=120:00:00
#PBS -l nodes=1:ncpus=1,mem=$mem
#PBS -o /tamir2/nicolaslynn/logging/output/pbs-\$PBS_JOBID.out
#PBS -e /tamir2/nicolaslynn/logging/error/pbs-\$PBS_JOBID.err
#PBS -q $partition

# Change to the specified directory
cd $directory || { echo "Directory not found"; exit 1; }

# Print the Job ID
echo "Job ID: \$PBS_JOBID"

# Print node information
echo "Node List for Job ID: \$PBS_JOBID"
cat \$PBS_NODEFILE

# Activate base environment
conda activate base

# Start Jupyter Lab
jupyter lab --ip=* --port=$port --no-browser
EOT