# Augmented Transformer
Benchmarking and serving modules for reaction outcome prediction with Graph2SMILES, based on the manuscript (https://pubs.acs.org/doi/abs/10.1021/acs.jcim.2c00321).

## Serving

### Step 1/4: Environment Setup

First set up the url to the remote registry
```
export ASKCOS_REGISTRY=registry.gitlab.com/mlpds_mit/askcosv2
```
Then follow the instructions below to use either Docker, or Singularity (if Docker or root privilege is not available). Building or pulling either CPU or GPU image would suffice. If GPUs are not available, just go with the CPU image.

#### Using Docker

- Option 1: pull pre-built image
```
(CPU) docker pull ${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-cpu
(GPU) docker pull ${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-gpu
```
- Option 2: build from local
```
(CPU) docker build -f Dockerfile_cpu -t ${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-cpu .
(GPU) docker build -f Dockerfile_gpu -t ${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-gpu .
```

#### Using Singularity

- Option 1: pull pre-built *docker* image (NOT recommended)
```
(CPU) singularity pull forward_graph2smiles_cpu.sif docker://${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-cpu
(GPU) singularity pull forward_graph2smiles_gpu.sif docker://${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-gpu
```
- Option 2: build from local
```
(CPU) singularity build -f forward_graph2smiles_cpu.sif singularity_cpu.def
(GPU) singularity build -f forward_graph2smiles_gpu.sif singularity_gpu.def
```


## Benchmarking (GPU Required)

### Step 1/4: Environment Setup
Follow the instructions in Step 1 in the Serving section to build or pull the GPU docker image. It should have the name `${ASKCOS_REGISTRY}/forward_graph2smiles:1.0-gpu`

Note: the Docker needs to be rebuilt before running whenever there is any change in code.

### Step 2/4: Data Preparation
Prepare the raw .csv files for train, validation and test (atom mapping not required). The required columns are "id" and "rxn_smiles", where "rxn_smiles" contains reaction SMILES, optionally with atom mapping.

### Step 3/4: Path Configuration
Configure the environment variables in ./scripts/benchmark_in_docker.sh, especially the paths, to point to the *absolute* paths of raw files and desired output paths.
```
export DATA_NAME="USPTO_480k_mix"
export TRAIN_FILE=$PWD/data/USPTO_480k_mix/raw/raw_train.csv
export VAL_FILE=$PWD/data/USPTO_480k_mix/raw/raw_val.csv
export TEST_FILE=$PWD/data/USPTO_480k_mix/raw/raw_test.csv
...
```

### Step 4/4: Benchmarking
Run benchmarking on a machine with GPU using
```
bash scripts/benchmark_in_docker.sh
```
This will run the preprocessing, training and predicting for Graph2SMILES with Top-n accuracies up to n=20 as the final outputs. Progress and result logs will be saved under ./logs.

The estimated running times for benchmarking the USPTO_480k dataset on a 32-core machine with 1 RTX3090 GPU are
* Preprocessing: ~1 hr
* Training: ~40 hrs
* Testing: ~30 mins

## Converting Trained Model into Servable Archive (Optional)
If you want to create servable model archives from own checkpoints (e.g., trained on different datasets),
please refer to the archiving scripts (scripts/archive_in_docker.sh).
Change the arguments accordingly in the script before running.
It's mostly bookkeeping by replacing the data name and/or checkpoint paths; the script should be self-explanatory. Then execute the scripts with
```
bash scripts/archive_in_docker.sh
```
The servable model archive (.mar) will be generated under ./mars. Serving newly archived models is straightforward; simply replace the `--models` args in `scripts/serve_{cpu,gp}_in_{docker,singularity}.sh`

with the new model name and .mar. The `--models` flag for torchserve can also take multiple arguments to serve multiple model archives concurrently.
