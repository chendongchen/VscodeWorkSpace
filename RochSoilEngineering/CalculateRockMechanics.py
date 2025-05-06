import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Elastic:
    """
    Elastic class to represent material properties.
    """

    def __init__(self, No, E, v=None):
        """
        Constructor to initialize material properties.

        :param No: Material number (identifier for different materials)
        :param E: Young's modulus (Elastic modulus)
        :param v: Poisson's ratio (optional)
        """
        self.No = No  # Material number
        self.E = E    # Young's modulus
        self.v = v    # Poisson's ratio (optional)

class DruckPrager(Elastic):
    """
    Druck-Prager class to represent material properties and plasticity behavior.
    """

    def __init__(self, No, E, v, alpha, k):
        """
        Constructor to initialize material properties.

        :param No: Material number
        :param E: Young's modulus
        :param v: Poisson's ratio
        :param alpha: Druck-Prager parameter alpha
        :param k: Druck-Prager parameter k
        """
        super().__init__(No, E, v)  # Call the parent class constructor
        self.alpha = alpha
        self.k = k

    def f(self, Stress):
        """
        Calculate the yield function.

        :param Stress: Stress value
        :return: Yield function value
        """
        return (self.alpha + np.sign(Stress) / (3 ** 0.5)) * Stress - self.k

    def PlasticFlow(self, StressTry):
        """
        Perform plastic flow calculation.

        :param StressTry: Trial stress
        :return: dStress, Lambda, dStrainp
        """
        Beta = self.alpha + np.sign(StressTry) / (3 ** 0.5)
        Lambda = (self.E * Beta) ** -1 * (StressTry - self.k / Beta)
        dStrainp = Lambda * Beta
        dStresst = self.E * dStrainp
        dStress = StressTry - dStresst
        return dStress, Lambda, dStrainp

    def GetElasticMatrix2D(self):
        """
        Get the 2D elastic matrix.

        :return: 2D elastic matrix
        """
        factor = self.E / (1 - self.v ** 2)
        D = factor * np.array([
            [1, self.v, 0],
            [self.v, 1, 0],
            [0, 0, (1 - self.v) / 2]
        ])
        return D

    def GetElasticMatrix3D(self):
        """
        Get the 3D elastic matrix for isotropic materials.

        :return: 3D elastic matrix
        """
        factor = self.E / ((1 + self.v) * (1 - 2 * self.v))
        D = factor * np.array([
            [1 - self.v, self.v, self.v, 0, 0, 0],
            [self.v, 1 - self.v, self.v, 0, 0, 0],
            [self.v, self.v, 1 - self.v, 0, 0, 0],
            [0, 0, 0, (1 - 2 * self.v) / 2, 0, 0],
            [0, 0, 0, 0, (1 - 2 * self.v) / 2, 0],
            [0, 0, 0, 0, 0, (1 - 2 * self.v) / 2]
        ])
        return D

class Element:
    """
    Element class to represent finite element properties.
    """

    def __init__(self, No, Nodes, Mat):
        """
        Constructor to initialize element properties.

        :param No: Element number
        :param Nodes: Nodes associated with the element
        :param Mat: Material associated with the element
        """
        self.No = No  # Element number
        self.Nodes = Nodes  # Nodes of the element
        self.Mat = Mat  # Material of the element
        self.Index = None  # Index of the element (optional, can be set later)
        self.Ke = None  # Element stiffness matrix
        self.Strainp = None  # Plastic strain
        self.Strain = None  # Strain
        self.Stress = None  # Stress
        self.dStrainp = None  # Incremental plastic strain
        self.dStrain = None  # Incremental strain
        self.dStress = None  # Incremental stress

class Node:
    """
    Node class to represent a finite element node.
    """

    def __init__(self, No, X):
        """
        Constructor to initialize node properties.

        :param No: Node number
        :param X: Coordinates of the node
        """
        self.No = No  # Node number
        self.X = X  # Coordinates of the node
        self.U = [0] * len(X)  # Displacement initialized to zero
        self.dU = [0] * len(X)  # Incremental displacement initialized to zero


