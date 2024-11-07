#######################################################################
#  TARDIS - Transformer And Rapid Dimensionless Instance Segmentation #
#                                                                     #
#  New York Structural Biology Center                                 #
#  Simons Machine Learning Center                                     #
#                                                                     #
#  Robert Kiewisz, Tristan Bepler                                     #
#  MIT License 2021 - 2024                                            #
#######################################################################
from collections import defaultdict
from itertools import combinations
from typing import List, Optional, Tuple, Union

from rfc3986.abnf_regexp import segments
from scipy.spatial import KDTree

try:
    import open3d as o3d
except ModuleNotFoundError:
    pass
from tardis_em.utils import SCANNET_COLOR_MAP_20, rgb_color

import matplotlib.pyplot as plt
import numpy as np


def img_is_color(img):
    if len(img.shape) == 3:
        # Check the color channels to see if they're all the same.
        c1, c2, c3 = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        if np.all(c1 == c2) and np.all(c2 == c3):
            return True

    return False


def show_image_list(
    list_images,
    list_titles=None,
    list_cmaps=None,
    list_mask_cmaps=None,
    grid=True,
    num_cols=2,
    figsize=(20, 10),
    title_fontsize=30,
    list_masks=None,
    dpi=100,
):
    """
    Shows a grid of images, where each image is a Numpy array. The images can be either
    RGB or grayscale.

    Args:
        list_images (list): List of the images to be displayed.
        list_titles (list or None): Optional list of titles to be shown for each image.
        list_cmaps (list, str or None): Optional list of cmap values for each image.
            If None, then cmap will be automatically inferred.
        list_mask_cmaps (list, str or None):
        grid (boolean): If True, show a grid over each image
        num_cols (int): Number of columns to show.
        figsize (tuple): Value to be passed to pyplot.figure()
        title_fontsize (int): Value to be passed to set_title()
        list_masks(list, None):
        dpi (int):
    """
    assert isinstance(list_images, list)
    assert len(list_images) > 0
    assert isinstance(list_images[0], np.ndarray)

    if list_titles is not None:
        assert isinstance(list_titles, list)
        assert len(list_images) == len(list_titles), "%d imgs != %d titles" % (
            len(list_images),
            len(list_titles),
        )

    if list_cmaps is not None:
        assert isinstance(list_cmaps, (list, str))
        if not isinstance(list_cmaps, str):
            assert len(list_images) == len(list_cmaps), "%d imgs != %d cmaps" % (
                len(list_images),
                len(list_cmaps),
            )

    if list_masks is not None:
        assert len(list_masks) == len(list_images)

    num_images = len(list_images)
    num_cols = min(num_images, num_cols)
    num_rows = int(num_images / num_cols) + (1 if num_images % num_cols != 0 else 0)

    # Create a grid of subplots.
    fig, axes = plt.subplots(num_rows, num_cols, figsize=figsize, dpi=dpi)

    # Create list of axes for easy iteration.
    if isinstance(axes, np.ndarray):
        list_axes = list(axes.flat)
    else:
        list_axes = [axes]

    for i in range(num_images):
        img = list_images[i]
        if list_masks is not None:
            mask = list_masks[i]

        if isinstance(list_cmaps, str):
            cmap = list_cmaps
        else:
            cmap = (
                list_cmaps[i]
                if list_cmaps is not None
                else (None if img_is_color(img) else "gray")
            )

        if list_mask_cmaps is not None:
            if isinstance(list_mask_cmaps, str):
                cmap_mask = list_mask_cmaps
            else:
                cmap_mask = (
                    list_mask_cmaps[i] if list_mask_cmaps is not None else "Reds"
                )
        else:
            cmap_mask = "Reds"

        list_axes[i].imshow(img, cmap=cmap)
        if list_masks is not None:
            list_axes[i].imshow(mask, cmap=cmap_mask, alpha=0.5)

        if title_fontsize is not None:
            list_axes[i].set_title(
                list_titles[i] if list_titles is not None else "Image %d" % i,
                fontsize=title_fontsize,
            )
        list_axes[i].grid(grid)

    for i in range(num_images, len(list_axes)):
        list_axes[i].set_visible(False)

    fig.tight_layout()
    plt.show()


