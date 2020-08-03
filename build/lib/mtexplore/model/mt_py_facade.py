import random
import numpy as np

class MtFacade:
     def __init__(self,debug):
         self._debug = debug

     def set_debug(self, debug_other):
        self._debug= debug_other

     def get_MT_obj(self):
        print('debug is {}'.format(self._debug))
        if self._debug:
            return MT_debug
        else:
            from mtpy.core.mt import MT
        return MT

class testsite:

    survey = 'example'

class MT_debug:

    def __init__(self,dir):
        self.dir = dir
        self.station  = str(random.randint(1,200))
        self.lat = random.random()*10 + 20
        self.lon = random.random()*10 -120
        self.elev = 10
        self.east = 0
        self.north = 0
        self.utm_zone = 0
        self.rotation_angle =0
        self.station = 1
        self.survey = 'test survey'

    def get_frequencies(self):
        """

        Returns
        -------
        frequencies: np.array
            returns an array of periods
        """
        return np.linspace(10,1,num=3)

    def extract_phases(self):
        """

        Returns
        -------
        phase_xx, phase_xy, phase_yx, phase_yy

        """
        phase_xx = np.ones((3,))
        phase_yy = np.ones((3,))*2
        phase_xy = np.ones((3,))*5
        phase_yx = np.ones((3,))*10
        return phase_xx, phase_yy, phase_xy, phase_yx

    def extract_phase_error(self):
        phase_xx_err = np.ones((3,))*0.01
        phase_yy_err = np.ones((3,))*0.01
        phase_xy_err = np.ones((3,))*0.01
        phase_yx_err = np.ones((3,))*0.01
        return phase_xx_err, phase_yy_err, phase_xy_err, phase_yx_err

    def extract_resistivity_error(self):
        res_xx_err = np.ones((3,))*0.01
        res_yy_err = np.ones((3,))*0.01
        res_xy_err = np.ones((3,))*0.01
        res_yx_err = np.ones((3,))*0.01
        return res_xx_err, res_yy_err, res_xy_err, res_yx_err

    def extract_resistivity(self):
        res_xx = np.ones((3,))*1
        res_yy = np.ones((3,))*10
        res_xy = np.ones((3,))*5
        res_yx = np.ones((3,))*100
        return res_xx, res_yy, res_xy, res_yx
    
    def extract_tipper(self):
        tipper_x = np.ones((3,2))
        tipper_y = np.ones((3,2))*2
        
        return tipper_x,tipper_y