class Prism(Element):
    """
    Prism class to represent prismatic finite elements.
    """

    def __init__(self, No, Nodes, Mat):
        """
        Constructor to initialize prismatic element properties.

        :param No: Element number
        :param Nodes: Nodes associated with the element
        :param Mat: Material associated with the element
        """
        super().__init__(No, Nodes, Mat)
        self.ElasticorPlastic = 1  # 1 for elastic, -1 for plastic
        self.Index = [node.No for node in Nodes]
        self.Volume = self.GetVolume()  # Calculate element volume
        self.Ke = self.GetK()  # Calculate stiffness matrix
        # Initialize stress, strain, and their increments
        self.Stress = self.Strain = self.Strainp = 0
        self.dStress = self.dStrain = self.dStrainp = 0

    def GetK(self):
        """
        Calculate the stiffness matrix.
        """
        return self.GetKOptimized()

    def Fint(self):
        """
        Calculate internal forces.
        """
        return self.GetNodeForce()

    def GetVolume(self):
        """
        Calculate the volume of the element.
        """
        x = np.array([node.X[0] for node in self.Nodes])  # x-coordinates
        y = np.array([node.X[1] for node in self.Nodes])  # y-coordinates
        z = np.array([node.X[2] for node in self.Nodes])  # z-coordinates

        if len(self.Nodes) == 6:  # 6-node prism
            A1 = self.polyarea(x[:3], y[:3])  # Bottom triangle area
            A2 = self.polyarea(x[3:], y[3:])  # Top triangle area
            h = abs(np.mean(z[:3]) - np.mean(z[3:]))  # Height
            self.Volume = (A1 + A2) / 2 * h
        elif len(self.Nodes) == 8:  # 8-node prism
            A1 = self.polyarea(x[:4], y[:4])  # Bottom quadrilateral area
            A2 = self.polyarea(x[4:], y[4:])  # Top quadrilateral area
            h = abs(np.mean(z[:4]) - np.mean(z[4:]))  # Height
            self.Volume = (A1 + A2) / 2 * h
        else:
            raise ValueError("Unsupported element type!")
        return self.Volume

    def GetKOptimized(self):
        """
        Optimized calculation of the stiffness matrix.
        """
        Ind = self.Index
        x = np.array([node.X[0] for node in self.Nodes])
        y = np.array([node.X[1] for node in self.Nodes])
        z = np.array([node.X[2] for node in self.Nodes])

        numNodes = len(self.Nodes)
        Ke = np.zeros((3 * numNodes, 3 * numNodes))

        n_gaussPoints = 5
        gaussPoints, gaussWeights = gauss_legendre(n_gaussPoints)

        shapeFunctionMethod = self.selectShapeFunctionMethod(numNodes)

        for i in range(n_gaussPoints):
            for j in range(n_gaussPoints):
                for k in range(n_gaussPoints):
                    xi, eta, zeta = gaussPoints[i], gaussPoints[j], gaussPoints[k]
                    _, dN_dXi = shapeFunctionMethod(xi, eta, zeta)
                    dN_dXi = dN_dXi.T

                    J = dN_dXi @ np.array([x, y, z]).T
                    invJ = np.linalg.inv(J)
                    dN_dX = invJ @ dN_dXi

                    B = self.GetBMatrix(dN_dX)
                    Ke += B.T @ self.Mat.GetElasticMatrix3D() @ B * np.linalg.det(J) * np.prod(gaussWeights[[i, j, k]])
        return Ke, Ind

    def selectShapeFunctionMethod(self, numNodes):
        """
        Select the appropriate shape function method based on the number of nodes.
        """
        if numNodes == 8:
            return self.GetShapeFunction
        elif numNodes == 6:
            return self.GetShapeFunctionPenta
        else:
            raise ValueError("Unsupported element type!")

    def GetShapeFunction(self, xi, eta, zeta):
        """
        Shape function and derivatives for 8-node hexahedral element.
        """
        N = 1 / 8 * np.array([
            (1 - xi) * (1 - eta) * (1 - zeta),
            (1 + xi) * (1 - eta) * (1 - zeta),
            (1 + xi) * (1 + eta) * (1 - zeta),
            (1 - xi) * (1 + eta) * (1 - zeta),
            (1 - xi) * (1 - eta) * (1 + zeta),
            (1 + xi) * (1 - eta) * (1 + zeta),
            (1 + xi) * (1 + eta) * (1 + zeta),
            (1 - xi) * (1 + eta) * (1 + zeta)
        ])
        dN_dXi = 1 / 8 * np.array([
            [-(1 - eta) * (1 - zeta), -(1 - xi) * (1 - zeta), -(1 - xi) * (1 - eta)],
            [(1 - eta) * (1 - zeta), -(1 + xi) * (1 - zeta), -(1 + xi) * (1 - eta)],
            [(1 + eta) * (1 - zeta), (1 + xi) * (1 - zeta), -(1 + xi) * (1 + eta)],
            [-(1 + eta) * (1 - zeta), (1 - xi) * (1 - zeta), -(1 - xi) * (1 + eta)],
            [-(1 - eta) * (1 + zeta), -(1 - xi) * (1 + zeta), (1 - xi) * (1 - eta)],
            [(1 - eta) * (1 + zeta), -(1 + xi) * (1 + zeta), (1 + xi) * (1 - eta)],
            [(1 + eta) * (1 + zeta), (1 + xi) * (1 + zeta), (1 + xi) * (1 + eta)],
            [-(1 + eta) * (1 + zeta), (1 - xi) * (1 + zeta), (1 - xi) * (1 + eta)]
        ])
        return N, dN_dXi

    def GetShapeFunctionPenta(self, xi, eta, zeta):
        """
        Shape function and derivatives for 6-node pentahedral element.
        """
        N = np.array([
            (1 - xi - eta) * (1 - zeta) / 2,
            xi * (1 - zeta) / 2,
            eta * (1 - zeta) / 2,
            (1 - xi - eta) * (1 + zeta) / 2,
            xi * (1 + zeta) / 2,
            eta * (1 + zeta) / 2
        ])
        dN_dXi = np.array([
            [-(1 - zeta) / 2, -(1 - zeta) / 2, -(1 - xi - eta) / 2],
            [(1 - zeta) / 2, 0, -xi / 2],
            [0, (1 - zeta) / 2, -eta / 2],
            [-(1 + zeta) / 2, -(1 + zeta) / 2, (1 - xi - eta) / 2],
            [(1 + zeta) / 2, 0, xi / 2],
            [0, (1 + zeta) / 2, eta / 2]
        ])
        return N, dN_dXi

    def GetBMatrix(self, dN_dX):
        """
        Construct the B matrix.
        """
        numNodes = dN_dX.shape[1]
        B = np.zeros((6, 3 * numNodes))
        for i in range(numNodes):
            B[0, i * 3] = dN_dX[0, i]
            B[1, i * 3 + 1] = dN_dX[1, i]
            B[2, i * 3 + 2] = dN_dX[2, i]
            B[3, i * 3] = dN_dX[1, i]
            B[3, i * 3 + 1] = dN_dX[0, i]
            B[4, i * 3 + 1] = dN_dX[2, i]
            B[4, i * 3 + 2] = dN_dX[1, i]
            B[5, i * 3] = dN_dX[2, i]
            B[5, i * 3 + 2] = dN_dX[0, i]
        return B

    def GetNodeForce(self):
        """
        Calculate nodal forces.
        """
        Ke = self.Ke
        U = np.concatenate([node.U for node in self.Nodes])
        Fi = Ke @ U
        return Fi, self.Index

    def polyarea(self, x, y):
        """
        Calculate the area of a polygon given its vertices.
        """
        return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

    def GetJacobian(self, X):
        """
        Calculate the Jacobian matrix.

        :param X: Node coordinates
        :return: Jacobian matrix
        """
        _, dN_dXi = self.GetShapeFunction(0, 0, 0)  # Use natural coordinate origin as an example
        J = dN_dXi @ X.T  # Calculate the Jacobian matrix
        return J

    def Update(self):
        """
        Update the stiffness matrix and element state.

        :return: Updated stiffness matrix and indices
        """
        # Example strain and stress calculation (commented out for now)
        # self.dStrain = (self.Nodes[1].dU - self.Nodes[0].dU) / self.L
        # dStress = self.dStrain * self.Mat.E
        # Stresstry = dStress + self.Stress

        # if self.Mat.f(Stresstry) <= 0:
        #     self.dStress = dStress
        #     self.dStrainp = 0
        #     self.ElasticorPlastic = 1
        # else:
        #     dStress, Lambda, dStrainp = self.Mat.PlasticFlow(Stresstry)
        #     self.dStress = dStress
        #     self.dStrainp = dStrainp
        #     self.ElasticorPlastic = -1

        Ke, Ind = self.GetK()
        return Ke, Ind

