import copy
import datetime
import json
import logging
import os.path
import tempfile
import uuid
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Sequence, Tuple, Union

from truefoundry.ml.artifact.truefoundry_artifact_repo import (
    ArtifactIdentifier,
    MlFoundryArtifactsRepository,
)
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ArtifactType,
    ArtifactVersionSerializationFormat,
    CreateArtifactVersionRequestDto,
    DeleteArtifactVersionsRequestDto,
    ExternalModelSource,
    FinalizeArtifactVersionRequestDto,
    Framework,
    MlfoundryArtifactsApi,
    ModelDto,
    ModelVersionDto,
    ModelVersionManifest,
    NotifyArtifactVersionFailureDto,
    TruefoundryModelSource,
    UpdateModelVersionRequestDto,
)
from truefoundry.ml.autogen.client import (
    Source as ModelVersionSource,
)
from truefoundry.ml.enums import ModelFramework
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.log_types.artifacts.constants import (
    INTERNAL_METADATA_PATH,
)
from truefoundry.ml.log_types.artifacts.utils import (
    _copy_additional_files,
    _get_src_dest_pairs,
    _validate_artifact_metadata,
    _validate_description,
    calculate_total_size,
)
from truefoundry.ml.model_framework import ModelFrameworkType, _ModelFramework
from truefoundry.ml.session import _get_api_client
from truefoundry.pydantic_v1 import BaseModel, Extra, StrictStr

if TYPE_CHECKING:
    from truefoundry.ml.mlfoundry_run import MlFoundryRun


logger = logging.getLogger(__name__)


# TODO: Support async download and upload
class ModelVersionInternalMetadata(BaseModel):
    class Config:
        extra = Extra.allow

    files_dir: str  # relative to root
    model_dir: str  # relative to `files_dir`
    model_is_null: bool = False
    framework: ModelFramework = ModelFramework.UNKNOWN
    transformers_pipeline_task: Optional[str] = None
    model_filename: Optional[str] = None
    mlfoundry_version: Optional[str] = None
    truefoundry_version: Optional[str] = None

    def dict(self, *args, **kwargs):
        dct = super().dict(*args, **kwargs)
        dct["framework"] = dct["framework"].value
        return dct


class BlobStorageModelDirectory(BaseModel):
    uri: StrictStr


class ModelVersionDownloadInfo(BaseModel):
    download_dir: str
    model_dir: str
    model_framework: ModelFramework = ModelFramework.UNKNOWN
    model_filename: Optional[str] = None


