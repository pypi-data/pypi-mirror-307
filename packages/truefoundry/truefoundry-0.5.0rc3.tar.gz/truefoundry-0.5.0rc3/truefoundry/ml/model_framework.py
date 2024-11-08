import warnings
from typing import Literal, Optional, Union, get_args

from truefoundry.ml import ModelFramework
from truefoundry.ml.autogen.entities import artifacts as autogen_artifacts
from truefoundry.pydantic_v1 import BaseModel, Field


class FastAIFramework(autogen_artifacts.FastAIFramework):
    """FastAI model Framework"""

    type: Literal["fastai"] = "fastai"


class GluonFramework(autogen_artifacts.GluonFramework):
    """Gluon model Framework"""

    type: Literal["gluon"] = "gluon"


class H2OFramework(autogen_artifacts.H2OFramework):
    """H2O model Framework"""

    type: Literal["h2o"] = "h2o"


class KerasFramework(autogen_artifacts.KerasFramework):
    """Keras model Framework"""

    type: Literal["keras"] = "keras"


class LightGBMFramework(autogen_artifacts.LightGBMFramework):
    """LightGBM model Framework"""

    type: Literal["lightgbm"] = "lightgbm"


class ONNXFramework(autogen_artifacts.ONNXFramework):
    """ONNX model Framework"""

    type: Literal["onnx"] = "onnx"


class PaddleFramework(autogen_artifacts.PaddleFramework):
    """Paddle model Framework"""

    type: Literal["paddle"] = "paddle"


class PyTorchFramework(autogen_artifacts.PyTorchFramework):
    """PyTorch model Framework"""

    type: Literal["pytorch"] = "pytorch"


class SklearnFramework(autogen_artifacts.SklearnFramework):
    """Sklearn model Framework"""

    type: Literal["sklearn"] = "sklearn"


class SpaCyFramework(autogen_artifacts.SpaCyFramework):
    """SpaCy model Framework"""

    type: Literal["spacy"] = "spacy"


class StatsModelsFramework(autogen_artifacts.StatsModelsFramework):
    """StatsModels model Framework"""

    type: Literal["statsmodels"] = "statsmodels"


class TensorFlowFramework(autogen_artifacts.TensorFlowFramework):
    """TensorFlow model Framework"""

    type: Literal["tensorflow"] = "tensorflow"


class TransformersFramework(autogen_artifacts.TransformersFramework):
    """Transformers model Framework"""

    type: Literal["transformers"] = "transformers"


class XGBoostFramework(autogen_artifacts.XGBoostFramework):
    """XGBoost model Framework"""

    type: Literal["xgboost"] = "xgboost"


# Union of all the model frameworks


ModelFrameworkType = Union[
    FastAIFramework,
    GluonFramework,
    H2OFramework,
    KerasFramework,
    LightGBMFramework,
    ONNXFramework,
    PaddleFramework,
    PyTorchFramework,
    SklearnFramework,
    SpaCyFramework,
    StatsModelsFramework,
    TensorFlowFramework,
    TransformersFramework,
    XGBoostFramework,
]


class _ModelFramework(BaseModel):
    __root__: ModelFrameworkType = Field(discriminator="type")

    @classmethod
    def to_model_framework_type(
        cls,
        framework: Optional[Union[str, ModelFramework, "ModelFrameworkType"]] = None,
    ) -> Optional["ModelFrameworkType"]:
        """
        Converts a ModelFramework or string representation to a ModelFrameworkType object.

        Args:
            framework (Optional[Union[str, ModelFramework, ModelFrameworkType]]): ModelFrameworkType or equivalent input.
                Supported frameworks can be found in `truefoundry.ml.enums.ModelFramework`.
                May be `None` if the framework is unknown or unsupported.
                **Deprecated**: Prefer passing a `ModelFrameworkType` instance.

        Returns:
            ModelFrameworkType corresponding to the input, or None if the input is None.
        """
        if framework is None:
            return None

        # Issue a deprecation warning for str and ModelFramework types
        if isinstance(framework, (str, ModelFramework)):
            warnings.warn(
                "Passing a string or ModelFramework Enum is deprecated. Please use a ModelFrameworkType object.",
                DeprecationWarning,
                stacklevel=2,
            )

        # Convert string to ModelFramework
        if isinstance(framework, str):
            framework = ModelFramework(framework)

        # Convert ModelFramework to ModelFrameworkType
        if isinstance(framework, ModelFramework):
            if framework == ModelFramework.UNKNOWN:
                return None
            return cls.parse_obj({"type": framework.value}).__root__

        # Directly return if already a ModelFrameworkType
        if isinstance(framework, get_args(ModelFrameworkType)):
            return framework

        raise ValueError(
            "framework must be a string, ModelFramework enum, or ModelFrameworkType object"
        )

    @classmethod
    def from_dict(cls, obj: dict) -> ModelFrameworkType:
        """Create an instance of ModelFramework from a dict"""
        if obj is None:
            return None

        return cls.parse_obj(obj).__root__
