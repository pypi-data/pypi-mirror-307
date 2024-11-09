import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
# import pyamg
import time
from sympy import symbols, Matrix, diff, expand
import itertools
import os
import pyvista

__version__ = "1.0.0"

def get_element_stiffness_matrix_2d(E=1, nu=1/3):
    _E = E
    _nu = nu
    # SymPy symbols:
    a, b, x, y = symbols('a b x y')
    E, nu = symbols('E nu')
    N1, N2, N3, N4 = symbols('N1 N2 N3 N4')
    xlist = [x] * 8
    ylist = [y] * 8
    yxlist = [y, x] * (8 // 2)

    # Shape functions:
    # 基函数
    N1 = (a - x) * (b - y) / (4 * a * b)  # (-a, -b)点对(x, y)点的影响
    N2 = (a - x) * (b + y) / (4 * a * b)  # (-a, b)点对(x, y)点的影响
    N3 = (a + x) * (b - y) / (4 * a * b)  # (a, -b)点对(x, y)点的影响
    N4 = (a + x) * (b + y) / (4 * a * b)  # (a, b)点对(x, y)点的影响

    # Create strain-displacement matrix B:
    B0 = tuple(map(diff, [N1, 0, N2, 0, N3, 0, N4, 0], xlist))
    B1 = tuple(map(diff, [0, N1, 0, N2, 0, N3, 0, N4], ylist))
    B2 = tuple(map(diff, [N1, N1, N2, N2, N3, N3, N4, N4], yxlist))
    B = Matrix([B0, B1, B2])

    # Create constitutive (material property) matrix for plane stress:
    C = (E / (1 - nu ** 2)) * Matrix([[1, nu, 0],
                                      [nu, 1, 0],
                                      [0,  0, (1 - nu) / 2]])

    dK = B.T * C * B
    # print('B =', B.subs({a: 0.5, b: 0.5, E: _E, nu: _nu}))
    # print('C =', C.subs({a: 0.5, b: 0.5, E: _E, nu: _nu}))

    # Integration:
    # print('SymPy is integrating: K for Q4...')
    K = dK.integrate((x, -a, a), (y, -b, b))

    # Convert SymPy Matrix to NumPy array:
    K = np.array(K.subs({a: 0.5, b: 0.5, E: _E, nu: _nu})).astype('double')

    # Set small (<< 0) values equal to zero:
    K[np.abs(K) < 1e-6] = 0
    
    return K

def get_element_stiffness_matrix_3d(E=1, nu=1/3):
    _E = E  # modulus of elasticity
    _nu = nu  # poisson's ratio

    _a, _b, _c = 0.5, 0.5, 0.5  # element dimensions (half-lengths) don't change!
    _G = _E / (2 * (1 + _nu))  # modulus of rigidity
    _g = _E /  ((1 + _nu) * (1 - 2 * _nu))
    
    # SymPy symbols:
    a, b, c, x, y, z = symbols('a b c x y z')
    N1, N2, N3, N4, N5, N6, N7, N8 = symbols('N1 N2 N3 N4 N5 N6 N7 N8')
    nu, g, G = symbols('nu g G')
    o = symbols('o') #  dummy symbol
    xlist = [x] * 24
    ylist = [y] * 24
    zlist = [z] * 24
    yxlist = [y, x, o] * (24 // 3)
    zylist = [o, z, y] * (24 // 3)
    zxlist = [z, o, x] * (24 // 3)

    # Shape functions:
    N1 = (a - x) * (b - y) * (c - z) / (8 * a * b * c)
    N2 = (a - x) * (b - y) * (c + z) / (8 * a * b * c)
    N3 = (a - x) * (b + y) * (c - z) / (8 * a * b * c)
    N4 = (a - x) * (b + y) * (c + z) / (8 * a * b * c)
    N5 = (a + x) * (b - y) * (c - z) / (8 * a * b * c)
    N6 = (a + x) * (b - y) * (c + z) / (8 * a * b * c)
    N7 = (a + x) * (b + y) * (c - z) / (8 * a * b * c)
    N8 = (a + x) * (b + y) * (c + z) / (8 * a * b * c)

    # Create strain-displacement matrix B:
    B0 = tuple(map(diff, [N1, 0, 0, N2, 0, 0, N3, 0, 0, N4, 0, 0, N5, 0, 0, N6, 0, 0, N7, 0, 0, N8, 0, 0], xlist))
    B1 = tuple(map(diff, [0, N1, 0, 0, N2, 0, 0, N3, 0, 0, N4, 0, 0, N5, 0, 0, N6, 0, 0, N7, 0, 0, N8, 0], ylist))
    B2 = tuple(map(diff, [0, 0, N1, 0, 0, N2, 0, 0, N3, 0, 0, N4, 0, 0, N5, 0, 0, N6, 0, 0, N7, 0, 0, N8], zlist))
    B3 = tuple(map(diff, [N1, N1, N1, N2, N2, N2, N3, N3, N3, N4, N4, N4, N5, N5, N5, N6, N6, N6, N7, N7, N7, N8, N8, N8], yxlist))
    B4 = tuple(map(diff, [N1, N1, N1, N2, N2, N2, N3, N3, N3, N4, N4, N4, N5, N5, N5, N6, N6, N6, N7, N7, N7, N8, N8, N8], zylist))
    B5 = tuple(map(diff, [N1, N1, N1, N2, N2, N2, N3, N3, N3, N4, N4, N4, N5, N5, N5, N6, N6, N6, N7, N7, N7, N8, N8, N8], zxlist))
    B = Matrix([B0, B1, B2, B3, B4, B5])

    # Create constitutive (material property) matrix:
    C = Matrix([[(1 - nu) * g, nu * g, nu * g, 0, 0, 0],
                [nu * g, (1 - nu) * g, nu * g, 0, 0, 0],
                [nu * g, nu * g, (1 - nu) * g, 0, 0, 0],
                [0, 0, 0,                      G, 0, 0],
                [0, 0, 0,                      0, G, 0],
                [0, 0, 0,                      0, 0, G]])
    C = C.subs({nu: _nu, g: _g, G: _G})

    dK = B.T * C * B
    # B_debug = B.subs({a: 0.5, b: 0.5, c: 0.5, E: _E, nu: _nu, x: 0.3, y: 0.6, z: 0.1})
    # C_debug = C.subs({a: 0.5, b: 0.5, c: 0.5, E: _E, nu: _nu, x: 0.3, y: 0.6, z: 0.1})
    # return B_debug, C_debug
    # return np.array(dK.subs({a: 0.5, b: 0.5, c: 0.5, E: _E, nu: _nu, x: 0.3, y: 0.6, z: 0.1}))

    # Integration:
    # print('SymPy is integrating: K for H8...')
    K = dK.integrate((x, -a, a),(y, -b, b),(z, -c, c))

    # Convert SymPy Matrix to NumPy array:
    K = np.array(K.subs({a: _a, b: _b, c: _c})).astype('double')
    
    return K

def get_M_n(d:int, n:int, E=1, nu=1/3):
    return E / (1-(n - 1) * nu - (d - n) * n / (1 - max(0, d - n - 1) * nu) * nu ** 2)

def get_element_stiffness_matrix(E=1, nu=1/3, dimensional=2):
    # E: modulus of elasticity
    # nu: poisson's ratio

    # if dimensional == 2:
    #     return get_element_stiffness_matrix_2d(E=E, nu=nu)
    # elif dimensional == 3:
    #     return get_element_stiffness_matrix_3d(E=E, nu=nu)
    # else:
    #     return None

    dof = dimensional * 2 ** dimensional
    M_1 = get_M_n(dimensional, 1, E=E, nu=nu)
    M_2 = get_M_n(dimensional, 2, E=E, nu=nu)
    G = E / (2 * (1 + nu))  # modulus of rigidity

    C = np.zeros([dimensional + dimensional * (dimensional - 1) // 2] * 2)
    C[:dimensional, :dimensional] = np.eye(dimensional) * (M_1 * 2 - M_2) + np.ones([dimensional] * 2) * (M_2 - M_1)
    C[dimensional:, dimensional:] = np.eye(dimensional * (dimensional - 1) // 2) * G

    C = Matrix(C)  # Constitutive (material property) matrix:
    
    # SymPy symbols
    xs = ''
    for i in range(dimensional):
        xs += (' ' if i > 0 else '') + 'x' + str(i)
    xs = symbols(xs)

    Ns = []
    for I in itertools.product(*([[-1, 1]] * dimensional)):
        Ns.append(1)
        for j, i in enumerate(I):
            Ns[-1] *= 0.5 + i * xs[j]
        
    # Create strain-displacement matrix B:
    B = [[0] * dof for i in range(dimensional)]
    for i, x in enumerate(xs):
        for j, N in enumerate(Ns):
            B[i][j * dimensional + i] = diff(N, x)
    for i, x in enumerate(xs):
        for j, y in enumerate(xs):
            if j <= i:
                continue
            B.append([0] * dof)
            for k, N in enumerate(Ns):
                B[-1][k * dimensional + i] = diff(N, y)
                B[-1][k * dimensional + j] = diff(N, x)
    B = Matrix(B)

    dK = B.T * C * B

    # Because dK is symmetric, only need to integrate about half of it. 
    K = np.zeros([dof] * 2)
    for i in range(dof):
        for j in range(0, i + 1):
            K[i, j] = expand(dK[i * dof + j]).integrate(*[[x, -0.5, 0.5] for x in xs])
    for i in range(dof):
        for j in range(i + 1, dof):
            K[i, j] = K[j, i]
    
    return K

# A 165 LINE 2D TOPOLOGY OPTIMIZATION CODE BY NIELS AAGE AND VILLADS EGEDE JOHANSEN, JANUARY 2013

def get_smoothen_kernel(rmin, resolution):
    iH  =  []
    jH  =  []
    sH  =  []
    for row, I in enumerate(itertools.product(*[range(e) for e in resolution])):
        KK1 = [int(np.maximum(i - (np.ceil(rmin) - 1), 0)) for i in I]
        KK2 = [int(np.minimum(i + np.ceil(rmin), nel)) for i, nel in zip(I, resolution)]
        for J in itertools.product(*[range(e_1, e_2) for e_1, e_2 in zip(KK1, KK2)]):
            col = 0
            for a, b in zip(J, resolution):
                col = col * b + a
            fac = rmin - np.sqrt(np.sum([(i - j) ** 2 for i, j in zip(I, J)]))
            iH.append(row)
            jH.append(col)
            sH.append(np.maximum(0., fac))
    # Finalize assembly and convert to csc format
    H = coo_matrix((sH, (iH, jH)), shape = (np.prod(resolution), np.prod(resolution))).tocsc()
    Hs = H.sum(1)
    H /= Hs
    return H
    
# Optimality criterion
def optimality_criteria(x, dc, dv, g, mask=None):  # Used to update the design variables
    # dc: Sensitivity of the compliance (objective function) with respect to the design variables.
    # dv: Sensitivity of the volume with respect to the design variables.
    # g: Constraint term used in the optimization.
    
    l1 = 0  # bounds for the Lagrange multiplier
    l2 = 1e9
    move = 0.2  # Maximum change allowed in the design variables in one iteration 0.2
    # reshape to perform vector operations
    while (l2 - l1) / (l1 + l2) > 1e-3:
        lmid = 0.5 * (l2 + l1)
        xnew =  np.maximum(0.0, np.maximum(x - move, np.minimum(1.0, np.minimum(x + move, x * np.sqrt(-dc / dv / lmid)))))
        if not mask is None:
            xnew[np.logical_not(mask)] = 0
        gt = g + np.sum((dv * (xnew - x)))
        if gt > 0 :
            l1 = lmid
        else:
            l2 = lmid
        # print(l1, l2)
    return (xnew, gt)

def solve(get_fixed,
          get_load,
          resolution,
          volfrac,
          penal,
          rmin,
          ft,
          E=1,
          nu=1/3,
          iterations=20,
          get_mask=None,
          change_threshold=0,
          intermediate_results_saving_path=None,
          element_stiffness_matrix_file_dir='./element_stiffness_matrices/',
          skip_calculating_element_stiffness_matrix_if_exists=True):  # 支持同时考虑多种受力状态的情况

    if not intermediate_results_saving_path is None:
        if not os.path.exists(intermediate_results_saving_path):
            os.makedirs(intermediate_results_saving_path)

    # Print problem setup
    print("Minimum compliance problem with OC")
    print("ndes:", resolution)
    print("volfrac: " + str(volfrac) + ", rmin: " + str(rmin) + ", penal: " + str(penal))
    print("Filter method: " + ["Sensitivity based", "Density based"][ft])
    
    # Max and min stiffness
    Emin = 1e-9
    Emax = 1.0
    
    # Degrees of freedom (DOFs)
    ndof = len(resolution) * np.prod([e + 1 for e in resolution])
    print('degrees of freedom =', ndof)
    
    # Set mask
    if not get_mask is None:
        mask = get_mask(resolution)
    else:
        mask = None
    
    # Allocate design variables (as array), initialize and allocate sens.
    x = volfrac / (1 if mask is None else np.mean(mask)) * np.ones(np.prod(resolution), dtype=float)
    if not mask is None:
        x[np.logical_not(mask)] = 0
    xold = x.copy()
    xPhys = x.copy()
    
    if not os.path.exists(element_stiffness_matrix_file_dir):
        os.makedirs(element_stiffness_matrix_file_dir)
    element_stiffness_matrix_file_name = 'KE_' + str(len(resolution)) + 'd_' + str(E) + ',' + str(nu) + '.npy'
    if skip_calculating_element_stiffness_matrix_if_exists and os.path.exists(element_stiffness_matrix_file_dir + element_stiffness_matrix_file_name):
        KE = np.load(element_stiffness_matrix_file_dir + element_stiffness_matrix_file_name)
    else:
        t_0 = time.time()
        KE = get_element_stiffness_matrix(E=E, nu=nu, dimensional=len(resolution))  # Element Stiffness Matrix
        np.save(element_stiffness_matrix_file_dir + element_stiffness_matrix_file_name, KE)
        print('time escaped in calculating element stiffness matrix =', time.time() - t_0)
    
    t_0 = time.time()

    dof_per_element = len(resolution) * 2 ** len(resolution)
    edofMat = np.zeros((np.prod(resolution), dof_per_element), dtype=int)
    for el, EL in enumerate(itertools.product(*[range(e) for e in resolution])):
        n1 = 0
        for a, b in zip(resolution, EL):
            n1 = (a + 1) * n1 + b
        indices = n1 * len(resolution) + np.arange(2 * len(resolution))
        j = len(resolution)
        for nel in resolution[-1:0:-1]:
            j *= nel + 1
            indices = list(indices) + list(np.array(indices) + j)
        edofMat[el] = indices
            
    # Construct the index pointers for the coo format
    iK  =  np.kron(edofMat, np.ones((dof_per_element, 1), dtype=np.int32)).flatten()
    jK  =  np.kron(edofMat, np.ones((1, dof_per_element), dtype=np.int32)).flatten()

    print('time escaped in calculating edofMat =', time.time() - t_0)

    # 构造一个卷积核用于模糊设计变量以实现正则化
    # Filter: Build (and assemble) the index+data vectors for the coo matrix format
    t_0 = time.time()
    H = get_smoothen_kernel(rmin, resolution)
    print('time escaped in calculating kernel for smoothening =', time.time() - t_0)
    
    t_0 = time.time()

    # Boundary Conditions (BCs) and support
    fixed = get_fixed(resolution, ndof)
    free = np.setdiff1d(np.arange(ndof), fixed)
    
    # Set load
    f = get_load(resolution, ndof)
    f = f.reshape(ndof, -1)
    if np.min(np.max(np.abs(f[free]), axis=0)) == 0:
        raise ValueError("No load found on free dofs.")
    
    # Solution
    u = np.zeros(f.shape)

    print('time escaped in preparing other things =', time.time() - t_0)
    
    # Set loop counter and gradient vectors 
    t_0 = time.time()
    loop = 0
    change = 1
    g = 0  # a constraint or a measure related to the volume of the design, must be initialized to use the NGuyen/Paulino OC approach
    while change > change_threshold and loop < iterations:
        loop += 1
        
        t_1 = time.time()

        # Setup and solve FE problem
        sK = ((KE.flatten()[np.newaxis]).T*(Emin+(xPhys)**penal*(Emax-Emin))).flatten(order = 'F')
        K  =  coo_matrix((sK, (iK, jK)), shape = (ndof, ndof)).tocsc()
        
        # Remove constrained dofs from matrix
        K  =  K[free, :][:, free]

        # print('whether symmetric?', np.max(np.abs(K[:10000, :10000].toarray() - K[:10000, :10000].toarray().T)))

        # print('time escaped in generating K =', time.time() - t_1)
        t_1 = time.time()
        
        # Solve system 
        u[free, :] = np.reshape(spsolve(K, f[free]), [len(free), -1])
        # u[free, :] = np.reshape(cg(K, f[free])[0], [len(free), -1])
        # u[free, :] = np.reshape(minres(K, f[free])[0], [len(free), -1])
        # ml = pyamg.ruge_stuben_solver(K)
        # u[free, :] = np.reshape(ml.solve(f[free], tol=1e-8), [len(free), -1])

        # print('time escaped in solving the linear system =', time.time() - t_1)
        t_1 = time.time()
        
        # Objective and sensitivity
        ce = np.zeros(np.prod(resolution))
        for e in u.T:
            u_element = e[edofMat].reshape(np.prod(resolution), dof_per_element)
            ce = np.maximum(ce, (np.dot(u_element, KE) * u_element).sum(1))  # Compliance energy
        # print('np.max(ce) =', np.max(ce))
        obj = ((Emin + xPhys ** penal * (Emax - Emin)) * ce ).sum()
        dc = (-penal * xPhys ** (penal - 1) * (Emax - Emin)) * ce  # 忽略d ce /d obj对梯度的贡献
        dv = np.ones(np.prod(resolution))
        
        # Sensitivity filtering:
        if ft == 0:
            dc  =  np.asarray((H * (x * dc))[np.newaxis].T)[:, 0] / np.maximum(0.001, x)
        elif ft == 1:
            dc  =  np.asarray(H * (dc[np.newaxis].T))[:, 0]
            dv  =  np.asarray(H * (dv[np.newaxis].T))[:, 0]
            
        # Optimality criteria (Update design variables)
        xold = x
        (x, g) = optimality_criteria(x, dc, dv, g, mask=mask)

        # print('time escaped in optimality criteria =', time.time() - t_1)
        t_1 = time.time()
        
        # Filter design variables
        if ft == 0:
            xPhys = x
        elif ft == 1:  # Directly adjusts the design variables x themselves based on their average within a neighborhood defined by rmin.
            xPhys = np.asarray(H * x[np.newaxis].T)[:, 0]
        
        # Compute the change by the inf. norm
        change = np.linalg.norm(x.reshape(np.prod(resolution), 1) - xold.reshape(np.prod(resolution), 1), np.inf)

        if not intermediate_results_saving_path is None:
            np.save(intermediate_results_saving_path + 'result_' + str(len(resolution)) + 'd_' + str(loop) + '.npy', xPhys.reshape(resolution))
        
        print('iteration ', loop,
              ', loss = ', obj,
              ', change = ', change,
              sep='')
    print('time escaped in main loop =', time.time() - t_0)
    
    return xPhys.reshape(resolution)

def get_indices_on_face(resolution, axis, start=False, end=False):
    indices = [range(e) for e in resolution]
    indices[axis] = ([0] if start else []) + ([resolution[axis] - 1] if end else [])
    indices = np.array(list(itertools.product(*indices)))
    indices *= [int(np.prod(resolution[i:])) for i in range(1, len(resolution) + 1)]
    return np.sum(indices, axis=-1)

def get_indices_on_boundary_elements(resolution, axis_selection):
    indices = []
    for a, b in zip(resolution, axis_selection):
        if b is None:
            indices.append(range(a))
        else:
            indices.append(([0] if b[0] else []) + ([a - 1] if b[1] else []))
    indices = np.array(list(itertools.product(*indices)))
    indices *= [int(np.prod(resolution[i:])) for i in range(1, len(resolution) + 1)]
    return np.sum(indices, axis=-1)

def mirrow_first_axis(a):
    shape = list(a.shape)
    shape[0] *= 2
    result = np.zeros(shape, dtype=a.dtype)
    result[:a.shape[0]] = a[::-1]
    result[a.shape[0]:] = a
    return result

def visualize_3d_array(a,
                       mirror_x=False,
                       mirror_y=False,
                       mirror_z=False,
                       volume_quality=5):  # Visualize the result with pyvista
    if mirror_x:
        a = mirrow_first_axis(a)
    a = np.transpose(a, [1, 2, 0])
    if mirror_y:
        a = mirrow_first_axis(a)
    a = np.transpose(a, [1, 2, 0])
    if mirror_z:
        a = mirrow_first_axis(a)
    a = np.transpose(a, [1, 2, 0])

    grid = pyvista.ImageData()
    grid.dimensions = np.array(a.shape) + 1
    grid.spacing = [volume_quality] * 3  #  数组中的一个元素在各轴上对应的单元格数，值越高，在可视化体积时质量越高
    grid.cell_data["values"] = a.flatten(order="F")

    grid.plot(volume=True, opacity=[0, 1, 1], cmap='magma', notebook=False)