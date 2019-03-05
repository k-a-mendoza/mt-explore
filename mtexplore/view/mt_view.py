from .view_base import ViewContract
from ..controller.controller import MainController
import numpy as np
from matplotlib.ticker import ScalarFormatter


class MTView(ViewContract):
    app_res_position = [0.55, 0.5, 0.4, 0.4]
    phase_position   = [0.55, 0.25, 0.4, 0.2]

    def __init__(self,view):
        super().__init__(view)
        self.app_res = AppRes()
        self.phase   = Phase()

    def _add_controller(self, controller: MainController):
        controller.get_mt_controller()._update_selection = self.update_selection

    def update_selection(self,args,**kwargs):
        self.phase.update(args, **kwargs)
        self.app_res.update(args,**kwargs)
        self.phase.update(args,**kwargs)

    def _configure(self):
        ax1=self.add_axes(self.app_res_position)
        ax2=self.add_axes(self.phase_position)
        ax1.get_shared_x_axes().join(ax1,ax2)
        ax1.set_xlim([1e-4, 1e4])
        ax1.tick_params(axis='x',which='major',  length=10, grid_linewidth=3,grid_linestyle='-')
        ax2.tick_params(axis='x', which='major', length=10, grid_linewidth=3, grid_linestyle='-')
        ax1.tick_params(axis='x', which='minor', length=7, grid_linewidth=3, grid_linestyle='--')
        ax2.tick_params(axis='x', which='minor', length=7, grid_linewidth=3, grid_linestyle='--')
        ax1.get_xaxis().set_major_formatter(ScalarFormatter())
        self.app_res.configure(ax1)
        self.phase.configure(ax2)
        ax1.loglog()
class _Format():
    yx_marker='o'
    xy_marker='s'
    xx_marker='s'
    yy_marker='o'
    marker_size=6
    lw=1.5
    yx_color=(.5, 0, 0)
    xy_color=(0, 0, .5)
    xx_color=(1,0,0)
    yy_color=(0,0,1)
    yx_ls=':'
    xy_ls=':'
    xx_ls=':'
    yy_ls=':'

    def __init__(self):
        pass

class Phase(_Format):
    fontsize = 12
    weight = 'bold'
    def __init__(self):
        super().__init__()
        self.plot = []
        self.legend = False

    def add_controller(self, controller):
        pass

    def configure(self,axes):
        axes.set_ylim([-180,180])
        axes.set_yticks(np.arange(-180,180+45,45))
        axes.set_ylabel('Apparent Phase',fontsize=self.fontsize,weight=self.weight)
        axes.xaxis.grid(True,linewidth=1,which='both',color='black')
        self.ax =axes

    def update(self,packed,*args,**kwargs):
        if self.plot:
            for plot in self.plot:
                plot.remove()

            self.plot=[]
        mt_obj = packed[2][1]

        Z_tensor = mt_obj.Z
        frequencies = 1.0 / Z_tensor.freq

        phase_xx = mt_obj.Z.phase_xx
        phase_yy = mt_obj.Z.phase_yy
        phase_xy = mt_obj.Z.phase_xy
        phase_yx = mt_obj.Z.phase_yx

        phase_xx_err = mt_obj.Z.phase_err_xx
        phase_yy_err = mt_obj.Z.phase_err_yy
        phase_xy_err = mt_obj.Z.phase_err_xy
        phase_yx_err = mt_obj.Z.phase_err_yx

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, phase_xx),
                                          get_nonzero_array(phase_xx, phase_xx),
                                          marker=self.xy_marker,
                                          ms=self.marker_size,
                                          mew=self.lw,
                                          mec=self.xx_color,
                                          color=self.xx_color,
                                          ecolor=self.xx_color,
                                          ls=self.xx_ls,
                                          lw=self.lw,
                                          yerr=get_nonzero_array(phase_xx_err, phase_xx),
                                          capsize=self.marker_size,
                                          capthick=self.lw, label='res_xx'))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, phase_xy),
                                          get_nonzero_array(phase_xy, phase_xy),
                                          marker=self.xy_marker,
                                          ms=self.marker_size,
                                          mew=self.lw,
                                          mec=self.xy_color,
                                          color=self.xy_color,
                                          ecolor=self.xy_color,
                                          ls=self.xy_ls,
                                          lw=self.lw,
                                          yerr=get_nonzero_array(phase_xy_err, phase_xy),
                                          capsize=self.marker_size,
                                          capthick=self.lw, label='res_xy'))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, phase_yy),
                                          get_nonzero_array(phase_yy, phase_yy),
                                          marker=self.yy_marker,
                                          ms=self.marker_size,
                                          mew=self.lw,
                                          mec=self.yy_color,
                                          color=self.yy_color,
                                          ecolor=self.yy_color,
                                          ls=self.yy_ls,
                                          lw=self.lw,
                                          yerr=get_nonzero_array(phase_yy_err, phase_yy),
                                          capsize=self.marker_size,
                                          capthick=self.lw, label='res_yy'))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, phase_yx),
                                          get_nonzero_array(phase_yx, phase_yx),
                                          marker=self.yx_marker,
                                          ms=self.marker_size,
                                          mew=self.lw,
                                          mec=self.yx_color,
                                          color=self.yx_color,
                                          ecolor=self.yx_color,
                                          ls=self.yx_ls,
                                          lw=self.lw,
                                          yerr=get_nonzero_array(phase_yx_err, phase_yx),
                                          capsize=self.marker_size,
                                          capthick=self.lw, label='res_yx'))

