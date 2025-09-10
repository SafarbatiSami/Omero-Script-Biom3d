#!/bin/bash
##############################
#       Job blueprint        #
##############################

#SBATCH --job-name=omero-job-biom3d
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:1
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --mem=120G         # Set memory requirement
#SBATCH --cpus-per-task=25
#              d-hh:mm:ss
#SBATCH --time=00:16:00

module load cuda/11.8.0
export CUDA_HOME=/usr/local/cuda-11.4
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

#SBATCH --output=omero-%j.log
#SBATCH --open-mode=append
#SBATCH --mail-type=END,FAIL


##############################
#       Job script           #
##############################

# Std out will get parsed into the logfile, so it is useful to log all your steps and variables
echo "Running Biom3d " 
# Load singularity module if needed
echo "Loading Singularity/Apptainer if needed..."
module load singularity > /dev/null 2>&1 || true



echo "Running workflow..."

# Verify if the number of parameters is correct
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <python_module> <params...>"
    exit 1
fi

# Extract the Python module name
python_module="$1"
shift  # Remove the first argument to leave only the parameters

# Extract the remaining parameters
params="$@"

# Define the Singularity image path (replace with your actual Singularity image path)
singularity_image="/storage/groups/omero/my-scratch/singularity_images/workflows/biom3d/biom3d.sif"


# Run Singularity container with provided parameters
WORKDIR=/storage/scratch/$LOGNAME/$SLURM_JOB_ID
TMPDIR=$WORKDIR/tmp
mkdir -p $WORKDIR
mkdir -p $TMPDIR
export TMPDIR

cd $WORKDIR
mkdir logs
export LD_PRELOAD=/opt/conda/lib/libiconv.so.2.6.1
singularity exec --nv  $singularity_image /Biom3d/deployment/dockerfiles/entrypoint.sh "$python_module" $params

rm -rf $WORKDIR

