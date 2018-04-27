import numpy as np
from scipy.ndimage.morphology import distance_transform_edt


def enlarge_binary_map(
    binary_map,
    radius,
    voxel_size,
    ring_inner=None,
    in_place=False):
    '''Enlarge existing regions in a binary map.

    Args:

        binary_map (numpy array):

            A matrix with zeros, in which regions to be enlarged are indicated
            with a 1 (regions can already represent larger areas).

        radius (float):

            The amount by which to enlarge forground objects in world units.

        voxel_size (tuple, list or numpy array):

            Indicates the physical voxel size of the binary_map.

        ring_inner (int, optional):

            If set, instead of just enlargin objects, a ring is grown around
            them (and the objects removed). The ring starts at ``ring_inner``
            and goes until ``radius``.

        in_place (bool, optional):

            If set to ``True``, argument ``binary_map`` will be modified
            directly.

    Returns:

        A matrix with 0s and 1s of same dimension as input binary_map with
        enlarged regions (indicated with 1), unless ``in_place`` is set.
    '''

    if len(np.unique(binary_map)) == 1:
        # Check whether there are regions at all. If there is no region (or
        # everything is full), return the same map.
        return binary_map

    if voxel_size is None:
        voxel_size = (1,)*binary_map.shape[0]

    voxel_size = np.asarray(voxel_size)

    if in_place:
        np.logical_not(binary_map, out=binary_map)
    else:
        binary_map = np.logical_not(binary_map)
    edtmap = distance_transform_edt(binary_map, sampling=voxel_size)

    # grow objects
    if in_place:
        binary_map[:] = edtmap <= radius
    else:
        binary_map = edtmap <= radius

    # unmask inner part, if requested
    if ring_inner is not None:
        binary_map[edtmap <= ring_inner] = False

    if in_place:
        return None

    return binary_map


def create_ball_kernel(radius, voxel_size):
    '''	Generates a ball-shaped structuring element.

    Args:

        radius (float):

            The radius of the ball-shaped structuring element in world-units

        voxel_size (tuple, list or numpy array):

            Indicates the physical voxel size of the structuring element.

    Returns:

        The structuring element where elements of the neighborhood are 1 and 0 otherwise. The shape of the returned
        array depends on radius and voxel_size. For instance voxel_size = [2, 1, 1], radius = 5 produces an array of
        shape (7, 11, 11)
    '''
    voxel_size = np.asarray(voxel_size)
    assert voxel_size.shape[0] <= 3, (
        "structuring element can only be generated in 2D or 3D")

    # Calculate shape for new kernel, make it sufficiently large (--> ceil)
    radius_voxel = np.ceil(float(radius) / voxel_size).astype(np.int)
    kernel_shape = np.array(radius_voxel) * 2 + 1

    kernel = np.zeros(kernel_shape, dtype=np.uint8)
    middle_point = kernel_shape / 2
    kernel[tuple(middle_point)] = 1
    return enlarge_binary_map(kernel, radius, voxel_size)