class AppRes(_Format):
    fontsize = 12
    weight ='bold'

    def __init__(self):
        super().__init__()
        self.plot=[]
        self.legend=False

    def add_controller(self, controller):
        pass

    def configure(self, axes):
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.set_ylim([1e-1,2e4])
        axes.set_ylabel('Apparent Resistivity',fontsize=self.fontsize,weight=self.weight)
        axes.tick_params(axis='both',length=10,grid_linewidth=3)
        axes.tick_params(axis='y', which='minor', length=7, grid_linewidth=0.5, grid_linestyle='--')
        axes.grid(True,linewidth=1,which='both',color='black')
        self.ax = axes

    def update(self,packed,*args,**kwargs):
        if self.plot:
            for plot in self.plot:
                plot.remove()

            self.plot=[]

        mt_obj = packed[2][1]
        Z_tensor = mt_obj.Z
        frequencies = 1.0/ Z_tensor.freq
        self.ax.set_xlim([min(frequencies),max(frequencies)])

        res_xx = mt_obj.Z.res_xx
        res_yy = mt_obj.Z.res_yy
        res_xy = mt_obj.Z.res_xy
        res_yx = mt_obj.Z.res_yx

        res_xx_err = mt_obj.Z.res_err_xx
        res_yy_err = mt_obj.Z.res_err_yy
        res_xy_err = mt_obj.Z.res_err_xy
        res_yx_err = mt_obj.Z.res_err_yx

        max_yval = max([max(res_xx), max(res_xy), max(res_yy), max(res_yx)])
        if max_yval > 1e3:
            self.ax.set_ylim(1e-1,np.power(10,int(np.log10(max_yval)*1.5)))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies,res_xx),
                                       get_nonzero_array(res_xx,res_xx),
                                       marker=self.xy_marker,
                                       ms=self.marker_size,
                                       mew=self.lw,
                                       mec=self.xx_color,
                                       color=self.xx_color,
                                       ecolor=self.xx_color,
                                       ls=self.xx_ls,
                                       lw=self.lw,
                                       yerr=get_nonzero_array(res_xx_err,res_xx),
                                       capsize=self.marker_size,
                                       capthick=self.lw,label='res_xx'))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, res_xy),
                         get_nonzero_array(res_xy, res_xy),
                         marker=self.xy_marker,
                         ms=self.marker_size,
                         mew=self.lw,
                         mec=self.xy_color,
                         color=self.xy_color,
                         ecolor=self.xy_color,
                         ls=self.xy_ls,
                         lw=self.lw,
                         yerr=get_nonzero_array(res_xy_err, res_xy),
                         capsize=self.marker_size,
                         capthick=self.lw,label='res_xy'))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, res_yy),
                         get_nonzero_array(res_yy, res_yy),
                         marker=self.yy_marker,
                         ms=self.marker_size,
                         mew=self.lw,
                         mec=self.yy_color,
                         color=self.yy_color,
                         ecolor=self.yy_color,
                         ls=self.yy_ls,
                         lw=self.lw,
                         yerr=get_nonzero_array(res_yy_err, res_yy),
                         capsize=self.marker_size,
                         capthick=self.lw,label='res_yy'))

        self.plot.append(self.ax.errorbar(get_nonzero_array(frequencies, res_yx),
                         get_nonzero_array(res_yx, res_yx),
                         marker=self.yx_marker,
                         ms=self.marker_size,
                         mew=self.lw,
                         mec=self.yx_color,
                         color=self.yx_color,
                         ecolor=self.yx_color,
                         ls=self.yx_ls,
                         lw=self.lw,
                         yerr=get_nonzero_array(res_yx_err, res_yx),
                         capsize=self.marker_size,
                         capthick=self.lw,label='res_yx'))

        if not self.legend:
            self.legend=self.ax.legend(loc='upper right')

def get_nonzero_array(target, source):
    nonzero_array = np.nonzero(source)
    return target[nonzero_array]
