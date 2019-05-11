from view.view_base import ViewContract
import numpy as np
from matplotlib.ticker import ScalarFormatter


class MTView(ViewContract):
    app_res_position = [0.55, 0.5, 0.4, 0.4]
    phase_position   = [0.55, 0.25, 0.4, 0.2]

    def __init__(self,view):
        super().__init__(view)
        self.app_res = AppRes()
        self.phase   = Phase()

    def _update_selection(self,selection_row,**kwargs):
        mt_obj = selection_row['mt obj']
        self.phase.update(mt_obj)
        self.app_res.update(mt_obj)

    def _is_in_axes(self, event):
        if event.inaxes==self.app_res.ax:
            return 'res'
        elif event.inaxes==self.phase.axe2:
            return 'phase'
        else:
            return None


    def _configure(self):
        ax1=self.add_axes(self.app_res_position)
        ax2=self.add_axes(self.phase_position)
        ax1.get_shared_x_axes().join(ax1,ax2)
        ax1.set_xlim([1e-3, 1e5])
        ax1.tick_params(axis='x',which='major',  length=10, grid_linewidth=3,grid_linestyle='-')
        ax2.tick_params(axis='x', which='major', length=10, grid_linewidth=3,grid_linestyle='-')
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
    yx_color=(1, 0.7, 0.2)
    xy_color=(0.7, 0.2, 1)
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

    def _to_pi_strings(self,angle_deg):
        multiplier = int(4*angle_deg/180.0)
        if abs(multiplier)==4:
            sign = np.sign(multiplier)
            if sign==1:
                return r'$\pi$'
            else:
                return r'$-\pi$'
        elif multiplier==0:
            return '0'
        elif multiplier<0:
            return r'$-\frac{' + str(abs(multiplier))+'}{4}\pi$'
        else:
            return r'$\frac{' + str(multiplier) + '}{4}\pi$'

    def configure(self,axes):
        axes.set_ylim([-180,180])
        axes.set_yticks(np.arange(-180,180+45,45))
        axes.set_ylabel('Apparent Phase',fontsize=self.fontsize,weight=self.weight)
        axes.set_xlabel('Period', fontsize=self.fontsize, weight=self.weight)
        axes.xaxis.grid(True,linewidth=1,which='both',color='black')
        axes.plot([1e-2,1e6],[1,1],color='orange',linestyle='--')
        axe2 = axes.twinx()
        axe2.yaxis.tick_right()
        ticks = np.arange(-180,180+45,45)
        labels= [self._to_pi_strings(x) for x in ticks]
        axe2.set_yticks(ticks)
        axe2.set_yticklabels(labels)
        self.axe2=axe2
        self.ax =axes

    def update(self,mt_obj,*args,**kwargs):
        if self.plot:
            for plot in self.plot:
                plot.remove()

            self.plot=[]
        frequencies=mt_obj.get_frequencies()

        res_xx,     res_yy,     res_xy,     res_yx     = mt_obj.extract_phases()
        res_xx_err, res_yy_err, res_xy_err, res_yx_err = mt_obj.extract_phase_error()

        #self.ax.set_xlim([log_cast(0.1, min(frequencies[np.nonzero(res_xx)])),
        #                 log_cast(10 , max(frequencies[np.nonzero(res_xx)]))])

        self.plot_series(frequencies, res_xx, res_xx_err,
                         self.xy_marker, self.xx_color,
                         self.xx_color, self.xx_color, self.xx_ls, r'$\rho_{xx}$')

        self.plot_series(frequencies, res_xy, res_xy_err,
                         self.xy_marker, self.xy_color,
                         self.xy_color, self.xy_color, self.xy_ls, r'$\rho_{xy}$')

        self.plot_series(frequencies, res_yy, res_yy_err,
                         self.yy_marker, self.yy_color,
                         self.yy_color, self.yy_color, self.yy_ls, r'$\rho_{yy}$')

        self.plot_series(frequencies, res_yx, res_yx_err,
                         self.yx_marker, self.yx_color,
                         self.yx_color, self.yx_color, self.yx_ls, r'$\rho_{yx}$')

    def plot_series(self, frequencies, res_xx, res_xx_err,
                            marker, mec, color, ecolor, ls, label):

        plot_obj=self.ax.errorbar(get_nonzero_array(frequencies, res_xx),
                                          get_nonzero_array(res_xx, res_xx),
                                          marker=marker,
                                          ms=self.marker_size,
                                          mew=self.lw,
                                          mec=mec,
                                          color=color,
                                          ecolor=ecolor,
                                          ls=ls,
                                          lw=self.lw,
                                          yerr=get_nonzero_array(res_xx_err, res_xx),
                                          capsize=self.marker_size,
                                          capthick=self.lw, label=label)
        self.plot.append(plot_obj)

