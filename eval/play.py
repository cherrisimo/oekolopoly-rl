#! /usr/bin/env python3

import sys, os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont                                    
from PyQt5.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QWidget, QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QPushButton, QLabel
from PyQt5.QtWidgets import QMainWindow, QSlider, QGridLayout


def clear (predict_table, status_label):
    predict_table.setColumnCount (0)
    status_label.setText ("")


def predict (play_whole_game, entries, model, predict_table, status_label):
    if not model['agent'] or not model['env']: return

    init_v = []

    for v_index in range (len (model['env'].V_NAMES)):
        entry = entries[v_index]
        init_v.append (entry.value ())

    model['env'].set_v (init_v)
    obs = model['env'].reset ()

    done = False

    while not done:
        action, state = model['agent'].predict (obs, deterministic=True)
        obs, reward, done, info = model['env'].step (action)

        predict_table_curr_col = predict_table.columnCount ()
        predict_table.setColumnCount (predict_table_curr_col + 1)

        for act_index in range (len (model['env'].ACT_NAMES)):
            item = QTableWidgetItem (str (model['env'].curr_action[act_index]))
            item.setFlags (Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            predict_table.setItem (act_index, predict_table_curr_col, item)

        for v_index in range (len (model['env'].V_NAMES)):
            item = QTableWidgetItem (str (model['env'].V[v_index]))
            item.setFlags (Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            predict_table.setItem (v_index + len (model['env'].ACT_NAMES) + 1, predict_table_curr_col, item)

        status_label.setText ("{}\n"
                              "Bilanz: {}\n"
                              "Reward: {}".format (info['done_reason'], info['balance'], reward))

        if not play_whole_game: break

    
def open_model (model, predict_button, play_button, clear_button):
    model_file_dialog = QFileDialog ()
    model_file_dialog.setNameFilter ("ZIP (*.zip)")
    if model_file_dialog.exec_ ():
        filenames = model_file_dialog.selectedFiles ()
        model_path = filenames[0]
        print (filenames)
        print (model_path)

        model_dirpath  = os.path.dirname  (model_path)
        model_filename = os.path.basename (model_path)
        if not model_filename.endswith ('.zip'): return
        env_name = model_filename[:-4]
        print (env_name)

        config_path = f'{model_dirpath}/{env_name}/config.yml'
        config_file = open (config_path)
        assert config_file
        config_lines = config_file.readlines ()
        config_file.close ()

        import gym
        model['env'] = gym.make (f'oekolopoly:{env_name}')

        for config_line in config_lines:
            if   config_line.endswith ('- utils.wrappers.OekoBoxActionWrapper\n'):
                from utils.wrappers import OekoBoxActionWrapper
                print ("wrapper: OekoBoxActionWrapper")
                model['env'] = OekoBoxActionWrapper (model['env'])
            elif config_line.endswith ('- utils.wrappers.OekoSimpleActionWrapper\n'):
                from utils.wrappers import OekoSimpleActionWrapper
                print ("wrapper: OekoSimpleActionWrapper")
                model['env'] = OekoSimpleActionWrapper (model['env'])
            elif config_line.endswith ('- utils.wrappers.OekoSimpleObsWrapper\n'):
                from utils.wrappers import OekoSimpleObsWrapper
                print ("wrapper: OekoSimpleObsWrapper")
                model['env'] = OekoSimpleObsWrapper (model['env'])
            elif config_line.endswith ('- utils.wrappers.OekoRewardWrapper\n'):
                from utils.wrappers import OekoRewardWrapper
                print ("wrapper: OekoRewardWrapper")
                model['env'] = OekoRewardWrapper (model['env'])
        
        newer_python_version = sys.version_info.major == 3 and sys.version_info.minor >= 8

        custom_objects = {}
        if newer_python_version:
            custom_objects = {
               "learning_rate": 0.0,
               "lr_schedule": lambda _: 0.0,
               "clip_range": lambda _: 0.0,
            }
        
        try:
            if model_path.find ('/ppo/') != -1:
                from stable_baselines3 import PPO
                print(model['env'])
                print(model_path)
                model['agent'] = PPO.load (model_path, model['env'], custom_objects=custom_objects)
            elif model_path.find ('/a2c/') != -1:
                from stable_baselines3 import A2C
                model['agent'] = A2C.load (model_path, model['env'], custom_objects=custom_objects)
            elif model_path.find ('/ddpg/') != -1:
                from stable_baselines3 import DDPG
                model['agent'] = DDPG.load (model_path, model['env'], custom_objects=custom_objects)
            elif model_path.find ('/td3/') != -1:
                from stable_baselines3 import TD3
                model['agent'] = TD3.load (model_path, model['env'], custom_objects=custom_objects)
            elif model_path.find ('/sac/') != -1:
                from stable_baselines3 import SAC
                model['agent'] = SAC.load (model_path, model['env'], custom_objects=custom_objects)
        except Exception as e:
            print (e)
            model['env'] = None
        
        if model['agent'] and model['env']:
            predict_button.setEnabled (True)
            play_button.setEnabled (True)
            clear_button.setEnabled (True)


def main ():
    import gym
    env = gym.make ('oekolopoly:Oekolopoly-v0')
    # env = DummyEnv ()
    # model = None

    model = {
        'agent': None,
        'env'  : None,
    }

    qapp = QApplication (sys.argv)

    f = open('play_res/Combinear/Combinear.qss')
    stylesheet = f.read()
    f.close ()

    window = QMainWindow ()
    window.setWindowTitle ("Oekolopoly-RL-Evaluationsprogramm")
    window.setWindowIcon (QIcon("play_res/Combinear/icons8-ai-64NO.png"))
    window.resize (800, 800)
    window.setStyleSheet (stylesheet)
    window.show()

    window_center = QWidget ()
    window.setCentralWidget (window_center)

    window_center_layout = QHBoxLayout ()
    window_center.setLayout (window_center_layout)

    obs_widget = QWidget ()
    window_center_layout.addWidget (obs_widget);
    obs_layout = QVBoxLayout ()
    obs_widget.setLayout (obs_layout)

    title_font = QFont ()
    title_font.setWeight (63)
    title_font.setPointSize (11)
    obs_title = QLabel ("Observation setzen")
    obs_title.setFont (title_font)
    obs_title.setAlignment(Qt.AlignCenter)
    obs_title.setStyleSheet("color: #F2C063")
    
    obs_layout.addWidget (obs_title)

    entries_widget = QWidget ()
    obs_layout.addWidget (entries_widget)
    
    entries_layout = QFormLayout ()
    entries_widget.setLayout (entries_layout)
    entries = []

    for v_index in range (len (env.V_NAMES)):
        entry = QSpinBox ()
        entries.append (entry)
        entry.setValue (env.init_v[v_index])
        entry.setMinimum (env.Vmin[v_index])
        entry.setMaximum (env.Vmax[v_index])
        entries_layout.addRow (env.V_NAMES[v_index], entry)

    obs_layout.addStretch (1)

    open_model_button = QPushButton ("&Open Model")
    obs_layout.addWidget (open_model_button)
    predict_button = QPushButton ("P&redict")
    predict_button.setEnabled (False)
    obs_layout.addWidget (predict_button)
    play_button = QPushButton ("&Play")
    play_button.setEnabled (False)
    obs_layout.addWidget (play_button)
    clear_button = QPushButton ("&Clear")
    clear_button.setEnabled (False)
    obs_layout.addWidget (clear_button)

    predict_view_widget = QWidget ()
    window_center_layout.addWidget (predict_view_widget)
    predict_view_layout = QVBoxLayout ()
    predict_view_widget.setLayout (predict_view_layout)

    predict_table = QTableWidget (len (env.ACT_NAMES) + len (env.V_NAMES) + 1, 0)
    predict_view_layout.addWidget (predict_table)
    for act_index in range (len (env.ACT_NAMES)):
        header = QTableWidgetItem (env.ACT_NAMES[act_index])
        predict_table.setVerticalHeaderItem (act_index, header)
    header = QTableWidgetItem ('')
    predict_table.setVerticalHeaderItem (len (env.ACT_NAMES), header)
    for v_index in range (len (env.V_NAMES)):
        header = QTableWidgetItem (env.V_NAMES[v_index])
        predict_table.setVerticalHeaderItem (v_index + len (env.ACT_NAMES) + 1, header)

    status_box_widget = QWidget ()
    predict_view_layout.addWidget (status_box_widget)
    status_box_layout = QHBoxLayout ()
    status_box_widget.setLayout (status_box_layout)
    status_label = QLabel ()
    status_label.setStyleSheet("font-weight: bold; color: #F2C063")
    status_box_layout.addWidget (status_label)

    open_model_button.clicked.connect (lambda value: open_model (model, predict_button, play_button, clear_button))
    play_button.clicked.connect    (lambda value: predict (True,  entries, model, predict_table, status_label))
    predict_button.clicked.connect (lambda value: predict (False, entries, model, predict_table, status_label))
    clear_button.clicked.connect   (lambda value: clear   (predict_table, status_label))

    qapp.exec_ ()

if __name__ == '__main__':
    main ()
