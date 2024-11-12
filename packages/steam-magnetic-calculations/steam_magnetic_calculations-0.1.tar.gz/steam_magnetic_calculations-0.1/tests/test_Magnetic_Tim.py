import  numpy as np
import  matplotlib.pyplot as plt
import  pandas as pd
import  os
from    matplotlib              import cm
import  time

def Mag_2D_XY_array(source, target, I):
    """ Calculates the Bx and By field given a current source pointing in the z direction.
    :param source: [x, y] The position of the source element.
    :param target: [x, y] The position of the target.
    :param I: The current.
    :return: Bx and By.
    """

    # Ampere's law: B = mu0I/2piR   for vectors  I*dL (current)  and   D  (element-center to XYZ)
    Dxy = np.array(target) - np.array(source)  # vector from element-center to XYZ
    D = np.linalg.norm(Dxy, axis=1)  # distance from element-center to XYZ
    f = 2e-7 * I / D
    angle1 = np.arccos(Dxy[:, 1]/D)
    angle2 = np.arccos(Dxy[:, 0]/D)
    Bx =  np.cos(angle1) * f
    By = -np.cos(angle2) * f
    Bx = np.sum(np.where(D > 0.0005, Bx, 0.0))
    By = np.sum(np.where(D > 0.0005, By, 0.0))
    return Bx, By

