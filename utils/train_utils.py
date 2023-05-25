import logging
import numpy as np
import os
import random
import sys
import torch
from datetime import datetime
from rdkit import RDLogger


def log_rank_0(message):
    if torch.distributed.is_initialized():
        if torch.distributed.get_rank() == 0:
            logging.info(message)
            sys.stdout.flush()
    else:
        logging.info(message)
        sys.stdout.flush()


def set_seed(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def setup_logger(args, warning_off: bool = False):
    if warning_off:
        RDLogger.DisableLog("rdApp.*")
    else:
        RDLogger.DisableLog("rdApp.warning")

    os.makedirs(f"./logs/{args.data_name}", exist_ok=True)
    dt = datetime.strftime(datetime.now(), "%y%m%d-%H%Mh")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(f"./logs/{args.data_name}/{args.log_file}.{dt}")
    sh = logging.StreamHandler(sys.stdout)
    fh.setLevel(logging.INFO)
    sh.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
