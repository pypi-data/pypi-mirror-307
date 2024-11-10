"""Load and process input data."""

import json
import logging
import math
import os
from collections import OrderedDict, defaultdict
from typing import DefaultDict, Dict, List, Union

import numpy as np
from scipy.interpolate import griddata

from soil_moisture_prediction.area_geometry import RectGeom
from soil_moisture_prediction.input_file_parser import (
    FileValidationError,
    PredictorParser,
    SoilMoistureParser,
)
from soil_moisture_prediction.pydantic_models import PredictorInformationHeader
from soil_moisture_prediction.streams import BkgElevationData, SoilGridsData

logger = logging.getLogger(__name__)

stream_dic: Dict[str, Union[SoilGridsData, BkgElevationData]] = {}

# stream_dic["corine"] = CorineData

stream_dic["elevation_bkg"] = BkgElevationData

soilgrid_keys = [
    "bdod",
    "cec",
    "cfvo",
    "clay",
    "nitrogen",
    "phh2o",
    "sand",
    "silt",
    "soc",
    "ocd",
    "ocs",
]
depth_levels = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]
for key in soilgrid_keys:
    for depth in depth_levels:
        stream_dic[key + "_" + depth] = SoilGridsData

elevation_keys = ["elevation", "elevation_bkg"]


class SoilMoistureData:
    """Class containing soil moisture measurements."""

    file_path: str
    x: OrderedDict[str, np.ndarray]
    y: OrderedDict[str, np.ndarray]
    soil_moisture: OrderedDict[str, np.ndarray]
    soil_moisture_dev_low: OrderedDict[str, np.ndarray]
    soil_moisture_dev_high: OrderedDict[str, np.ndarray]
    time_steps: List[str]
    geometry: RectGeom
    uncertainty: bool
    training_coordinates: OrderedDict[str, np.ndarray]

    def __init__(self, file_path, geometry, uncertainty):
        """
        Initialize the SoilMoistureData object.

        Parameters:
        - soil_moisture_file (str): Path to the soil moisture file.
        - geometry (RectGeom): RectGeom object defining the geometry.
        - uncertainty (bool): Whether uncertainty data is present.

        This method opens the soil moisture file and saves the data to NumPy arrays.
        """
        self.x = OrderedDict()
        self.y = OrderedDict()
        self.soil_moisture = OrderedDict()
        self.soil_moisture_dev_low = OrderedDict()
        self.soil_moisture_dev_high = OrderedDict()
        self.time_steps = []
        self.geometry = geometry
        self.uncertainty = uncertainty
        self.file_path = file_path
        self.training_coordinates = {}

        self._parse_soil_moisture_file()
        self._set_training_coordinates()

    def _parse_soil_moisture_file(self, sm_filtering=False):
        """
        Open the soil moisture file and save data to NumPy arrays.

        Parameters:
        - soil_moisture_file (str): Path to the soil moisture file.
        - sm_filtering (bool): whether apply a median filter on soil moisture data

        This method reads the soil moisture file line by line, parses the data,
        and updates the appropriate attributes accordingly.
        """
        logger.info(f"Loading soil moisture data from {self.file_path}")
        parser = SoilMoistureParser(self.geometry)

        if not os.path.exists(self.file_path):
            raise FileValidationError(f"File {self.file_path} does not exist")

        with open(self.file_path, "r") as file:
            for row in parser.parse(file):
                x, y, time_step, soil_moisture, err_low, err_high = row

                if time_step not in self.time_steps:
                    self._initiate_time(time_step)
                self.x[time_step].append(x)
                self.y[time_step].append(y)
                self.soil_moisture[time_step].append(soil_moisture)
                if self.uncertainty:
                    self.soil_moisture_dev_low[time_step].append(err_low)
                    self.soil_moisture_dev_high[time_step].append(err_high)

        for time_step in self.time_steps:
            self.x[time_step] = np.array(self.x[time_step])
            self.y[time_step] = np.array(self.y[time_step])
            self.soil_moisture[time_step] = np.array(self.soil_moisture[time_step])
            if self.uncertainty:
                self.soil_moisture_dev_low[time_step] = np.array(
                    self.soil_moisture_dev_low[time_step]
                )
                self.soil_moisture_dev_high[time_step] = np.array(
                    self.soil_moisture_dev_high[time_step]
                )

            if sm_filtering:
                self._soil_moisture_filtering(time_step)

    def _initiate_time(self, time_step):
        """
        Initialize lists to store soil moisture data for the given start time.

        Parameters:
        - time_step (str): Time step of the measurements.
        - uncertainty (bool): Whether uncertainty data is present.

        This method initializes empty lists to store soil moisture data for the
        specified start time.
        """
        self.time_steps.append(time_step)
        self.x[time_step] = []
        self.y[time_step] = []
        self.soil_moisture[time_step] = []
        self.soil_moisture_dev_low[time_step] = []
        self.soil_moisture_dev_high[time_step] = []

    def _set_training_coordinates(self):
        """Build a dictionary of training coordinates for each time step."""
        for time_step in self.time_steps:
            self.training_coordinates[time_step] = self.geometry.find_nearest_node(
                self.x[time_step],
                self.y[time_step],
            )

    def separate_branches(self, x, y, z, threshold_distance=1):
        """
        Identify branch transitions based on distance between consecutive points.

        Parameters:
        - x (numpy.ndarray): Array of x-coordinates.
        - y (numpy.ndarray): Array of y-coordinates.
        - z (numpy.ndarray): Array of z-coordinates (soil moisture measurements).
        - threshold_distance (float): Threshold distance for identifying branch
        transitions.

        Returns:
        - list: List of arrays representing separate branches.

        This method identifies branch transitions based on the distance between
        consecutive points (specified by threshold_distance) in the x-y plane.
        It splits the data into separate branches and returns them as a list
        of arrays.
        """
        # Threshold by time when time data input is added?
        distances = np.sqrt(np.diff(x) ** 2 + np.diff(y) ** 2)
        branch_transitions = np.where(distances > threshold_distance)[0] + 1
        branches = np.split(np.column_stack([x, y, z]), branch_transitions)
        return branches