class Magnetic_Tim:
    # Points
    sources: list   = None
    targets: list   = None
    source_x        = None
    source_y        = None
    source_I        = None
    source_Bx       = None
    source_By       = None
    Bx: list        = None
    By: list        = None

    # Grid
    xmin            = None
    xmax            = None
    ymin            = None
    ymax            = None
    dx              = None
    dy              = None
    nxy: int        = 55
    xv              = None
    yv              = None
    Bx_grid         = None
    By_grid         = None

    # Comparison
    error               = None
    max_error: float    = 1e-3
    passed: bool        = False

    # Analytics:
    t1_start            = None
    t1_stop             = None
    t2_start            = None
    t2_stop             = None

    # Figures
    fig1 = None

    ax1 = None
    ax2 = None
    ax3 = None
    ax4 = None
    ax5 = None
    ax6 = None

    # Input
    magnet_path     = None
    magnet_name     = None
    output_folder   = None

    def __init__(self, mp):
        self.magnet_path = mp

        self.reset()
        self.make_folders()
        self.load_magnet()
        self.calc_B_grid()
        self.calc_B_points()
        self.plot_magnet()
        self.check_test()
        self.plot_analytics()

    def reset(self):
        # Points
        self.sources = []
        self.targets= []
        self.source_x = None
        self.source_y = None
        self.source_I = None
        self.source_Bx = None
        self.source_By = None
        self.Bx = []
        self.By = []

        # Grid
        self.xmin       = None
        self.xmax       = None
        self.ymin       = None
        self.ymax       = None
        self.dx = None
        self.dy = None
        self.nxy        = 55
        self.xv         = None
        self.yv         = None
        self.Bx_grid    = None
        self.By_grid    = None

        # Comparison
        self.error      = None
        self.max_error  = 1e-3
        self.passed     = False

        # Analytics:
        self.t1_start   = None
        self.t1_stop    = None
        self.t2_start   = None
        self.t2_stop    = None

        # Figures
        self.fig1 = plt.figure(figsize=(15, 10))

        self.ax1 = self.fig1.add_subplot(231)
        self.ax2 = self.fig1.add_subplot(232)
        self.ax3 = self.fig1.add_subplot(233)
        self.ax4 = self.fig1.add_subplot(234)
        self.ax5 = self.fig1.add_subplot(235)
        self.ax6 = self.fig1.add_subplot(236)

        # Inputs
        self.magnet_name  = None
        self.output_folder = None

    def check_test(self):
        if np.max(self.error) < self.max_error:
            self.passed = True

    def make_folders(self):
        cpath = os.getcwd()

        self.output_folder = cpath + os.sep + 'output'
        try:
            os.mkdir(self.output_folder)
        except OSError:
            print("Creation of the directory %s failed" % self.output_folder)
        else:
            print("Successfully created the directory %s " % self.output_folder)

        self.magnet_name = os.path.basename(self.magnet_path)

    def plot_analytics(self):
        self.ax6.text(0, 1, 'Analytics', ha='left', va='top')
        self.ax6.text(0, 0.95, 'Number of nodes: ' + str(len(self.source_x)), ha='left', va='top')
        self.ax6.text(0, 0.9, 'Peak magnetic field, T (map2d): ' + str(np.round(np.max((np.array(self.source_Bx) ** 2 + np.array(self.source_By) ** 2) ** 0.5), 3)), ha='left', va='top')
        self.ax6.text(0, 0.85, 'Number of field map nodes: ' + str(self.nxy*self.nxy), ha='left', va='top')
        self.ax6.text(0, 0.80, 'Computing time Field Map, s: ' + str(np.round(self.t1_stop-self.t1_start, 3)), ha='left', va='top')
        self.ax6.text(0, 0.75, 'Computing time Field Conductor, s: ' + str(np.round(self.t2_stop-self.t2_start, 3)), ha='left', va='top')
        self.ax6.text(0, 0.70, 'Max error, dt/T$_{max}$: ' + str(np.max(self.error)), ha='left', va='top')
        self.ax6.text(0, 0.65, 'Max allowed error, dt/T$_{max}$: ' + str(self.max_error), ha='left', va='top')
        self.ax6.text(0, 0.60, 'Test passed: ' + str(self.passed), ha='left', va='top')

        self.ax6.axis('off')

        self.fig1.savefig(self.output_folder + os.sep + self.magnet_name + '.png', dpi=300)

    def load_magnet(self):
        df1 = pd.read_csv(self.magnet_path, delim_whitespace=True)
        print(df1.columns)
        self.source_x = df1['X-POS/MM'].values*1e-3
        self.source_y = df1['Y-POS/MM'].values*1e-3
        self.source_I = df1['CURRENT'].values
        self.source_Bx = df1['BX/T'].values
        self.source_By = df1['BY/T'].values

        for i in range(len(self.source_x)):
            self.sources.append([self.source_x[i], self.source_y[i], self.source_I[i]])
            self.targets.append([self.source_x[i], self.source_y[i]])

        self.xmax = np.max(self.source_x)
        self.xmin = np.min(self.source_x)
        self.ymax = np.max(self.source_y)
        self.ymin = np.min(self.source_y)

        self.dx = (self.xmax - self.xmin)/2
        self.dy = (self.ymax - self.ymin)/2
        self.xv, self.yv = np.meshgrid(np.linspace(self.xmin-self.dx, self.xmax+self.dx, self.nxy), np.linspace(self.ymin-self.dy, self.ymax+self.dy, self.nxy))
        print(df1.head())

    def calc_B_grid(self):
        self.Bx_grid = np.zeros((self.nxy, self.nxy))
        self.By_grid = np.zeros((self.nxy, self.nxy))
        x = np.linspace(self.xmin-self.dx, self.xmax+self.dx, self.nxy)
        y = np.linspace(self.ymin-self.dy, self.ymax+self.dy, self.nxy)
        self.t1_start = time.time()
        for i in range(len(x)):
            for j in range(len(y)):
                self.Bx_grid[j,i], self.By_grid[j,i] = Mag_2D_XY_array(self.targets, [x[i], y[j]], self.source_I)
        self.t1_stop = time.time()

    def calc_B_points(self):
        self.t2_start = time.time()
        for i in self.targets:
            Bxt, Byt = Mag_2D_XY_array(self.targets, i, self.source_I)
            self.Bx.append(Bxt)
            self.By.append(Byt)
        self.t2_stop = time.time()

    def plot_magnet(self):
        # x = [i[0] for i in self.sources]
        # y = [i[1] for i in self.sources]
        x1, y1 = [], []
        x2, y2 = [], []
        for i in range(len(self.source_I)):
            if self.source_I[i] > 0.0:
                x1.append(self.source_x[i])
                y1.append(self.source_y[i])
            else:
                x2.append(self.source_x[i])
                y2.append(self.source_y[i])

        self.ax1.plot(x1, y1, ls='', marker='o', color='red', mfc='white', markersize=1)
        self.ax1.plot(x2, y2, ls='', marker='o', color='blue', mfc='white', markersize=1)
        self.ax1.contourf(self.xv, self.yv, (self.Bx_grid**2+self.By_grid**2)*0.5, cmap=cm.coolwarm, levels=35)
        self.ax1.streamplot(self.xv, self.yv, self.Bx_grid, self.By_grid, density=1.0, color='white')
        self.ax1.set_xlim((self.xmin, self.xmax))
        self.ax1.set_ylim((self.ymin, self.ymax))
        self.ax1.axis('equal')
        self.ax1.set_xlabel('Position, m')
        self.ax1.set_ylabel('Position, m')
        self.ax1.set_title('Field Map')

        B = (np.array(self.Bx)**2+np.array(self.By)**2)**0.5
        self.ax2.scatter(self.source_x, self.source_y, c=B, vmin=0, vmax=np.max(B), cmap=cm.coolwarm)
        self.ax2.axis('equal')
        self.ax2.set_xlabel('Position, m')
        self.ax2.set_ylabel('Position, m')
        self.ax2.set_title('Biot Savart - Tim')

        B2 = (np.array(self.source_Bx) ** 2 + np.array(self.source_By) ** 2) ** 0.5
        self.ax3.scatter(self.source_x, self.source_y, c=B2, vmin=0, vmax=np.max(B2), cmap=cm.coolwarm)
        self.ax3.axis('equal')
        self.ax3.set_xlabel('Position, m')
        self.ax3.set_ylabel('Position, m')
        self.ax3.set_title('Biot Savart - map2d')

        self.error = abs(B-B2)/np.max(abs(B2))
        self.ax4.scatter(self.source_x, self.source_y, c=self.error, vmin=0, vmax=np.max(self.error), cmap=cm.coolwarm)
        self.ax4.axis('equal')
        self.ax4.set_xlabel('Position, m')
        self.ax4.set_ylabel('Position, m')
        self.ax4.set_title('Difference BS-map2d')

        self.ax5.plot(self.error, ls='', marker='o', color='black', mfc='white', markersize=1)
        self.ax5.set_xlabel('Position, m')
        self.ax5.set_ylabel('Relative error, dT/T$_{max}$')
        self.ax5.set_title('Difference BS-map2d')