def _dataset_format(coord: np.ndarray, segmented: bool) -> Tuple[np.ndarray, bool]:
    """
    Silently check for an array format and correct 2D datasets to 3D.

    Args:
        coord (np.ndarray): 2D or 3D array of shape [(s) x X x Y x Z] or [(s) x X x Y].
        segmented (bool): If True expect (s) in a data format as segmented values.

    Returns:
        Tuple[np.ndarray, bool]: Checked and corrected coord array with boolean
        statement if array is compatible.
    """
    check = True

    if segmented:
        if coord.shape[1] not in [3, 4]:
            check = False
            print("Coord data must be 2D/3D with labels (4D/5D)")

        # Correct 2D to 3D
        if coord.shape[1] == 3:
            coord = np.vstack(
                (coord[:, 0], coord[:, 1], coord[:, 2], np.zeros((coord.shape[0],)))
            ).T
    else:
        if coord.shape[1] not in [2, 3]:
            check = False
            print("Coord data must be 2D/3D with labels (2D/3D)")

        # Correct 2D to 3D
        if coord.shape[1] == 2:
            coord = np.vstack((coord[:, 0], coord[:, 1], np.zeros((coord.shape[0],)))).T

    return coord, check


def _rgb(
    coord: np.ndarray, segmented: bool, ScanNet=False, color=False, filaments=False
) -> np.ndarray:
    """
    Convert float to RGB classes.

    Use predefined Scannet V2 RBG classes or random RGB classes.

    Args:
        coord (np.ndarray): 2D or 3D array of shape [(s) x X x Y x Z] or [(s) x X x Y].
        segmented (bool): If True expect (s) in a data format as segmented values.
        ScanNet (bool): If True output scannet v2 classes.

    Returns:
        np.ndarray: 3D array with RGB values for each point.
    """
    if filaments:
        unique_ids = np.unique(coord[:, 0])
        rgb_list = [
            np.array((np.random.rand(), np.random.rand(), np.random.rand()))
            for _ in unique_ids
        ]
        return rgb_list
    rgb = np.zeros((coord.shape[0], 3), dtype=np.float64)

    if segmented:
        if ScanNet:
            for id_, i in enumerate(coord[:, 0]):
                color = SCANNET_COLOR_MAP_20.get(i, SCANNET_COLOR_MAP_20[0])
                rgb[id_, :] = [x / 255 for x in color]
        else:
            unique_ids = np.unique(coord[:, 0])
            if color:
                rgb_list = [np.array((0, 0, 0)) for _ in unique_ids]
            else:
                rgb_list = [
                    np.array((np.random.rand(), np.random.rand(), np.random.rand()))
                    for _ in unique_ids
                ]
            id_to_rgb = {idx: color for idx, color in zip(unique_ids, rgb_list)}

            for id_, i in enumerate(coord[:, 0]):
                df = id_to_rgb[i]
                rgb[id_, :] = df
    else:
        rgb[:] = [1, 0, 0]

    return rgb


def segment_to_graph(coord: np.ndarray) -> list:
    """
    Build filament vector lines for open3D.

    Args:
        coord (np.ndarray): 2D or 3D array of shape [(s) x X x Y x Z] or [(s) x X x Y].

    Returns:
        list: list of segments converted for open3D
    """
    graph_list = []
    stop = 0

    for i in np.unique(coord[:, 0]):
        id_ = np.where(coord[:, 0] == i)[0]
        id_ = coord[id_]

        x = 0  # Iterator checking if current point is a first on in the list
        start = stop
        stop += len(id_)

        if x == 0:
            graph_list.append([start, start + 1])

        length = stop - start  # Number of point in a segment
        for j in range(1, length - 1):
            graph_list.append([start + (x + 1), start + x])

            if j != (stop - 1):
                graph_list.append([start + (x + 1), start + (x + 2)])
            x += 1
        graph_list.append([start + (x + 1), start + x])

    return graph_list


