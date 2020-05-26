from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import copy

import numpy as np
import misc.utils as utils
import torch

from .ShowTellModel import ShowTellModel
from .FCModel import FCModel
from .OldModel import ShowAttendTellModel, AllImgModel
#from .Att2inModel import Att2inModel
from .AttModel import *
from .TransformerModel import TransformerModel
from .pervasive import Pervasive

def setup(opt):
    
    if opt.caption_model == 'fc':
        model = FCModel(opt)
    if opt.caption_model == 'show_tell':
        model = ShowTellModel(opt)
    # Att2in model in self-critical
    elif opt.caption_model == 'att2in':
        model = Att2inModel(opt)
    # Att2in model with two-layer MLP img embedding and word embedding
    elif opt.caption_model == 'att2in2':
        model = Att2in2Model(opt)
    elif opt.caption_model == 'att2all2':
        model = Att2all2Model(opt)
    # Adaptive Attention model from Knowing when to look
    elif opt.caption_model == 'adaatt':
        model = AdaAttModel(opt)
    # Adaptive Attention with maxout lstm
    elif opt.caption_model == 'adaattmo':
        model = AdaAttMOModel(opt)
    # Top-down attention model
    elif opt.caption_model == 'topdown':
        model = TopDownModel(opt)
    # StackAtt
    elif opt.caption_model == 'stackatt':
        model = StackAttModel(opt)
    # DenseAtt
    elif opt.caption_model == 'denseatt':
        model = DenseAttModel(opt)
    # Transformer
    elif opt.caption_model == 'transformer':
        model = TransformerModel(opt)
    # Pervasive Attention
    elif opt.caption_model == 'pervasive':
        jobname = opt.modelname
        src_vocab_size = opt.vocab_size - 10
        trg_vocab_size = opt.vocab_size + 1
        trg_specials = {'EOS': 9488, #trg_loader.eos,
                        'BOS': 9489, #trg_loader.bos,
                        'UNK': 9487, #trg_loader.unk,
                        'PAD': 0, #trg_loader.pad,
                        }
        model = Pervasive(jobname, vars(opt), src_vocab_size,
                          trg_vocab_size, trg_specials)
        model.init_weights()
    else:
        raise Exception("Caption model not supported: {}".format(opt.caption_model))

    # check compatibility if training is continued from previously saved model
    if vars(opt).get('start_from_path', None) is not None:
        # check if all necessary files exist 
        assert os.path.isdir(opt.start_from_path)," %s must be a a path" % opt.start_from
        assert os.path.isfile(os.path.join(opt.start_from_path,"infos_"+opt.id+".pkl")),"infos.pkl file does not exist in path %s"%opt.start_from
        model.load_state_dict(torch.load(os.path.join(opt.start_from_path, 'model.pth')))

    return model