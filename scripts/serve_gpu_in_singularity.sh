#!/bin/bash

singularity exec --nv \
  graph2smiles_gpu.sif \
  torchserve \
  --start \
  --foreground \
  --ncs \
  --model-store=./mars \
  --models \
  USPTO_480k_mix=USPTO_480k_mix.mar \
  --ts-config ./config.properties
