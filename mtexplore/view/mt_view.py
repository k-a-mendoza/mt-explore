from .view_base import ViewContract
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, LogFormatterExponent
import collections

class MTView(ViewContract):
    app_res_position = [0.6, 0.5, 0.35, 0.4]
    phase_position   = [0.6, 0.25, 0.35, 0.15]
    induction_position  = [0.1, 0.25, 0.40,0.15]
    tipper_position  = [0.6, 0.05, 0.35,0.1]
    weight_position  = [0.1, 0.05, 0.40,0.15]

    def __init__(self,view):
        super().__init__(view)
        self.app_res = AppResView()
        self.phase   = PhaseView()
        self.induction  = InductionView()
        self.tipper  = TipperView()
        self.weights = WeightsView()

    def _update_selection(self,mt_obj,**kwargs):
        mt_obj = mt_obj['mt_data']
        if mt_obj is None:
            self.phase._clean()
            self.app_res._clean()
            self.induction._clean()
            self.weights._clean()
        else:

            self.phase.update(mt_obj)
            self.app_res.update(mt_obj)
            self.tipper.update(mt_obj)
            self.induction.update(mt_obj)
            self.weights.update(mt_obj)
            self.ax.set_xlim([1e-3, 1e5])

    def _is_in_axes(self, event):
        if event.inaxes==self.app_res.ax:
            return 'res'
        elif event.inaxes==self.phase.ax:
            return 'phase'
        elif event.inaxes==self.tipper.ax:
            return 'tipper'
        elif event.inaxes==self.weights.ax:
            return 'weights'
        elif event.inaxes==self.induction.ax:
            return 'induction'
        else:
            return None


    def _configure(self):
        ax1=self.add_axes(self.app_res_position,label='app_res')
        ax2=self.add_axes(self.phase_position,label='phase')
        ax3=self.add_axes(self.induction_position,label='induction')
        ax4=self.add_axes(self.weight_position,label='weights')
        ax5=self.add_axes(self.tipper_position,label='tipper')
        ax1.get_shared_x_axes().join(ax1,ax2,ax4)
        ax1.set_xlim([1e-3, 1e5])
        ax1.set_xscale('log')
        ax1.tick_params(axis='x', which='major',  length=10, grid_linewidth=3,grid_linestyle='-')
        ax1.tick_params(axis='x', which='minor', length=7, grid_linewidth=3, grid_linestyle='--')
        self.ax=ax1
        self.app_res.configure(ax1)
        self.phase.configure(ax2)
        self.tipper.configure(ax5)
        self.weights.configure(ax4)
        self.induction.configure(ax3)

       


class _Format():
    kx_marker='^'
    ky_marker='^'
    yx_marker='o'
    xy_marker='s'
    xx_marker='s'
    yy_marker='o'
    marker_size=6
    lw=1.5
    kx_color='lime'
    ky_color='darkgreen'
    xx_color=(1, 0.7, 0.2)
    yy_color=(0.7, 0.2, 1)
    yx_color=(1,0,0)
    xy_color=(0,0,1)
    yx_ls=':'
    xy_ls=':'
    xx_ls=':'
    yy_ls=':'

    def __init__(self):
        pass
    
    def delist(self,input_data):
        for element in input_data:
            if isinstance(element, collections.Iterable) and not isinstance(element, (str, bytes)):
                yield from self.delist(element)
            else:
                yield element
    
    def _clean(self):
        if self.plot:
            plot_array = self.delist(self.plot)
            for plot in plot_array:
                plot.remove()

            self.plot=[]