def test1():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'CFD_600A_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test2():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'd11T_1in1_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test3():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'D1_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test4():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'D2_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test5():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'ERMC_V1_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test6():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'FRESCA2_15T_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test7():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'FRESCA2_15T_All_NoIron_NoSelfField_testTODELETE.map2d')
	assert x.passed

def test8():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD2_2019_REV_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test9():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD2_B_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test10():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD2_D_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test11():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD2_REV_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test12():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD3_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test13():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD3_CuSC200pp_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test14():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'HD3_Modifications_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test15():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MBRB_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test16():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MBRC_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test17():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MBX_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test18():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MB_2COILS_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test19():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MB_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test20():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBCH_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test21():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBCV_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test22():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBH_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test23():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBV_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test24():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBXF_HV_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test25():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBX_HV_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test26():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBX_HV_CopperWedges_ThCool_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test27():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBX_HV_ROXIE_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test28():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBYH_1AP_SHORT1209_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test29():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBYV_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test30():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBY_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test31():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBY_1P_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test32():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCBY_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test33():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCDO_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test34():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCDXF_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test35():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCOXF_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test36():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCSXF_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test37():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCS_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test38():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCS_All_NoIron_NoSelfField_55A.map2d')
	assert x.passed

def test39():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCS_All_NoIron_NoSelfField_5A.map2d')
	assert x.passed

def test40():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCTSXF_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test41():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MCTX_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test42():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MED_C_COMB_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test43():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MO_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test44():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MO_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test45():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQM_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test46():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQSXF_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test47():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQSX_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test48():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQS_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test49():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQTLH_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test50():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQTLH_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test51():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQTLI_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test52():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQT_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test53():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQXA_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test54():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQXA_All_NoIron_NoSelfField_no_contraction.map2d')
	assert x.passed

def test55():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQXB_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test56():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQXF_V2_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test57():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQY_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test58():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQ_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test59():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MQ_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test60():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MSS_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test61():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MS_1AP_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test62():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'MU_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test63():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'RMM_V1_6CS_All_NoIron_NoSelfField.map2d')
	assert x.passed

def test64():
	path = os.getcwd()
	x = Magnetic_Tim(path + os.sep + 'input' + os.sep + 'map2d_noIron_NoSelfField' + os.sep + 'RMM_V1_All_NoIron_NoSelfField.map2d')
	assert x.passed
