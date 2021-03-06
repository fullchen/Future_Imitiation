from __future__ import print_function
from __future__ import print_function
import numpy as np
from Training.RGB.utils.dirs import create_dirs
from Training.RGB.utils.model_summary import print_network_state
import os
import traceback
from Training.RGB.single_view_model import SingleViewModel
from Training.RGB.single_view_trainer import Trainer
from Training.RGB.single_view_generator import DataLoader
import os
from scipy import misc
import tensorflow as tf
from Training.RGB.config import Config
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import sys
if '/media/eslam/426b7820-cb81-4c46-9430-be5429970ddb/home/eslam/Future_Imitiation/video_prediction-master/' not in sys.path:
    sys.path.append('/media/eslam/426b7820-cb81-4c46-9430-be5429970ddb/home/eslam/Future_Imitiation/video_prediction-master/')
from scripts.generate_future import inference_future_generator


def main():
    s_config = Config()
    create_dirs(
        [s_config.exp_name,
         s_config.exp_name + s_config.images_dir,
         s_config.checkpoint_dir,
         s_config.exp_name + s_config.summary_dir,
         s_config.exp_name + s_config.visualization_dir,
         s_config.exp_name + s_config.saving_visualization_img_right_path,
         s_config.exp_name + s_config.saving_visualization_img_straight_path
         ])

    s_config.images_dir = s_config.exp_name + s_config.images_dir
    s_config.summary_dir = s_config.exp_name + s_config.summary_dir
    tf.reset_default_graph()

    config = tf.ConfigProto(allow_soft_placement=True)
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    model = SingleViewModel(s_config)
    model.load(sess, s_config.load)
    print_network_state()
    # Intialize future predictor
    if s_config.preprocessed_data:
        future_generator = None
    else:
        future_generator = inference_future_generator(s_config.f_stacking_frames, batch_size=s_config.batch_size)
    data_loader = DataLoader(s_config, future_generator, is_training=True)
    val_loader = DataLoader(s_config, future_generator, is_training=False)
    print("Data Loaded Successfully")
    try:
        trainer = Trainer(sess, model, data_loader, val_loader, s_config)

        if s_config.apply_auggmentation:
            print('Augmentation ON')
            print('With percentage: ', 1 / s_config.apply_auggmentation_every * 100)
        else:
            print('Augmentation OFF')

        print('Strating training...')
        trainer.train()
    except:
        print("...EXCEPTION...\nTraceback:")
        traceback.print_exc()
        model.save(sess)


if __name__ == '__main__':
    main()