class AppRes(_Format):
    fontsize = 12
    weight ='bold'

    def __init__(self):
        super().__init__()
        self.plot=[]
        self.legend=False

    def configure(self, axes):
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.set_ylim([1e-1,2e4])
        axes.set_ylabel('Apparent Resistivity',fontsize=self.fontsize,weight=self.weight)
        axes.tick_params(axis='both',length=10,grid_linewidth=3)
        axes.tick_params(axis='y', which='minor', length=7, grid_linewidth=0.5, grid_linestyle='--')
        axes.grid(True,linewidth=1,which='both',color='black')
        self.ax = axes

    def update(self,mt_obj,*args,**kwargs):
        if self.plot:
            for plot in self.plot:
                plot.remove()

            self.plot=[]

        frequencies = mt_obj.get_frequencies()

        #self.ax.set_xlim([min(frequencies),max(frequencies)])

        res_xx,     res_yy,     res_xy,     res_yx     = mt_obj.extract_resistivity()
        res_xx_err, res_yy_err, res_xy_err, res_yx_err = mt_obj.extract_resistivity_error()

        max_yval =  get_max_value(res_xx, res_yy, res_xy, res_yx)
        min_yval = -get_max_value(-res_xx, -res_yy, -res_xy, -res_yx)
        self.ax.set_ylim([log_cast(0.1,min_yval),log_cast(10,max_yval)])

        self.plot_series(frequencies, res_xx, res_xx_err,
                         self.xy_marker,self.xx_color,
                         self.xx_color,self.xx_color,self.xx_ls,r'$\rho_{xx}$')

        self.plot_series(frequencies, res_xy, res_xy_err,
                         self.xy_marker, self.xy_color,
                         self.xy_color, self.xy_color, self.xy_ls,r'$\rho_{xy}$')

        self.plot_series(frequencies, res_yy, res_yy_err,
                         self.yy_marker, self.yy_color,
                         self.yy_color, self.yy_color, self.yy_ls,r'$\rho_{yy}$')

        self.plot_series(frequencies, res_yx, res_yx_err,
                         self.yx_marker, self.yx_color,
                         self.yx_color, self.yx_color, self.yx_ls,r'$\rho_{yx}$')

        if not self.legend:
            self.legend=self.ax.legend(loc='upper right',ncol=2)

    def plot_series(self, frequencies, res_xx, res_xx_err,
                            marker, mec, color, ecolor, ls, label):

        plot_obj=self.ax.errorbar(get_nonzero_array(frequencies, res_xx),
                                          get_nonzero_array(res_xx, res_xx),
                                          marker=marker,
                                          ms=self.marker_size,
                                          mew=self.lw,
                                          mec=mec,
                                          color=color,
                                          ecolor=ecolor,
                                          ls=ls,
                                          lw=self.lw,
                                          yerr=get_nonzero_array(res_xx_err, res_xx),
                                          capsize=self.marker_size,
                                          capthick=self.lw, label=label)
        self.plot.append(plot_obj)


def get_max_value(*args):
    nonzero_args=[]
    for arg in args:
        nonzero_args.append(get_nonzero_array(arg,arg))
    newlist=[]
    for arg in nonzero_args:
        newlist.append(max(arg))
    return max(newlist)


def log_cast(multiplier,value):
    return np.power(10.0,int(np.log10(value*multiplier)))


def get_nonzero_array(target, source):
    nonzero_array = np.nonzero(source)
    return target[nonzero_array]
