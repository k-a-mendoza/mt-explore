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
        return MTPYFacade

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


class MTPYFacade:

    def __init__(self,dir):
        self.dir = dir
        from mtpy.core.mt import MT
        mt_obj = MT(dir)
        self.mt_obj = mt_obj
        self.lat = mt_obj.lat
        self.lon = mt_obj.lon
        self.elev = mt_obj.elev
        self.east = mt_obj.east
        self.north = mt_obj.north
        self.utm_zone = mt_obj.utm_zone
        self.rotation_angle = mt_obj.rotation_angle
        self.station = mt_obj.station
        try:
            self.survey  = mt_obj.Notes.info_dict['SURVEY']
        except KeyError:
            survey = mt_obj.Notes.info_dict['SURVEY ID']
            if survey=='SoUt':
                self.survey = 'UU:Southern Utah'


    def get_frequencies(self):
        """

        Returns
        -------
        frequencies: np.array
            returns an array of periods
        """
        Z_tensor = self.mt_obj.Z
        frequencies = 1.0 / Z_tensor.freq
        return frequencies

    def clean(self,array):
        new_arr = []
        for arr in array:
            arr[arr==np.inf]=0
            arr[arr==-np.inf]=0
            new_arr.append(arr)
        return new_arr

    def extract_phases(self):
        """

        Returns
        -------
        phases: list
            phase values for the given frequencies
        ordered as xx, yy, xy, yx

        """
        arr = []
        arr.append(self.mt_obj.Z.phase_xx)
        arr.append(self.mt_obj.Z.phase_yy)
        arr.append(self.mt_obj.Z.phase_xy)
        arr.append(self.mt_obj.Z.phase_yx)
        arr = self.clean(arr)
        return arr

    def extract_phase_error(self):
        """

        Returns
        -------
        phase_errors: list
            errors for the given frequencies. ordered as
            xx, yy, xy, yx

        """
        err=[]
        err.append(self.mt_obj.Z.phase_err_xx)
        err.append(self.mt_obj.Z.phase_err_yy)
        err.append(self.mt_obj.Z.phase_err_xy)
        err.append(self.mt_obj.Z.phase_err_yx)
        arr = self.clean(err)
        return arr

    def extract_resistivity_error(self):
        """

        Returns
        -------
        resistivity_errors: list
            errors for the given frequencies. ordered as xx, yy, xy, yx
        """
        err=[]
        err.append(self.mt_obj.Z.res_err_xx)
        err.append(self.mt_obj.Z.res_err_yy)
        err.append(self.mt_obj.Z.res_err_xy)
        err.append(self.mt_obj.Z.res_err_yx)
        arr = self.clean(err)
        return arr

    def extract_resistivity(self):
        """

        Returns
        -------
        resistivity: list
            apparent resistivity for the given frequencies. ordered as xx, yy, xy, yx

        """
        res=[]
        res.append(self.mt_obj.Z.res_xx)
        res.append(self.mt_obj.Z.res_yy)
        res.append(self.mt_obj.Z.res_xy)
        res.append(self.mt_obj.Z.res_yx)
        arr = self.clean(res)
        return res

