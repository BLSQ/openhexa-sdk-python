# Generated by ariadne-codegen

from .add_pipeline_recipient import (
    AddPipelineRecipient,
    AddPipelineRecipientAddPipelineRecipient,
)
from .add_webapp_to_favorites import (
    AddWebappToFavorites,
    AddWebappToFavoritesAddToFavorites,
)
from .archive_workspace import ArchiveWorkspace, ArchiveWorkspaceArchiveWorkspace
from .base_client import BaseClient
from .base_model import BaseModel, Upload
from .client import Client
from .create_connection import (
    CreateConnection,
    CreateConnectionCreateConnection,
    CreateConnectionCreateConnectionConnection,
)
from .create_dataset import (
    CreateDataset,
    CreateDatasetCreateDataset,
    CreateDatasetCreateDatasetDataset,
)
from .create_pipeline import (
    CreatePipeline,
    CreatePipelineCreatePipeline,
    CreatePipelineCreatePipelinePipeline,
)
from .create_pipeline_from_template_version import (
    CreatePipelineFromTemplateVersion,
    CreatePipelineFromTemplateVersionCreatePipelineFromTemplateVersion,
    CreatePipelineFromTemplateVersionCreatePipelineFromTemplateVersionPipeline,
)
from .create_pipeline_template_version import (
    CreatePipelineTemplateVersion,
    CreatePipelineTemplateVersionCreatePipelineTemplateVersion,
    CreatePipelineTemplateVersionCreatePipelineTemplateVersionPipelineTemplate,
)
from .create_webapp import (
    CreateWebapp,
    CreateWebappCreateWebapp,
    CreateWebappCreateWebappWebapp,
)
from .create_workspace import (
    CreateWorkspace,
    CreateWorkspaceCreateWorkspace,
    CreateWorkspaceCreateWorkspaceWorkspace,
    CreateWorkspaceCreateWorkspaceWorkspaceCountries,
)
from .dataset import (
    Dataset,
    DatasetDataset,
    DatasetDatasetCreatedBy,
    DatasetDatasetPermissions,
    DatasetDatasetVersions,
    DatasetDatasetVersionsItems,
    DatasetDatasetVersionsItemsCreatedBy,
    DatasetDatasetWorkspace,
)
from .datasets import (
    Datasets,
    DatasetsDatasets,
    DatasetsDatasetsItems,
    DatasetsDatasetsItemsCreatedBy,
    DatasetsDatasetsItemsPermissions,
)
from .delete_connection import DeleteConnection, DeleteConnectionDeleteConnection
from .delete_dataset import DeleteDataset, DeleteDatasetDeleteDataset
from .delete_pipeline import DeletePipeline, DeletePipelineDeletePipeline
from .delete_pipeline_template import (
    DeletePipelineTemplate,
    DeletePipelineTemplateDeletePipelineTemplate,
)
from .delete_pipeline_version import (
    DeletePipelineVersion,
    DeletePipelineVersionDeletePipelineVersion,
)
from .delete_webapp import DeleteWebapp, DeleteWebappDeleteWebapp
from .enums import (
    AccessmodAccessibilityAnalysisAlgorithm,
    AccessmodAccessRequestStatus,
    AccessmodAnalysisStatus,
    AccessmodAnalysisType,
    AccessmodFilesetFormat,
    AccessmodFilesetMode,
    AccessmodFilesetRoleCode,
    AccessmodFilesetStatus,
    AccessmodProjectOrder,
    AddToFavoritesError,
    ApproveAccessmodAccessRequestError,
    ArchiveWorkspaceError,
    BucketObjectType,
    ConnectionType,
    CreateAccessmodAccessibilityAnalysisError,
    CreateAccessmodFileError,
    CreateAccessmodFilesetError,
    CreateAccessmodProjectError,
    CreateAccessmodProjectMemberError,
    CreateAccessmodZonalStatisticsError,
    CreateBucketFolderError,
    CreateConnectionError,
    CreateDatasetError,
    CreateDatasetVersionError,
    CreateDatasetVersionFileError,
    CreateMembershipError,
    CreatePipelineFromTemplateVersionError,
    CreatePipelineTemplateVersionError,
    CreateTeamError,
    CreateTemplateVersionPermissionReason,
    CreateWebappError,
    CreateWorkspaceError,
    DAGRunOrderBy,
    DAGRunStatus,
    DAGRunTrigger,
    DeclineWorkspaceInvitationError,
    DeleteAccessmodAnalysisError,
    DeleteAccessmodFilesetError,
    DeleteAccessmodProjectError,
    DeleteAccessmodProjectMemberError,
    DeleteBucketObjectError,
    DeleteConnectionError,
    DeleteDatasetError,
    DeleteDatasetLinkError,
    DeleteDatasetVersionError,
    DeleteMembershipError,
    DeleteMetadataAttributeError,
    DeletePipelineVersionError,
    DeleteTeamError,
    DeleteTemplateVersionError,
    DeleteWebappError,
    DeleteWorkspaceDatabaseTableError,
    DeleteWorkspaceError,
    DeleteWorkspaceInvitationError,
    DeleteWorkspaceMemberError,
    DenyAccessmodAccessRequestError,
    DHIS2ConnectionError,
    DHIS2ConnectionStatus,
    DHIS2MetadataType,
    DisableTwoFactorError,
    EnableTwoFactorError,
    FileSampleStatus,
    FileType,
    GenerateChallengeError,
    GenerateNewDatabasePasswordError,
    GeneratePipelineWebhookUrlError,
    GenerateWorkspaceTokenError,
    IASOConnectionError,
    IASOMetadataType,
    InviteWorkspaceMembershipError,
    JoinWorkspaceError,
    LaunchAccessmodAnalysisError,
    LaunchNotebookServerError,
    LinkDatasetError,
    LoginError,
    MembershipRole,
    MessagePriority,
    OrderByDirection,
    ParameterType,
    ParameterWidget,
    PermissionMode,
    PinDatasetError,
    PipelineError,
    PipelineNotificationLevel,
    PipelineRecipientError,
    PipelineRunOrderBy,
    PipelineRunStatus,
    PipelineRunTrigger,
    PipelineTemplateError,
    PipelineType,
    PrepareObjectDownloadError,
    PrepareObjectUploadError,
    PrepareVersionFileDownloadError,
    RegisterError,
    RemoveFromFavoritesError,
    RequestAccessmodAccessError,
    ResendWorkspaceInvitationError,
    RunDAGError,
    SetDAGRunFavoriteError,
    SetMetadataAttributeError,
    SetPasswordError,
    UpdateAccessmodAccessibilityAnalysisError,
    UpdateAccessmodFilesetError,
    UpdateAccessmodProjectError,
    UpdateAccessmodProjectMemberError,
    UpdateAccessmodZonalStatisticsError,
    UpdateConnectionError,
    UpdateDAGError,
    UpdateDatasetError,
    UpdateDatasetVersionError,
    UpdateMembershipError,
    UpdatePipelineError,
    UpdatePipelineVersionError,
    UpdateTeamError,
    UpdateTemplateError,
    UpdateTemplateVersionError,
    UpdateUserError,
    UpdateWebappError,
    UpdateWorkspaceError,
    UpdateWorkspaceMemberError,
    UpgradePipelineVersionFromTemplateError,
    VerifyDeviceError,
    WorkspaceInvitationStatus,
    WorkspaceMembershipRole,
)
from .exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
    GraphQLClientInvalidResponseError,
)
from .get_users import GetUsers, GetUsersUsers, GetUsersUsersAvatar
from .input_types import (
    AddPipelineOutputInput,
    AddToFavoritesInput,
    ApproveAccessmodAccessRequestInput,
    ArchiveWorkspaceInput,
    ConnectionFieldInput,
    CountryInput,
    CreateAccessmodAccessibilityAnalysisInput,
    CreateAccessmodFileInput,
    CreateAccessmodFilesetInput,
    CreateAccessmodProjectInput,
    CreateAccessmodProjectMemberInput,
    CreateAccessmodZonalStatisticsInput,
    CreateBucketFolderInput,
    CreateConnectionInput,
    CreateDatasetInput,
    CreateDatasetVersionFileInput,
    CreateDatasetVersionInput,
    CreateMembershipInput,
    CreatePipelineFromTemplateVersionInput,
    CreatePipelineInput,
    CreatePipelineRecipientInput,
    CreatePipelineTemplateVersionInput,
    CreateTeamInput,
    CreateWebappInput,
    CreateWorkspaceInput,
    DeclineWorkspaceInvitationInput,
    DeleteAccessmodAnalysisInput,
    DeleteAccessmodFilesetInput,
    DeleteAccessmodProjectInput,
    DeleteAccessmodProjectMemberInput,
    DeleteBucketObjectInput,
    DeleteConnectionInput,
    DeleteDatasetInput,
    DeleteDatasetLinkInput,
    DeleteDatasetVersionInput,
    DeleteMembershipInput,
    DeleteMetadataAttributeInput,
    DeletePipelineInput,
    DeletePipelineRecipientInput,
    DeletePipelineTemplateInput,
    DeletePipelineVersionInput,
    DeleteTeamInput,
    DeleteTemplateVersionInput,
    DeleteWebappInput,
    DeleteWorkspaceDatabaseTableInput,
    DeleteWorkspaceInput,
    DeleteWorkspaceInvitationInput,
    DeleteWorkspaceMemberInput,
    DenyAccessmodAccessRequestInput,
    DisableTwoFactorInput,
    EnableTwoFactorInput,
    GenerateDatasetUploadUrlInput,
    GenerateNewDatabasePasswordInput,
    GeneratePipelineWebhookUrlInput,
    GenerateWorkspaceTokenInput,
    IASOQueryFilterInput,
    InviteWorkspaceMemberInput,
    JoinWorkspaceInput,
    LaunchAccessmodAnalysisInput,
    LaunchNotebookServerInput,
    LinkDatasetInput,
    LoginInput,
    LogPipelineMessageInput,
    OrganizationInput,
    ParameterInput,
    PinDatasetInput,
    PipelineTokenInput,
    PrepareAccessmodFileDownloadInput,
    PrepareAccessmodFilesetVisualizationDownloadInput,
    PrepareAccessmodFileUploadInput,
    PrepareDownloadURLInput,
    PrepareObjectDownloadInput,
    PrepareObjectUploadInput,
    PrepareVersionFileDownloadInput,
    RegisterInput,
    RemoveFromFavoritesInput,
    RequestAccessmodAccessInput,
    ResendWorkspaceInvitationInput,
    ResetPasswordInput,
    RunDAGInput,
    RunPipelineInput,
    SetDAGRunFavoriteInput,
    SetMetadataAttributeInput,
    SetPasswordInput,
    StopPipelineInput,
    UpdateAccessmodAccessibilityAnalysisInput,
    UpdateAccessmodFilesetInput,
    UpdateAccessmodProjectInput,
    UpdateAccessmodProjectMemberInput,
    UpdateAccessmodZonalStatisticsInput,
    UpdateConnectionInput,
    UpdateDAGInput,
    UpdateDatasetInput,
    UpdateDatasetVersionInput,
    UpdateMembershipInput,
    UpdatePipelineInput,
    UpdatePipelineProgressInput,
    UpdatePipelineRecipientInput,
    UpdatePipelineVersionInput,
    UpdateTeamInput,
    UpdateTemplateInput,
    UpdateTemplateVersionInput,
    UpdateUserInput,
    UpdateWebappInput,
    UpdateWorkspaceInput,
    UpdateWorkspaceMemberInput,
    UpgradePipelineVersionFromTemplateInput,
    UploadPipelineInput,
    VerifyDeviceInput,
)
from .invite_workspace_member import (
    InviteWorkspaceMember,
    InviteWorkspaceMemberInviteWorkspaceMember,
    InviteWorkspaceMemberInviteWorkspaceMemberWorkspaceMembership,
)
from .pipeline import (
    Pipeline,
    PipelinePipelineByCode,
    PipelinePipelineByCodeCurrentVersion,
    PipelinePipelineByCodeCurrentVersionUser,
    PipelinePipelineByCodeCurrentVersionUserAvatar,
    PipelinePipelineByCodeNewTemplateVersions,
    PipelinePipelineByCodeRecipients,
    PipelinePipelineByCodeRecipientsUser,
    PipelinePipelineByCodeRuns,
    PipelinePipelineByCodeRunsItems,
    PipelinePipelineByCodeRunsItemsUser,
    PipelinePipelineByCodeSourceTemplate,
)
from .pipelines import (
    Pipelines,
    PipelinesPipelines,
    PipelinesPipelinesItems,
    PipelinesPipelinesItemsCurrentVersion,
    PipelinesPipelinesItemsLastRuns,
    PipelinesPipelinesItemsLastRunsItems,
)
from .remove_webapp_from_favorites import (
    RemoveWebappFromFavorites,
    RemoveWebappFromFavoritesRemoveFromFavorites,
)
from .stop_pipeline import StopPipeline, StopPipelineStopPipeline
from .update_connection import (
    UpdateConnection,
    UpdateConnectionUpdateConnection,
    UpdateConnectionUpdateConnectionConnection,
    UpdateConnectionUpdateConnectionConnectionFields,
)
from .update_dataset import (
    UpdateDataset,
    UpdateDatasetUpdateDataset,
    UpdateDatasetUpdateDatasetDataset,
)
from .update_webapp import UpdateWebapp, UpdateWebappUpdateWebapp
from .update_workspace import (
    UpdateWorkspace,
    UpdateWorkspaceUpdateWorkspace,
    UpdateWorkspaceUpdateWorkspaceWorkspace,
    UpdateWorkspaceUpdateWorkspaceWorkspaceCountries,
)
from .upgrade_pipeline_version_from_template import (
    UpgradePipelineVersionFromTemplate,
    UpgradePipelineVersionFromTemplateUpgradePipelineVersionFromTemplate,
)
from .workspace import (
    Workspace,
    WorkspaceWorkspace,
    WorkspaceWorkspaceCountries,
    WorkspaceWorkspacePermissions,
)
from .workspaces import (
    Workspaces,
    WorkspacesWorkspaces,
    WorkspacesWorkspacesItems,
    WorkspacesWorkspacesItemsCountries,
)

