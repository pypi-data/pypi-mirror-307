# type: ignore

from scipy.linalg import solve_discrete_are
from typing import Dict, Optional
import sys 
sys.path.append('.')
import c4dynamics as c4d 
import numpy as np
import warnings 


def _noncontwarning(x): 
  warnings.warn(f"""The system is not continuous. \nDid you mean {x}?""" , c4d.c4warn)


class kalman(c4d.state):
  ''' 
    Kalman Filter.

    Kalman filter class for state estimation. 
    :class:`kalman` provides methods for prediction and update
    phases of the Kalman filter, including both discrete and continuous systems.

    For background material, implementation, and examples, 
    please refer to :mod:`filters <c4dynamics.filters>`. 


    
    Parameters
    ==========
    X : dict
        Initial state variables and their values.
    dt : float, optional 
        Time step to advance the process model. The time interval between two predictions. 
        Mandatory if continuous-time matrices are provided. 
    P0 : numpy.ndarray, optional
        Covariance matrix, or standard deviations array, of the 
        initial estimation error. Mandatory if `steadystate` is False.
        If P0 is one-dimensional array, standard deviation values are 
        expected. Otherwise, variance values are expected.  
    steadystate : bool, optional
        Flag to indicate if the filter is in steady-state mode. Defaults to False.
    A : numpy.ndarray, optional
        Continuous-time state transition matrix. Defaults to None.
    B : numpy.ndarray, optional
        Continuous-time control matrix. Defaults to None.
    C : numpy.ndarray, optional
        Continuous-time measurement matrix. Defaults to None.
    Q : numpy.ndarray, optional
        Process noise covariance matrix. Defaults to None.
    R : numpy.ndarray, optional
        Measurement noise covariance matrix. Defaults to None.
    F : numpy.ndarray, optional
        Discrete-time state transition matrix. Defaults to None.
    G : numpy.ndarray, optional
        Discrete-time control matrix. Defaults to None.
    H : numpy.ndarray, optional
        Discrete-time measurement matrix. Defaults to None.
          
    Notes 
    =====
    1. `kalman` is a subclass of :class:`state <c4dynamics.states.state.state>`, 
    as such the variables provided within the parameter `X` form its state variables. 
    Hence, `X` is a dictionary of variables and their initial values, for example:
    ``X = {'x': x0, 'y': y0, 'z': z0}``.

    2. The filter may be initialized with either continuous-time matrices
    or with discrete-time matrices. 
    However, all the necessary parameters, 
    i.e. `A` and `B` (for continuous system) or `F` and `G` 
    (for discrete system) must be provided consistently.

    3. If continuous-time matrices are provided, then a time step parameter `dt` 
    has to be provided for the advance of the process model between two predictions. 

    4. Steady-state mode: if the underlying system is linear time-invariant (`LTI`), 
    and the noise covariance matrices are time-invariant, 
    then a steady-state mode of the Kalman filter can be employed. 
    In steady-state mode the Kalman gain (`K`) and the estimation covariance matrix 
    (`P`) are computed once and remain constant ('steady-state') for the entire run-time, 
    performing as well as the time-varying filter.   



    Raises
    ======
    TypeError: 
        If X is not a dictionary.
    ValueError: 
        If P0 is not provided when steadystate is False.
    ValueError: 
        If neither continuous nor discrete system matrices are fully provided.


        
    See Also
    ========
    .filters
    .ekf 
    .lowpass
    .seeker 
    .eqm 


    

    Examples
    ========

    The examples in the introduction to the 
    :mod:`filters <c4dynamics.filters>`
    module demonstrate the operations of 
    the Kalman filter for inputs from  
    electromagnetic devices, such as an altimeter, 
    which measures the altitude. 



    
    An accurate Japaneese train travels 150 meters in one second 
    (:math:`F = 1, u = 1, B = 150, Q = 0.05`). 
    A sensor measures the train position with noise 
    variance of :math:`200m^2` (:math:`H = 1, R = 200`).
    The initial position of the train is known with uncertainty 
    of :math:`0.5m` (:math:`P0 = 0.5^2`).
    

    **Note** 

    The system may be interpreted as follows: 
    
    - :math:`F = 1`             - constant position
    
    - :math:`u = 1, B = 150`    - constant velocity control input 
    
    The advantage of this model is in its being first order. 
    However, a slight difference between the actual dynamics and 
    the modeled process will result in a lag with the tracked object.



    Import required packages: 

    .. code:: 

      >>> from c4dynamics.filters import kalman 
      >>> from matplotlib import pyplot as plt  
      >>> import c4dynamics as c4d
 
    
    Let's run a filter.

    First, since the covariance matrices are 
    constant we can utilize the steady state mode of the filter.
    This requires initalization with the respective flag:

    .. code:: 

      >>> v = 150
      >>> sensor_noise = 200 
      >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, G = v, H = 1
      ...                         , Q = 0.05, R = sensor_noise**2, steadystate = True)


    This initialization uses the discrete form of the model. 
    Alternatively, the filter can be initialized with continuous matrices.
    The only requirement for using continuous form is to provide 
    the time step at the initialization stage: 


    .. code:: 

      >>> kf = kalman({'x': 0}, P0 = 0.5**2, A = 0, B = v, C = 1, Q = 0.05
      ...                         , R = sensor_noise**2, steadystate = True, dt = 1)


    .. code:: 

      >>> for t in range(1, 26): #  seconds. 
      ...   # store for later 
      ...   kf.store(t)
      ...   # predict + correct 
      ...   kf.predict(u = 1) 
      ...   kf.detect = v * t + np.random.randn() * sensor_noise 
      ...   kf.storeparams('detect', t)

      
    Recall that a :class:`kalman` object, as subclass of 
    the :class:`state <c4dynamics.states.state.state>`, 
    encapsulates the process state vector:

    .. code:: 

      >>> print(kf)
      [ x ]
    
      
    It can also employ the 
    :meth:`plot <c4dynamics.states.state.state.plot>` 
    or any other method of the `state` class: 


    .. code::

      >>> kf.plot('x')  
      <Axes: ...>
      >>> plt.gca().plot(*kf.data('detect'), 'co', label = 'detection') # doctest: +ELLIPSIS
      [<matplotlib.lines.Line2D ...>]
      >>> plt.gca().legend() 
      <matplotlib.legend.Legend ...>
      >>> plt.show() 

    .. figure:: /_example/kf/steadystate.png

    
    Let's now assume that as the 
    train moves farther from the station, 
    the sensor measurements degrade. 

    The measurement covariance matrix therefore increases accordingly,
    and the steady state mode cannot be used:


    .. code:: 

      >>> v = 150
      >>> kf = kalman({'x': 0}, P0 = 0.5*2, F = 1, G = v, H = 1, Q = 0.05)
      >>> for t in range(1, 26): #  seconds. 
      ...   kf.store(t)
      ...   sensor_noise = 200 + 8 * t 
      ...   kf.predict(u = 1)
      ...   kf.detect = v * t + np.random.randn() * sensor_noise   
      ...   kf.K = kf.update(kf.detect, R = sensor_noise**2) 
      ...   kf.storeparams('detect', t)

      
    .. figure:: /_example/kf/varying_r.png
    
    

  '''
  # TODO maybe change 'time histories' with 'time series' or 'time evolution' 

  Kinf = None 


  def __init__(self, X: dict, dt: Optional[float] = None, P0: Optional[np.ndarray] = None, steadystate: bool = False
                , A: Optional[np.ndarray] = None, B: Optional[np.ndarray] = None, C: Optional[np.ndarray] = None
                  , F: Optional[np.ndarray] = None, G: Optional[np.ndarray] = None, H: Optional[np.ndarray] = None
                    , Q: Optional[np.ndarray] = None, R: Optional[np.ndarray] = None):
    # 
    # P0 is mandatory and it is either the initial state covariance matrix itself or 
    # a vector of the diagonal standard deviations. 
    # dt is for the predict integration.
    # F and H are linear transition matrix and linear measure matrix for
    # a linear kalman filter.
    # Q and R are process noise and measure noise matrices when they are time invariant. 
    ##  



    if not isinstance(X, dict):
      raise TypeError("""X must be a dictionary containig pairs of variables 
                          and initial conditions, e.g.: {''x'': 0, ''y'': 0}""")
    super().__init__(**X)


    # initialize cont or discrete system 
    self.isdiscrete = True 
    #
    # verify shapes consistency: 
    #   x = Fx + Gu + w
    #   y = Hx + v
    # X: nx1, F: nxn, G: nxm, u: mx1, y: 1xk, H: kxn
    # P: nxn, Q: nxn, R: kxk 
    # state matrices should be 2dim array. 
    ##  
    def vershape(M1name, M1rows, M2name, M2columns):
      if M1rows.shape[0] != M2columns.shape[1]: 
        raise ValueError(f"The columns of {M2name} ({M2columns}) must equal """ 
                            f"the rows of {M1name} ({M1rows}).")

    self.G = None 
    if A is not None and C is not None:
      # continuous system 
      # 
      self.isdiscrete = False  
      if dt is None:
        raise ValueError("""dt is necessary for a continuous system""")

      self.dt = dt
      #         

      self.F  = np.atleast_2d(A * dt).astype(float) 
      vershape('A', self.F, 'A', self.F)          # A: nxn
      vershape('X', self.X.T, 'A', self.F)        # A: n columns 
      self.F += np.eye(len(self.F))               # F = I + A*dt  

      self.H  = np.atleast_2d(C) 
      vershape('X', self.X.T, 'C', self.H)        # C: n columns  
      if B is not None: 
        self.G = np.atleast_2d(B * dt).reshape(self.F.shape[0], -1) # now G is necessarily a column vector. 
        # self.G = np.atleast_2d(B) * dt 
        # self.G = self.G.reshape(self.F.shape[0], -1) # now G is necessarily a column vector. 
        # vershape('G (or B)', self.G, 'F (or A)', self.F)    # G: n rows. this one is useless because previous reshpae guarentees is has the correct size.  

    elif F is not None and H is not None:
      # discrete
      self.F  = np.atleast_2d(F).astype(float)
      vershape('F', self.F, 'F', self.F)          # F: nxn
      vershape('X', self.X.T, 'A', self.F)        # F: n columns 

      self.H  = np.atleast_2d(H) 
      vershape('X', self.X.T, 'H', self.H)        # H: n columns  

      if G is not None: 
        self.G = np.atleast_2d(G).reshape(self.F.shape[0], -1) # now G is necessarily a column vector. 
        
    else: 
      raise ValueError("""At least one set of matrices has to be provided entirely:"""
                          """\nFor a continuous system: A, C (B is optional). Where: x' = A*x + B*u + w, y = C*x + v"""
                            """\nFor a dicscrete system: F, H (G is optional). Where: x(k) = F*x(k-1) + G*u(k-1) + w(k-1), y(k) = H*x(k) + v(k)""")
    
    self.Q = None
    self.R = None 
    if Q is not None:
      self.Q = np.atleast_2d(Q) 
      vershape('Q', self.Q, 'Q', self.Q)                    # Q: nxn 
      vershape('X', self.X.T, 'Q', self.Q)                  # Q: n columns 
    if R is not None:
      self.R = np.atleast_2d(R)  
      vershape('R', self.R, 'R', self.R)                    # R: kxk 
      vershape('H' if self.isdiscrete else 'H', self.H, 'R', self.R) # R: k columns 
      
    
    if steadystate: 
      # in steady state mode Q and R must be provided: 
      if self.Q is None or self.R is None:
        raise ValueError("""In steady-state mode, the noise matrices Q and R must be provided.""")

      self.P = solve_discrete_are(self.F.T, self.H.T, self.Q, self.R)
      self.Kinf = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)

    else: # steady state is off 
      if P0 is None:
        # NOTE maybe init with zeros and raising warning is better solution. 
        raise ValueError(r'P0 must be provided (optional only in steadystate mode)')


      if np.array(P0).ndim == 1: 
        # an array of standard deviations is provided 
        self.P = np.diag(np.array(P0).ravel()**2)
      else:
        P0 = np.atleast_2d(P0)      
        if P0.shape[0] == P0.shape[1]:  
          # square matrix
          self.P = P0

    self._Pdata = []   



  @property
  def A(self):
    if self.isdiscrete: 
      _noncontwarning('F')
      return None
    
    a = (self.F - np.eye(len(self.F))) / self.dt 
    return a 

  @A.setter
  def A(self, a):
    if self.isdiscrete: 
      _noncontwarning('F') 
    else: 
      self.F = np.eye(len(a)) + a * self.dt 


  @property 
  def B(self):
    if self.isdiscrete: 
      _noncontwarning('G') # the system is not continuous. did u mean G? 
      return None 
    elif self.G is None: 
      return None 
    
    return self.G / self.dt  
  
  @B.setter
  def B(self, b):
    if self.isdiscrete: 
      _noncontwarning('G')
    else: 
      self.G = b * self.dt 


  @property 
  def C(self):
    if self.isdiscrete: 
      _noncontwarning('H')
      return None 
    return self.H 
  
  @C.setter
  def C(self, c):
    if self.isdiscrete: 
      _noncontwarning('H')
    else: 
      self.H = c


  def predict(self, u: Optional[np.ndarray] = None, Q: Optional[np.ndarray] = None):
    '''
      Predicts the filter's next state and covariance matrix based 
      on the current state and the process model.
      
      Parameters
      ----------
      u : numpy.ndarray, optional
          Control input. Defaults to None.
      Q : numpy.ndarray, optional
          Process noise covariance matrix. Defaults to None.


      Raises
      ------
      ValueError
          If `Q` is not missing (neither provided 
          during construction nor passed to `predict`). 
      ValueError
          If a control input is provided, but the number of elements in `u` 
          does not match the number of columns of the input matrix (`B` or `G`). 
          
          
      Examples
      --------
      For more detailed usage, 
      see the examples in the introduction to 
      the :mod:`c4dynamics.filters` module and 
      the :class:`kalman` class.

      

      
      Import required packages: 

      .. code:: 

        >>> from c4dynamics.filters import kalman 



      Plain `predict` step 
      (predict in steady-state mode where the process variance matrix 
      remains constant 
      and is provided once to initialize the filter): 

      .. code:: 

        >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, H = 1, Q = 0.05, R = 200, steadystate = True)
        >>> print(kf)
        [ x ]
        >>> kf.X 
        array([0.])
        >>> kf.P
        array([[3.18...]])
        >>> kf.predict()
        >>> kf.X
        array([0.])
        >>> kf.P
        array([[3.18...]])


      Predict with control input: 

      .. code:: 

        >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, G = 150, H = 1, R = 200, Q = 0.05)
        >>> kf.X
        array([0.])
        >>> kf.P
        array([[0.25...]])
        >>> kf.predict(u = 1)
        >>> kf.X
        array([150.])
        >>> kf.P
        array([[0.3]])


        
      Predict with updated process noise covariance matrix: 

      .. code:: 

        >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, G = 150, H = 1, R = 200, Q = 0.05)
        >>> kf.X
        array([0.])
        >>> kf.P
        array([[0.25]])
        >>> kf.predict(u = 1, Q = 0.01)
        >>> kf.X
        array([150.])
        >>> kf.P
        array([[0.26]])


    '''
    # TODO test the size of the objects. 
    # test the type. 
    # make sure the user is working with c4d modules. 
    # actually only u should be tested here all the other need be tested at the init stage. 
	  # this F must be linear, but it can be linearized once for the entire
    # process (regular kalman), or linearized and delivered at each step (extended kalman)
  

    if self.Kinf is None:

      if Q is not None: 
        self.Q = np.atleast_2d(Q) 
      elif self.Q is None: 
        raise ValueError("""Q is missing. It can be provided once at construction """
                         """or in every call to predict() """)

      self.P = self.F @ self.P @ self.F.T + self.Q
         
    # this F can be either linear or nonlinear function of x. 
    self.X = self.F @ self.X 

    if u is not None: 
      if self.G is None:
        warnings.warn(f"""\nWarning: u={u} is introduced as control input but the input matrix is zero! (G for discrete system or B for continuous).""", c4d.c4warn) 
      else:   
        u = np.atleast_2d(u)      
        if len(u.ravel()) != self.G.shape[1]:
          raise ValueError(f"""The number of elements in u must equal the number of columns of the input matrix (B or G), {len(u.ravel())} != {self.G.shape[1]}""")
        self.X += self.G @ u.ravel() 

    
 
  def update(self, z: np.ndarray, R: Optional[np.ndarray] = None):
    '''
      Updates (corrects) the state estimate based on the given measurements.
      
      Parameters
      ----------
      z : numpy.ndarray
          Measurement vector.
      R : numpy.ndarray, optional
          Measurement noise covariance matrix. Defaults to None.

      Returns
      -------
      K : numpy.ndarray 
          Kalman gain. 


      Raises
      ------
      ValueError
          If the number of elements in `z` does not match 
          the number of rows in the measurement matrix (C or H). 
      ValueError
          If `R` is missing (neither provided 
          during construction 
          nor passed to `update`). 
          
      Examples
      --------
      For more detailed usage, 
      see the examples in the introduction to 
      the :mod:`c4dynamics.filters` module and 
      the :class:`kalman` class.

      
      
      Import required packages: 

      .. code:: 

        >>> from c4dynamics.filters import kalman 



      Plain update step 
      (update in steady-state mode 
      where the measurement covariance matrix remains 
      and is provided once during filter initialization): 

      .. code:: 

        >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, H = 1, Q = 0.05, R = 200, steadystate = True)
        >>> print(kf)
        [ x ]
        >>> kf.X 
        array([0.])
        >>> kf.P
        array([[3.18...]])
        >>> kf.update(z = 100) # returns Kalman gain
        array([[0.01568688]])
        >>> kf.X
        array([1.56...])
        >>> kf.P
        array([[3.18...]])


        
      Update with modified measurement noise covariance matrix: 

      .. code:: 

        >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, G = 150, H = 1, R = 200, Q = 0.05)
        >>> kf.X
        array([0.])
        >>> kf.P
        array([[0.25]])
        >>> K = kf.update(z = 150, R = 0)
        >>> K 
        array([[1.]])
        >>> kf.X
        array([150.])
        >>> kf.P
        array([[0.]])

          
    '''

    
    # this H must be linear, but as F may it be linearized once about an equilibrium point for 
    # the entire process (regular kalman) or at each 
    # iteration about the current state (ekf). 
    # TODO add Mahalanobis optional test 
    z = np.atleast_2d(z).ravel()
    if len(z) != self.H.shape[0]:
      raise ValueError(f"""The number of elements in the input z must equal """
                          f"""the number of rows of the measurement matrix (C or H), """
                              f"""{len(z.ravel())} != {self.H.shape[0]}""")
    
    if self.Kinf is None:
      if R is not None: 
        self.R = np.atleast_2d(R)
      elif self.R is None: 
        raise ValueError("""R is missing. It can be provided once at construction """
                         """or in every call to update() """)

      K = self.P @ self.H.T @ np.linalg.inv(self.H @ self.P @ self.H.T + self.R)
      self.P = self.P - K @ self.H @ self.P
    else: 
      K = self.Kinf

    # this H can be expressed as either linear or nonlinear function of x.  
    self.X += K @ (z - self.H @ self.X) # nx1 = nxm @ (mx1 - mxn @ nx1)
    return K 
    

  def store(self, t: int = -1):
    ''' 
      Stores the current state and diagonal elements of the covariance matrix.
          
      The :meth:`store` method captures the current state of the Kalman filter, 
      storing the state vector (`X`) and the error covariance matrix (`P`) 
      at the specified time. 
      

      Parameters
      ----------
      t : int, optional
          The current time at which the state is being stored. Defaults to -1.
      

      Notes
      -----
      1. The stored data can be accessed via :meth:`data` or other methods for 
         post-analysis or visualization.
      2. The elements on the main diagonal of the covariance matrix are named 
         according to their position, starting with 'P' followed by their row and column indices. 
         For example, the first element is named 'P00', and so on.
      3. See also :meth:`store <c4dynamics.states.state.state.store>` 
         and :meth:`data <c4dynamics.states.state.state.data>` 
         for more details. 

      Examples
      -------- 
      For more detailed usage, 
      see the examples in the introduction to 
      the :mod:`c4dynamics.filters` module and 
      the :class:`kalman` class.

        

        
      Import required packages: 

      .. code:: 

        >>> from c4dynamics.filters import kalman 


      
      .. code:: 

        >>> kf = kalman({'x': 0}, P0 = 0.5**2, F = 1, H = 1, Q = 0.05, R = 200)
        >>> # store initial conditions
        >>> kf.store() 
        >>> kf.predict()
        >>> # store X after prediction
        >>> kf.store() 
        >>> kf.update(z = 100) 
        array([[0.00149...]])
        >>> # store X after correct
        >>> kf.store() 

      Access stored data: 
      
      .. code:: 

        >>> kf.data('x')[1]
        array([0.        , 0.        , 0.14977534])
        >>> kf.data('P00')[1]
        array([0.25      , 0.3       , 0.29955067])
          
    '''
    
    super().store(t) # store state 
    # store covariance: 
    for i, p in enumerate(np.diag(self.P)): 
      pstr = f'P{i}{i}'
      setattr(self, pstr, p) # set 
      self.storeparams(pstr, t) # store 
    

  @staticmethod
  def velocitymodel(dt: float, process_noise: float, measure_noise: float):
    '''
      Defines a linear Kalman filter model for tracking position and velocity.

      Parameters
      ----------
      dt : float
          Time step for the system model.
      process_noise : float
          Standard deviation of the process noise.
      measure_noise : float
          Standard deviation of the measurement noise.

      Returns
      -------
      kf : kalman
          A Kalman filter object initialized with the linear system model.

          

      X = [x, y, w, h, vx, vy]
      #    0  1  2  3  4   5  

      x'  = vx
      y'  = vy
      w'  = 0
      h'  = 0
      vx' = 0
      vy' = 0

      H = [1 0 0 0 0 0
          0 1 0 0 0 0
          0 0 1 0 0 0
          0 0 0 1 0 0]
    '''
    from scipy.linalg import expm 

    A = np.zeros((6, 6))
    A[0, 4] = A[1, 5] = 1
    F = expm(A * dt)
    H = np.zeros((4, 6))
    H[0, 0] = H[1, 1] = H[2, 2] = H[3, 3] = 1

    Q = np.eye(6) * process_noise**2
    R = np.eye(4) * measure_noise**2

    kf = kalman({'x': 0, 'y': 0, 'w': 0, 'h': 0, 'vx': 0, 'vy': 0}
                          , steadystate = True, F = F, H = H, Q = Q, R = R)
    return kf 


  @staticmethod
  def nees(kf, true_obj):
    ''' normalized estimated error squared '''

    Ptimes = kf.data('P00')[0]
    err = []
    for t in kf.data('t'):

      xkf = kf.timestate(t)
      xtrain = true_obj.timestate(t)

      idx = min(range(len(Ptimes)), key = lambda i: abs(Ptimes[i] - t))
      P = kf.data('P00')[1][idx]

      xerr = xtrain - xkf
      err.append(xerr**2 / P)  
    return np.mean(err)







if __name__ == "__main__":
  import contextlib
  import doctest

  doctest.testmod(optionflags = doctest.ELLIPSIS)

  # # Redirect both stdout and stderr to a file within this block
  # with open(os.path.join('tests', '_out', 'output.txt'), 'w') as f:
  #   with contextlib.redirect_stdout(f), contextlib.redirect_stderr(f):
  #     doctest.testmod()
 



