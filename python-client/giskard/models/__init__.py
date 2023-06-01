from importlib import import_module
from typing import Callable, Optional, Iterable, Any

import pandas as pd

from giskard.core.core import ModelType
from giskard.core.validation import configured_validate_arguments


def get_class(_lib, _class):
    return getattr(import_module(_lib), _class)


@configured_validate_arguments
def wrap_model(model,
               model_type: ModelType,
               data_preprocessing_function: Callable[[pd.DataFrame], Any] = None,
               model_postprocessing_function: Callable[[Any], Any] = None,
               name: Optional[str] = None,
               feature_names: Optional[Iterable] = None,
               classification_threshold: float = 0.5,
               classification_labels: Optional[Iterable] = None,
               **kwargs):
    """
    Wraps a trained model of type `model_type` into a Giskard model.

    Args:
        model (Union[BaseEstimator, PreTrainedModel, CatBoost, Module]): The trained model to be wrapped.
        model_type (ModelType): The type of the model to be wrapped.
        data_preprocessing_function (Optional[Callable[[pd.DataFrame], Any]]): A function that processes the input data before feeding it to the model.
        model_postprocessing_function (Optional[Callable[[Any], Any]]): A function that processes the output of the model.
        name (Optional[str]): The name of the model.
        feature_names (Optional[Iterable[str]]): The feature names.
        classification_threshold (float): The threshold used for classification models.
        classification_labels (Optional[Iterable[str]]): The labels used for classification models.
        **kwargs: Additional keyword arguments.

    Returns:
        Union[SKLearnModel, HuggingFaceModel, CatboostModel, PyTorchModel, TensorFlowModel]: The wrapped Giskard model.

    Raises:
        ValueError: If the model library cannot be inferred.
    """
    _libraries = {
        ("giskard.models.huggingface", "HuggingFaceModel"): [("transformers", "PreTrainedModel")],
        ("giskard.models.sklearn", "SKLearnModel"): [("sklearn.base", "BaseEstimator")],
        ("giskard.models.catboost", "CatboostModel"): [("catboost", "CatBoost")],
        ("giskard.models.pytorch", "PyTorchModel"): [("torch.nn", "Module")],
        ("giskard.models.tensorflow", "TensorFlowModel"): [("tensorflow", "Module")]
    }
    for _giskard_class, _base_libs in _libraries.items():
        try:
            giskard_class = get_class(*_giskard_class)
            base_libs = [get_class(*_base_lib) for _base_lib in _base_libs]
            if isinstance(model, tuple(base_libs)):
                origin_library = _base_libs[0][0].split(".")[0]
                giskard_wrapper = _giskard_class[1]
                print("Your '" + origin_library + "' model is successfully wrapped by Giskard's '"
                      + giskard_wrapper + "' wrapper class.")
                return giskard_class(model=model,
                                     model_type=model_type,
                                     data_preprocessing_function=data_preprocessing_function,
                                     model_postprocessing_function=model_postprocessing_function,
                                     name=name,
                                     feature_names=feature_names,
                                     classification_threshold=classification_threshold,
                                     classification_labels=classification_labels,
                                     **kwargs)
        except ImportError:
            pass

    raise ValueError(
        'We could not infer your model library. We currently only support models from:'
        '\n- sklearn'
        '\n- pytorch'
        '\n- tensorflow'
        '\n- huggingface'
    )


