#!/bin/bash

singularity exec \
  graph2smiles_cpu.sif \
  torchserve \
  --start \
  --foreground \
  --ncs \
  --model-store=./mars \
  --models \
  USPTO_480k_mix=USPTO_480k_mix.mar \
  --ts-config ./config.properties