__all__ = [
    "AccessmodAccessRequestStatus",
    "AccessmodAccessibilityAnalysisAlgorithm",
    "AccessmodAnalysisStatus",
    "AccessmodAnalysisType",
    "AccessmodFilesetFormat",
    "AccessmodFilesetMode",
    "AccessmodFilesetRoleCode",
    "AccessmodFilesetStatus",
    "AccessmodProjectOrder",
    "AddPipelineOutputInput",
    "AddPipelineRecipient",
    "AddPipelineRecipientAddPipelineRecipient",
    "AddToFavoritesError",
    "AddToFavoritesInput",
    "AddWebappToFavorites",
    "AddWebappToFavoritesAddToFavorites",
    "ApproveAccessmodAccessRequestError",
    "ApproveAccessmodAccessRequestInput",
    "ArchiveWorkspace",
    "ArchiveWorkspaceArchiveWorkspace",
    "ArchiveWorkspaceError",
    "ArchiveWorkspaceInput",
    "BaseClient",
    "BaseModel",
    "BucketObjectType",
    "Client",
    "ConnectionFieldInput",
    "ConnectionType",
    "CountryInput",
    "CreateAccessmodAccessibilityAnalysisError",
    "CreateAccessmodAccessibilityAnalysisInput",
    "CreateAccessmodFileError",
    "CreateAccessmodFileInput",
    "CreateAccessmodFilesetError",
    "CreateAccessmodFilesetInput",
    "CreateAccessmodProjectError",
    "CreateAccessmodProjectInput",
    "CreateAccessmodProjectMemberError",
    "CreateAccessmodProjectMemberInput",
    "CreateAccessmodZonalStatisticsError",
    "CreateAccessmodZonalStatisticsInput",
    "CreateBucketFolderError",
    "CreateBucketFolderInput",
    "CreateConnection",
    "CreateConnectionCreateConnection",
    "CreateConnectionCreateConnectionConnection",
    "CreateConnectionError",
    "CreateConnectionInput",
    "CreateDataset",
    "CreateDatasetCreateDataset",
    "CreateDatasetCreateDatasetDataset",
    "CreateDatasetError",
    "CreateDatasetInput",
    "CreateDatasetVersionError",
    "CreateDatasetVersionFileError",
    "CreateDatasetVersionFileInput",
    "CreateDatasetVersionInput",
    "CreateMembershipError",
    "CreateMembershipInput",
    "CreatePipeline",
    "CreatePipelineCreatePipeline",
    "CreatePipelineCreatePipelinePipeline",
    "CreatePipelineFromTemplateVersion",
    "CreatePipelineFromTemplateVersionCreatePipelineFromTemplateVersion",
    "CreatePipelineFromTemplateVersionCreatePipelineFromTemplateVersionPipeline",
    "CreatePipelineFromTemplateVersionError",
    "CreatePipelineFromTemplateVersionInput",
    "CreatePipelineInput",
    "CreatePipelineRecipientInput",
    "CreatePipelineTemplateVersion",
    "CreatePipelineTemplateVersionCreatePipelineTemplateVersion",
    "CreatePipelineTemplateVersionCreatePipelineTemplateVersionPipelineTemplate",
    "CreatePipelineTemplateVersionError",
    "CreatePipelineTemplateVersionInput",
    "CreateTeamError",
    "CreateTeamInput",
    "CreateTemplateVersionPermissionReason",
    "CreateWebapp",
    "CreateWebappCreateWebapp",
    "CreateWebappCreateWebappWebapp",
    "CreateWebappError",
    "CreateWebappInput",
    "CreateWorkspace",
    "CreateWorkspaceCreateWorkspace",
    "CreateWorkspaceCreateWorkspaceWorkspace",
    "CreateWorkspaceCreateWorkspaceWorkspaceCountries",
    "CreateWorkspaceError",
    "CreateWorkspaceInput",
    "DAGRunOrderBy",
    "DAGRunStatus",
    "DAGRunTrigger",
    "DHIS2ConnectionError",
    "DHIS2ConnectionStatus",
    "DHIS2MetadataType",
    "Dataset",
    "DatasetDataset",
    "DatasetDatasetCreatedBy",
    "DatasetDatasetPermissions",
    "DatasetDatasetVersions",
    "DatasetDatasetVersionsItems",
    "DatasetDatasetVersionsItemsCreatedBy",
    "DatasetDatasetWorkspace",
    "Datasets",
    "DatasetsDatasets",
    "DatasetsDatasetsItems",
    "DatasetsDatasetsItemsCreatedBy",
    "DatasetsDatasetsItemsPermissions",
    "DeclineWorkspaceInvitationError",
    "DeclineWorkspaceInvitationInput",
    "DeleteAccessmodAnalysisError",
    "DeleteAccessmodAnalysisInput",
    "DeleteAccessmodFilesetError",
    "DeleteAccessmodFilesetInput",
    "DeleteAccessmodProjectError",
    "DeleteAccessmodProjectInput",
    "DeleteAccessmodProjectMemberError",
    "DeleteAccessmodProjectMemberInput",
    "DeleteBucketObjectError",
    "DeleteBucketObjectInput",
    "DeleteConnection",
    "DeleteConnectionDeleteConnection",
    "DeleteConnectionError",
    "DeleteConnectionInput",
    "DeleteDataset",
    "DeleteDatasetDeleteDataset",
    "DeleteDatasetError",
    "DeleteDatasetInput",
    "DeleteDatasetLinkError",
    "DeleteDatasetLinkInput",
    "DeleteDatasetVersionError",
    "DeleteDatasetVersionInput",
    "DeleteMembershipError",
    "DeleteMembershipInput",
    "DeleteMetadataAttributeError",
    "DeleteMetadataAttributeInput",
    "DeletePipeline",
    "DeletePipelineDeletePipeline",
    "DeletePipelineInput",
    "DeletePipelineRecipientInput",
    "DeletePipelineTemplate",
    "DeletePipelineTemplateDeletePipelineTemplate",
    "DeletePipelineTemplateInput",
    "DeletePipelineVersion",
    "DeletePipelineVersionDeletePipelineVersion",
    "DeletePipelineVersionError",
    "DeletePipelineVersionInput",
    "DeleteTeamError",
    "DeleteTeamInput",
    "DeleteTemplateVersionError",
    "DeleteTemplateVersionInput",
    "DeleteWebapp",
    "DeleteWebappDeleteWebapp",
    "DeleteWebappError",
    "DeleteWebappInput",
    "DeleteWorkspaceDatabaseTableError",
    "DeleteWorkspaceDatabaseTableInput",
    "DeleteWorkspaceError",
    "DeleteWorkspaceInput",
    "DeleteWorkspaceInvitationError",
    "DeleteWorkspaceInvitationInput",
    "DeleteWorkspaceMemberError",
    "DeleteWorkspaceMemberInput",
    "DenyAccessmodAccessRequestError",
    "DenyAccessmodAccessRequestInput",
    "DisableTwoFactorError",
    "DisableTwoFactorInput",
    "EnableTwoFactorError",
    "EnableTwoFactorInput",
    "FileSampleStatus",
    "FileType",
    "GenerateChallengeError",
    "GenerateDatasetUploadUrlInput",
    "GenerateNewDatabasePasswordError",
    "GenerateNewDatabasePasswordInput",
    "GeneratePipelineWebhookUrlError",
    "GeneratePipelineWebhookUrlInput",
    "GenerateWorkspaceTokenError",
    "GenerateWorkspaceTokenInput",
    "GetUsers",
    "GetUsersUsers",
    "GetUsersUsersAvatar",
    "GraphQLClientError",
    "GraphQLClientGraphQLError",
    "GraphQLClientGraphQLMultiError",
    "GraphQLClientHttpError",
    "GraphQLClientInvalidResponseError",
    "IASOConnectionError",
    "IASOMetadataType",
    "IASOQueryFilterInput",
    "InviteWorkspaceMember",
    "InviteWorkspaceMemberInput",
    "InviteWorkspaceMemberInviteWorkspaceMember",
    "InviteWorkspaceMemberInviteWorkspaceMemberWorkspaceMembership",
    "InviteWorkspaceMembershipError",
    "JoinWorkspaceError",
    "JoinWorkspaceInput",
    "LaunchAccessmodAnalysisError",
    "LaunchAccessmodAnalysisInput",
    "LaunchNotebookServerError",
    "LaunchNotebookServerInput",
    "LinkDatasetError",
    "LinkDatasetInput",
    "LogPipelineMessageInput",
    "LoginError",
    "LoginInput",
    "MembershipRole",
    "MessagePriority",
    "OrderByDirection",
    "OrganizationInput",
    "ParameterInput",
    "ParameterType",
    "ParameterWidget",
    "PermissionMode",
    "PinDatasetError",
    "PinDatasetInput",
    "Pipeline",
    "PipelineError",
    "PipelineNotificationLevel",
    "PipelinePipelineByCode",
    "PipelinePipelineByCodeCurrentVersion",
    "PipelinePipelineByCodeCurrentVersionUser",
    "PipelinePipelineByCodeCurrentVersionUserAvatar",
    "PipelinePipelineByCodeNewTemplateVersions",
    "PipelinePipelineByCodeRecipients",
    "PipelinePipelineByCodeRecipientsUser",
    "PipelinePipelineByCodeRuns",
    "PipelinePipelineByCodeRunsItems",
    "PipelinePipelineByCodeRunsItemsUser",
    "PipelinePipelineByCodeSourceTemplate",
    "PipelineRecipientError",
    "PipelineRunOrderBy",
    "PipelineRunStatus",
    "PipelineRunTrigger",
    "PipelineTemplateError",
    "PipelineTokenInput",
    "PipelineType",
    "Pipelines",
    "PipelinesPipelines",
    "PipelinesPipelinesItems",
    "PipelinesPipelinesItemsCurrentVersion",
    "PipelinesPipelinesItemsLastRuns",
    "PipelinesPipelinesItemsLastRunsItems",
    "PrepareAccessmodFileDownloadInput",
    "PrepareAccessmodFileUploadInput",
    "PrepareAccessmodFilesetVisualizationDownloadInput",
    "PrepareDownloadURLInput",
    "PrepareObjectDownloadError",
    "PrepareObjectDownloadInput",
    "PrepareObjectUploadError",
    "PrepareObjectUploadInput",
    "PrepareVersionFileDownloadError",
    "PrepareVersionFileDownloadInput",
    "RegisterError",
    "RegisterInput",
    "RemoveFromFavoritesError",
    "RemoveFromFavoritesInput",
    "RemoveWebappFromFavorites",
    "RemoveWebappFromFavoritesRemoveFromFavorites",
    "RequestAccessmodAccessError",
    "RequestAccessmodAccessInput",
    "ResendWorkspaceInvitationError",
    "ResendWorkspaceInvitationInput",
    "ResetPasswordInput",
    "RunDAGError",
    "RunDAGInput",
    "RunPipelineInput",
    "SetDAGRunFavoriteError",
    "SetDAGRunFavoriteInput",
    "SetMetadataAttributeError",
    "SetMetadataAttributeInput",
    "SetPasswordError",
    "SetPasswordInput",
    "StopPipeline",
    "StopPipelineInput",
    "StopPipelineStopPipeline",
    "UpdateAccessmodAccessibilityAnalysisError",
    "UpdateAccessmodAccessibilityAnalysisInput",
    "UpdateAccessmodFilesetError",
    "UpdateAccessmodFilesetInput",
    "UpdateAccessmodProjectError",
    "UpdateAccessmodProjectInput",
    "UpdateAccessmodProjectMemberError",
    "UpdateAccessmodProjectMemberInput",
    "UpdateAccessmodZonalStatisticsError",
    "UpdateAccessmodZonalStatisticsInput",
    "UpdateConnection",
    "UpdateConnectionError",
    "UpdateConnectionInput",
    "UpdateConnectionUpdateConnection",
    "UpdateConnectionUpdateConnectionConnection",
    "UpdateConnectionUpdateConnectionConnectionFields",
    "UpdateDAGError",
    "UpdateDAGInput",
    "UpdateDataset",
    "UpdateDatasetError",
    "UpdateDatasetInput",
    "UpdateDatasetUpdateDataset",
    "UpdateDatasetUpdateDatasetDataset",
    "UpdateDatasetVersionError",
    "UpdateDatasetVersionInput",
    "UpdateMembershipError",
    "UpdateMembershipInput",
    "UpdatePipelineError",
    "UpdatePipelineInput",
    "UpdatePipelineProgressInput",
    "UpdatePipelineRecipientInput",
    "UpdatePipelineVersionError",
    "UpdatePipelineVersionInput",
    "UpdateTeamError",
    "UpdateTeamInput",
    "UpdateTemplateError",
    "UpdateTemplateInput",
    "UpdateTemplateVersionError",
    "UpdateTemplateVersionInput",
    "UpdateUserError",
    "UpdateUserInput",
    "UpdateWebapp",
    "UpdateWebappError",
    "UpdateWebappInput",
    "UpdateWebappUpdateWebapp",
    "UpdateWorkspace",
    "UpdateWorkspaceError",
    "UpdateWorkspaceInput",
    "UpdateWorkspaceMemberError",
    "UpdateWorkspaceMemberInput",
    "UpdateWorkspaceUpdateWorkspace",
    "UpdateWorkspaceUpdateWorkspaceWorkspace",
    "UpdateWorkspaceUpdateWorkspaceWorkspaceCountries",
    "UpgradePipelineVersionFromTemplate",
    "UpgradePipelineVersionFromTemplateError",
    "UpgradePipelineVersionFromTemplateInput",
    "UpgradePipelineVersionFromTemplateUpgradePipelineVersionFromTemplate",
    "Upload",
    "UploadPipelineInput",
    "VerifyDeviceError",
    "VerifyDeviceInput",
    "Workspace",
    "WorkspaceInvitationStatus",
    "WorkspaceMembershipRole",
    "WorkspaceWorkspace",
    "WorkspaceWorkspaceCountries",
    "WorkspaceWorkspacePermissions",
    "Workspaces",
    "WorkspacesWorkspaces",
    "WorkspacesWorkspacesItems",
    "WorkspacesWorkspacesItemsCountries",
]