@configured_validate_arguments
def model_from_sklearn(model, model_type: ModelType, name: Optional[str] = None,
                       data_preprocessing_function: Callable[[pd.DataFrame], Any] = None,
                       model_postprocessing_function: Callable[[Any], Any] = None,
                       feature_names: Optional[Iterable] = None, classification_threshold: float = 0.5,
                       classification_labels: Optional[Iterable] = None):
    """
    Factory method that creates an instance of the `SKLearnModel` class.

    Parameters:
        model: Any
            The trained scikit-learn model object to wrap.
        model_type: ModelType
            The type of the model, either `ModelType.CLASSIFICATION` or `ModelType.REGRESSION`.
        name: Optional[str], default=None
            The name of the model.
        data_preprocessing_function: Optional[Callable[[pd.DataFrame], Any]], default=None
            A function that preprocesses the input data before it is fed to the model.
        model_postprocessing_function: Optional[Callable[[Any], Any]], default=None
            A function that post-processes the model's output.
        feature_names: Optional[Iterable], default=None
            A list of feature names.
        classification_threshold: float, default=0.5
            The threshold value used for classification models.
        classification_labels: Optional[Iterable], default=None
            A list of classification labels.

    Returns:
        SKLearnModel
            An instance of the `SKLearnModel` class.
    """
    from giskard import SKLearnModel
    return SKLearnModel(model,
                        model_type,
                        name,
                        data_preprocessing_function,
                        model_postprocessing_function,
                        feature_names,
                        classification_threshold,
                        classification_labels)


@configured_validate_arguments
def model_from_catboost(model, model_type: ModelType, name: Optional[str] = None,
                        data_preprocessing_function: Callable[[pd.DataFrame], Any] = None,
                        model_postprocessing_function: Callable[[Any], Any] = None,
                        feature_names: Optional[Iterable] = None, classification_threshold: float = 0.5,
                        classification_labels: Optional[Iterable] = None):
    """
    Factory method that creates an instance of the `CatboostModel` class.

    Args:
        model (Any): The trained Catboost model object to wrap.
        model_type (ModelType): The type of the model, either `ModelType.CLASSIFICATION` or `ModelType.REGRESSION`.
        name (Optional[str], optional): The name of the model. Defaults to None.
        data_preprocessing_function (Optional[Callable[[pd.DataFrame], Any]], optional):
            A function that preprocesses the input data before it is fed to the model. Defaults to None.
        model_postprocessing_function (Optional[Callable[[Any], Any]], optional):
            A function that post-processes the model's output. Defaults to None.
        feature_names (Optional[Iterable], optional):
            A list of feature names. Defaults to None.
        classification_threshold (float, optional):
            The threshold value used for classification models. Defaults to 0.5.
        classification_labels (Optional[Iterable], optional):
            A list of classification labels. Defaults to None.

    Returns:
        CatboostModel: An instance of the `CatboostModel` class.
    """
    from giskard import CatboostModel
    return CatboostModel(model,
                         model_type,
                         name,
                         data_preprocessing_function,
                         model_postprocessing_function,
                         feature_names,
                         classification_threshold,
                         classification_labels)


@configured_validate_arguments
def model_from_pytorch(model, model_type: ModelType, torch_dtype=None, device: Optional[str] = "cpu",
                       name: Optional[str] = None,
                       data_preprocessing_function: Callable[[pd.DataFrame], Any] = None,
                       model_postprocessing_function: Callable[[Any], Any] = None,
                       feature_names: Optional[Iterable] = None, classification_threshold: float = 0.5,
                       classification_labels: Optional[Iterable] = None, iterate_dataset=True):
    """
    Factory method that creates an instance of the `PyTorchModel` class.

    Args:
        model (Any): The trained PyTorch model object to wrap.
        model_type (ModelType): The type of the model, either `ModelType.CLASSIFICATION` or `ModelType.REGRESSION`.
        torch_dtype (Optional[torch.dtype], optional): The data type of the input tensors. Defaults to torch.float32.
        device (Optional[str], optional): The device to run the model on, either "cpu" or "cuda". Defaults to "cpu".
        name (Optional[str], optional): The name of the model. Defaults to None.
        data_preprocessing_function (Optional[Callable[[pd.DataFrame], Any]], optional):
            A function that preprocesses the input data before it is fed to the model. Defaults to None.
        model_postprocessing_function (Optional[Callable[[Any], Any]], optional):
            A function that post-processes the model's output. Defaults to None.
        feature_names (Optional[Iterable], optional):
            A list of feature names. Defaults to None.
        classification_threshold (float, optional):
            The threshold value used for classification models. Defaults to 0.5.
        classification_labels (Optional[Iterable], optional):
            A list of classification labels. Defaults to None.
        iterate_dataset (bool, optional): Whether to iterate over the dataset or feed it to the model at once.
            Defaults to True.

    Returns:
        PyTorchModel: An instance of the `PyTorchModel` class.
    """
    from giskard import PyTorchModel
    try:
        import torch
    except ImportError as e:
        raise ImportError("Please install it via 'pip install torch'") from e

    torch_dtype = torch.float32 if not torch_dtype else torch_dtype
    return PyTorchModel(model,
                        model_type,
                        torch_dtype,
                        device,
                        name,
                        data_preprocessing_function,
                        model_postprocessing_function,
                        feature_names,
                        classification_threshold,
                        classification_labels,
                        iterate_dataset)