def calculate_max_u_range(Exam1):
    """
    Calculate the maximum range of the average U values for all elements in Exam1.

    :param Exam1: An object containing elements with nodes and their U values
    :return: Maximum range of average U values
    """
    # Initialize the maximum range
    max_range = np.array([0, 0, 0])

    # Iterate through all elements
    for elem in Exam1.Elements:
        # Get all nodes of the element
        nodes = elem.Nodes

        # Extract all U values of the nodes and calculate the mean
        U_values = np.array([node.U for node in nodes]).T  # Each column is a node's U
        U_mean = np.mean(U_values, axis=1)  # Calculate the mean

        # Update the maximum range
        max_range = np.maximum(max_range, U_mean)

    # Print the maximum range
    print("U 平均值的最大值范围为：")
    print(max_range)

    return max_range

def gauss_legendre(n):
    """
    Compute the Gauss-Legendre quadrature points and weights.

    :param n: Number of quadrature points
    :return: Tuple (x, w) where x are the points and w are the weights
    """
    i = np.arange(1, n)
    a = i / np.sqrt(4 * i**2 - 1)
    # Construct the symmetric tridiagonal matrix
    T = np.diag(a, 1) + np.diag(a, -1)
    # Compute eigenvalues and eigenvectors
    x, V = np.linalg.eigh(T)
    # Sort eigenvalues and corresponding eigenvectors
    ind = np.argsort(x)
    x = x[ind]
    w = 2 * V[0, ind]**2
    return x, w

