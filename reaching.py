import os
import numpy as np


class Reaching:
    """
    Class that contains all the parameters for handling the reaching task
    """

    def __init__(self):
        # pygame parameters
        self._width = 1366
        self._height = 768
        self._crs_radius = 15
        self._tgt_radius = 40
        self._tgt_dist = 260

        # Reaching parameters (from c# Baseform)
        self._tot_blocks = 11
        self._tot_repetitions = [1, 7, 7, 7, 7, 1, 7, 7, 7, 7, 1]
        self._tot_targets = [8, 4, 4, 4, 4, 8, 4, 4, 4, 4, 8]
        self._block = 1
        self._repetition = 1
        self._trial = 1
        self._target = 0
        self._state = 0
        self._comeback = 1
        with open(
            os.path.dirname(os.path.abspath(__file__)) + "/targets/circle_coadapt.txt",
            "r",
        ) as f:
            list_tgt_tmp = f.read().splitlines()
        self._list_tgt = [int(x) for x in list_tgt_tmp]
        self._score = 0

        # Reaching parameters (from c# PracticeForm)
        self._is_terminated = False
        self._is_paused = False
        self._is_blind = 0
        self._at_home = 1
        self._count_mouse = 0
        self._crs_x = self._width / 2
        self._crs_y = self._height / 2
        self._old_crs_x = self._crs_x
        self._old_crs_y = self._crs_y
        self._body = np.zeros((6,))
        self._tgt_x = 0
        self._tgt_y = 0
        self._score = 0
        self._tgt_x_list = []
        self._tgt_y_list = []

        # file parameters
        self._path_log = os.path.dirname(os.path.abspath(__file__)) + "/Practice/"

    # pygame parameters
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def crs_radius(self):
        return self._crs_radius

    @property
    def tgt_radius(self):
        return self._tgt_radius

    @property
    def tgt_dist(self):
        return self._tgt_dist

    # Reaching parameters (from c# Baseform)

    @property
    def tot_blocks(self):
        return self._tot_blocks

    @property
    def tot_targets(self):
        return self._tot_targets

    @property
    def tot_repetitions(self):
        return self._tot_repetitions

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, value):
        self._block = value

    @property
    def repetition(self):
        return self._repetition

    @repetition.setter
    def repetition(self, value):
        self._repetition = value

    @property
    def trial(self):
        return self._trial

    @trial.setter
    def trial(self, value):
        self._trial = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def comeback(self):
        return self._comeback

    @comeback.setter
    def comeback(self, value):
        self._comeback = value

    @property
    def list_tgt(self):
        return self._list_tgt

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    # Reaching parameters (from c# PracticeForm)
    @property
    def is_terminated(self):
        return self._is_terminated

    @is_terminated.setter
    def is_terminated(self, value):
        self._is_terminated = value

    @property
    def is_paused(self):
        return self._is_paused

    @is_paused.setter
    def is_paused(self, value):
        self._is_paused = value

    @property
    def is_blind(self):
        return self._is_blind

    @is_blind.setter
    def is_blind(self, value):
        self._is_blind = value

    @property
    def at_home(self):
        return self._at_home

    @at_home.setter
    def at_home(self, value):
        self._at_home = value

    @property
    def count_mouse(self):
        return self._count_mouse

    @count_mouse.setter
    def count_mouse(self, value):
        self._count_mouse = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @property
    def crs_x(self):
        return self._crs_x

    @crs_x.setter
    def crs_x(self, value):
        self._crs_x = value

    @property
    def crs_y(self):
        return self._crs_y

    @crs_y.setter
    def crs_y(self, value):
        self._crs_y = value

    @property
    def old_crs_x(self):
        return self._old_crs_x

    @old_crs_x.setter
    def old_crs_x(self, value):
        self._old_crs_x = value

    @property
    def old_crs_y(self):
        return self._old_crs_y

    @old_crs_y.setter
    def old_crs_y(self, value):
        self._old_crs_y = value

    @property
    def tgt_x(self):
        return self._tgt_x

    @tgt_x.setter
    def tgt_x(self, value):
        self._tgt_x = value

    @property
    def tgt_y(self):
        return self._tgt_y

    @tgt_y.setter
    def tgt_y(self, value):
        self._tgt_y = value

    @property
    def tgt_x_list(self):
        return self._tgt_x_list

    def empty_tgt_x_list(self):
        self._tgt_x_list = []

    @property
    def tgt_y_list(self):
        return self._tgt_y_list

    def empty_tgt_y_list(self):
        self._tgt_y_list = []

    # File parameters
    @property
    def path_log(self):
        return self._path_log
