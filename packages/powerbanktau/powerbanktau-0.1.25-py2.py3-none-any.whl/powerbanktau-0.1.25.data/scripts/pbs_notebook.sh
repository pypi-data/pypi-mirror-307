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
env=${4:-main}

# Submit the job to PBS
qsub -q $partition -l mem=$mem <<EOT
#!/bin/bash
#PBS -N test_job
#PBS -l walltime=120:00:00
#PBS -l nodes=1:ncpus=1,mem=$mem
#PBS -o /tamir2/nicolaslynn/logging/output/pbs-$PBS_JOBID.out
#PBS -e /tamir2/nicolaslynn/logging/error/pbs-$PBS_JOBID.err
#PBS -q $partition

# Change to the specified directory
cd $directory || { echo "Directory not found"; exit 1; }
echo "Using env: $env"
echo "Starting up..."
conda activate py310

# Print the Job ID
echo "Job ID: $PBS_JOBID"

# Sleep for a short time
sleep 10

# Print node information
echo "Node List for Job ID: $PBS_JOBID"
cat $PBS_NODEFILE

# Starting base port for Jupyter Lab
base_port=8888

# Function to find an available port
find_available_port() {
    local port=\$base_port
    while netstat -tuln | grep ":\$port" >/dev/null; do
        port=\$((port + 1))
    done
    echo \$port
}

# Find an available port
port=\$(find_available_port)
echo "Using port: \$port"

# Start Jupyter Lab
jupyter lab --ip=* --port="\$port" --no-browser
EOT