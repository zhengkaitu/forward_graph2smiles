#!/bin/bash

docker run --rm --gpus '"device=0"' \
  -p 9520-9522:9520-9522 \
  -v "$PWD/mars":/app/graph2smiles/mars \
  -t "${ASKCOS_REGISTRY}"/forward_graph2smiles:1.0-gpu \
  torchserve \
  --start \
  --foreground \
  --ncs \
  --model-store=/app/graph2smiles/mars \
  --models \
  USPTO_480k_mix=USPTO_480k_mix.mar \
  --ts-config ./config.properties