class PhaseView(_Format):
    fontsize = 12
    weight = 'bold'
    def __init__(self):
        super().__init__()
        self.plot = []
        self.legend = False

    def configure(self,axes):
        axes.set_ylim([-180,180])
        axes.set_yticks(np.arange(-180,180+45,45))
        axes.set_ylabel('Apparent Phase',fontsize=self.fontsize,weight=self.weight)
        axes.set_xlabel('Period', fontsize=self.fontsize, weight=self.weight)
        axes.xaxis.grid(True,linewidth=1,which='both',color='black')
        axes.plot([1e-2,1e6],[1,1],color='orange',linestyle='--')
        ticks = np.arange(-180,180+45,45)
        self.ax =axes

    def update(self,mt_obj,*args,**kwargs):
        self._clean()
        periods=1/mt_obj.Z.freq

        res_xx,     res_yy,     res_xy,     res_yx     = mt_obj.Z.phase_xx, mt_obj.Z.phase_yy, mt_obj.Z.phase_xy, mt_obj.Z.phase_yx
        res_xx_err, res_yy_err, res_xy_err, res_yx_err = mt_obj.Z.phase_err_xx, mt_obj.Z.phase_err_yy, mt_obj.Z.phase_err_xy, mt_obj.Z.phase_err_yx

        lim = [min(periods),max(periods)]
        nearest_pow_10 = np.log10(lim).round()
        offset_decade  = np.asarray([-1,1]) + nearest_pow_10
        new_limits     = 10**offset_decade
       
        self.ax.set_xlim(new_limits)

        self.plot_series(periods, res_xx, res_xx_err,
                         self.xy_marker, self.xx_color,
                         self.xx_color, self.xx_color, self.xx_ls, r'$\rho_{xx}$')

        self.plot_series(periods, res_xy, res_xy_err,
                         self.xy_marker, self.xy_color,
                         self.xy_color, self.xy_color, self.xy_ls, r'$\rho_{xy}$')

        self.plot_series(periods, res_yy, res_yy_err,
                         self.yy_marker, self.yy_color,
                         self.yy_color, self.yy_color, self.yy_ls, r'$\rho_{yy}$')

        self.plot_series(periods, res_yx, res_yx_err,
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
        

class AppResView(_Format):
    fontsize = 12
    weight ='bold'

    def __init__(self):
        super().__init__()
        self.plot=[]
        self.legend=False

    def configure(self, axes):
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.set_ylim([1e-1,2e4])
        axes.set_yscale('log')
        axes.set_ylabel('Apparent Resistivity',fontsize=self.fontsize,weight=self.weight)
        axes.tick_params(axis='both',length=10,grid_linewidth=3)
        axes.tick_params(axis='y', which='minor', length=7, grid_linewidth=0.5, grid_linestyle='--')
        axes.grid(True,linewidth=1,which='both',color='black')
        self.ax = axes

    def update(self,mt_obj,*args,**kwargs):
        self._clean()
        periods = 1/mt_obj.Z.freq

        res_xx,     res_yy,     res_xy,     res_yx     = mt_obj.Z.res_xx, mt_obj.Z.res_yy, mt_obj.Z.res_xy, mt_obj.Z.res_yx
        res_xx_err, res_yy_err, res_xy_err, res_yx_err = mt_obj.Z.res_err_xx, mt_obj.Z.res_err_yy, mt_obj.Z.res_err_xy, mt_obj.Z.res_err_yx

        max_yval =  get_max_value(res_xx, res_yy, res_xy, res_yx)
        min_yval = -get_max_value(-res_xx, -res_yy, -res_xy, -res_yx)
        self.ax.set_ylim([log_cast(0.1,min_yval),log_cast(10,max_yval)])
        self.ax.set_title(mt_obj.station)

        
        self.plot_series(periods, res_yx, res_yx_err,
                         self.yx_marker, self.yx_color,
                         self.yx_color, self.yx_color, self.yx_ls,r'$\rho_{yx}$')

        self.plot_series(periods, res_xy, res_xy_err,
                         self.xy_marker, self.xy_color,
                         self.xy_color, self.xy_color, self.xy_ls,r'$\rho_{xy}$')

        self.plot_series(periods, res_yy, res_yy_err,
                         self.yy_marker, self.yy_color,
                         self.yy_color, self.yy_color, self.yy_ls,r'$\rho_{yy}$')
        
        self.plot_series(periods, res_xx, res_xx_err,
                         self.xy_marker,self.xx_color,
                         self.xx_color,self.xx_color,self.xx_ls,r'$\rho_{xx}$')


        if not self.legend:
            self.legend=self.ax.legend(loc='upper right',ncol=2)

    def plot_series(self, periods, res_xx, res_xx_err,
                            marker, mec, color, ecolor, ls, label):

        plot_obj=self.ax.errorbar(get_nonzero_array(periods, res_xx),
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
    
class InductionView(_Format):
    fontsize = 12
    weight ='bold'
    arrow_lw =0.7
    facecolor_real = 'blue'
    facecolor_imag = 'green'
    head_width = 0.01
    head_length = 0.03
    length_includes_head=False
    def __init__(self):
        super().__init__()
        self.plot=[]
        self.legend=True

    def configure(self, axes):
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.set_ylim([-1,1])
        axes.set_ylabel('Induction Arrows',fontsize=self.fontsize,weight=self.weight)
        axes.tick_params(axis='both',length=10,grid_linewidth=3)
        axes.tick_params(axis='y', which='minor', length=7, grid_linewidth=0.5, grid_linestyle='--')
        axes.grid(True,linewidth=1,which='both',color='black')
        self.ax = axes

    def update(self,mt_obj,*args,**kwargs):
        self._clean()
        periods = np.log10(1/mt_obj.Tipper.freq)
        
        angle_imag = np.deg2rad(mt_obj.Tipper.angle_imag)
        mag_imag   = mt_obj.Tipper.mag_imag
        angle_real = np.deg2rad(mt_obj.Tipper.angle_real)
        mag_real   = mt_obj.Tipper.mag_real

        # borrowed from MtPy
        txr = np.cos(angle_real)*mag_real
        txi = np.cos(angle_imag)*mag_imag
        tyr = np.sin(angle_real)*mag_real
        tyi = np.sin(angle_imag)*mag_imag
      
        offset_decade  = np.asarray([-3,5])
        self.ax.set_ylim([-0.5,0.5])
        self.ax.set_xlim(offset_decade)
        
     
        self.plot_series(periods, txr, tyr, label='real',color=self.facecolor_real)
        self.plot_series(periods, txi, tyi, label='imag',color=self.facecolor_imag)
        
        if  self.legend:
            self.legend=self.ax.legend(loc='upper left')
            self.legend=False
        
    def plot_series(self, periods, dx, dy, color, label):
        """
        
        dx/y flipped to conform to geographic coordinates

        Parameters
        ----------
        periods : TYPE
            DESCRIPTION.
        dx : TYPE
            DESCRIPTION.
        dy : TYPE
            DESCRIPTION.
        color : TYPE
            DESCRIPTION.
        label : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        quiver_obj=self.ax.quiver(periods,np.zeros(periods.shape),dy,dx,label=label,angles='xy',
                      color=color,headwidth=self.head_width,headlength=self.head_length)
        self.plot.append(quiver_obj)
        
        
class TipperView(_Format):
    fontsize = 12
    weight ='bold'
    kxr_color = 'crimson'
    kxi_color = 'crimson'
    kyr_color = 'blue'
    kyi_color = 'blue'
    def __init__(self):
        super().__init__()
        self.plot=[]
        self.legend=True

    def configure(self, axes):
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.set_ylim([-1,1])
        axes.set_ylabel('Tipper',fontsize=self.fontsize,weight=self.weight)
        axes.tick_params(axis='both',length=10,grid_linewidth=3)
        axes.tick_params(axis='y', which='minor', length=7, grid_linewidth=0.5, grid_linestyle='--')
        axes.grid(True,linewidth=1,which='both',color='black')
        self.ax = axes

    def update(self,mt_obj,*args,**kwargs):
        self._clean()
        freq = 1/mt_obj.Tipper.freq
        
        kxr   = np.real(mt_obj.Tipper.tipper[:,0,0])
        kyr   = np.real(mt_obj.Tipper.tipper[:,0,1])
        kxi   = np.imag(mt_obj.Tipper.tipper[:,0,0])
        kyi   = np.imag(mt_obj.Tipper.tipper[:,0,1])

        all_values = np.stack([kxr,kyr,kxi,kyi])
      
        offset_decade  = np.asarray([1e-3,1e5])
        self.ax.set_ylim([-0.3,0.3])
        self.ax.set_xlim(offset_decade)
        
        self.plot.append(self.ax.semilogx(freq,kxr,color=self.kxr_color,label='kxr',
                                          marker=self.xx_marker))
        self.plot.append(self.ax.semilogx(freq,kxi,color=self.kxi_color,linestyle=':',
                                          label='kxi',marker=self.xx_marker,markerfacecolor='none'))
        self.plot.append(self.ax.semilogx(freq,kyr,color=self.kyr_color,label='kyr',
                                          marker=self.xx_marker))
        self.plot.append(self.ax.semilogx(freq,kyi,color=self.kyi_color,linestyle=':',
                                          label='kyi',marker=self.xx_marker,markerfacecolor='none'))
        
        if  self.legend:
            self.legend=self.ax.legend(loc='upper left')
            self.legend=False
        
   
        
    
    
class WeightsView(_Format):
    fontsize = 12
    weight ='bold'

    def __init__(self):
        super().__init__()
        self.plot=[]
        self.legend=True
    def configure(self, axes):
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.set_ylim([-0.5,2])
        axes.set_ylabel('Weights',fontsize=self.fontsize,weight=self.weight)
        axes.tick_params(axis='both',length=10,grid_linewidth=3)
        axes.tick_params(axis='y', which='minor', length=7, grid_linewidth=0.5, grid_linestyle='--')
        axes.grid(True,linewidth=1,which='both',color='black')
        self.ax = axes

    def update(self,mt_obj,*args,**kwargs):
        self._clean()
        periods = 1/mt_obj.Z.freq
        if hasattr(mt_obj,'Weights'):
            print('has weights')
            impedance_stdvs =  np.copy(mt_obj.Weights.impedance_weights)
            impedance_stdvs[impedance_stdvs==-1]=mt_obj.Weights.impedance_ceiling
            
            tipper_stdvs    =  np.copy(mt_obj.Weights.tipper_weights)
            tipper_stdvs[tipper_stdvs==-1]=mt_obj.Weights.tipper_ceiling
            
            period_range = self.ax.get_xlim()
            ones = np.ones(np.asarray(period_range).shape)
            self.ax.set_ylabel('Weights')
            self.plot.append(self.ax.plot(period_range,mt_obj.Weights.impedance_ceiling*ones,
                                          ls='--',color='red',label='Z Ceiling'))
            self.plot.append(self.ax.plot(period_range,mt_obj.Weights.impedance_floor*ones,
                                          color='black',label='Z Floor'))
            self.plot.append(self.ax.plot(period_range,mt_obj.Weights.tipper_ceiling*ones,
                                          ls='--',color='orange',label='K Ceiling'))
            self.plot.append(self.ax.plot(period_range,mt_obj.Weights.tipper_floor*ones,
                                          ls=':',color='darkorange',label='K Floor'))
        else:
            print('printing stdevs')
            impedance_stdvs = mt_obj.Z.z_err
            tipper_stdvs    = mt_obj.Tipper.tipper_err
            max_val = np.amax(impedance_stdvs)
            self.ax.set_ylabel('St-devs')
        
        self.ax.set_ylim([0,1])
        

        self.plot_series(periods, impedance_stdvs[:,0,1],
                         self.xy_marker, self.xy_color,self.xy_ls,r'$Z_{xy}$')
        
        self.plot_series(periods, impedance_stdvs[:,1,0],
                         self.yx_marker, self.yx_color,self.yx_ls,r'$Z_{yx}$')

        self.plot_series(periods, impedance_stdvs[:,1,1], 
                         self.yy_marker, self.yy_color, self.yy_ls,r'$Z_{yy}$')
        
        self.plot_series(periods, impedance_stdvs[:,0,0], 
                         self.xy_marker,self.xx_color,self.xx_ls,r'$Z_{xx}$')
        
        self.plot_series(periods, tipper_stdvs[:,0,0], 
                         self.kx_marker, self.kx_color, self.yy_ls,r'$K_{x}$')

        self.plot_series(periods, tipper_stdvs[:,0,1],
                         self.ky_marker, self.ky_color,self.yx_ls,r'$K_{y}$')
        if  self.legend:
            self.legend=self.ax.legend(loc='upper center',fontsize=7,ncol=6)
            self.legend=False
        
        
        
    def plot_series(self, frequencies, stdev,marker,color,line,label):
        plot_obj=self.ax.plot(get_nonzero_array(frequencies, stdev),
                              get_nonzero_array(stdev, stdev),
                              marker=marker,
                              markersize=self.marker_size,
                              linewidth=self.lw,
                              color=color,
                              ls=line,label=label)
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