class PredictorData:
    """Class containing predictor data."""

    source: Union[str, None, SoilGridsData, BkgElevationData]
    values_on_nodes: Union[OrderedDict[str, np.ndarray], DefaultDict[str, np.ndarray]]
    constant_values_on_nodes: Union[None, np.ndarray]
    std_deviation_on_nodes: Union[
        None, OrderedDict[str, np.ndarray], DefaultDict[str, np.ndarray]
    ]
    constant_std_deviation_on_nodes: Union[None, np.ndarray]
    time_steps: List[str]
    geometry: RectGeom
    information: PredictorInformationHeader

    def __init__(
        self,
        source: Union[str, SoilGridsData, BkgElevationData, None],
        information: PredictorInformationHeader,
        geometry: RectGeom,
    ) -> None:
        """
        Initialize the SoilMoistureData object.

        Parameters:
        - source (str, None, DataStream): Path to the predictor file, None or a
          DataStream object.
        - information (PredictorInformationHeader): Information about the predictor.
        - geometry (RectGeom): RectGeom object defining the geometry.

        This method opens the soil moisture file and saves the data to NumPy arrays.
        """
        if information.constant:
            self.values_on_nodes = defaultdict(lambda: self.constant_values_on_nodes)
            self.constant_values_on_nodes = np.zeros((geometry.dim_x, geometry.dim_y))
        else:
            self.values_on_nodes = OrderedDict()
            self.constant_values_on_nodes = None

        if information.std_deviation and information.constant:
            self.std_deviation_on_nodes = defaultdict(
                lambda: self.constant_std_deviation_on_nodes
            )
            self.constant_std_deviation_on_nodes = np.zeros(
                (geometry.dim_x, geometry.dim_y)
            )
        elif information.std_deviation and not information.constant:
            self.std_deviation_on_nodes = OrderedDict()
            self.constant_std_deviation_on_nodes = None
        else:
            self.std_deviation_on_nodes = None

        if source is None:
            logger.info(f"Create new predictor {information.predictor_name}")
        elif type(source) is str:
            if not os.path.exists(source):
                raise FileValidationError(f"File {source} does not exist")
            logger.info(f"Loading predictor data from {source}")
        else:
            logger.info(f"Loading predictor data from {information.predictor_name}")

        self.source = source
        self.information = information
        self.geometry = geometry

        if source is not None:
            self.time_steps = []
            self._parse_data()
        else:
            self.time_steps = [None]

    def __str__(self):
        """Return a string representation of the predictor."""
        return f"Predictor {self.information.predictor_name}"

    def full_info(self):
        """Return a string with the full information of the predictor."""
        value_info = "\n".join(
            (f"{time}:\n{values}" for time, values in self.values_on_nodes.items())
        )
        std_deviation_info = "\n".join(
            (
                f"{time}:\n{values}"
                for time, values in self.std_deviation_on_nodes.items()
            )
        )
        info = (
            f"Predictor {self.information.predictor_name} - {self.information.unit}\n"
            f"Values: \n{value_info}\n"
            f"Standard deviation: \n{std_deviation_info}"
        )

        return info

    def _parse_data(self):
        if type(self.source) is str:
            generator = self._file_generator()
        else:
            generator = self.source.stream()

        xs = []
        ys = []
        values = []
        std_deviations = []

        for row in generator:
            x, y, value, std_deviation, time_step = row
            if time_step not in self.time_steps:
                try:
                    previous_time_step = self.time_steps[-1]
                # This is for the first start time in the file
                except IndexError:
                    previous_time_step = None

                # For the first start time, we don't have any data to interpolate
                if previous_time_step is not None:
                    self._interpolate_to_grid(
                        xs, ys, values, std_deviations, previous_time_step
                    )

                self.time_steps.append(time_step)
                xs = []
                ys = []
                values = []
                std_deviations = []

            xs.append(x)
            ys.append(y)
            values.append(value)
            std_deviations.append(std_deviation)

        self._interpolate_to_grid(xs, ys, values, std_deviations, time_step)

    def _file_generator(self):
        parser = PredictorParser(self.geometry, self.information)
        with open(self.source, "r") as file:
            for row in parser.parse(file):
                yield row

    def _interpolate_to_grid(self, xs, ys, values, std_deviations, time_step):
        if self.information.constant:
            self.constant_values_on_nodes = griddata(
                (xs, ys),
                values,
                (self.geometry.grid_x, self.geometry.grid_y),
                method="linear",
            )
        else:
            self.values_on_nodes[time_step] = griddata(
                (xs, ys),
                values,
                (self.geometry.grid_x, self.geometry.grid_y),
                method="linear",
            )

        if self.information.std_deviation and not self.information.constant:
            self.std_deviation_on_nodes[time_step] = griddata(
                (xs, ys),
                std_deviations,
                (self.geometry.grid_x, self.geometry.grid_y),
                method="linear",
            )
        elif self.information.std_deviation and self.information.constant:
            self.constant_std_deviation_on_nodes = griddata(
                (xs, ys),
                std_deviations,
                (self.geometry.grid_x, self.geometry.grid_y),
                method="linear",
            )

    def get_values_by_line(self, time_step, line_index):
        """
        Get the values of the predictor for a given line index.

        Parameters:
        - time_step (str): Time step of the measurements.
        - line_index (int): Index of the line.

        Returns:
        - numpy.ndarray: Array of values for the given line index.

        This method retrieves the values of the predictor for the specified start
        time and line index.
        """
        return self.values_on_nodes[time_step][line_index, :]


