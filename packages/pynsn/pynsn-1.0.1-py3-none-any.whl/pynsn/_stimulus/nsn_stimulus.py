"""

"""
from __future__ import annotations
from copy import deepcopy

__author__ = "Oliver Lindemann <lindemann@cognitive-psychology.eu>"

from hashlib import md5
from typing import Optional, Union

import numpy as np
from numpy.typing import NDArray

from .. import defaults
from .._misc import formated_json
from .._shapes import Dot, Ellipse, Point2D, PolygonShape, Rectangle
from .._shapes.abc_shapes import AbstractShape
from ..errors import NoSolutionError, ShapeOutsideError, ShapeOverlapsError
from ..rnd._random_shape import AbstractRndShape
from .properties import ArrayProperties
from .shape_array import ShapeArray
from .stimulus_colours import StimulusColours
from .target_area import TargetArea


class NSNStimulus(ShapeArray):
    """Non-Symbolic Number Stimulus

    NSN-Stimulus are restricted to a certain target area. The classes are
    optimized for numpy calculations
    """

    def __init__(self,
                 target_area_shape: Union[Dot, Rectangle, Ellipse, PolygonShape],
                 min_distance: int = defaults.MIN_DISTANCE,
                 min_distance_target_area: int = defaults.MIN_DISTANCE
                 ) -> None:

        super().__init__()
        self._target_area = TargetArea(shape=target_area_shape,
                                       min_dist_boarder=min_distance_target_area)
        self.min_distance = min_distance
        self._properties = ArrayProperties(self)
        self._colours = StimulusColours(target_area=self._target_area.colour)

    @property
    def target_area(self) -> TargetArea:
        """the target area of the stimulus"""
        return self._target_area

    @property
    def colours(self) -> StimulusColours:
        """the colours of the stimulus"""
        return self._colours

    @colours.setter
    def colours(self, val: StimulusColours):
        """the colours of the stimulus"""
        assert isinstance(val, StimulusColours)
        self._colours = val

    @property
    def properties(self) -> ArrayProperties:
        """Properties of the nsn stimulus.

        ``ArrayProperties`` represents and handles (fitting, scaling) visual
        properties

        * numerosity
        * average_dot_diameter/average_rectangle_size
        * total_surface_area
        * average_surface_area
        * total_perimeter
        * average_perimeter
        * field_area
        * field_area_positions
        * sparsity
        * log_spacing
        * log_size
        * coverage
        """
        return self._properties

    def properties_txt(self, with_hash: bool = False, short_format: bool = False) -> str:
        if with_hash:
            if not short_format:
                rtn = f"- Hash {self.hash()}\n "
            else:
                rtn = "HASH: {} ".format(self.hash())
        else:
            rtn = ""

        return rtn + self._properties.totext(short_format)

    def hash(self) -> str:
        """Hash (MD5 hash) of the array

        The hash can be used as an unique identifier of the nsn stimulus.

        Notes:
            Hashing is based on the byte representations of the positions, perimeter
            and attributes.
        """

        rtn = md5()
        # to_byte required: https://stackoverflow.com/questions/16589791/most-efficient-property-to-hash-for-numpy-array
        rtn.update(self._xy.tobytes())
        try:
            rtn.update(self.properties.perimeter.tobytes())
        except AttributeError:
            pass
        return rtn.hexdigest()

    def todict(self, tabular: bool = True) -> dict:
        """Dict representation of the shape array
        """
        rtn = {"hash": self.hash(),
               "target_area": self.target_area.todict(),
               "min_distance": self.min_distance,
               "colours": self._colours.todict()}

        if tabular:
            rtn.update({"shape_table": self.table_dict()})
        else:
            rtn.update(super().todict())

        return rtn

    def tojson(self,
               filename: str = "",
               indent: int = 2, tabular: bool = True) -> str:
        d = self.todict(tabular=tabular)
        json_str = formated_json(d, indent=indent)
        if filename:
            with open(filename, "w", encoding="utf-8") as fl:
                fl.write(json_str)
        return json_str

    def fix_overlaps(self,
                     inside_convex_hull: bool = False,
                     minimal_replacing: bool = True,
                     sort_before: bool = True,
                     max_iterations: Optional[int] = None) -> bool:
        """move an selected object that overlaps to an free position in the
        neighbourhood.

        minimal_replacing: try to find a new random position is a neighbourhood,
            otherwise overlapping object will be randomly replaced anywhere in the
            search area
        returns True if position has been changed

        raise exception if not found
        occupied space: see generator generate
        """
        if max_iterations is None:
            max_iterations = defaults.MAX_ITERATIONS

        if sort_before:
            self.sort_by_excentricity()

        if inside_convex_hull:
            area = TargetArea(
                shape=PolygonShape(self.convex_hull.polygon),
                min_dist_boarder=self._target_area.min_dist_boarder)
        else:
            area = self._target_area

        changes = False
        cnt = 0
        while cnt < 20:
            resp = np.empty(0, dtype=int)
            for x in range(len(self._shapes)):
                r = self._fix_overlap(index=x,
                                      min_distance=self.min_distance,
                                      minimal_replacing=minimal_replacing,
                                      target_area=area,
                                      max_iterations=max_iterations)
                resp = np.append(resp, r)
            if np.any(resp == 1):
                changes = True
            if not np.any(resp == -1):  # solution found?
                return changes
            cnt += 1

        raise NoSolutionError("Can't find a solution with no overlaps")

    def contains_overlaps(self, min_distance: Optional[float] = None) -> bool:
        """Returns True for two or more elements overlap (i.e. taking
        into account the minimum distance).
        """
        if min_distance is None:
            min_distance = self.min_distance
        return super().contains_overlaps(min_distance)

    def get_overlaps(self, index: int,
                     min_distance: Optional[float] = None) -> NDArray[np.bool_]:
        """get overlaps with other shapes. Ignores overlap with oneself."""
        if min_distance is None:
            min_distance = self.min_distance
        return super().get_overlaps(index, min_distance)

    def shape_overlaps(self, shape: Union[Point2D, AbstractShape],
                       min_distance: Optional[float] = None) -> NDArray[np.bool_]:
        """Returns True for all elements that overlap with the particular shape
        (i.e. taking into account the minimum distance).
        """
        # FIXME unreliable ellipses overlapping

        if min_distance is None:
            min_distance = self.min_distance
        return self.dwithin(shape, distance=min_distance)

    def inside_target_area(self, shape: Union[Point2D, AbstractShape]) -> bool:
        """Returns True if shape is inside target area.
        """
        return self._target_area.is_object_inside(shape)

    def shape_add(self, shape: AbstractShape,
                  ignore_overlaps: bool = False):
        """"adds shape to random positions in the array"""

        if not ignore_overlaps and np.any(self.shape_overlaps(shape)):
            raise ShapeOverlapsError(f"Shape overlaps with array. {shape}")
        if not self.target_area.is_object_inside(shape):
            raise ShapeOutsideError(f"Shape outside target array. {shape}")

        super().shape_add(shape)

    def __add_random_pos(self,
                         shape: AbstractShape,
                         ignore_overlaps: bool = False,
                         inside_convex_hull: bool = False,
                         max_iterations: Optional[int] = None):
        """"adds shape to random positions in the array"""

        try:
            shape = self.random_free_position(
                shape=shape,
                ignore_overlaps=ignore_overlaps,
                inside_convex_hull=inside_convex_hull,
                max_iterations=max_iterations)
        except NoSolutionError as err:
            raise NoSolutionError("Can't find a free position: "
                                  + f"Current n={self.n_shapes}") from err

        super().shape_add(shape)

    def shape_add_random_pos(self,
                             ref_object: Union[AbstractShape, AbstractRndShape],
                             n: int = 1,
                             ignore_overlaps: bool = False,
                             inside_convex_hull: bool = False,
                             max_iterations: Optional[int] = None):
        """Creates n copies of the shape(s) or n instances of the random shape(s)
        and adds them at random positions to the array (default n=1)"""

        if isinstance(ref_object, AbstractRndShape):
            for obj in ref_object.sample(n):
                self.__add_random_pos(obj,
                                      ignore_overlaps=ignore_overlaps,
                                      inside_convex_hull=inside_convex_hull,
                                      max_iterations=max_iterations)
        else:
            while n > 0:
                self.__add_random_pos(deepcopy(ref_object),
                                      ignore_overlaps=ignore_overlaps,
                                      inside_convex_hull=inside_convex_hull,
                                      max_iterations=max_iterations)
                n = n - 1

    def random_free_position(self,
                             shape: AbstractShape,
                             ignore_overlaps: bool = False,
                             inside_convex_hull: bool = False,
                             max_iterations: Optional[int] = None) -> AbstractShape:
        """moves the object to a random free position

        raise exception if not found
        """
        if not isinstance(shape, AbstractShape):
            raise NotImplementedError("Not implemented for "
                                      f"{type(shape).__name__}")
        if max_iterations is None:
            max_iterations = defaults.MAX_ITERATIONS

        if inside_convex_hull:
            area = TargetArea(
                shape=PolygonShape(self.convex_hull.polygon),
                min_dist_boarder=self._target_area.min_dist_boarder)
        else:
            area = self._target_area

        return self._random_free_position(shape=shape,
                                          min_distance=self.min_distance,
                                          ignore_overlaps=ignore_overlaps,
                                          target_area=area,
                                          max_iterations=max_iterations)

    def table_dict(self) -> dict:
        """Tabular representation of the array of the shapes.

        This representation can not deal with PolygonShapes. It"s useful to
        create Pandas dataframe or Arrow Tables.

        Examples
        --------
        >>> df_dict = stimulus.table_dict()
        >>> df = pandas.DataFrame(df_dict) # Pandas dataframe

        >>> table = pyarrow.Table.from_pydict(df_dict) # Arrow Table
        """

        if np.any(self.get_shape_types() == PolygonShape.shape_type()):
            raise RuntimeError("tabular shape representation can not deal with "
                               "PolygonShapes")
        d = {"type": self.get_shape_types().tolist(),
             "x": self.xy[:, 0].tolist(),
             "y": self.xy[:, 1].tolist(),
             "width": self.sizes[:, 0].tolist(),
             "height": self.sizes[:, 1].tolist(),
             "attributes": [str(x) for x in self.get_attributes()]
             }
        return d
