import numpy as np
from BaselineRemoval import BaselineRemoval
from pykalman import KalmanFilter
from pykalman import KalmanFilter

def filter_sort(x):
    output = []
    for i in range(len(x)):
        if i<2 or (i>(len(x)-2)):
            output.append(x[i])
            pass
        else:
            a=x[i-1:i+2]
            a=np.array(a)
            a.sort()
            output.append(a[1])
            pass
        pass
    return output
    pass

def remove_baseline(x,method,para):
    if len(x)<64:
        return x
        pass

    x = np.array(x, dtype=np.float64)
    y = []

    baseObj1 = BaselineRemoval(x)
    if method == 'ModPoly':
        output1 = baseObj1.ModPoly(para)
        y.extend(list(output1))
        pass
    elif method == 'IModPoly':
        output1 = baseObj1.IModPoly(para)
        y.extend(list(output1))
        pass
    elif method == 'ZhangFit':
        output1 = baseObj1.ZhangFit(para)
        y.extend(list(output1))
        pass
    else:
        y.extend(x)
        pass
    if len(y)>0:
        return y
    return x
    pass

def convolve( data, conv_core):
    x = np.array(data, dtype=np.float32)
    conv_core = -1.0*np.array(conv_core, dtype=np.float32)
    if conv_core.sum() != 0:
        conv_core /= conv_core.sum()

    i = len(conv_core) >> 1
    l = len(x)
    xx = [x[0]] * (len(conv_core) >> 1)
    xx.extend(x)
    xx.extend([x[-1]] * (len(conv_core) >> 1))
    y = np.convolve(xx, np.array(conv_core, dtype=np.float32), 'same')[i:i + l]

    # y = np.convolve(x, conv_core, 'same')

    return np.array(y)
    pass

gause1_window = [1, 2, 4, 8, 16, 32, 16, 8, 4, 2, 1]
def Smooth(x):
    y=convolve(x,gause1_window)
    return y
    pass

def Derivative( x):
    derivative_3point = [-0.5, 0, 0.5]
    derivative_5point = [-0.083, 0.66,0, -066.,0.083]

    y=x
    # y=self.fir(y,self.gause_window)
    # y=self.fir(y,self.gause_window)
    y = convolve(y, derivative_3point)
    # y=self.fir(y,self.gause_window)
    return y
    pass

def normalization(x,pos):
    res = []
    dat = x
    if pos<5 or pos>(len(dat)-5):
        th = dat[pos]
        pass
    else:
        th_data=dat[(pos-5):(pos+5)]
        th = max(th_data)
        if th == 0:
            th = sum(th_data) / len(th_data)
            pass
    a = []
    for j in range(len(dat)):
        try:
            a.append(float(dat[j]) / float(th))
        except Exception as e:
            a.append(0)
        pass
    res.extend(a)
    return res
    pass

def snv(data):
    b=np.array(data)
    std=np.std(b)
    average=np.average(b)

    res=[]
    for i in b:
        res.append((i-average)/std)
        pass
    return np.array(res,dtype=float)
    pass

def select_range(x,parameter):
    res=x[parameter[0]:parameter[0] + parameter[1]]
    return res
    pass

def toList(y):
    try:
        return y.tolist()
    except Exception as e:
        return  y
    
def Kalman1D(observations, damping=1):
    # To return the smoothed time series data
    observation_covariance = damping
    initial_value_guess = observations[0]
    transition_matrix = 1
    transition_covariance = 0.1
    initial_value_guess
    kf = KalmanFilter(
        initial_state_mean=initial_value_guess,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition_matrix
    )
    pred_state, state_cov = kf.smooth(observations)
    return pred_state
# 数据预处理
def proc_data(methods,x):
    if len(x) == 0:
        return x
        pass
    y = x
    step = []
    for method in methods:
        if method['method'] == 'RemoveNoise':
            y = filter_sort(y)
            step.append(toList(y))
            pass
        elif method['method'] == 'RemoveBaseline':
            y1 = []
            for parameter in method['parameters']:
                _select_range = y[parameter['select_range'][0]:parameter['select_range'][0] +
                                                              parameter['select_range'][1]]
                para = parameter['parameter']
                func = parameter['func']
                y1.extend(remove_baseline(_select_range, func, para))
                pass
            y = y1
            step.append(toList(y))
            pass
        elif method['method'] == 'Smooth':
            y = Smooth(y).tolist()
            step.append(toList(y))
            pass
        elif method['method'] == 'Derivative':
            y = Derivative(y).tolist()
            step.append(toList(y))
            pass
        elif method['method'] == 'Select_Range':
            y = select_range(y, method['parameters'])
            step.append(toList(y))
            pass
        elif method['method'] == 'Normalization':
            y = normalization(y, method['parameters']['position_index'])
            step.append(toList(y))
            pass
        elif method['method'] == 'Kalman':
            y = np.array(Kalman1D(y)).reshape(-1)
            step.append(toList(y))
            pass
        elif method['method'] == 'SNV':
            y = np.array(snv(y)).reshape(-1)
            step.append(toList(y))
            pass
        pass
    result = []
    try:
        result = y.tolist()
    except Exception as e:
        result =  y
    return result,step