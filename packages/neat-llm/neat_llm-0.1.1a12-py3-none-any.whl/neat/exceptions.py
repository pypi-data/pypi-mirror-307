class IncompatibleArgumentsError(Exception):
    """Exception raised when incompatible arguments are provided."""

    pass


class ModelNameError(Exception):
    """Raised when the model name is invalid."""

    pass


class TemperatureRangeError(Exception):
    """Raised when the temperature is outside the valid range."""

    pass


class UnsupportedModelFeaturesError(Exception):
    """Raised when trying to use unsupported features with a specific model."""

    pass


class ModelNotFoundError(Exception):
    pass