def point_cloud_to_mesh(point_cloud, k=6):
    # Initialize lists to store all vertices and faces across IDs
    all_vertices = []
    all_faces = []
    vertex_offset = 0  # To keep track of the current vertex index across different IDs

    # Group points by ID
    point_groups = defaultdict(list)
    for point in point_cloud:
        point_id = point[0]
        coordinates = point[1:]
        point_groups[point_id].append(coordinates)

    for point_id in point_groups.keys():
        points = point_groups[point_id]
        points = np.array(points)
        if len(points) < 3:
            print(f"Not enough points for triangulation with ID {point_id}")
            continue

        # Build a KDTree for finding nearest neighbors
        kdtree = KDTree(points)
        all_faces_set = set()

        # For each point, find the k nearest neighbors and form triangles
        neighbors = kdtree.query(points, k=k)[
            1
        ]  # Get all neighbors at once for efficiency

        # Generate triangles by connecting each point with pairs of neighbors
        for i, neighbor_indices in enumerate(neighbors):
            for j, m in combinations(
                neighbor_indices[1:], 2
            ):  # Avoid using the point itself
                face = tuple(sorted([i, j, m]))
                all_faces_set.add(face)

        # Convert set of faces to a NumPy array
        faces = np.array(list(all_faces_set))

        # Append the points and faces for this ID to the main lists
        all_vertices.append(points)
        all_faces.append(faces)
        vertex_offset += len(points)  # Update offset for the next group

    return all_vertices, all_faces


def rotate_view(vis):
    """
    Optional viewing parameter for open3D to constantly rotate scene.
    Args:
        vis: Open3D view control setting.
    """
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    opt.mesh_show_back_face = True

    ctr = vis.get_view_control()
    ctr.rotate(2.0, 0.0)

    return False


def background_view(vis):
    """
    Optional viewing parameter for open3D to constantly rotate scene.
    Args:
        vis: Open3D view control setting.
    """
    opt = vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    opt.mesh_show_back_face = True
    return False


def VisualizePointCloud(
    coord: np.ndarray,
    segmented: bool = True,
    rgb: Optional[np.ndarray] = None,
    animate=False,
    return_=False,
):
    """
    Visualized point cloud.

    Output color coded point cloud. Color values indicate individual segments.

    Args:
        coord (np.ndarray): 2D or 3D array of shape [(s) x X x Y x Z] or [(s) x X x Y].
        segmented (bool): If True expect (s) in a data format as segmented values.
        rgb (np.ndarray): Optional, indicate rgb values.
        animate (bool): Optional trigger to turn off animated rotation.
    """
    coord, check = _dataset_format(coord=coord, segmented=segmented)

    if check:
        pcd = o3d.geometry.PointCloud()

        if segmented:
            pcd.points = o3d.utility.Vector3dVector(coord[:, 1:])
        else:
            pcd.points = o3d.utility.Vector3dVector(coord)

        if rgb is None and coord.shape[1] == 3:
            rgb = rgb_color["red"]
        elif isinstance(rgb, str):
            assert (
                rgb in rgb_color.keys()
            ), f"Color: {rgb} suppoerted. Choose one of: {rgb_color}"
            rgb = rgb_color[rgb]

        if rgb is None:
            pcd.colors = o3d.utility.Vector3dVector(_rgb(coord, True))
        else:
            pcd.paint_uniform_color(rgb)
        if return_:
            return pcd

        VisualizeCompose(animate=animate, pcd=pcd)