class FEM:
    """
    Finite Element Method (FEM) class to manage materials, nodes, elements, and boundary conditions.
    """

    def __init__(self):
        self.Mats = []  # List of materials (Elastic objects)
        self.Nodes = []  # List of nodes (Node objects)
        self.Elements = []  # List of elements (Element objects)
        self.Boundary1 = []  # First type boundary conditions [Node No, DOF, Displacement]
        self.Boundary2 = []  # Second type boundary conditions [Boundary No, Normal Vector, Displacement]

    def Fint(self):
        """
        Calculate internal force vector.
        """
        F = np.zeros(len(self.Nodes) * 3)
        for Ei in self.Elements:
            Fi, Ind = Ei.Fint()
            dofInd = [3 * (i - 1) + j for i in Ind for j in range(1, 4)]
            F[dofInd] += Fi
        return F

    def Solve(self):
        """
        Solve the FEM system.
        """
        K = self.Update()
        self.Boundary1 = self.NeumannBoundary()
        flag = 0
        for Iter in range(8):
            Fint = self.Fint()
            Fext = np.zeros_like(Fint)
            R = Fint - Fext
            K, R = self.DirchletBoundary(K, R)
            dU = np.linalg.solve(K, R)
            K = self.Update(dU)
            if np.linalg.norm(R) < 1e-6:
                flag = 1
                break
        self.Update(flag)
        return flag

    def DirchletBoundary(self, K, R):
        """
        Apply Dirichlet boundary conditions using penalty method.
        """
        P = np.mean(np.diag(K)) * 1e6

        for B1i in self.Boundary1:
            NDNo = B1i[0]  # Node number
            Ind = np.reshape([3 * (NDNo - 1) + 1, 3 * (NDNo - 1) + 2, 3 * (NDNo - 1) + 3], -1)
            K[np.ix_(Ind, Ind)] += P * np.eye(3)
            ui = self.Nodes[NDNo - 1].U + self.Nodes[NDNo - 1].dU
            R[Ind] += P * (B1i[2:] - ui)
        return K, R

    def NeumannBoundary(self):
        """
        Generate first type boundary conditions from second type boundary conditions.
        """
        self.Boundary1 = []
        for B2i in self.Boundary2:
            for Element in self.Elements:
                for Nodei in Element.Nodes:
                    temp = B2i[4]  # Extract row vector
                    Fn = B2i[1:4]  # Extract first 3 elements
                    if np.dot(Nodei.X, Fn) == temp:
                        self.Boundary1.append([Nodei.No, 3, *B2i[5:8]])
        return self.Boundary1

    def Update(self, dU=None):
        """
        Update the stiffness matrix and element state.
        """
        if dU is not None and len(dU) > 1:  # Iterative update
            for Nodei in self.Nodes:
                Ind = Nodei.No
                dofInd = [3 * (i - 1) + j for i in Ind for j in range(1, 4)]
                Nodei.dU += dU[dofInd]
                self.Nodes[Ind - 1].U += Nodei.dU

        if dU is None or len(dU) > 1:
            K = np.zeros((len(self.Nodes) * 3, len(self.Nodes) * 3))
            for Ei in self.Elements:
                Ke, Ind = Ei.Update()
                dofInd = [3 * (i - 1) + j for i in Ind for j in range(1, 4)]
                K[np.ix_(dofInd, dofInd)] += Ke
            return K

        if dU is not None and len(dU) == 1:  # Final update
            if dU == 1:
                for Nodei in self.Nodes:
                    Nodei.U += Nodei.dU
                for Ei in self.Elements:
                    Ei.Stress += Ei.dStress
                    Ei.Strain += Ei.dStrain
                    Ei.Strainp += Ei.dStrainp

            for Nodei in self.Nodes:
                Nodei.dU = np.zeros_like(Nodei.dU)
            for Ei in self.Elements:
                Ei.dStress = np.zeros_like(Ei.dStress)
                Ei.dStrain = np.zeros_like(Ei.dStrain)
                Ei.dStrainp = np.zeros_like(Ei.dStrainp)

