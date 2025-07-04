# Generated by ariadne-codegen
# Source: openhexa/graphql/schema.generated.graphql

from enum import Enum


class AccessmodAccessRequestStatus(str, Enum):
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    PENDING = "PENDING"


class AccessmodAccessibilityAnalysisAlgorithm(str, Enum):
    ANISOTROPIC = "ANISOTROPIC"
    ISOTROPIC = "ISOTROPIC"


class AccessmodAnalysisStatus(str, Enum):
    DRAFT = "DRAFT"
    FAILED = "FAILED"
    QUEUED = "QUEUED"
    READY = "READY"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"


class AccessmodAnalysisType(str, Enum):
    ACCESSIBILITY = "ACCESSIBILITY"
    GEOGRAPHIC_COVERAGE = "GEOGRAPHIC_COVERAGE"
    ZONAL_STATISTICS = "ZONAL_STATISTICS"


class AccessmodFilesetFormat(str, Enum):
    RASTER = "RASTER"
    TABULAR = "TABULAR"
    VECTOR = "VECTOR"


class AccessmodFilesetMode(str, Enum):
    AUTOMATIC_ACQUISITION = "AUTOMATIC_ACQUISITION"
    USER_INPUT = "USER_INPUT"


class AccessmodFilesetRoleCode(str, Enum):
    BARRIER = "BARRIER"
    BOUNDARIES = "BOUNDARIES"
    COVERAGE = "COVERAGE"
    DEM = "DEM"
    FRICTION_SURFACE = "FRICTION_SURFACE"
    GEOMETRY = "GEOMETRY"
    HEALTH_FACILITIES = "HEALTH_FACILITIES"
    LAND_COVER = "LAND_COVER"
    POPULATION = "POPULATION"
    STACK = "STACK"
    TRANSPORT_NETWORK = "TRANSPORT_NETWORK"
    TRAVEL_TIMES = "TRAVEL_TIMES"
    WATER = "WATER"
    ZONAL_STATISTICS = "ZONAL_STATISTICS"
    ZONAL_STATISTICS_TABLE = "ZONAL_STATISTICS_TABLE"


class AccessmodFilesetStatus(str, Enum):
    INVALID = "INVALID"
    PENDING = "PENDING"
    TO_ACQUIRE = "TO_ACQUIRE"
    VALID = "VALID"
    VALIDATING = "VALIDATING"


class AccessmodProjectOrder(str, Enum):
    NAME_ASC = "NAME_ASC"
    NAME_DESC = "NAME_DESC"
    UPDATED_AT_ASC = "UPDATED_AT_ASC"
    UPDATED_AT_DESC = "UPDATED_AT_DESC"


class AddToFavoritesError(str, Enum):
    WEBAPP_NOT_FOUND = "WEBAPP_NOT_FOUND"


class ApproveAccessmodAccessRequestError(str, Enum):
    INVALID = "INVALID"


class ArchiveWorkspaceError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class BucketObjectType(str, Enum):
    DIRECTORY = "DIRECTORY"
    FILE = "FILE"


class ConnectionType(str, Enum):
    CUSTOM = "CUSTOM"
    DHIS2 = "DHIS2"
    GCS = "GCS"
    IASO = "IASO"
    POSTGRESQL = "POSTGRESQL"
    S3 = "S3"


class CreateAccessmodAccessibilityAnalysisError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"


class CreateAccessmodFileError(str, Enum):
    URI_DUPLICATE = "URI_DUPLICATE"


class CreateAccessmodFilesetError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreateAccessmodProjectError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreateAccessmodProjectMemberError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreateAccessmodZonalStatisticsError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"


class CreateBucketFolderError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreateConnectionError(str, Enum):
    INVALID_SLUG = "INVALID_SLUG"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class CreateDatasetError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class CreateDatasetVersionError(str, Enum):
    DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
    DUPLICATE_NAME = "DUPLICATE_NAME"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreateDatasetVersionFileError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INVALID_URI = "INVALID_URI"
    LOCKED_VERSION = "LOCKED_VERSION"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    VERSION_NOT_FOUND = "VERSION_NOT_FOUND"