class InputData:
    """Class containing all input data, predictors and soil moisture measurements."""

    predictors: OrderedDict[str, PredictorData]
    soil_moisture_data: SoilMoistureData
    # Used to compute slope and aspect, stored to cache the values
    elev_dx: Union[np.ndarray, None]
    elev_dy: Union[np.ndarray, None]

    def __init__(
        self,
        input_parameters,
        geometry,
        work_dir,
    ):
        """
        Initialize the InputData object.

        Parameters:
        - input_parameters (InputParameters): Dictionary containing input parameters.
        - geometry (RectGeom): RectGeom object defining the geometry.
        - has_mask (bool): Whether a mask is present in the data.

        This method initializes the input data and opens the soil moisture file.
        """
        logger.info("Loading input data.")
        self.predictors = OrderedDict()
        self.elev_dx = None
        self.elev_dy = None

        self._load_soil_moisture_data(input_parameters, geometry, work_dir)
        logger.info("Loading predictors")
        self._load_predictors(input_parameters, geometry, work_dir)
        logger.info("Check time intervals")
        self._check_time_steps()

        if input_parameters.reset_when_rain_occured and "rain" not in self.predictors:
            raise FileValidationError(
                "Rainfall data is not available, but parameter reset_when_rain_occured is set to True"  # noqa
            )

        if (
            input_parameters.monte_carlo_predictors
            and len(self.predictors_with_nan()) > 0
        ):
            logger.error(
                f"Predictors with NaN values: {', '.join(self.predictors_with_nan())}"
            )  # noqa
            raise FileValidationError(
                "QMC sampling is not supported with predictors containing NaN values"
            )

        if input_parameters.compute_slope:
            logger.info("Computing slope from elevation")
            self._create_slope()

        if input_parameters.compute_aspect:
            logger.info("Computing aspect from elevation")
            self._create_aspect()

        if input_parameters.past_prediction_as_feature:
            logger.info("Adding past prediction as feature")
            self._past_prediction_as_feature(geometry)

    def _load_soil_moisture_data(self, input_parameters, geometry, work_dir):
        # See if the file is a path or a name
        if not os.path.dirname(input_parameters.soil_moisture_data):
            soil_moisture_file = os.path.join(
                work_dir, input_parameters.soil_moisture_data
            )
        else:
            soil_moisture_file = input_parameters.soil_moisture_data

        try:
            self.soil_moisture_data = SoilMoistureData(
                soil_moisture_file, geometry, input_parameters.monte_carlo_soil_moisture
            )
        except FileValidationError as file_validation_error:
            raise FileValidationError(
                f"Error with soil moisture file {soil_moisture_file}:\n"
                f"{file_validation_error}"
            )

    def _load_predictors(self, input_parameters, geometry, work_dir):
        for (
            predictor_name,
            predictor_information,
        ) in input_parameters.predictors.items():
            if predictor_name in stream_dic:
                if predictor_information is not None:
                    message = (
                        "Invalid input parameters:\n"
                        f"Predictor {predictor_name} is a known stream and information is provided.\n"  # noqa
                        "If you want to use the predictor set information to null.\n"
                        "If you want to use your own data use a different name.\n"
                    )
                    raise FileValidationError(message)
                predictor_source = stream_dic[predictor_name](
                    predictor_name, input_parameters
                )
                predictor_information = predictor_source.information
            else:
                if predictor_information is None:
                    raise FileValidationError(
                        "Invalid input parameters:\n"
                        f"Predictor {predictor_name} is not a known stream and no information is provided.\n"  # noqa
                    )
                predictor_information = PredictorInformationHeader(
                    **predictor_information.model_dump(), predictor_name=predictor_name
                )
                # See if the file_path is a path
                if os.path.dirname(predictor_information.file_path):
                    predictor_file_name = os.path.basename(
                        predictor_information.file_path
                    )
                # or if the file_path is a file
                else:
                    predictor_file_name = predictor_information.file_path
                    predictor_information.file_path = os.path.join(
                        work_dir, predictor_information.file_path
                    )

                predictor_source = predictor_information.file_path

            if predictor_name in self.predictors:
                raise FileValidationError(
                    f"Predictor {predictor_name} is defined multiple times"
                )

            try:
                self.predictors[predictor_name] = PredictorData(
                    predictor_source,
                    predictor_information,
                    geometry,
                )
            except FileValidationError as file_validation_error:
                raise FileValidationError(
                    f"Error with predictor file {predictor_name}:\n"
                    f"{file_validation_error}"
                )
            if predictor_name == "rain":
                raise NotImplementedError("Rainfall data is not supported yet")
                self.rain_time_serie = os.path.join(self.work_dir, predictor_file_name)

    def _check_elevation_keys(self):
        elevation_keys_present = [
            key for key in elevation_keys if key in self.predictors
        ]
        if len(elevation_keys_present) == 0:
            raise FileValidationError("Elevation data is required to compute slope")
        elif len(elevation_keys_present) == 1:
            return elevation_keys_present[0]
        else:
            raise FileValidationError(
                f"Multiple elevation data are available: {', '.join(elevation_keys_present)}\n"  # noqa
                "Only one elevation data is allowed if slope or aspect computation is enabled."  # noqa
            )

    def _check_time_steps(self):
        """Check if all start times are the same for soil moisture and predictors."""
        for time_step in self.soil_moisture_data.time_steps:
            for predictor_name, predictor_data in self.predictors.items():
                if predictor_data.information.constant:
                    continue

                if time_step not in predictor_data.time_steps:
                    logger.error(
                        f"Time steps of predictor {predictor_name}: "
                        + predictor_data.time_steps
                    )
                    raise FileValidationError(
                        f"Time step {time_step} is not present in predictor {predictor_name}"  # noqa
                    )

    def _create_slope(self):
        """Create slope predictor."""
        elevation_key = self._check_elevation_keys()

        if "slope" in self.predictors:
            raise FileValidationError(
                "Both the option to compute slope and the slope predictor are present"
            )

        information = PredictorInformationHeader(
            predictor_name="slope",
            unit="m/m",
            std_deviation=False,
            constant=True,
            nan_value="",
            file_path=None,
        )

        slope = PredictorData(
            None,
            information,
            self.predictors[elevation_key].geometry,
        )
        slope.constant_values_on_nodes = self.compute_slope(
            self.predictors[elevation_key].constant_values_on_nodes
        )

        self.predictors["slope"] = slope

    def compute_slope(self, elevation_on_node):
        """Compute slope from elevation data."""
        if self.elev_dx is None:
            self.elev_dx, self.elev_dy = np.gradient(elevation_on_node)

        return np.sqrt(self.elev_dx * self.elev_dx + self.elev_dy * self.elev_dy)

    def _create_aspect(self):
        """Create aspect predictor."""
        elevation_key = self._check_elevation_keys()

        aspect_in_data = any(
            (k in ["aspect_we", "aspect_ns", "aspect"] for k in self.predictors.keys())
        )
        if aspect_in_data:
            raise FileValidationError(
                "Both the option to compute aspect and the aspect predictor are present"
            )

        elevation_on_node = self.predictors[elevation_key].constant_values_on_nodes

        information = PredictorInformationHeader(
            predictor_name="aspect_we",
            unit="degree",
            std_deviation=False,
            constant=True,
            nan_value="",
            file_path=None,
        )
        aspect_we = PredictorData(
            None,
            information,
            self.predictors[elevation_key].geometry,
        )
        aspect_we.constant_values_on_nodes = self.compute_aspect(
            elevation_on_node, "we"
        )
        self.predictors["aspect_we"] = aspect_we

        information.predictor_name = "aspect_ns"
        aspect_ns = PredictorData(
            None,
            information,
            self.predictors[elevation_key].geometry,
        )
        aspect_ns.constant_values_on_nodes = self.compute_aspect(
            elevation_on_node, "ns"
        )
        self.predictors["aspect_ns"] = aspect_ns

    def compute_aspect(self, elevation_on_node, direction):
        """Compute aspect from elevation data."""
        if self.elev_dx is None:
            self.elev_dx, self.elev_dy = np.gradient(elevation_on_node)

        aspect = np.arctan2(-self.elev_dx, self.elev_dy)

        if direction == "we":
            return 90 - 90 * np.sin(aspect)
        elif direction == "ns":
            return 90 - 90 * np.cos(aspect)
        else:
            raise ValueError("Invalid direction for aspect computation")

    def _past_prediction_as_feature(self, geometry):
        information = PredictorInformationHeader(
            predictor_name="past_prediction",
            unit="g/g",
            std_deviation=False,
            constant=False,
            nan_value="",
            file_path=None,
        )
        past_prediction = PredictorData(
            None,
            information,
            geometry,
        )
        past_prediction.time_steps = self.soil_moisture_data.time_steps
        for time_step in past_prediction.time_steps:
            past_prediction.values_on_nodes[time_step] = np.zeros(
                (geometry.dim_x, geometry.dim_y)
            )
        self.predictors["past_prediction"] = past_prediction

    def all_predictors_constant(self):
        """Check if all predictors are constant over time."""
        for predictor in self.predictors.values():
            if not predictor.information.constant:
                return False
        return True

    def predictors_with_nan(self):
        """Return a list of predictors containing NaN values."""
        predictors_with_nan = set()
        for time_step in self.soil_moisture_data.time_steps:
            for predictor_name, predictor_data in self.predictors.items():
                if np.any(np.isnan(predictor_data.values_on_nodes[time_step])):
                    predictors_with_nan.add(predictor_name)

        return list(predictors_with_nan)

    def get_nan_mask(self, time_step):
        """Get a mask of NaN values in predictors for a given start time."""
        first_predictor = next(iter(self.predictors.values()))
        xaxis = first_predictor.geometry.dim_x
        yaxis = first_predictor.geometry.dim_y

        nan_mask = np.zeros((xaxis, yaxis), dtype=bool)

        for predictor in self.predictors.values():
            values_on_nodes = predictor.values_on_nodes[time_step]

            nan_mask = np.logical_or(nan_mask, np.isnan(values_on_nodes))
        return nan_mask

    def compute_correlation_matrix(self, time_step):
        """
        Compute the correlation matrix between predictors.

        Returns:
        - numpy.ndarray: 2D array representing the correlation matrix.

        This method computes the correlation matrix between predictors and returns it.
        """
        num_predictors = len(self.predictors)

        correlation_matrix = np.zeros((num_predictors, num_predictors))

        for index_a in range(num_predictors):
            for index_b in range(index_a, num_predictors):
                pred_a = list(self.predictors.values())[index_a]
                pred_b = list(self.predictors.values())[index_b]

                values_on_nodes_a = pred_a.values_on_nodes[time_step]
                values_on_nodes_b = pred_b.values_on_nodes[time_step]

                correlation = self._compute_pred_correlation(
                    values_on_nodes_a, values_on_nodes_b
                )

                correlation_matrix[index_a, index_b] = correlation
                correlation_matrix[index_b, index_a] = correlation

        return correlation_matrix

    def _compute_pred_correlation(self, arr1, arr2):
        """
        Compute the correlation coefficient between two 2D arrays.

        Parameters:
        - arr1 (numpy.ndarray): First 2D array.
        - arr2 (numpy.ndarray): Second 2D array.

        Returns:
        - float: Correlation coefficient.

        This method computes the correlation coefficient between two 2D arrays.
        """
        arr1_nonan = np.ma.array(arr1, mask=np.isnan(arr1))
        arr2_nonan = np.ma.array(arr2, mask=np.isnan(arr2))

        arr1_mean = np.mean(arr1_nonan)
        arr2_mean = np.mean(arr2_nonan)

        arr1_norm = arr1_nonan - arr1_mean
        arr2_norm = arr2_nonan - arr2_mean

        arr1_norm_sq_sum = np.sum(arr1_norm * arr1_norm)
        arr2_norm_sq_sum = np.sum(arr2_norm * arr2_norm)

        # Check for zero sums of squares to avoid division by zero
        if arr1_norm_sq_sum == 0 or arr2_norm_sq_sum == 0:
            return float("nan")

        correlation_coeff = np.sum(arr1_norm * arr2_norm) / math.sqrt(
            arr1_norm_sq_sum * arr2_norm_sq_sum
        )

        return correlation_coeff

    def check_rainfall_occurences(self, n_timesteps_reset, time_step):
        """
        Check if rainfall occurred in the previous days.

        Parameters:
        - n_timesteps_reset (int): Number of time steps to check for rainfall.
        - time_step (int): Current time step.
        - rain_time_serie (str): Path to the rainfall time series data.

        Returns:
        - bool: True if rainfall occurred in the previous days, False otherwise.

        This method checks if rainfall occurred in the previous n_timesteps_reset
        days based on the rainfall time series data.
        It returns True if rainfall occurred, otherwise False.
        """
        return False
        raise NotImplementedError("Rainfall data is not supported yet")
        rain_occurs = False
        rain_time_serie = self.predictors["rain"].file_path
        for past_time_step in range(n_timesteps_reset):
            time_step = self.soil_moisture_data.time_steps[time_step - past_time_step]
            time_step_rainfall = self.get_time_step_rainfall(time_step, rain_time_serie)
            if time_step_rainfall > 0:
                rain_occurs = True
                break
        return rain_occurs

    def get_time_step_rainfall(self, time_step, rain_time_serie):
        """
        Get the rainfall value for the given start time.

        Parameters:
        - time_step (str): Time step for which rainfall value is required.
        - rain_time_serie (str): Path to the rainfall time series data.

        Returns:
        - int: Rainfall value for the given start time.

        This method retrieves the rainfall value for the specified start time
        from the rainfall time series data.
        """
        with open(rain_time_serie, "r") as json_file:
            rainfall_values = json.load(json_file)
        time_step_rainfall = rainfall_values[time_step]
        return time_step_rainfall