def show(Exam1):
    """
    Visualize 3D elements and their displacement fields.
    """
    # Plot 3D elements
    fig = plt.figure(1)
    ax = fig.add_subplot(111, projection='3d')
    cmap = plt.get_cmap('hot')
    plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, label='Element Index')

    for elem_idx, element in enumerate(Exam1.Elements, start=1):
        if elem_idx % 2 != 0:
            continue

        nodes = element.Nodes
        coords = np.array([node.X for node in nodes])

        if coords.shape[0] == 6:  # Triangular prism
            faces = [[0, 1, 2], [3, 4, 5], [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]]
        elif coords.shape[0] == 8:  # Quadrilateral prism
            faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
        else:
            continue

        poly3d = [[coords[face] for face in face_group] for face_group in faces]
        ax.add_collection3d(Poly3DCollection(poly3d, facecolors=cmap(elem_idx / len(Exam1.Elements)), edgecolor='k', alpha=0.75))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Element Visualization')
    plt.show()

    # Plot displacement fields
    directions = [0, 1, 2]  # X, Y, Z directions
    names = ['X方向位移', 'Y方向位移', 'Z方向位移']
    max_values = calculate_max_u_range(Exam1)

    for dir_idx, direction in enumerate(directions):
        fig = plt.figure(dir_idx + 2)
        ax = fig.add_subplot(111, projection='3d')
        cmap = plt.get_cmap('hot')
        plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), ax=ax, label=names[dir_idx])

        for elem_idx, element in enumerate(Exam1.Elements, start=1):
            nodes = element.Nodes
            coords = np.array([node.X for node in nodes])
            u_values = np.array([node.U for node in nodes])
            u_mean = np.mean(u_values, axis=0)
            elem_value = u_mean[direction]

            if coords.shape[0] == 6:  # Triangular prism
                faces = [[0, 1, 2], [3, 4, 5], [0, 1, 4, 3], [1, 2, 5, 4], [2, 0, 3, 5]]
            elif coords.shape[0] == 8:  # Quadrilateral prism
                faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [1, 2, 6, 5], [2, 3, 7, 6], [3, 0, 4, 7]]
            else:
                continue

            poly3d = [[coords[face] for face in face_group] for face_group in faces]
            ax.add_collection3d(Poly3DCollection(poly3d, facecolors=cmap((elem_value + max_values[direction]) / (2 * max_values[direction])), edgecolor='k', alpha=0.75))

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'3D Element Visualization - {names[dir_idx]}')
        plt.show()

    # Save plots
    for dir_idx in range(4):
        plt.figure(dir_idx + 1)
        plt.savefig(f'3D_Plot_Direction_{dir_idx + 1}.png')
    print('所有绘制的图像已保存为 3D_Plot_Direction_*.png')