class CreateMembershipError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreatePipelineFromTemplateVersionError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_TEMPLATE_VERSION_NOT_FOUND = "PIPELINE_TEMPLATE_VERSION_NOT_FOUND"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class CreatePipelineTemplateVersionError(str, Enum):
    DUPLICATE_TEMPLATE_NAME_OR_CODE = "DUPLICATE_TEMPLATE_NAME_OR_CODE"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    PIPELINE_VERSION_NOT_FOUND = "PIPELINE_VERSION_NOT_FOUND"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class CreateTeamError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class CreateTemplateVersionPermissionReason(str, Enum):
    NO_NEW_TEMPLATE_VERSION_AVAILABLE = "NO_NEW_TEMPLATE_VERSION_AVAILABLE"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_IS_ALREADY_FROM_TEMPLATE = "PIPELINE_IS_ALREADY_FROM_TEMPLATE"
    PIPELINE_IS_NOTEBOOK = "PIPELINE_IS_NOTEBOOK"


class CreateWebappError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class CreateWorkspaceError(str, Enum):
    INVALID_SLUG = "INVALID_SLUG"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DAGRunOrderBy(str, Enum):
    EXECUTION_DATE_ASC = "EXECUTION_DATE_ASC"
    EXECUTION_DATE_DESC = "EXECUTION_DATE_DESC"


class DAGRunStatus(str, Enum):
    failed = "failed"
    queued = "queued"
    running = "running"
    stopped = "stopped"
    success = "success"
    terminating = "terminating"


class DAGRunTrigger(str, Enum):
    MANUAL = "MANUAL"
    SCHEDULED = "SCHEDULED"


class DHIS2ConnectionError(str, Enum):
    REQUEST_ERROR = "REQUEST_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class DHIS2ConnectionStatus(str, Enum):
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"
    UP = "UP"


class DHIS2MetadataType(str, Enum):
    DATASETS = "DATASETS"
    DATA_ELEMENTS = "DATA_ELEMENTS"
    DATA_ELEMENT_GROUPS = "DATA_ELEMENT_GROUPS"
    INDICATORS = "INDICATORS"
    INDICATOR_GROUPS = "INDICATOR_GROUPS"
    ORG_UNITS = "ORG_UNITS"
    ORG_UNIT_GROUPS = "ORG_UNIT_GROUPS"
    ORG_UNIT_LEVELS = "ORG_UNIT_LEVELS"


class DeclineWorkspaceInvitationError(str, Enum):
    INVITATION_NOT_FOUND = "INVITATION_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteAccessmodAnalysisError(str, Enum):
    DELETE_FAILED = "DELETE_FAILED"
    NOT_FOUND = "NOT_FOUND"


class DeleteAccessmodFilesetError(str, Enum):
    FILESET_IN_USE = "FILESET_IN_USE"
    NOT_FOUND = "NOT_FOUND"


class DeleteAccessmodProjectError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteAccessmodProjectMemberError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteBucketObjectError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteConnectionError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteDatasetError(str, Enum):
    DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteDatasetLinkError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteDatasetVersionError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    VERSION_NOT_FOUND = "VERSION_NOT_FOUND"


class DeleteMembershipError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteMetadataAttributeError(str, Enum):
    METADATA_ATTRIBUTE_NOT_FOUND = "METADATA_ATTRIBUTE_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    TARGET_NOT_FOUND = "TARGET_NOT_FOUND"


class DeletePipelineVersionError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    PIPELINE_VERSION_NOT_FOUND = "PIPELINE_VERSION_NOT_FOUND"


class DeleteTeamError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteTemplateVersionError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    TEMPLATE_VERSION_NOT_FOUND = "TEMPLATE_VERSION_NOT_FOUND"


class DeleteWebappError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WEBAPP_NOT_FOUND = "WEBAPP_NOT_FOUND"


class DeleteWorkspaceDatabaseTableError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    TABLE_NOT_FOUND = "TABLE_NOT_FOUND"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class DeleteWorkspaceError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteWorkspaceInvitationError(str, Enum):
    INVITATION_NOT_FOUND = "INVITATION_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DeleteWorkspaceMemberError(str, Enum):
    MEMBERSHIP_NOT_FOUND = "MEMBERSHIP_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class DenyAccessmodAccessRequestError(str, Enum):
    INVALID = "INVALID"


class DisableTwoFactorError(str, Enum):
    INVALID_OTP = "INVALID_OTP"
    NOT_ENABLED = "NOT_ENABLED"


class EnableTwoFactorError(str, Enum):
    ALREADY_ENABLED = "ALREADY_ENABLED"
    EMAIL_MISMATCH = "EMAIL_MISMATCH"


class FileSampleStatus(str, Enum):
    FAILED = "FAILED"
    FINISHED = "FINISHED"
    PROCESSING = "PROCESSING"


class FileType(str, Enum):
    directory = "directory"
    file = "file"


class GenerateChallengeError(str, Enum):
    CHALLENGE_ERROR = "CHALLENGE_ERROR"
    DEVICE_NOT_FOUND = "DEVICE_NOT_FOUND"


