"""Module for the main class for the module."""

import logging
import os
import random
from collections import OrderedDict

import numpy as np
from scipy.stats import halfnorm, norm, qmc
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

from soil_moisture_prediction.area_geometry import RectGeom
from soil_moisture_prediction.input_data import InputData
from soil_moisture_prediction.input_file_parser import FileValidationError
from soil_moisture_prediction.plot_functions import plot_selection
from soil_moisture_prediction.pydantic_models import InputParameters

# TODO define private and public attribues and methods

logger = logging.getLogger(__name__)

RANDOM_SEED = 46
random.seed(RANDOM_SEED)

NUMBER_TIMESTEPS_FOR_AVERAGE = 3


class RFoModel(object):
    """Class to store the output of the Random Forest regression.

    Support deterministic and probabilistic (Monte Carlo) predictions
    """

    N_TREES: int = 40
    TREE_DEPTH: int = 8

    parameters: InputParameters
    work_dir: str
    random_forest_models: [RandomForestRegressor]
    RF_prediction: np.ndarray
    predictor_importance: np.ndarray
    MC_mean: np.ndarray
    dispersion_coefficient: np.ndarray

    def __init__(
        self,
        *,
        input_parameters,
        work_dir,
        load_results=False,
    ):
        """Construct."""
        logger.info("Create model")
        self.work_dir = work_dir
        self.parameters = input_parameters

        self.geometry = RectGeom(input_parameters.geometry)
        self.input_data = InputData(
            self.parameters,
            self.geometry,
            self.work_dir,
        )

        # TODO add to pydantic
        if (
            not self.parameters.monte_carlo_predictors
            and self.parameters.predictor_qmc_sampling
        ):
            logging.warning(
                "Quasi-Monte Carlo sampling is only available for Monte Carlo predictor"
            )

        if not (
            self.parameters.monte_carlo_soil_moisture
            or self.parameters.monte_carlo_predictors
        ):
            self.parameters.monte_carlo_iterations = 1

        if load_results:
            self._load_predictions()
        else:
            self._initiate_result_arrays()

        # Already plot figures which are only based on the input data
        plot_selection(self, plot_results=False)

    def _load_predictions(self):
        """
        Load prediction results and RF feature importance from files.

        If Monte Carlo is switched on, the mean and coefficient of dispersion
        are also loaded.
        """
        logger.info("Loading prediction results from files...")
        self.RF_prediction = np.load(os.path.join(self.work_dir, "RF_predictions.npy"))
        self.predictor_importance = np.load(
            os.path.join(self.work_dir, "RF_feat_importance.npy")
        )
        if (
            self.parameters.monte_carlo_soil_moisture
            or self.parameters.monte_carlo_predictors
        ):
            self.MC_mean = np.load(os.path.join(self.work_dir, "MC_mean.npy"))
            self.dispersion_coefficient = np.load(
                os.path.join(self.work_dir, "MC_coefficient_dispersion.npy")
            )

    def _initiate_result_arrays(self):
        """Initiate the arrays to store the results."""
        logger.info("Initiating result arrays")
        self.random_forest_models = []
        self.RF_prediction = np.empty(
            (
                self.parameters.monte_carlo_iterations,
                len(self.input_data.soil_moisture_data.time_steps),
                self.geometry.dim_x,
                self.geometry.dim_y,
            )
        )

        if (
            self.parameters.monte_carlo_soil_moisture
            or self.parameters.monte_carlo_predictors
        ):
            shape = (
                len(self.input_data.soil_moisture_data.time_steps),
                self.geometry.dim_x,
                self.geometry.dim_y,
            )
            (
                self.MC_mean,
                self.dispersion_coefficient,
            ) = [np.empty(shape) for _ in range(2)]

        self.predictor_importance = np.zeros(
            (
                self.parameters.monte_carlo_iterations,
                len(self.input_data.soil_moisture_data.time_steps),
                len(self.input_data.predictors),
            )
        )

    def complete_prediction(self):
        """Build model and make predictions."""
        logger.info("Building model and making predictions.")

        if self.parameters.average_measurements_over_time:
            logger.info("Averaging soil moisture measurements over the previous days.")
            self.average_measurements()

        for time_index, time_step in enumerate(
            self.input_data.soil_moisture_data.time_steps
        ):
            if time_index > 0 and self.parameters.past_prediction_as_feature:
                self._add_prediction_to_feature(time_step, time_index)
            self.train_random_forest_models(time_step)
            self.apply_random_forest_models(time_index, time_step)
            if (
                self.parameters.monte_carlo_soil_moisture
                or self.parameters.monte_carlo_predictors
            ):
                self.compute_mc_stats(time_step, time_index)

        if self.parameters.save_results:
            self.save_predictions()

        plot_selection(self, plot_input=False)

    def average_measurements(self):
        """Average soil moisture measurements over the previous days."""
        if (
            len(self.input_data.soil_moisture_data.time_steps)
            < NUMBER_TIMESTEPS_FOR_AVERAGE
        ):
            logging.warning(
                "Will not apply average over time intervals. Not enough intervals!"
            )
            return
        soil_moisture_averaged = self.input_data.soil_moisture_data.soil_moisture
        for time_index, time_step in enumerate(
            self.input_data.soil_moisture_data.time_steps
        ):
            if time_index > NUMBER_TIMESTEPS_FOR_AVERAGE:
                number_timesteps_rainfall_reset = NUMBER_TIMESTEPS_FOR_AVERAGE
                rain_occurs = self.input_data.check_rainfall_occurences(
                    number_timesteps_rainfall_reset,
                    time_index,
                )
                if not rain_occurs:
                    for past_time_index in range(1, NUMBER_TIMESTEPS_FOR_AVERAGE + 1):
                        past_time_step = self.input_data.soil_moisture_data.time_steps[
                            time_index - past_time_index
                        ]
                        soil_moisture_averaged[
                            time_step
                        ] += self.input_data.soil_moisture_data.soil_moisture[
                            past_time_step
                        ]
                    soil_moisture_averaged[time_step] /= (
                        NUMBER_TIMESTEPS_FOR_AVERAGE + 1
                    )
        self.input_data.soil_moisture_data.soil_moisture = soil_moisture_averaged

    def _add_prediction_to_feature(self, time_step, time_index):
        """Add the previous day's prediction to the features."""
        number_timesteps_rainfall_reset = 1

        rain_occurs = self.input_data.check_rainfall_occurences(
            number_timesteps_rainfall_reset,
            time_index,
        )

        past_prediction = self.input_data.predictors["past_prediction"]

        if not rain_occurs:
            past_prediction.values_on_nodes[time_step] = self.RF_prediction[
                0, time_index - 1, :, :
            ]
        else:
            past_prediction.values_on_nodes[time_step] = np.zeros(
                (self.geometry.dim_x, self.geometry.dim_y),
            )

    def train_random_forest_models(self, time_step):
        """Train the random forest models.

        Iterates over measurements and iterations for Monte Carlo sampling.
        Trains random forest models for each iteration.

        Parameters:
        - time_step (str): Time step for training.
        """
        logger.info(f"[{time_step}] Training Random Forest models...")

        number_measurements = len(
            self.input_data.soil_moisture_data.soil_moisture[time_step]
        )

        for iteration in range(self.parameters.monte_carlo_iterations):
            soil_moisture_labels = self.input_data.soil_moisture_data.soil_moisture[
                time_step
            ]

            if self.parameters.monte_carlo_soil_moisture:
                for measurement in range(number_measurements):
                    soil_moisture_labels[measurement] = (
                        self.compute_uncertain_soil_moisture(
                            measurement, iteration, time_step
                        )
                    )

            predictor_features = self._collect_predictors_training(iteration, time_step)

            self.random_forest_models.append(
                self.train_random_forest(
                    predictor_features,
                    soil_moisture_labels,
                    time_step,
                )
            )

    def _collect_predictors_training(self, iteration, time_step):
        """Collect predictors at training locations."""
        number_measurements = len(
            self.input_data.soil_moisture_data.soil_moisture[time_step]
        )
        number_predictors = len(self.input_data.predictors)
        training_coordinates = self.input_data.soil_moisture_data.training_coordinates[
            time_step
        ]

        training_predictors = np.empty((number_measurements, number_predictors))
        if self.parameters.monte_carlo_predictors:
            if self.parameters.predictor_qmc_sampling:
                noisy_predictors = self._sample_multivariate_normal_qmc(
                    time_step, iteration
                )
            else:
                noisy_predictors = self._sample_from_normal_distribution(
                    time_step, iteration
                )

        for coord_index, coord in enumerate(training_coordinates):
            if self.parameters.monte_carlo_predictors:
                predictor_values = self._collect_noisy_values(noisy_predictors, coord)
            else:
                predictor_values = self._collect_predictor_values(time_step, coord)
            training_predictors[coord_index] = predictor_values

        return training_predictors

    def _sample_from_normal_distribution(self, time_step, rdm_seed):
        """Compute noisy predictors at measurement locations.

        Returns np array with values of noisy predictors at measurement locations.

        For the derivative predictors (slope and aspect), the elevation data is
        sampled from the distribution to compute the derivative predictors.

        Parameters:
        - time_step (str): Time step for computation.
        - rdm_seed (int): Random seed for reproducibility.
        """
        noisy_predictors = OrderedDict()
        for predictor_name, predictor_data in self.input_data.predictors.items():
            # Derivative predictors
            # InputData.predictors is an ordered dict, derivative predictors should
            # occure after precursor predictors
            if predictor_name == "slope" and self.parameters.compute_slope:
                noisy_values_on_nodes = self.input_data.compute_slope(
                    noisy_predictors["elevation"]
                )
            elif (
                predictor_name in ["aspect_we", "aspect_ns"]
                and self.parameters.compute_aspect
            ):
                noisy_values_on_nodes = self.input_data.compute_aspect(
                    noisy_predictors["elevation"], direction=predictor_name[-2:]
                )
            elif predictor_name == "past_prediction":
                time_index = self.input_data.soil_moisture_data.time_steps.index(
                    time_step
                )
                noisy_predictors["past_prediction"] = self.RF_prediction[
                    0, time_index - 1, :, :
                ]
            elif not predictor_data.information.std_deviation:
                noisy_values_on_nodes = predictor_data.values_on_nodes[time_step]
            else:
                noisy_values_on_nodes = self._sample_from_predictor(
                    predictor_name, time_step, rdm_seed
                )

            noisy_predictors[predictor_name] = noisy_values_on_nodes

        return noisy_predictors

    def _sample_multivariate_normal_qmc(self, time_step, rdm_seed):
        """Sample from a Multivariate Normal distribution using Quasi-Monte Carlo (QMC).

        This method generates samples from a Multivariate Normal distribution using
        Quasi-Monte Carlo (QMC) sampling technique. It constructs the covariance
        matrix based on the standard deviations of predictors and their correlations.
        The QMC sampling aims to improve the efficiency of sampling in high-dimensional
        spaces compared to traditional Monte Carlo methods.
        """
        noisy_predictors = OrderedDict()
        for pred_name, pred_data in self.input_data.predictors.items():
            noisy_predictors[pred_name] = pred_data.values_on_nodes[time_step]

        for x in range(self.geometry.dim_x):
            for y in range(self.geometry.dim_y):
                mean = []
                covariance = []
                for pred_name, pred_data in self.input_data.predictors.items():
                    if pred_data.std_deviation_on_nodes is not None:
                        mean.append(pred_data.values_on_nodes[time_step][x][y])
                        covariance.append(
                            pred_data.std_deviation_on_nodes[time_step][x][y] ** 2
                        )
                covariance_diag = np.diag(covariance)
                seed = rdm_seed * 1000000 + x * 1000 + y
                distribution = qmc.MultivariateNormalQMC(
                    mean=mean, cov=covariance_diag, seed=seed
                )

                random_sample = distribution.random(1)
                for pred_i, pred_name in enumerate(self.input_data.predictors.keys()):
                    if pred_data.std_deviation_on_nodes is None:
                        continue
                    noisy_predictors[pred_name][x, y] = random_sample[0, pred_i]

        # Derivative predictors
        if "slope" in self.input_data.predictors and self.parameters.compute_slope:
            noisy_predictors["slope"] = self.input_data.compute_slope(
                noisy_predictors["elevation"]
            )
        if "aspect_we" in self.input_data.predictors and self.parameters.compute_aspect:
            noisy_predictors["aspect_we"] = self.input_data.compute_aspect(
                noisy_predictors["elevation"], direction="we"
            )
            noisy_predictors["aspect_ns"] = self.input_data.compute_aspect(
                noisy_predictors["elevation"], direction="ns"
            )

        for pred_name, pred_data in self.input_data.predictors.items():
            if pred_name not in noisy_predictors:
                noisy_predictors[pred_name] = pred_data.values_on_nodes[time_step]

        if self.parameters.past_prediction_as_feature:
            time_index = self.input_data.soil_moisture_data.time_steps.index(time_step)
            noisy_predictors["past_prediction"] = self.RF_prediction[
                0, time_index - 1, :, :
            ]

        return noisy_predictors

    def _collect_noisy_values(self, noisy_predictors, coordinates):
        """
        Collect noisy predictor values at the given coordinates.

        Parameters:
        - noisy_predictors (dict): Dictionary of noisy predictor values.
        - coordinates (np.ndarray): Array of coordinates to collect predictor values.

        Returns:
        - list: List of noisy predictor values at the given coordinates.
        """
        predictor_values = []
        for predictor_name, predictor_data in noisy_predictors.items():
            predictor_value = predictor_data[coordinates[0], coordinates[1]]
            if np.isnan(predictor_value) and not self.parameters.allow_nan_in_training:
                message = (
                    "Nan in training data!\n"
                    f"Noisy predictor {predictor_name} has NaN value at coordinates {coordinates}.\n"  # noqa
                    "The values of the predictor were generated from a distribution.\n"
                    "You can see the plotted data with: Parameters['what_to_plot']['plot_predictors'].\n"  # noqa
                    "To allow NaN values in training data, set Parameters['allow_nan_in_training'] to True."  # noqa
                )
                raise FileValidationError(message)
            predictor_values.append(predictor_value)

        return predictor_values

    def _collect_predictor_values(self, time_step, coordinates):
        """
        Collect predictor values at the given coordinates and start time.

        Parameters:
        - time_step (str): Time step for collecting predictor values.
        - coordinates (np.ndarray): Array of coordinates to collect predictor values.

        Returns:
        - list: List of predictor values at the given coordinates.
        """
        predictor_values = []
        for predictor_name, predictor_data in self.input_data.predictors.items():
            predictor_value = predictor_data.values_on_nodes[time_step][
                coordinates[0], coordinates[1]
            ]

            if np.isnan(predictor_value) and not self.parameters.allow_nan_in_training:
                message = (
                    "Nan in training data!\n"
                    f"Predictor {predictor_name} has NaN value at coordinates {coordinates}.\n"  # noqa
                    "You can see the plotted data with: Parameters['what_to_plot']['plot_predictors'].\n"  # noqa
                    "To allow NaN values in training data, set Parameters['allow_nan_in_training'] to True."  # noqa
                )
                raise FileValidationError(message)
            predictor_values.append(predictor_value)

        return predictor_values

    def compute_uncertain_soil_moisture(self, measurement, iteration, time_step):
        """
        Compute the uncertain soil moisture for the Monte Carlo simulation.

        Parameters:
        - measurement (int): Index of the soil moisture measurement.
        - iteration (int): Index of the Monte Carlo iteration.
        - time_step (str): Time step of the soil moisture data.

        Returns:
        - float: Uncertain soil moisture value.
        """
        soil_moisture = self.input_data.soil_moisture_data.soil_moisture[time_step][
            measurement
        ]
        soil_moisture_dev_low = (
            self.input_data.soil_moisture_data.soil_moisture_dev_low[time_step][
                measurement
            ]
        )
        soil_moisture_dev_high = (
            self.input_data.soil_moisture_data.soil_moisture_dev_high[time_step][
                measurement
            ]
        )
        lower_uncertainty = 2 * soil_moisture - float(
            halfnorm.rvs(
                soil_moisture,
                soil_moisture_dev_low,
                1,
                random_state=measurement * 100 + iteration,
            )[0]
        )
        upper_uncertainty = float(
            halfnorm.rvs(
                soil_moisture,
                soil_moisture_dev_high,
                1,
                random_state=measurement * 100 + iteration,
            )[0]
        )

        # TODO This random variable is not effected by the seed. So it is not
        # deterministic.
        random_binary = random.randint(0, 1)
        soil_moisture_uncertain = (
            random_binary * lower_uncertainty + (1 - random_binary) * upper_uncertainty
        )
        return soil_moisture_uncertain

    def _sample_from_predictor(self, predictor_name, time_step, rdm_seed):
        """Sample from a distribution to add noise to predictor data.

        Generates noisy predictor data by sampling from a normal distribution
        with mean `predictor` and standard deviation obtained from the input data
        for the given predictor `pred_name`. The noise is added to each grid point
        defined by the geometry.

        Parameters:
        - predictor (float): Mean value of the predictor.
        - pred_name (str): Name of the predictor.
        - rdm_seed (int): Random seed for reproducibility.

        Returns:
        - numpy.ndarray: Noisy predictor data sampled from the distribution.
        """
        mean = self.input_data.predictors[predictor_name].values_on_nodes[time_step]
        std_dev = self.input_data.predictors[predictor_name].std_deviation_on_nodes[
            time_step
        ]

        noisy_predictor = norm.rvs(
            mean,
            std_dev,
            size=self.geometry.grid_x.shape,
            random_state=rdm_seed,
        )
        return noisy_predictor

    def train_random_forest(self, features, labels, time_step):
        """Build and train a random forest regressor.

        Parameters:
        - features : array-like, shape = [n_samples, n_features]
            Training input samples.
        - labels : array-like, shape = [n_samples]
            Target values (Real soil moisture).
        - time_step : str
            Time step of the soil moisture data.

        Returns:
        - RandomForestRegressor: Trained random forest regressor.
        """
        # TODO random_state hard coded
        train_features, test_features, train_labels, test_labels = train_test_split(
            features, labels, test_size=0.3, random_state=40
        )
        train_labels = np.ravel(train_labels)
        test_labels = np.ravel(test_labels)

        random_forest = RandomForestRegressor(
            n_estimators=self.N_TREES,
            max_depth=self.TREE_DEPTH,
            random_state=RANDOM_SEED,
        )
        random_forest.fit(train_features, train_labels)

        predictions = random_forest.predict(test_features)
        r2 = r2_score(test_labels, predictions)
        logger.info(f"[{time_step}] Random Forest R2: {round(r2, 3)}")
        rf_res = predictions - test_labels
        errors = abs(rf_res) ** 2
        mean_absolute_error = round(np.mean(errors), 6)
        logger.info(
            f"[{time_step}] Random Forest Mean Absolute Error: {mean_absolute_error} "
            f"with prediction mean value: {round(np.mean(predictions), 2)}"
        )

        return random_forest

    def apply_random_forest_models(self, time_index, time_step):
        """Apply the random forest on the full area and compute feature importance."""
        logger.info(f"[{time_step}] Applying Random Forest model")

        for monte_carlo_iteration in range(self.parameters.monte_carlo_iterations):
            for line in range(self.geometry.dim_x):
                predictors = np.array(
                    [
                        predictor.get_values_by_line(time_step, line)
                        for predictor in self.input_data.predictors.values()
                    ]
                ).T
                self.RF_prediction[monte_carlo_iteration, time_index, line, :] = (
                    self.random_forest_models[monte_carlo_iteration].predict(predictors)
                )

            self.predictor_importance[monte_carlo_iteration, time_index] = (
                self.random_forest_models[monte_carlo_iteration].feature_importances_
            )

    def compute_mc_stats(self, time_step, time_index):
        """Compute mean and percentiles of the prediction for a given day.

        The function computes the 5th, 25th, 75th and 95th percentiles.
        """
        logger.info(f"[{time_step}] Computing Monte Carlo statistics.")
        p25 = self.dispersion_coefficient
        p75 = self.dispersion_coefficient

        self.MC_mean[time_index, :, :] = np.mean(
            self.RF_prediction[:, time_index, :, :], axis=0
        )

        (
            p25[time_index, :, :],
            p75[time_index, :, :],
        ) = [
            np.percentile(self.RF_prediction[:, time_index, :, :], q=perc, axis=0)
            for perc in [25, 75]
        ]
        self.dispersion_coefficient[time_index, :, :] = (
            p75[time_index, :, :] - p25[time_index, :, :]
        ) / (p75[time_index, :, :] + p25[time_index, :, :])

    def save_predictions(self):
        """
        Save the prediction results and RF feature importance to files.

        If Monte Carlo is switched on, the mean and coefficient of dispersion
        are also saved.
        """
        logger.info("Saving predictions to files...")
        np.save(os.path.join(self.work_dir, "RF_predictions"), self.RF_prediction)
        np.save(
            os.path.join(self.work_dir, "RF_feat_importance"),
            self.predictor_importance,
        )
        if (
            self.parameters.monte_carlo_soil_moisture
            or self.parameters.monte_carlo_predictors
        ):
            np.save(os.path.join(self.work_dir, "MC_mean"), self.MC_mean)
            np.save(
                os.path.join(self.work_dir, "MC_coefficient_dispersion"),
                self.dispersion_coefficient,
            )
