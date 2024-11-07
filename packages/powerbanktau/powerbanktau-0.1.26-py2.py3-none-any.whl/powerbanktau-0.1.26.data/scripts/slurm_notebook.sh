#!/bin/bash

# Check if a directory is passed as an argument
if [ -z "$1" ]; then
  echo "Error: No directory provided."
  echo "Usage: ./script.sh /path/to/directory"
  exit 1
fi

directory=$1  # The first argument is the directory
partition=${2:-engineering}  # Second argument: partition (default to 'engineering')
mem=${3:-3G} #Third argument: memory (default to 3)
gpus=${4:0}
env=${5:-main}
account=""
# If GPUs are requested, set account and gres options
if [ "$gpus" -gt 0 ]; then
  account="--gres=gpu:$gpus -A gpu-general-users"
fi

sbatch <<EOT
#!/bin/bash
source ~/.bashrc  # Ensure conda is initialized
#SBATCH --partition=$partition
#SBATCH --mem=$mem
#SBATCH --job-name=test_job
#SBATCH --ntasks=1
#SBATCH --time=7200
#SBATCH --output=/tamir2/nicolaslynn/logging/output/slurm-%j.out
#SBATCH --error=/tamir2/nicolaslynn/logging/error/slurm-%j.err  # Separate log for errors
#SBATCH $account

conda init

# If GPUs are requested, load the Miniconda module
if [ "$gpus" -gt 0 ]; then
    module load miniconda/miniconda3-2023-environmentally || { echo "Failed to load miniconda module"; exit 1; }
fi


echo "Job ID: $SLURM_JOB_ID"
sleep 10
echo "Fetching NodeList for Job ID: $SLURM_JOB_ID"

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

# Change to the specified directory
cd $directory || { echo "Directory not found"; exit 1; }
conda activate $env

# Start Jupyter Lab
jupyter lab --ip=* --port="\$port" --no-browser
EOT
