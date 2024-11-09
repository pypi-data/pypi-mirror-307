from collections import namedtuple
import math

import numpy as np
import scipy.linalg


def assemble(ndofs, *matrices):
    matrix = np.zeros((ndofs, ndofs))
    for i, local_matrix in enumerate(matrices):
        matrix[i * 3: i * 3 + 6, i * 3: i * 3 + 6] += local_matrix
    return matrix


def reduce(constrained_dofs, matrix):
    if len(matrix.shape) == 1:  # vector
        matrix = np.delete(matrix, constrained_dofs)
    else:  # vector
        for i in [0, 1]:
            matrix = np.delete(matrix, constrained_dofs, axis=i)
    return matrix


def expand(constrained_dofs, matrix):
    for dof in constrained_dofs:
        matrix = np.insert(matrix, dof, 0)
    return matrix


Element = namedtuple("Element", "stiffness_matrix mass_matrix end_support")

def get_element(L, m, EI, EA, GA=0, end_support=False):
    # https://people.duke.edu/~hpgavin/StructuralDynamics/StructuralElements.pdf
    # consistent mass matrix euler-bernouilli beam
    mass_matrix = (m * L / 420) * np.array(
        [
            [140, 0, 0, 70, 0, 0],
            [0, 156, 22 * L, 0, 54, -13 * L],
            [0, 22 * L, 4 * L ** 2, 0, 13 * L, -3 * L ** 2],
            [70, 0, 0, 140, 0, 0],
            [0, 54, 13 * L, 0, 156, -22 * L],
            [0, -13 * L, -3 * L ** 2, 0, -22 * L, 4 * L ** 2],
        ]
    )

    # shear factor
    phi = (12 * EI / (GA * L ** 2)) if GA > 0 else 0
    c_1 = EA / L
    c_2 = EI / (L ** 3 * (1 + phi))

    stiffness_matrix = np.array(
        [
            [c_1, 0, 0, -c_1, 0, 0],
            [0, 12 * c_2, 6 * c_2 * L, 0, -12 * c_2, 6 * c_2 * L],
            [0, 6 * c_2 * L, (4 + phi) * c_2 * L ** 2, 0, -6 * c_2 * L, (2 - phi) * c_2 * L ** 2],
            [-c_1, 0, 0, c_1, 0, 0],
            [0, -12 * c_2, -6 * c_2 * L, 0, 12 * c_2, -6 * c_2 * L],
            [0, 6 * c_2 * L, (2 - phi) * c_2 * L ** 2, 0, -6 * c_2 * L, (4 + phi) * c_2 * L ** 2],
        ]
    )
    return Element(stiffness_matrix=stiffness_matrix, mass_matrix=mass_matrix, end_support=end_support)


def get_beam_frequencies(elements):
    nelems = len(elements)
    nnodes = nelems + 1
    ndofs = 3 * nnodes

    # FREE = BoundaryCondition(None, None, None)
    # SLIDING = BoundaryCondition(None, 0, None)
    # PINNED = BoundaryCondition(0, 0, None)
    # CLAMPED = BoundaryCondition(0, 0, 0)

    constrained = [0, 1] + [3 * (i + 1) + 1 for i, elem in enumerate(elements) if elem.end_support]  # pinned in x/y for first node
    # print(constrained)
    K = assemble(ndofs, *(e.stiffness_matrix for e in elements))
    K_red = reduce(constrained, K)

    M = assemble(ndofs, *(e.mass_matrix for e in elements))
    M_red = reduce(constrained, M)

    try:
        # find the natural frequencies
        # evals, evecs = scipy.linalg.eigh(K_red, M_red, turbo=True)
        evals = scipy.linalg.eigvalsh(K_red, M_red)
        return np.sqrt(np.abs(evals)) / (2 * np.pi)
    except np.linalg.LinAlgError:  # could not solve, maybe the system has no mass?
        return []


def singlespan(L, EA, EI, m, elem_length=None):
    if elem_length is None:
        elem_length = L / 20
    if EA < EI:
        raise ValueError("EA must be > EI")

    elements = []
    n = max(1, int(L / elem_length))  # nr of elements
    dx = L / n
    elements += (n - 1) * [get_element(dx, m, EI, EA, 0, end_support=False)] + [
        get_element(dx, m, EI, EA, 0, end_support=True)]

    return get_beam_frequencies(elements)

def multispan(spans, EA, EI, m, elem_length=None):
    L = sum(spans)
    if elem_length is None:
        elem_length = L / 40
    if EA < EI:
        raise ValueError("EA must be > EI")

    elements = []
    for l in spans:
        n = max(1, int(l / elem_length))  # nr of elements
        dx = l / n
        elements += (n - 1) * [get_element(dx, m, EI, EA, 0, end_support=False)] + [
            get_element(dx, m, EI, EA, 0, end_support=True)]

    return get_beam_frequencies(elements)