def VisualizeFilaments(
    coord: np.ndarray, animate=True, with_node=False, filament_color=None, return_=False
):
    """
    Visualized filaments.

    Output color coded point cloud. Color values indicate individual segments.

    Args:
        coord (np.ndarray): 2D or 3D array of shape [(s) x X x Y x Z] or [(s) x X x Y].
        animate (bool): Optional trigger to turn off animated rotation.
        with_node (bool): Optional, If True, show point on filaments
        filament_color (None, list): Uniform filament color
        return_ (bool): If True return open3d object
    """
    coord, check = _dataset_format(coord=coord, segmented=True)

    if filament_color is None:
        filament_color = rgb_color["black"]
    elif isinstance(filament_color, str):
        assert (
            filament_color in rgb_color.keys()
        ), f"Color: {filament_color} suppoerted. Choose one of: {rgb_color}"
        filament_color = rgb_color[filament_color]

    if check:
        if with_node:
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(coord[:, 1:])
            pcd.colors = o3d.utility.Vector3dVector(_rgb(coord, True))

        graph = segment_to_graph(coord=coord)
        line_set = o3d.geometry.LineSet()

        line_set.points = o3d.utility.Vector3dVector(coord[:, 1:])
        line_set.lines = o3d.utility.Vector2iVector(graph)

        line_set.paint_uniform_color(filament_color)

        if return_:
            return line_set

        if with_node:
            VisualizeCompose(animate=animate, pcd=pcd, line_set=line_set)
        else:
            VisualizeCompose(animate=animate, line_set=line_set)


def VisualizeScanNet(coord: np.ndarray, segmented: True, return_=False):
    """
    Visualized scannet scene

    Output color-coded point cloud. Color values indicate individual segments.

    Args:
        coord (np.ndarray): 2D or 3D array of shape [(s) x X x Y x Z] or [(s) x X x Y].
        segmented (bool): If True expect (s) in a data format as segmented values.
    """
    coord, check = _dataset_format(coord=coord, segmented=segmented)

    if check:
        pcd = o3d.geometry.PointCloud()

        if segmented:
            pcd.points = o3d.utility.Vector3dVector(coord[:, 1:])
        else:
            pcd.points = o3d.utility.Vector3dVector(coord)
        pcd.colors = o3d.utility.Vector3dVector(_rgb(coord, segmented, True))

        if return_:
            return pcd

        VisualizeCompose(animate=False, meshes=pcd)


def VisualizeSurface(
    vertices: Union[tuple, list, np.ndarray] = None,
    triangles: Union[tuple, list, np.ndarray] = None,
    point_cloud=None,
    animate=False,
    return_=False,
):
    if vertices is None and triangles is None and point_cloud is None:
        return

    if isinstance(vertices, np.ndarray):
        vertices = [vertices]

    if isinstance(triangles, np.ndarray):
        triangles = [triangles]

    if point_cloud is not None:
        if point_cloud.shape[1] == 4:
            pc = []
            for id_ in np.unique(point_cloud[:, 0]):
                pc.append(point_cloud[point_cloud[:, 0] == id_, 1:])
        else:
            pc = [point_cloud]

        vertices, triangles = [], []
        for i in pc:
            pcd = VisualizePointCloud(i, segmented=False, return_=True)
            pcd.estimate_normals()
            # mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, linear_fit=True)[0]
            mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
                pcd, scale=1
            )[0]

            vertices.append(mesh.vertices)
            triangles.append(mesh.triangles)

    meshes = []
    for v, t in zip(vertices, triangles):
        meshes.append(o3d.geometry.TriangleMesh())

        meshes[-1].vertices = o3d.utility.Vector3dVector(v)
        meshes[-1].triangles = o3d.utility.Vector3iVector(t)
        meshes[-1].paint_uniform_color(list(np.random.random(3)))

        # meshes[-1].filter_smooth_laplacian(5, )
        voxel_size = max(meshes[-1].get_max_bound() - meshes[-1].get_min_bound()) / 512
        meshes[-1] = meshes[-1].simplify_vertex_clustering(
            voxel_size=voxel_size,
            contraction=o3d.geometry.SimplificationContraction.Average,
        )

        meshes[-1].compute_vertex_normals()

    if return_:
        return meshes

    VisualizeCompose(animate, meshes=meshes)


def VisualizeCompose(animate=False, **kwargs):
    if all(value is None for value in kwargs.values()):
        return

    objects_ = []
    for o in kwargs.values():
        if isinstance(o, List):
            for i in o:
                objects_.append(i)
        else:
            objects_.append(o)

    if animate:
        o3d.visualization.draw_geometries_with_animation_callback(objects_, rotate_view)
    else:
        o3d.visualization.draw_geometries_with_animation_callback(
            objects_, background_view
        )