class GenerateNewDatabasePasswordError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class GeneratePipelineWebhookUrlError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    WEBHOOK_NOT_ENABLED = "WEBHOOK_NOT_ENABLED"


class GenerateWorkspaceTokenError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class IASOConnectionError(str, Enum):
    REQUEST_ERROR = "REQUEST_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class IASOMetadataType(str, Enum):
    IASO_FORMS = "IASO_FORMS"
    IASO_ORG_UNITS = "IASO_ORG_UNITS"
    IASO_PROJECTS = "IASO_PROJECTS"


class InviteWorkspaceMembershipError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class JoinWorkspaceError(str, Enum):
    ALREADY_ACCEPTED = "ALREADY_ACCEPTED"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INVITATION_NOT_FOUND = "INVITATION_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class LaunchAccessmodAnalysisError(str, Enum):
    LAUNCH_FAILED = "LAUNCH_FAILED"


class LaunchNotebookServerError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class LinkDatasetError(str, Enum):
    ALREADY_LINKED = "ALREADY_LINKED"
    DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class LoginError(str, Enum):
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_OTP = "INVALID_OTP"
    OTP_REQUIRED = "OTP_REQUIRED"


class MembershipRole(str, Enum):
    ADMIN = "ADMIN"
    REGULAR = "REGULAR"


class MessagePriority(str, Enum):
    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"
    WARNING = "WARNING"


class OrderByDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class ParameterType(str, Enum):
    bool = "bool"
    custom = "custom"
    dataset = "dataset"
    dhis2 = "dhis2"
    float = "float"
    gcs = "gcs"
    iaso = "iaso"
    int = "int"
    postgresql = "postgresql"
    s3 = "s3"
    str = "str"


class ParameterWidget(str, Enum):
    DHIS2_DATASETS = "DHIS2_DATASETS"
    DHIS2_DATA_ELEMENTS = "DHIS2_DATA_ELEMENTS"
    DHIS2_DATA_ELEMENT_GROUPS = "DHIS2_DATA_ELEMENT_GROUPS"
    DHIS2_INDICATORS = "DHIS2_INDICATORS"
    DHIS2_INDICATOR_GROUPS = "DHIS2_INDICATOR_GROUPS"
    DHIS2_ORG_UNITS = "DHIS2_ORG_UNITS"
    DHIS2_ORG_UNIT_GROUPS = "DHIS2_ORG_UNIT_GROUPS"
    DHIS2_ORG_UNIT_LEVELS = "DHIS2_ORG_UNIT_LEVELS"
    IASO_FORMS = "IASO_FORMS"
    IASO_ORG_UNITS = "IASO_ORG_UNITS"
    IASO_PROJECTS = "IASO_PROJECTS"


class PermissionMode(str, Enum):
    EDITOR = "EDITOR"
    OWNER = "OWNER"
    VIEWER = "VIEWER"


class PinDatasetError(str, Enum):
    LINK_NOT_FOUND = "LINK_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class PipelineError(str, Enum):
    CANNOT_UPDATE_NOTEBOOK_PIPELINE = "CANNOT_UPDATE_NOTEBOOK_PIPELINE"
    DUPLICATE_PIPELINE_VERSION_NAME = "DUPLICATE_PIPELINE_VERSION_NAME"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_CONFIG = "INVALID_CONFIG"
    INVALID_TIMEOUT_VALUE = "INVALID_TIMEOUT_VALUE"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_ALREADY_COMPLETED = "PIPELINE_ALREADY_COMPLETED"
    PIPELINE_ALREADY_STOPPED = "PIPELINE_ALREADY_STOPPED"
    PIPELINE_DOES_NOT_SUPPORT_PARAMETERS = "PIPELINE_DOES_NOT_SUPPORT_PARAMETERS"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    PIPELINE_VERSION_NOT_FOUND = "PIPELINE_VERSION_NOT_FOUND"
    TABLE_NOT_FOUND = "TABLE_NOT_FOUND"
    WORKSPACE_NOT_FOUND = "WORKSPACE_NOT_FOUND"


class PipelineNotificationLevel(str, Enum):
    ALL = "ALL"
    ERROR = "ERROR"


class PipelineRecipientError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    RECIPIENT_NOT_FOUND = "RECIPIENT_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"


class PipelineRunOrderBy(str, Enum):
    EXECUTION_DATE_ASC = "EXECUTION_DATE_ASC"
    EXECUTION_DATE_DESC = "EXECUTION_DATE_DESC"


class PipelineRunStatus(str, Enum):
    failed = "failed"
    queued = "queued"
    running = "running"
    stopped = "stopped"
    success = "success"
    terminating = "terminating"