@configured_validate_arguments
def model_from_tensorflow(model, model_type: ModelType, name: Optional[str] = None,
                          data_preprocessing_function: Callable[[pd.DataFrame], Any] = None,
                          model_postprocessing_function: Callable[[Any], Any] = None,
                          feature_names: Optional[Iterable] = None, classification_threshold: float = 0.5,
                          classification_labels: Optional[Iterable] = None):
    """
    Factory method that creates an instance of the `TensorFlowModel` class.

    Args:
        model (Any): The trained TensorFlow model object to wrap.
        model_type (ModelType): The type of the model, either `ModelType.CLASSIFICATION` or `ModelType.REGRESSION`.
        name (Optional[str], optional): The name of the model. Defaults to None.
        data_preprocessing_function (Optional[Callable[[pd.DataFrame], Any]], optional):
            A function that preprocesses the input data before it is fed to the model. Defaults to None.
        model_postprocessing_function (Optional[Callable[[Any], Any]], optional):
            A function that post-processes the model's output. Defaults to None.
        feature_names (Optional[Iterable], optional):
            A list of feature names. Defaults to None.
        classification_threshold (float, optional):
            The threshold value used for classification models. Defaults to 0.5.
        classification_labels (Optional[Iterable], optional):
            A list of classification labels. Defaults to None.

    Returns:
        TensorFlowModel: An instance of the `TensorFlowModel` class.
    """
    from giskard import TensorFlowModel
    return TensorFlowModel(model,
                           model_type,
                           name,
                           data_preprocessing_function,
                           model_postprocessing_function,
                           feature_names,
                           classification_threshold,
                           classification_labels)


@configured_validate_arguments
def model_from_huggingface(model, model_type: ModelType, name: Optional[str] = None,
                           data_preprocessing_function: Callable[[pd.DataFrame], Any] = None,
                           model_postprocessing_function: Callable[[Any], Any] = None,
                           feature_names: Optional[Iterable] = None, classification_threshold: float = 0.5,
                           classification_labels: Optional[Iterable] = None):
    """
    Factory method that creates an instance of the `HuggingFaceModel` class.

    Args:
        model (Any): The trained Hugging Face model object to wrap.
        model_type (ModelType): The type of the model, either `ModelType.CLASSIFICATION` or `ModelType.REGRESSION`.
        name (Optional[str], optional): The name of the model. Defaults to None.
        data_preprocessing_function (Optional[Callable[[pd.DataFrame], Any]], optional):
            A function that preprocesses the input data before it is fed to the model. Defaults to None.
        model_postprocessing_function (Optional[Callable[[Any], Any]], optional):
            A function that post-processes the model's output. Defaults to None.
        feature_names (Optional[Iterable], optional):
            A list of feature names. Defaults to None.
        classification_threshold (float, optional):
            The threshold value used for classification models. Defaults to 0.5.
        classification_labels (Optional[Iterable], optional):
            A list of classification labels. Defaults to None.

    Returns:
        HuggingFaceModel: An instance of the `HuggingFaceModel` class.
    """
    from giskard import HuggingFaceModel
    return HuggingFaceModel(model,
                            model_type,
                            name,
                            data_preprocessing_function,
                            model_postprocessing_function,
                            feature_names,
                            classification_threshold,
                            classification_labels)