def main():
    # 清空工作区和命令窗口，避免旧数据干扰
    Exam1 = FEM()

    # 定义材料属性 (ID:1, 弹性模量E=1000)
    E = 1e3
    v = 0.2
    c = 10
    phi = 60
    alpha = 2 * np.sin(np.radians(phi)) / (3**0.5) / (3 - np.sin(np.radians(phi)))
    k = 6 * c * np.cos(np.radians(phi)) / (3**0.5) / (3 - np.sin(np.radians(phi)))
    Exam1.Mats.append(DruckPrager(1, E, v, alpha, k))

    # 定义变截面参数：r(x)=ax²+c (抛物线形截面半径)
    a = 1 / 200
    c = 25 / 2  # 半径函数系数

    # 创建节点 (ID, 坐标X)
    Number_R = 5
    Number_Theta = 10
    Number_L = 5
    R = np.linspace(0, 1, Number_R)
    theta = np.linspace(0, 2 * np.pi, Number_Theta)
    R, theta = np.meshgrid(R[1:], theta[:-1])
    X = R * np.cos(theta)
    Y = R * np.sin(theta)

    # 添加中心的特殊节点
    X = np.concatenate(([0], X.flatten()))
    Y = np.concatenate(([0], Y.flatten()))

    Ls = np.linspace(0, 50, Number_L)
    for Li in Ls:
        Radius_Li = a * Li**2 + c
        for nXi in range(len(X)):
            Noi = len(Exam1.Nodes) + 1
            Exam1.Nodes.append(Node(Noi, [Radius_Li * X[nXi], Radius_Li * Y[nXi], Li]))

    # 创建六面体单元
    for nLi in range(1,len(Ls)):
        All_Node_Li = 1 + (Number_R - 1) * (Number_Theta - 1)
        CenterNode = (nLi-1)*All_Node_Li+1

        for No_triangular in range(1,Number_Theta):
            Noi = len(Exam1.Elements) + 1
            NodeNos_1 = CenterNode
            NodeNos_2 = CenterNode + No_triangular + 1
            NodeNos_3 = NodeNos_2 + 1
            if No_triangular == Number_Theta - 1:
                NodeNos_3 = CenterNode + 1
            NodeNos_Down = [NodeNos_1, NodeNos_2, NodeNos_3]
            NodeNos_Up = [n + All_Node_Li for n in NodeNos_Down]
            NodeNos = NodeNos_Down + NodeNos_Up
            Exam1.Elements.append(Prism(Noi, [Exam1.Nodes[n - 1] for n in NodeNos], Exam1.Mats[0]))

        for No_radius in range(1, Number_R - 1):
            for No_angle in range(1,Number_Theta ):
                Noi = len(Exam1.Elements) + 1
                NodeNos_1 = CenterNode + (No_radius - 1) * (Number_Theta - 1) + No_angle + 1
                NodeNos_2 = NodeNos_1 + Number_Theta - 1
                NodeNos_3 = NodeNos_1 + Number_Theta
                NodeNos_4 = NodeNos_1 + 1
                if No_angle == Number_Theta - 1:
                    NodeNos_4 = CenterNode + (No_radius - 1) * (Number_Theta - 1) + 1
                    NodeNos_3 = CenterNode + No_radius * (Number_Theta - 1) + 1
                NodeNos_Down = [NodeNos_1, NodeNos_2, NodeNos_3, NodeNos_4]
                NodeNos_Up = [n + All_Node_Li for n in NodeNos_Down]
                NodeNos = NodeNos_Down + NodeNos_Up
                Exam1.Elements.append(Prism(Noi, [Exam1.Nodes[n - 1] for n in NodeNos], Exam1.Mats[0]))

    Exam1.Boundary2 = [
        [1, [0, 0, 1, 0], [0, 0, 0]],
        [2, [0, 0, 1, 50], [0, 0, 0.1]],
    ]
    Exam1.Solve()

    print(f"Number of elements: {len(Exam1.Elements)}")
    print(f"Volume of the last element: {Exam1.Elements[-1].Volume}")

    show(Exam1)

if __name__ == "__main__":
    main()