class PipelineRunTrigger(str, Enum):
    manual = "manual"
    scheduled = "scheduled"
    webhook = "webhook"


class PipelineTemplateError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    PIPELINE_TEMPLATE_NOT_FOUND = "PIPELINE_TEMPLATE_NOT_FOUND"


class PipelineType(str, Enum):
    notebook = "notebook"
    zipFile = "zipFile"


class PrepareObjectDownloadError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class PrepareObjectUploadError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"


class PrepareVersionFileDownloadError(str, Enum):
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_NOT_UPLOADED = "FILE_NOT_UPLOADED"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class RegisterError(str, Enum):
    ALREADY_LOGGED_IN = "ALREADY_LOGGED_IN"
    EMAIL_TAKEN = "EMAIL_TAKEN"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    INVALID_TOKEN = "INVALID_TOKEN"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"


class RemoveFromFavoritesError(str, Enum):
    WEBAPP_NOT_FOUND = "WEBAPP_NOT_FOUND"


class RequestAccessmodAccessError(str, Enum):
    ALREADY_EXISTS = "ALREADY_EXISTS"
    INVALID = "INVALID"
    MUST_ACCEPT_TOS = "MUST_ACCEPT_TOS"


class ResendWorkspaceInvitationError(str, Enum):
    INVITATION_NOT_FOUND = "INVITATION_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class RunDAGError(str, Enum):
    DAG_NOT_FOUND = "DAG_NOT_FOUND"
    INVALID_CONFIG = "INVALID_CONFIG"


class SetDAGRunFavoriteError(str, Enum):
    INVALID = "INVALID"
    MISSING_LABEL = "MISSING_LABEL"
    NOT_FOUND = "NOT_FOUND"


class SetMetadataAttributeError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    TARGET_NOT_FOUND = "TARGET_NOT_FOUND"


class SetPasswordError(str, Enum):
    INVALID_PASSWORD = "INVALID_PASSWORD"
    INVALID_TOKEN = "INVALID_TOKEN"
    PASSWORD_MISMATCH = "PASSWORD_MISMATCH"
    USER_NOT_FOUND = "USER_NOT_FOUND"


class UpdateAccessmodAccessibilityAnalysisError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    NOT_FOUND = "NOT_FOUND"


class UpdateAccessmodFilesetError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateAccessmodProjectError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateAccessmodProjectMemberError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateAccessmodZonalStatisticsError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    NOT_FOUND = "NOT_FOUND"


class UpdateConnectionError(str, Enum):
    INVALID_SLUG = "INVALID_SLUG"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateDAGError(str, Enum):
    INVALID = "INVALID"
    NOT_FOUND = "NOT_FOUND"


class UpdateDatasetError(str, Enum):
    DATASET_NOT_FOUND = "DATASET_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateDatasetVersionError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    VERSION_NOT_FOUND = "VERSION_NOT_FOUND"


class UpdateMembershipError(str, Enum):
    INVALID_ROLE = "INVALID_ROLE"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdatePipelineError(str, Enum):
    INVALID_CONFIG = "INVALID_CONFIG"
    MISSING_VERSION_CONFIG = "MISSING_VERSION_CONFIG"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdatePipelineVersionError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateTeamError(str, Enum):
    NAME_DUPLICATE = "NAME_DUPLICATE"
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateTemplateError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateTemplateVersionError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateUserError(str, Enum):
    INVALID_LANGUAGE = "INVALID_LANGUAGE"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateWebappError(str, Enum):
    PERMISSION_DENIED = "PERMISSION_DENIED"
    WEBAPP_NOT_FOUND = "WEBAPP_NOT_FOUND"


class UpdateWorkspaceError(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpdateWorkspaceMemberError(str, Enum):
    MEMBERSHIP_NOT_FOUND = "MEMBERSHIP_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class UpgradePipelineVersionFromTemplateError(str, Enum):
    NO_NEW_TEMPLATE_VERSION_AVAILABLE = "NO_NEW_TEMPLATE_VERSION_AVAILABLE"
    PIPELINE_NOT_FOUND = "PIPELINE_NOT_FOUND"
    PIPELINE_NOT_FROM_TEMPLATE = "PIPELINE_NOT_FROM_TEMPLATE"


class VerifyDeviceError(str, Enum):
    INVALID_OTP = "INVALID_OTP"
    NO_DEVICE = "NO_DEVICE"


class WorkspaceInvitationStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    PENDING = "PENDING"


class WorkspaceMembershipRole(str, Enum):
    ADMIN = "ADMIN"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"
