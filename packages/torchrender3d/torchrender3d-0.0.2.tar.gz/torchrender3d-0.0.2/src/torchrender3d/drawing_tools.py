#import time
import numpy as np
import torch.fx as fx
#import torch.nn as nn
import vtk

class DrawTools:
    @staticmethod
    def draw_text_actor(
        text: str, bounding_box: vtk.vtkBoundingBox, color: tuple = (1, 1, 1)
    ):
        text_actor = (
            vtk.vtkBillboardTextActor3D()
        )  # vtkBillboardTextActor3D vtkTextActor3D
        text_actor.SetInput(text)
        minX, maxX = bounding_box.GetMinPoint()[0], bounding_box.GetMaxPoint()[0]
        minY, maxY = bounding_box.GetMinPoint()[1], bounding_box.GetMaxPoint()[1]
        minZ, maxZ = bounding_box.GetMinPoint()[2], bounding_box.GetMaxPoint()[2]
        text_actor.SetPosition(minX - 20, minY - 20, (minZ+maxZ)/2)
        text_actor.GetTextProperty().SetFontSize(15)
        text_actor.GetTextProperty().SetColor(*color)
        text_actor.SetOrientation(0, 0, 90)
        return text_actor

    @staticmethod
    def distribute_points_in_2d_grid(
        num_points: int, gap_length: tuple[float], layer_pos: float
    ):
        grid_size = int(np.ceil(np.sqrt(num_points)))
        x = np.linspace(0, grid_size * (gap_length[0]), grid_size)
        y = np.linspace(0, grid_size * (gap_length[1]), grid_size)
        x = x - np.mean(x.flatten())
        y = y - np.mean(y.flatten())
        xx, yy = np.meshgrid(x, y)
        points = np.vstack([xx.ravel(), yy.ravel()]).T
        uniform_points = points[0:num_points]
        uniform_points_3d = np.array([[x, y, layer_pos] for x, y in uniform_points[:]])
        return uniform_points_3d

    @staticmethod
    def draw_colored_cubes_in_2d_grid(
        cube_colors: list, layer_pos: float, inter_cube_gap: float
    ):
        uniform_points_n_3d = np.array(
            DrawTools.distribute_points_in_2d_grid(
                num_points=len(cube_colors),
                gap_length=(inter_cube_gap, inter_cube_gap),
                layer_pos=layer_pos,
            )
        )

        points = vtk.vtkPoints()
        points_polydata = vtk.vtkPolyData()
        for k in range(uniform_points_n_3d.shape[0]):
            points.InsertNextPoint(
                uniform_points_n_3d[k, :] + 1 * np.array([0, 0, -0.5])
            )
        points_polydata.SetPoints(points)

        scalars = vtk.vtkFloatArray()
        scalars.SetNumberOfComponents(1)
        scalars.SetName("Colors")

        for color in cube_colors:
            scalars.InsertNextValue(color)
        points_polydata.GetPointData().SetScalars(scalars)

        cube_source = vtk.vtkCubeSource()
        cube_source.SetXLength(1)
        cube_source.SetYLength(1)
        cube_source.SetZLength(1)

        glyph_mapper = vtk.vtkGlyph3DMapper()
        glyph_mapper.SetInputData(points_polydata)
        glyph_mapper.SetSourceConnection(cube_source.GetOutputPort())
        glyph_mapper.ScalingOff()
        glyph_mapper.SetScalarModeToUsePointData()

        lookupTable = vtk.vtkLookupTable()
        lookupTable.SetNumberOfTableValues(256)
        # lookupTable.SetRange(scalars.GetRange())
        lookupTable.SetRange(-1, 1)
        lookupTable.Build()
        glyph_mapper.SetLookupTable(lookupTable)
        glyph_mapper.SetScalarRange(-1, 1)

        cube_actor = vtk.vtkLODActor()
        cube_actor.SetMapper(glyph_mapper)
        return cube_actor

    @staticmethod
    def update_colored_cubes(cube_actor: vtk.vtkLODActor, updated_cube_colors: list):
        glyph_mapper = cube_actor.GetMapper()  # Get the mapper from the actor
        points_polydata = glyph_mapper.GetInput()
        scalars = points_polydata.GetPointData().GetScalars()
        if len(updated_cube_colors) != scalars.GetNumberOfTuples():
            raise ValueError("Number of weights does not match the number of points!")

        for i, new_weight in enumerate(updated_cube_colors):
            # new_weight = np.random.rand()
            scalars.SetValue(i, new_weight)

        scalars.Modified()
        glyph_mapper.Modified()
        cube_actor.GetMapper().GetInput().Modified()  # Signal that the input data has changed
        cube_actor.GetMapper().Modified()

    @staticmethod
    def draw_filled_grid_3d(volume_data: np.ndarray, coors_3d: tuple):
        depth, height, width = volume_data.shape
        points = vtk.vtkPoints()
        for z in range(depth + 1):  # +1 for points at the boundaries of cells
            for y in range(height + 1):
                for x in range(width + 1):
                    points.InsertNextPoint(x, y, z)

        structuredGrid = vtk.vtkStructuredGrid()
        structuredGrid.SetDimensions(width + 1, height + 1, depth + 1)
        structuredGrid.SetPoints(points)

        scalars = vtk.vtkFloatArray()
        scalars.SetNumberOfComponents(1)
        scalars.SetName("Cell Weights")

        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    weight = volume_data[z, y, x]
                    scalars.InsertNextValue(weight)

        structuredGrid.GetCellData().SetScalars(scalars)

        lookupTable = vtk.vtkLookupTable()
        # lookupTable.SetRange(scalars.GetRange())
        lookupTable.SetRange(-1, 1)
        # lookupTable.SetTableRange(-1,1)
        lookupTable.SetHueRange(0, 0)
        lookupTable.SetSaturationRange(0, 0)
        lookupTable.SetValueRange(0, 1)
        lookupTable.Build()

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(structuredGrid)
        mapper.SetLookupTable(lookupTable)
        # mapper.SetScalarRange(scalars.GetRange())
        mapper.SetScalarRange(-1, 1)
        mapper.SetScalarModeToUseCellData()

        actor = vtk.vtkLODActor()
        actor.SetMapper(mapper)
        actor.SetPosition(
            coors_3d[0] - width / 2, coors_3d[1] - height / 2, coors_3d[2] - depth / 2
        )
        actor.GetProperty().SetOpacity(0.90)
        return actor

    @staticmethod
    def update_filled_grid_3d(
        volume_actor: vtk.vtkLODActor, updated_volume_data: np.ndarray
    ):
        mapper = volume_actor.GetMapper()  # Get the mapper from the actor
        structuredGrid = mapper.GetInput()
        scalars = structuredGrid.GetCellData().GetScalars()
        depth, height, width = updated_volume_data.shape
        # print(f'debug158 {depth, height, width}')
        for z in range(depth):
            for y in range(height):
                for x in range(width):
                    weight = updated_volume_data[z, y, x]
                    # weight = np.random.rand()
                    scalars.SetValue(z * height * width + y * width + x, weight)
        structuredGrid.GetCellData().SetScalars(scalars)
        structuredGrid.Modified()
        mapper.Modified()

    @staticmethod
    def draw_connections(
        connection_mat: np.ndarray,
        layer_pos: float,
        layer_spacing: float,
        draw_nodes: bool = True,
        gap_length: float = 1,
    ):
        in_neuron_coors = DrawTools.distribute_points_in_2d_grid(
            num_points=connection_mat.shape[1],
            gap_length=(gap_length, gap_length),
            layer_pos=layer_pos,
        )
        out_neuron_coors = DrawTools.distribute_points_in_2d_grid(
            num_points=connection_mat.shape[0],
            gap_length=(gap_length, gap_length),
            layer_pos=layer_pos + layer_spacing,
        )
        all_points = np.concatenate((in_neuron_coors, out_neuron_coors), axis=0)
        in_neuron_ids = np.arange(0, in_neuron_coors.shape[0], 1)
        out_neuron_ids = np.arange(
            0 + in_neuron_coors.shape[0],
            out_neuron_coors.shape[0] + in_neuron_coors.shape[0],
            1,
        )

        points = vtk.vtkPoints()
        for k in range(all_points.shape[0]):
            points.InsertNextPoint(all_points[k, :])

        lines = vtk.vtkCellArray()
        lines_polydata = vtk.vtkPolyData()
        weights_array = vtk.vtkFloatArray()
        weights_array.SetName("Weights")
        weights_array.SetNumberOfComponents(1)

        for i in range(len(in_neuron_ids)):  # Each input neuron
            for j in range(len(out_neuron_ids)):  # Each output neuron
                line = vtk.vtkLine()
                line.GetPointIds().SetId(0, in_neuron_ids[i])  # Input point
                line.GetPointIds().SetId(
                    1, out_neuron_ids[j]
                )  # Output point (offset by input_size)
                lines.InsertNextCell(line)
                weight_value = connection_mat[j, i]
                weights_array.InsertNextValue(weight_value)

        lines_polydata.SetPoints(points)
        lines_polydata.SetLines(lines)
        lines_polydata.GetCellData().SetScalars(weights_array)

        weights_min = np.min(connection_mat.flatten())
        weights_max = np.max(connection_mat.flatten())
        lut = vtk.vtkLookupTable()
        lut.SetTableRange(weights_min, weights_max)
        lut.SetTableRange(-1, 1)
        lut.SetSaturationRange(0.0, 0.0)  # Grayscale (no color)
        lut.SetValueRange(0.0, 1.0)  # From black (0) to white (1)
        lut.SetAlphaRange(0.1, 1.0)
        # lut.SetValueRange(0.0, 1.0)
        lut.Build()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(lines_polydata)
        mapper.SetScalarModeToUseCellData()
        mapper.SetScalarRange(-1, 1)

        mapper.SetLookupTable(lut)
        mapper.UseLookupTableScalarRangeOn()
        mapper.SetScalarModeToUseCellData()

        # Step 6: Create an actor for the lines
        linear_actor = vtk.vtkLODActor()
        linear_actor.SetMapper(mapper)
        linear_actor.GetProperty().SetOpacity(1.0)

        if draw_nodes:
            sphere_source = vtk.vtkSphereSource()
            sphere_source.SetRadius(0.25)  # Set the radius of the spheres

            glyph_mapper = vtk.vtkGlyph3DMapper()
            glyph_mapper.SetInputData(
                lines_polydata
            )  # Use the same polydata that contains the points
            glyph_mapper.SetSourceConnection(
                sphere_source.GetOutputPort()
            )  # Set the sphere as the glyph source
            glyph_mapper.ScalarVisibilityOff()  #

            spheres_actor = vtk.vtkLODActor()
            spheres_actor.SetMapper(glyph_mapper)
            spheres_actor.GetProperty().SetColor(1.0, 1.0, 1.0)

        return [linear_actor, spheres_actor]

    @staticmethod
    def update_connections(
        linear_actor: vtk.vtkLODActor, updated_connection_mat: np.ndarray
    ):
        mapper = linear_actor.GetMapper()
        lines_polydata = mapper.GetInput()
        weights_array = lines_polydata.GetCellData().GetScalars()
        num_cells = weights_array.GetNumberOfTuples()

        if len(updated_connection_mat.flatten()) != num_cells:
            raise ValueError(
                "New weights shape does not match the existing number of cells!"
            )

        in_neurons = updated_connection_mat.shape[1]
        out_neurons = updated_connection_mat.shape[0]

        for i in range((in_neurons)):
            for j in range((out_neurons)):
                weight_value = updated_connection_mat[j, i]
                # weight_value = np.random.rand()
                weights_array.SetValue(i * out_neurons + j, weight_value)

        weights_array.Modified()
        lines_polydata.Modified()
        mapper.Modified()

    @staticmethod
    def draw_bounding_box_around_actors(
        actors: list[vtk.vtkLODActor], box_name: str, color: tuple = (1, 1, 1)
    ):
        bounding_box = vtk.vtkBoundingBox()
        for actor in actors:
            bounds = actor.GetBounds()
            bounding_box.AddBounds(bounds)
        minX, maxX = bounding_box.GetMinPoint()[0], bounding_box.GetMaxPoint()[0]
        minY, maxY = bounding_box.GetMinPoint()[1], bounding_box.GetMaxPoint()[1]
        minZ, maxZ = bounding_box.GetMinPoint()[2], bounding_box.GetMaxPoint()[2]

        # Create a vtkCubeSource to represent the bounding box
        cube_source = vtk.vtkCubeSource()
        cube_source.SetBounds(minX, maxX, minY, maxY, minZ, maxZ)

        # Create a mapper and an actor for the bounding box
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(cube_source.GetOutputPort())

        box_actor = vtk.vtkLODActor()
        box_actor.SetMapper(mapper)

        # Set the color and style for the bounding box
        box_actor.GetProperty().SetColor(1, 0, 0)  # Red color
        box_actor.GetProperty().SetRepresentationToWireframe()
        box_actor.GetProperty().SetColor(*color)

        label_actor = DrawTools.draw_text_actor(
            text=box_name, bounding_box=bounding_box, color=color
        )
        return box_actor, label_actor


