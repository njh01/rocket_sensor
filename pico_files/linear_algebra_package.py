import math


'''
Various Linear Algebra functions
'''
r2d = 180/math.pi
d2r = math.pi/180
    
def zeros_mat(rows,cols):
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M

def identity(n):
    IdM = zeros_mat(n, n)
    for i in range(n):
        IdM[i][i] = 1.0

    return IdM

def copy_matrix(M):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied
 
        :return: A copy of the given matrix
    """
    # Section 1: Get matrix dimensions
    rows = len(M)
    cols = len(M[0])
 
    # Section 2: Create a new matrix of zeros
    MC = zeros_mat(rows, cols)
 
    # Section 3: Copy values of M into the copy
    for i in range(rows):
        for j in range(cols):
            MC[i][j] = M[i][j]
 
    return MC

def transpose(M):
    """
    Returns a transpose of a matrix.
        :param M: The matrix to be transposed
 
        :return: The transpose of the given matrix
    """
    # Section 1: if a 1D array, convert to a 2D array = matrix
    if not isinstance(M[0],list):
        M = [M]
 
    # Section 2: Get dimensions
    rows = len(M)
    cols = len(M[0])
 
    # Section 3: MT is zeros matrix with transposed dimensions
    MT = zeros_mat(cols, rows)
 
    # Section 4: Copy values from M to it's transpose MT
    for i in range(rows):
        for j in range(cols):
            MT[j][i] = M[i][j]
 
    return MT

def print_matrix(M, decimals=3):
    """
    Print a matrix one row at a time
        :param M: The matrix to be printed
    """
    for row in M:
        print([round(x,decimals)+0 for x in row])

def matrix_subtraction(A, B):
    """
    Subtracts matrix B from matrix A and returns difference
        :param A: The first matrix
        :param B: The second matrix
 
        :return: Matrix difference
    """
    # Section 1: Ensure dimensions are valid for matrix subtraction
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if rowsA != rowsB or colsA != colsB:
        raise ArithmeticError('Matrices are NOT the same size.')
 
    # Section 2: Create a new matrix for the matrix difference
    C = zeros_mat(rowsA, colsB)
 
    # Section 3: Perform element by element subtraction
    for i in range(rowsA):
        for j in range(colsB):
            C[i][j] = A[i][j] - B[i][j]
 
    return C

def matrix_addition(A, B):
    """
    Adds two matrices and returns the sum
        :param A: The first matrix
        :param B: The second matrix
 
        :return: Matrix sum
    """
    # Section 1: Ensure dimensions are valid for matrix addition
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if rowsA != rowsB or colsA != colsB:
        raise ArithmeticError('Matrices are NOT the same size.')
 
    # Section 2: Create a new matrix for the matrix sum
    C = zeros_mat(rowsA, colsB)
 
    # Section 3: Perform element by element sum
    for i in range(rowsA):
        for j in range(colsB):
            C[i][j] = A[i][j] + B[i][j]
 
    return C

def scalar_mult(A,a):
    copy = copy_matrix(A)
    for i in range(len(A)):
        for j in range(len(A[0])):
            copy[i][j] = A[i][j]*a
    return copy
    
def matrix_multiply(A, B):
    """
    Returns the product of the matrix A * B
        :param A: The first matrix - ORDER MATTERS!
        :param B: The second matrix
 
        :return: The product of the two matrices
    """
    # Section 1: Ensure A & B dimensions are correct for multiplication
    rowsA = len(A)
    colsA = len(A[0])
    rowsB = len(B)
    colsB = len(B[0])
    if colsA != rowsB:
        raise ArithmeticError(
            'Number of A columns must equal number of B rows.')
     
    # Section 2: Store matrix multiplication in a new matrix
    C = zeros_mat(rowsA, colsB)
    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total
     
    return C
    
def invert_matrix(A, tol=None):
    """
    Returns the inverse of the passed in matrix.
    :param A: The matrix to be inversed
    
    :return: The inverse of the matrix A
    """
    # Section 1: Make sure A can be inverted.
     
    # Section 2: Make copies of A & I, AM & IM, to use for row ops
    n = len(A)
    AM = copy_matrix(A)
    I = identity(n)
    IM = copy_matrix(I)
     
    # Section 3: Perform row operations
    indices = list(range(n)) # to allow flexible row referencing ***
    for fd in range(n): # fd stands for focus diagonal
        fdScaler = 1.0 / AM[fd][fd]
        # FIRST: scale fd row with fd inverse. 
        for j in range(n): # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd+1:]: 
            # *** skip row with fd in it.
            crScaler = AM[i][fd] # cr stands for "current row".
            for j in range(n): 
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
    return IM