class ModelVersion:
    def __init__(
        self,
        model_version: ModelVersionDto,
        model: ModelDto,
    ) -> None:
        self._api_client = _get_api_client()
        self._mlfoundry_artifacts_api = MlfoundryArtifactsApi(
            api_client=self._api_client
        )
        self._model_version = model_version
        self._model = model
        self._deleted = False
        self._description: str = ""
        self._metadata: Dict[str, Any] = {}
        self._framework: Optional["Framework"] = None
        self._set_mutable_attrs()

    @classmethod
    def from_fqn(cls, fqn: str) -> "ModelVersion":
        """
        Get the version of a model to download contents or load them in memory

        Args:
            fqn (str): Fully qualified name of the model version.

        Returns:
            ModelVersion: An ModelVersion instance of the Model

        Examples:

            ```python
            from truefoundry.ml import get_client, ModelVersion

            client = get_client()
            model_version = ModelVersion.from_fqn(fqn="<your-model-fqn>")
            ```
        """
        api_client = _get_api_client()
        mlfoundry_artifacts_api = MlfoundryArtifactsApi(api_client=api_client)
        _model_version = mlfoundry_artifacts_api.get_model_version_by_fqn_get(fqn=fqn)
        model_version = _model_version.model_version
        _model = mlfoundry_artifacts_api.get_model_get(id=model_version.model_id)
        model = _model.model
        instance = cls(model_version=model_version, model=model)
        return instance

    def _ensure_not_deleted(self):
        if self._deleted:
            raise MlFoundryException(
                "Model Version was deleted, cannot perform updates on a deleted version"
            )

    def _set_mutable_attrs(self):
        self._description = self._model_version.description or ""
        self._metadata = copy.deepcopy(self._model_version.artifact_metadata)
        self._framework = (
            copy.deepcopy(self._model_version.manifest.framework)
            if self._model_version.manifest
            else None
        )

    def _refetch_model_version(self):
        _model_version = self._mlfoundry_artifacts_api.get_model_version_get(
            id=self._model_version.id
        )
        self._model_version = _model_version.model_version
        self._set_mutable_attrs()

    def __repr__(self):
        return f"{self.__class__.__name__}(fqn={self.fqn!r})"

    def _get_artifacts_repo(self):
        return MlFoundryArtifactsRepository(
            artifact_identifier=ArtifactIdentifier(
                artifact_version_id=uuid.UUID(self._model_version.id)
            ),
            api_client=self._api_client,
        )

    @property
    def name(self) -> str:
        """Get the name of the model"""
        return self._model.name

    @property
    def model_fqn(self) -> str:
        """Get fqn of the model"""
        return self._model.fqn

    @property
    def version(self) -> int:
        """Get version information of the model"""
        return self._model_version.version

    @property
    def fqn(self) -> str:
        """Get fqn of the current model version"""
        return self._model_version.fqn

    @property
    def step(self) -> int:
        """Get the step in which model was created"""
        return self._model_version.step

    @property
    def description(self) -> Optional[str]:
        """Get description of the model"""
        return self._description

    @description.setter
    def description(self, value: str):
        """set the description of the model"""
        _validate_description(value)
        self._description = value
        if self._model_version.manifest:
            self._model_version.manifest.description = value

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata for the current model"""
        return self._metadata

    @metadata.setter
    def metadata(self, value: Dict[str, Any]):
        """set the metadata for current model"""
        _validate_artifact_metadata(value)
        self._metadata = value
        if self._model_version.manifest:
            self._model_version.manifest.metadata = value

    @property
    def framework(self) -> Optional["ModelFrameworkType"]:
        """Get the framework of the model"""
        return (
            _ModelFramework.from_dict(self._framework.actual_instance.dict())
            if self._framework and self._framework.actual_instance
            else None
        )

    @framework.setter
    def framework(
        self, value: Optional[Union[str, ModelFramework, "ModelFrameworkType"]]
    ):
        """set the framework of the model"""
        model_framework_type: Optional[ModelFrameworkType] = None

        if value is not None:
            model_framework_type = _ModelFramework.to_model_framework_type(value)

        if (
            self._model_version.serialization_format
            == ArtifactVersionSerializationFormat.V2
        ):
            self._model_version.manifest.framework = self._framework = (
                Framework.from_dict(model_framework_type.dict())
                if model_framework_type
                else None
            )
        else:
            warnings.warn(
                message="This model version was created using an older serialization format. Framework will not be updated",
                category=DeprecationWarning,
                stacklevel=2,
            )

    @property
    def created_at(self) -> datetime.datetime:
        """Get the time at which model version was created"""
        return self._model_version.created_at

    @property
    def updated_at(self) -> datetime.datetime:
        """Get the information about when the model version was updated"""
        return self._model_version.updated_at

    def raw_download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> str:
        """
        Download a model file or directory to a local directory if applicable, and return a
        local path for it.

        Args:
            path (str): Absolute path of the local filesystem destination directory to which to
                        download the specified models. This directory must already exist.
                        If unspecified, the models will either be downloaded to a new
                        uniquely-named directory on the local filesystem.
            overwrite (bool): If True it will overwrite the file if it is already present in the download directory else
                              it will throw an error
            progress (bool): value to show progress bar, defaults to None.

        Returns:
            path:  Absolute path of the local filesystem location containing the desired models.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            model_version.raw_download(path="<your-desired-download-path>")
            ```
        """
        logger.info("Downloading model version contents, this might take a while ...")
        artifacts_repo = self._get_artifacts_repo()
        return artifacts_repo.download_artifacts(
            artifact_path="", dst_path=path, overwrite=overwrite, progress=progress
        )

    def _download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> ModelVersionDownloadInfo:
        self._ensure_not_deleted()
        download_dir = self.raw_download(
            path=path, overwrite=overwrite, progress=progress
        )

        if (
            self._model_version.serialization_format
            == ArtifactVersionSerializationFormat.V2
        ):
            model_framework = (
                ModelFramework(self.framework.type)
                if self.framework
                else ModelFramework.UNKNOWN
            )
            download_info = ModelVersionDownloadInfo(
                download_dir=download_dir,
                model_dir=download_dir,
                model_framework=model_framework,
                model_filename=None,
            )
            return download_info

        internal_metadata_path = os.path.join(download_dir, INTERNAL_METADATA_PATH)
        if not os.path.exists(internal_metadata_path):
            raise MlFoundryException(
                "Model version seems to be corrupted or in invalid format due to missing model metadata. "
                "You can still use .raw_download(path='/your/path/here') to download and inspect files."
            )
        with open(internal_metadata_path) as f:
            internal_metadata = ModelVersionInternalMetadata.parse_obj(json.load(f))
        download_info = ModelVersionDownloadInfo(
            download_dir=os.path.join(download_dir, internal_metadata.files_dir),
            model_dir=os.path.join(
                download_dir,
                internal_metadata.files_dir,
                internal_metadata.model_dir,
            ),
            model_framework=internal_metadata.framework,
            model_filename=internal_metadata.model_filename,
        )
        return download_info

    def download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> ModelVersionDownloadInfo:
        """
        Download a model file or directory to a local directory if applicable, and return download info
        containing `model_dir` - local path where model was downloaded

        Args:
            path (str): Absolute path of the local filesystem destination directory to which to
                        download the specified models. This directory must already exist.
                        If unspecified, the models will either be downloaded to a new
                        uniquely-named directory on the local filesystem.
            overwrite (bool): If True it will overwrite the file if it is already present in the download directory else
                              it will throw an error
            progress (bool): value to show progress bar, defaults to None.

        Returns:
            ModelVersionDownloadInfo:  Download Info instance containing
                `model_dir` (path to downloaded model folder) and other metadata

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            download_info = model_version.download(path="<your-desired-download-path>")
            print(download_info.model_dir)
            ```
        """
        download_info = self._download(
            path=path, overwrite=overwrite, progress=progress
        )
        return download_info

    def delete(self) -> bool:
        """
        Deletes the current instance of the ModelVersion hence deleting the current version.

        Returns:
            True if model was deleted successfully

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            model_version.delete()
            ```
        """
        self._ensure_not_deleted()
        self._mlfoundry_artifacts_api.delete_artifact_version_post(
            delete_artifact_versions_request_dto=DeleteArtifactVersionsRequestDto(
                id=self._model_version.id
            )
        )
        self._deleted = True
        return True

    def update(self):
        """
        Updates the current instance of the ModelVersion hence updating the current version.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            model_version.description = 'This is the new description'
            model_version.update()
            ```
        """
        self._ensure_not_deleted()
        _model_version = self._mlfoundry_artifacts_api.update_model_version_post(
            update_model_version_request_dto=UpdateModelVersionRequestDto(
                id=self._model_version.id,
                description=self.description,
                artifact_metadata=self.metadata,
                manifest=self._model_version.manifest,
            )
        )
        self._model_version = _model_version.model_version
        self._set_mutable_attrs()


def _log_model_version(  # noqa: C901
    run: Optional["MlFoundryRun"],
    name: str,
    model_file_or_folder: Union[str, BlobStorageModelDirectory],
    mlfoundry_artifacts_api: Optional[MlfoundryArtifactsApi] = None,
    ml_repo_id: Optional[str] = None,
    additional_files: Sequence[Tuple[Union[str, Path], Optional[str]]] = (),
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    step: Optional[int] = 0,
    progress: Optional[bool] = None,
    framework: Optional[Union[str, ModelFramework, "ModelFrameworkType"]] = None,
) -> ModelVersion:
    if (run and mlfoundry_artifacts_api) or (not run and not mlfoundry_artifacts_api):
        raise MlFoundryException(
            "Exactly one of run, mlfoundry_artifacts_api should be passed"
        )

    if not isinstance(model_file_or_folder, (str, BlobStorageModelDirectory)):
        raise MlFoundryException(
            "model_file_or_folder should be of type str or BlobStorageModelDirectory"
        )

    if mlfoundry_artifacts_api and not ml_repo_id:
        raise MlFoundryException(
            "If mlfoundry_artifacts_api is passed, ml_repo_id must also be passed"
        )
    if run:
        mlfoundry_artifacts_api = run._mlfoundry_artifacts_api

    assert mlfoundry_artifacts_api is not None

    step = step or 0
    total_size = None
    metadata = metadata or {}
    additional_files = additional_files or {}

    _validate_description(description)
    _validate_artifact_metadata(metadata)

    if isinstance(model_file_or_folder, str):
        logger.info("Logging model and additional files, this might take a while ...")
        temp_dir = tempfile.TemporaryDirectory(prefix="truefoundry-")
        try:
            logger.info("Adding model file/folder to model version content")
            temp_dest_to_src_map = _copy_additional_files(
                root_dir=temp_dir.name,
                files_dir="",
                model_dir=None,
                additional_files=[(model_file_or_folder, "")],
                ignore_model_dir_dest_conflict=True,
            )

            # verify additional files and paths, copy additional files
            if additional_files:
                logger.info("Adding `additional_files` to model version contents")
                temp_dest_to_src_map = _copy_additional_files(
                    root_dir=temp_dir.name,
                    files_dir="",
                    model_dir=None,
                    additional_files=additional_files,
                    ignore_model_dir_dest_conflict=False,
                    existing_dest_to_src_map=temp_dest_to_src_map,
                )
        except Exception as e:
            temp_dir.cleanup()
            raise MlFoundryException("Failed to log model") from e

    # create entry
    _create_artifact_version_response = (
        mlfoundry_artifacts_api.create_artifact_version_post(
            create_artifact_version_request_dto=CreateArtifactVersionRequestDto(
                experiment_id=int(run._experiment_id if run else ml_repo_id),
                artifact_type=ArtifactType.MODEL,
                name=name,
            )
        )
    )
    version_id = _create_artifact_version_response.id
    artifact_storage_root = _create_artifact_version_response.artifact_storage_root
    if isinstance(model_file_or_folder, str):
        # Source is of type TruefoundryModelSource
        source = ModelVersionSource.from_json(
            TruefoundryModelSource(
                type="truefoundry", uri=artifact_storage_root
            ).to_json()
        )
        artifacts_repo = MlFoundryArtifactsRepository(
            artifact_identifier=ArtifactIdentifier(
                artifact_version_id=uuid.UUID(version_id)
            ),
            api_client=mlfoundry_artifacts_api.api_client,
        )
        total_size = calculate_total_size(list(temp_dest_to_src_map.values()))
        try:
            logger.info(
                "Packaging and uploading files to remote with Total Size: %.6f MB",
                total_size / 1000000.0,
            )
            src_dest_pairs = _get_src_dest_pairs(
                root_dir=temp_dir.name, dest_to_src_map=temp_dest_to_src_map
            )
            artifacts_repo.log_artifacts(
                src_dest_pairs=src_dest_pairs, progress=progress
            )
        except Exception as e:
            mlfoundry_artifacts_api.notify_failure_post(
                notify_artifact_version_failure_dto=NotifyArtifactVersionFailureDto(
                    id=version_id
                )
            )
            raise MlFoundryException("Failed to log model") from e
        finally:
            temp_dir.cleanup()
    elif isinstance(model_file_or_folder, BlobStorageModelDirectory):
        source = ModelVersionSource.from_json(
            ExternalModelSource(type="external", uri=model_file_or_folder.uri).to_json()
        )
    else:
        raise MlFoundryException("Invalid model_file_or_folder provided")

    _framework = _ModelFramework.to_model_framework_type(framework)
    model_manifest = ModelVersionManifest(
        description=description,
        metadata=metadata,
        source=source,
        framework=Framework.from_dict(_framework.dict()) if _framework else None,
        step=step if run else 0,
    )
    artifact_version_response = mlfoundry_artifacts_api.finalize_artifact_version_post(
        finalize_artifact_version_request_dto=FinalizeArtifactVersionRequestDto(
            id=version_id,
            run_uuid=run.run_id if run else None,
            artifact_size=total_size,
            artifact_metadata=metadata,
            internal_metadata=None,
            step=model_manifest.step,
            manifest=model_manifest,
        )
    )
    return ModelVersion.from_fqn(fqn=artifact_version_response.artifact_version.fqn)
