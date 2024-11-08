/*
Snowflake Database grammar.
The MIT License (MIT).

Copyright (c) 2022, Michał Lorek.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

// =================================================================================
// Please reformat the grammr file before a change commit. See remorph/core/README.md
// For formatting, see: https://github.com/mike-lischke/antlr-format/blob/main/doc/formatting.md

// $antlr-format alignTrailingComments true
// $antlr-format columnLimit 150
// $antlr-format maxEmptyLinesToKeep 1
// $antlr-format reflowComments false
// $antlr-format useTab false
// $antlr-format allowShortRulesOnASingleLine true
// $antlr-format allowShortBlocksOnASingleLine true
// $antlr-format minEmptyLines 0
// $antlr-format alignSemicolons ownLine
// $antlr-format alignColons trailing
// $antlr-format singleLineOverrulesHangingColon true
// $antlr-format alignLexerCommands true
// $antlr-format alignLabels true
// $antlr-format alignTrailers true
// =================================================================================
lexer grammar SnowflakeLexer;

options {
    caseInsensitive = true;
}

tokens {
    STRING_CONTENT
}

ABORT                                         : 'ABORT';
ABORT_DETACHED_QUERY                          : 'ABORT_DETACHED_QUERY';
ABORT_STATEMENT                               : 'ABORT_STATEMENT';
ACCESS                                        : 'ACCESS';
ACCOUNT                                       : 'ACCOUNT';
ACCOUNTADMIN                                  : 'ACCOUNTADMIN';
ACCOUNTS                                      : 'ACCOUNTS';
ACTION                                        : 'ACTION';
ADD                                           : 'ADD';
ADMIN_NAME                                    : 'ADMIN_NAME';
ADMIN_PASSWORD                                : 'ADMIN_PASSWORD';
AES                                           : 'AES';
AFTER                                         : 'AFTER';
ALERT                                         : 'ALERT';
ALERTS                                        : 'ALERTS';
ALL                                           : 'ALL';
ALLOWED_ACCOUNTS                              : 'ALLOWED_ACCOUNTS';
ALLOWED_DATABASES                             : 'ALLOWED_DATABASES';
ALLOWED_INTEGRATION_TYPES                     : 'ALLOWED_INTEGRATION_TYPES';
ALLOWED_IP_LIST                               : 'ALLOWED_IP_LIST';
ALLOWED_SHARES                                : 'ALLOWED_SHARES';
ALLOWED_VALUES                                : 'ALLOWED_VALUES';
ALLOW_CLIENT_MFA_CACHING                      : 'ALLOW_CLIENT_MFA_CACHING';
ALLOW_DUPLICATE                               : 'ALLOW_DUPLICATE';
ALLOW_ID_TOKEN                                : 'ALLOW_ID_TOKEN';
ALLOW_OVERLAPPING_EXECUTION                   : 'ALLOW_OVERLAPPING_EXECUTION';
ALTER                                         : 'ALTER';
AND                                           : 'AND';
ANY                                           : 'ANY';
API                                           : 'API';
API_ALLOWED_PREFIXES                          : 'API_ALLOWED_PREFIXES';
API_AWS_ROLE_ARN                              : 'API_AWS_ROLE_ARN';
API_BLOCKED_PREFIXES                          : 'API_BLOCKED_PREFIXES';
API_INTEGRATION                               : 'API_INTEGRATION';
API_KEY                                       : 'API_KEY';
API_PROVIDER                                  : 'API_PROVIDER';
APPEND                                        : 'APPEND';
APPEND_ONLY                                   : 'APPEND_ONLY';
APPLY                                         : 'APPLY';
ARRAY_AGG                                     : 'ARRAY' '_'? 'AGG';
AS                                            : 'AS';
ASC                                           : 'ASC';
ATTACH                                        : 'ATTACH';
AT_KEYWORD                                    : 'AT';
AUTHORIZATION                                 : 'AUTHORIZATION';
AUTHORIZATIONS                                : 'AUTHORIZATIONS';
AUTO                                          : 'AUTO';
AUTOCOMMIT                                    : 'AUTOCOMMIT';
AUTOCOMMIT_API_SUPPORTED                      : 'AUTOCOMMIT_API_SUPPORTED';
AUTOINCREMENT                                 : 'AUTOINCREMENT';
AUTO_COMPRESS                                 : 'AUTO_COMPRESS';
AUTO_DETECT                                   : 'AUTO_DETECT';
AUTO_INGEST                                   : 'AUTO_INGEST';
AUTO_REFRESH                                  : 'AUTO_REFRESH';
AUTO_RESUME                                   : 'AUTO_RESUME';
AUTO_SUSPEND                                  : 'AUTO_SUSPEND';
AVRO                                          : 'AVRO';
AWS_KEY_ID                                    : 'AWS_KEY_ID';
AWS_ROLE                                      : 'AWS_ROLE';
AWS_SECRET_KEY                                : 'AWS_SECRET_KEY';
AWS_SNS                                       : 'AWS_SNS';
AWS_SNS_ROLE_ARN                              : 'AWS_SNS_ROLE_ARN';
AWS_SNS_TOPIC                                 : 'AWS_SNS_TOPIC';
AWS_SNS_TOPIC_ARN                             : 'AWS_SNS_TOPIC_ARN';
AWS_TOKEN                                     : 'AWS_TOKEN';
AZURE_AD_APPLICATION_ID                       : 'AZURE_AD_APPLICATION_ID';
AZURE_EVENT_GRID                              : 'AZURE_EVENT_GRID';
AZURE_EVENT_GRID_TOPIC_ENDPOINT               : 'AZURE_EVENT_GRID_TOPIC_ENDPOINT';
AZURE_SAS_TOKEN                               : 'AZURE_SAS_TOKEN';
AZURE_STORAGE_QUEUE_PRIMARY_URI               : 'AZURE_STORAGE_QUEUE_PRIMARY_URI';
AZURE_TENANT_ID                               : 'AZURE_TENANT_ID';
BASE64                                        : 'BASE64';
BEFORE                                        : 'BEFORE';
BEGIN                                         : 'BEGIN';
BERNOULLI                                     : 'BERNOULLI';
BETWEEN                                       : 'BETWEEN';
BINARY_AS_TEXT                                : 'BINARY_AS_TEXT';
BINARY_FORMAT                                 : 'BINARY_FORMAT';
BINARY_INPUT_FORMAT                           : 'BINARY_INPUT_FORMAT';
BINARY_OUTPUT_FORMAT                          : 'BINARY_OUTPUT_FORMAT';
BLOCK                                         : 'BLOCK';
BLOCKED_IP_LIST                               : 'BLOCKED_IP_LIST';
BLOCKED_ROLES_LIST                            : 'BLOCKED_ROLES_LIST';
BODY                                          : 'BODY';
BROTLI                                        : 'BROTLI';
BUSINESS_CRITICAL                             : 'BUSINESS_CRITICAL';
BY                                            : 'BY';
BZ2                                           : 'BZ2';
CALL                                          : 'CALL';
CALLED                                        : 'CALLED';
CALLER                                        : 'CALLER';
CASCADE                                       : 'CASCADE';
CASE                                          : 'CASE';
CASE_INSENSITIVE                              : 'CASE_INSENSITIVE';
CASE_SENSITIVE                                : 'CASE_SENSITIVE';
CAST                                          : 'CAST';
CHANGES                                       : 'CHANGES';
CHANGE_TRACKING                               : 'CHANGE_TRACKING';
CHANNELS                                      : 'CHANNELS';
CHAR                                          : 'CHAR';
CHARACTER                                     : 'CHARACTER';
CHECK                                         : 'CHECK';
CHECKSUM                                      : 'CHECKSUM';
CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS   : 'CLIENT_ENABLE_LOG_INFO_STATEMENT_PARAMETERS';
CLIENT_ENCRYPTION_KEY_SIZE                    : 'CLIENT_ENCRYPTION_KEY_SIZE';
CLIENT_MEMORY_LIMIT                           : 'CLIENT_MEMORY_LIMIT';
CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX    : 'CLIENT_METADATA_REQUEST_USE_CONNECTION_CTX';
CLIENT_METADATA_USE_SESSION_DATABASE          : 'CLIENT_METADATA_USE_SESSION_DATABASE';
CLIENT_PREFETCH_THREADS                       : 'CLIENT_PREFETCH_THREADS';
CLIENT_RESULT_CHUNK_SIZE                      : 'CLIENT_RESULT_CHUNK_SIZE';
CLIENT_RESULT_COLUMN_CASE_INSENSITIVE         : 'CLIENT_RESULT_COLUMN_CASE_INSENSITIVE';
CLIENT_SESSION_KEEP_ALIVE                     : 'CLIENT_SESSION_KEEP_ALIVE';
CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY : 'CLIENT_SESSION_KEEP_ALIVE_HEARTBEAT_FREQUENCY';
CLIENT_TIMESTAMP_TYPE_MAPPING                 : 'CLIENT_TIMESTAMP_TYPE_MAPPING';
CLONE                                         : 'CLONE';
CLUSTER                                       : 'CLUSTER';
CLUSTERING                                    : 'CLUSTERING';
COLLATE                                       : 'COLLATE';
COLLECTION                                    : 'COLLECTION';
COLUMN                                        : 'COLUMN';
COLUMNS                                       : 'COLUMNS';
COMMENT                                       : 'COMMENT';
COMMIT                                        : 'COMMIT';
COMPRESSION                                   : 'COMPRESSION';
CONDITION                                     : 'CONDITION';
CONFIGURATION                                 : 'CONFIGURATION';
CONNECT                                       : 'CONNECT';
CONNECTION                                    : 'CONNECTION';
CONNECTIONS                                   : 'CONNECTIONS';
CONSTRAINT                                    : 'CONSTRAINT';
CONTEXT_HEADERS                               : 'CONTEXT_HEADERS';
CONTINUE                                      : 'CONTINUE';
COPY                                          : 'COPY';
COPY_OPTIONS_                                 : 'COPY_OPTIONS';
CREATE                                        : 'CREATE';
CREDENTIALS                                   : 'CREDENTIALS';
CREDIT_QUOTA                                  : 'CREDIT_QUOTA';
CROSS                                         : 'CROSS';
CSV                                           : 'CSV';
CUBE                                          : 'CUBE';
CURRENT                                       : 'CURRENT';
CURRENT_DATE                                  : 'CURRENT_DATE';
CURRENT_TIME                                  : 'CURRENT_TIME';
CURRENT_TIMESTAMP                             : 'CURRENT_TIMESTAMP';
CURSOR                                        : 'CURSOR';
CUSTOM                                        : 'CUSTOM';
DAILY                                         : 'DAILY';
DATA                                          : 'DATA';
DATABASE                                      : 'DATABASE';
DATABASES                                     : 'DATABASES';
DATA_RETENTION_TIME_IN_DAYS                   : 'DATA_RETENTION_TIME_IN_DAYS';
DATE_FORMAT                                   : 'DATE_FORMAT';
DATE_INPUT_FORMAT                             : 'DATE_INPUT_FORMAT';
DATE_OUTPUT_FORMAT                            : 'DATE_OUTPUT_FORMAT';
DAYS_TO_EXPIRY                                : 'DAYS_TO_EXPIRY';
DECLARE                                       : 'DECLARE';
DEFAULT                                       : 'DEFAULT';
DEFAULT_DDL_COLLATION_                        : 'DEFAULT_DDL_COLLATION';
DEFAULT_NAMESPACE                             : 'DEFAULT_NAMESPACE';
DEFAULT_ROLE                                  : 'DEFAULT_ROLE';
DEFAULT_WAREHOUSE                             : 'DEFAULT_WAREHOUSE';
DEFERRABLE                                    : 'DEFERRABLE';
DEFERRED                                      : 'DEFERRED';
DEFINE                                        : 'DEFINE';
DEFINITION                                    : 'DEFINITION';
DEFLATE                                       : 'DEFLATE';
DELEGATED                                     : 'DELEGATED';
DELETE                                        : 'DELETE';
DELTA                                         : 'DELTA';
DENSE_RANK                                    : 'DENSE_RANK';
DESC                                          : 'DESC';
DESCRIBE                                      : 'DESCRIBE';
DIRECTION                                     : 'DIRECTION';
DIRECTORY                                     : 'DIRECTORY';
DISABLE                                       : 'DISABLE';
DISABLED                                      : 'DISABLED';
DISABLE_AUTO_CONVERT                          : 'DISABLE_AUTO_CONVERT';
DISABLE_SNOWFLAKE_DATA                        : 'DISABLE_SNOWFLAKE_DATA';
DISPLAY_NAME                                  : 'DISPLAY_NAME';
DISTINCT                                      : 'DISTINCT';
DO                                            : 'DO';
DOWNSTREAM                                    : 'DOWNSTREAM';
DROP                                          : 'DROP';
DYNAMIC                                       : 'DYNAMIC';
ECONOMY                                       : 'ECONOMY';
EDITION                                       : 'EDITION';
ELSE                                          : 'ELSE';
EMAIL                                         : 'EMAIL';
EMPTY_                                        : 'EMPTY';
EMPTY_FIELD_AS_NULL                           : 'EMPTY_FIELD_AS_NULL';
ENABLE                                        : 'ENABLE';
ENABLED                                       : 'ENABLED';
ENABLE_FOR_PRIVILEGE                          : 'ENABLE_FOR_PRIVILEGE';
ENABLE_INTERNAL_STAGES_PRIVATELINK            : 'ENABLE_INTERNAL_STAGES_PRIVATELINK';
ENABLE_OCTAL                                  : 'ENABLE_OCTAL';
ENABLE_QUERY_ACCELERATION                     : 'ENABLE_QUERY_ACCELERATION';
ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION      : 'ENABLE_UNLOAD_PHYSICAL_TYPE_OPTIMIZATION';
ENCODING                                      : 'ENCODING';
ENCRYPTION                                    : 'ENCRYPTION';
END                                           : 'END';
END_TIMESTAMP                                 : 'END_TIMESTAMP';
ENFORCED                                      : 'ENFORCED';
ENFORCE_LENGTH                                : 'ENFORCE_LENGTH';
ENFORCE_SESSION_POLICY                        : 'ENFORCE_SESSION_POLICY';
ENTERPRISE                                    : 'ENTERPRISE';
EQUALITY                                      : 'EQUALITY';
ERROR_INTEGRATION                             : 'ERROR_INTEGRATION';
ERROR_ON_COLUMN_COUNT_MISMATCH                : 'ERROR_ON_COLUMN_COUNT_MISMATCH';
ERROR_ON_NONDETERMINISTIC_MERGE               : 'ERROR_ON_NONDETERMINISTIC_MERGE';
ERROR_ON_NONDETERMINISTIC_UPDATE              : 'ERROR_ON_NONDETERMINISTIC_UPDATE';
ESCAPE                                        : 'ESCAPE';
ESCAPE_UNENCLOSED_FIELD                       : 'ESCAPE_UNENCLOSED_FIELD';
EVENT                                         : 'EVENT';
EXCEPT                                        : 'EXCEPT';
EXCEPTION                                     : 'EXCEPTION';
EXCHANGE                                      : 'EXCHANGE';
EXECUTE                                       : 'EXEC' 'UTE'?;
EXECUTION                                     : 'EXECUTION';
EXISTS                                        : 'EXISTS';
EXPIRY_DATE                                   : 'EXPIRY_DATE';
EXPLAIN                                       : 'EXPLAIN';
EXTERNAL                                      : 'EXTERNAL';
EXTERNAL_OAUTH                                : 'EXTERNAL_OAUTH';
EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST:
    'EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST'
;
EXTERNAL_OAUTH_ALLOWED_ROLES_LIST : 'EXTERNAL_OAUTH_ALLOWED_ROLES_LIST';
EXTERNAL_OAUTH_ANY_ROLE_MODE      : 'EXTERNAL_OAUTH_ANY_ROLE_MODE';
EXTERNAL_OAUTH_AUDIENCE_LIST      : 'EXTERNAL_OAUTH_AUDIENCE_LIST';
EXTERNAL_OAUTH_BLOCKED_ROLES_LIST : 'EXTERNAL_OAUTH_BLOCKED_ROLES_LIST';
EXTERNAL_OAUTH_ISSUER             : 'EXTERNAL_OAUTH_ISSUER';
EXTERNAL_OAUTH_JWS_KEYS_URL       : 'EXTERNAL_OAUTH_JWS_KEYS_URL';
EXTERNAL_OAUTH_RSA_PUBLIC_KEY     : 'EXTERNAL_OAUTH_RSA_PUBLIC_KEY';
EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2   : 'EXTERNAL_OAUTH_RSA_PUBLIC_KEY_2';
EXTERNAL_OAUTH_SCOPE_DELIMITER    : 'EXTERNAL_OAUTH_SCOPE_DELIMITER';
EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE:
    'EXTERNAL_OAUTH_SNOWFLAKE_USER_MAPPING_ATTRIBUTE'
;
EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM        : 'EXTERNAL_OAUTH_TOKEN_USER_MAPPING_CLAIM';
EXTERNAL_OAUTH_TYPE                            : 'EXTERNAL_OAUTH_TYPE';
EXTERNAL_STAGE                                 : 'EXTERNAL_STAGE';
EXTRACT                                        : 'EXTRACT';
FAILOVER                                       : 'FAILOVER';
FALSE                                          : 'FALSE';
FETCH                                          : 'FETCH';
FIELD_DELIMITER                                : 'FIELD_DELIMITER';
FIELD_OPTIONALLY_ENCLOSED_BY                   : 'FIELD_OPTIONALLY_ENCLOSED_BY';
FILE                                           : 'FILE';
FILES                                          : 'FILES';
FILE_EXTENSION                                 : 'FILE_EXTENSION';
FILE_FORMAT                                    : 'FILE_FORMAT';
FIRST                                          : 'FIRST';
FIRST_NAME                                     : 'FIRST_NAME';
FLATTEN                                        : 'FLATTEN';
FOR                                            : 'FOR';
FORCE                                          : 'FORCE';
FOREIGN                                        : 'FOREIGN';
FORMAT                                         : 'FORMAT';
FORMATS                                        : 'FORMATS';
FORMAT_NAME                                    : 'FORMAT_NAME';
FREQUENCY                                      : 'FREQUENCY';
FROM                                           : 'FROM';
FULL                                           : 'FULL';
FUNCTION                                       : 'FUNCTION';
FUNCTIONS                                      : 'FUNCTIONS';
FUTURE                                         : 'FUTURE';
GCP_PUBSUB                                     : 'GCP_PUBSUB';
GCP_PUBSUB_SUBSCRIPTION_NAME                   : 'GCP_PUBSUB_SUBSCRIPTION_NAME';
GCP_PUBSUB_TOPIC_NAME                          : 'GCP_PUBSUB_TOPIC_NAME';
GEO                                            : 'GEO';
GEOGRAPHY_OUTPUT_FORMAT                        : 'GEOGRAPHY_OUTPUT_FORMAT';
GEOMETRY_OUTPUT_FORMAT                         : 'GEOMETRY_OUTPUT_FORMAT';
GET                                            : 'GET';
GETDATE                                        : 'GETDATE';
GLOBAL                                         : 'GLOBAL';
GOOGLE_AUDIENCE                                : 'GOOGLE_AUDIENCE';
GRANT                                          : 'GRANT';
GRANTS                                         : 'GRANTS';
GROUP                                          : 'GROUP';
GROUPING                                       : 'GROUPING';
GROUPS                                         : 'GROUPS';
GZIP                                           : 'GZIP';
HANDLER                                        : 'HANDLER';
HAVING                                         : 'HAVING';
HEADER                                         : 'HEADER';
HEADERS                                        : 'HEADERS';
HEX                                            : 'HEX';
HISTORY                                        : 'HISTORY';
IDENTIFIER                                     : 'IDENTIFIER';
IDENTITY                                       : 'IDENTITY';
IF                                             : 'IF';
IFF                                            : 'IFF';
IGNORE                                         : 'IGNORE';
IGNORE_UTF8_ERRORS                             : 'IGNORE_UTF8_ERRORS';
ILIKE                                          : 'ILIKE';
IMMEDIATE                                      : 'IMMEDIATE';
IMMEDIATELY                                    : 'IMMEDIATELY';
IMMUTABLE                                      : 'IMMUTABLE';
IMPLICIT                                       : 'IMPLICIT';
IMPORT                                         : 'IMPORT';
IMPORTS                                        : 'IMPORTS';
IMPORTED                                       : 'IMPORTED';
IN                                             : 'IN';
INCREMENT                                      : 'INCREMENT';
INDEX                                          : 'INDEX';
INFORMATION                                    : 'INFORMATION';
INITIALLY                                      : 'INITIALLY';
INITIALLY_SUSPENDED                            : 'INITIALLY_SUSPENDED';
INITIAL_REPLICATION_SIZE_LIMIT_IN_TB           : 'INITIAL_REPLICATION_SIZE_LIMIT_IN_TB';
INNER                                          : 'INNER';
INPUT                                          : 'INPUT';
INSERT                                         : 'INSERT';
INSERT_ONLY                                    : 'INSERT_ONLY';
INT                                            : 'INT';
INTEGRATION                                    : 'INTEGRATION';
INTEGRATIONS                                   : 'INTEGRATIONS';
INTERSECT                                      : 'INTERSECT';
INTERVAL                                       : 'INTERVAL';
INTO                                           : 'INTO';
IS                                             : 'IS';
JAVA                                           : 'JAVA';
JAVASCRIPT                                     : 'JAVASCRIPT';
SCALA                                          : 'SCALA';
JDBC_TREAT_DECIMAL_AS_INT                      : 'JDBC_TREAT_DECIMAL_AS_INT';
JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC                : 'JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC';
JDBC_USE_SESSION_TIMEZONE                      : 'JDBC_USE_SESSION_TIMEZONE';
JOIN                                           : 'JOIN';
JSON                                           : 'JSON';
JSON_INDENT                                    : 'JSON_INDENT';
JS_TREAT_INTEGER_AS_BIGINT                     : 'JS_TREAT_INTEGER_AS_BIGINT';
KEY                                            : 'KEY';
KEYS                                           : 'KEYS';
KMS_KEY_ID                                     : 'KMS_KEY_ID';
LANGUAGE                                       : 'LANGUAGE';
LARGE                                          : 'LARGE';
LAST                                           : 'LAST';
LAST_NAME                                      : 'LAST_NAME';
LAST_QUERY_ID                                  : 'LAST_QUERY_ID';
LATERAL                                        : 'LATERAL';
LET                                            : 'LET';
LEAD                                           : 'LEAD';
LEFT                                           : 'LEFT';
LENGTH                                         : 'LENGTH';
LIKE                                           : 'LIKE';
LIMIT                                          : 'LIMIT';
LINEAR                                         : 'LINEAR';
LIST                                           : 'LIST';
LISTING                                        : 'LISTING';
LOCAL                                          : 'LOCAL';
LOCALTIME                                      : 'LOCALTIME';
LOCALTIMESTAMP                                 : 'LOCALTIMESTAMP';
LOCATION                                       : 'LOCATION';
LOCKS                                          : 'LOCKS';
LOCK_TIMEOUT                                   : 'LOCK_TIMEOUT';
LOGIN_NAME                                     : 'LOGIN_NAME';
LOOKER                                         : 'LOOKER';
LZO                                            : 'LZO';
MANAGE                                         : 'MANAGE';
MANAGED                                        : 'MANAGED';
MASKING                                        : 'MASKING';
MASTER_KEY                                     : 'MASTER_KEY';
MATCH                                          : 'MATCH';
MATCHED                                        : 'MATCHED';
MATCHES                                        : 'MATCHES';
MATCH_BY_COLUMN_NAME                           : 'MATCH_BY_COLUMN_NAME';
MATCH_RECOGNIZE                                : 'MATCH_RECOGNIZE';
MATERIALIZED                                   : 'MATERIALIZED';
MAX_BATCH_ROWS                                 : 'MAX_BATCH_ROWS';
MAX_CLUSTER_COUNT                              : 'MAX_CLUSTER_COUNT';
MAX_CONCURRENCY_LEVEL                          : 'MAX_CONCURRENCY_LEVEL';
MAX_DATA_EXTENSION_TIME_IN_DAYS                : 'MAX_DATA_EXTENSION_TIME_IN_DAYS';
MAX_SIZE                                       : 'MAX_SIZE';
MEASURES                                       : 'MEASURES';
MEDIUM                                         : 'MEDIUM';
MEMOIZABLE                                     : 'MEMOIZABLE';
MERGE                                          : 'MERGE';
MIDDLE_NAME                                    : 'MIDDLE_NAME';
MINS_TO_BYPASS_MFA                             : 'MINS_TO_BYPASS_MFA';
MINS_TO_UNLOCK                                 : 'MINS_TO_UNLOCK';
MINUS_                                         : 'MINUS';
MIN_CLUSTER_COUNT                              : 'MIN_CLUSTER_COUNT';
MIN_DATA_RETENTION_TIME_IN_DAYS                : 'MIN_DATA_RETENTION_TIME_IN_DAYS';
MODE                                           : 'MODE';
MODIFIED_AFTER                                 : 'MODIFIED_AFTER';
MODIFY                                         : 'MODIFY';
MONITOR                                        : 'MONITOR';
MONITORS                                       : 'MONITORS';
MONTHLY                                        : 'MONTHLY';
MOVE                                           : 'MOVE';
MULTI_STATEMENT_COUNT                          : 'MULTI_STATEMENT_COUNT';
MUST_CHANGE_PASSWORD                           : 'MUST_CHANGE_PASSWORD';
NAME                                           : 'NAME';
NATURAL                                        : 'NATURAL';
NETWORK                                        : 'NETWORK';
NETWORK_POLICY                                 : 'NETWORK_POLICY';
NEVER                                          : 'NEVER';
NEXT                                           : 'NEXT';
NEXTVAL                                        : 'NEXTVAL';
NO                                             : 'NO';
NONE                                           : 'NONE';
NOORDER                                        : 'NOORDER';
NORELY                                         : 'NORELY';
NOT                                            : 'NOT';
NOTIFICATION                                   : 'NOTIFICATION';
NOTIFICATION_INTEGRATION                       : 'NOTIFICATION_INTEGRATION';
NOTIFICATION_PROVIDER                          : 'NOTIFICATION_PROVIDER';
NOTIFY                                         : 'NOTIFY';
NOTIFY_USERS                                   : 'NOTIFY_USERS';
NOVALIDATE                                     : 'NOVALIDATE';
NULLS                                          : 'NULLS';
NULL                                           : 'NULL';
NULL_IF                                        : 'NULL_IF';
NUMBER                                         : 'NUMBER';
OAUTH                                          : 'OAUTH';
OAUTH_ALLOW_NON_TLS_REDIRECT_URI               : 'OAUTH_ALLOW_NON_TLS_REDIRECT_URI';
OAUTH_CLIENT                                   : 'OAUTH_CLIENT';
OAUTH_CLIENT_RSA_PUBLIC_KEY                    : 'OAUTH_CLIENT_RSA_PUBLIC_KEY';
OAUTH_CLIENT_RSA_PUBLIC_KEY_2                  : 'OAUTH_CLIENT_RSA_PUBLIC_KEY_2';
OAUTH_ENFORCE_PKCE                             : 'OAUTH_ENFORCE_PKCE';
OAUTH_ISSUE_REFRESH_TOKENS                     : 'OAUTH_ISSUE_REFRESH_TOKENS';
OAUTH_REDIRECT_URI                             : 'OAUTH_REDIRECT_URI';
OAUTH_REFRESH_TOKEN_VALIDITY                   : 'OAUTH_REFRESH_TOKEN_VALIDITY';
OAUTH_USE_SECONDARY_ROLES                      : 'OAUTH_USE_SECONDARY_ROLES';
OBJECT                                         : 'OBJECT';
OBJECTS                                        : 'OBJECTS';
OBJECT_TYPES                                   : 'OBJECT_TYPES';
OF                                             : 'OF';
OFFSET                                         : 'OFFSET';
OKTA                                           : 'OKTA';
OLD                                            : 'OLD';
OMIT                                           : 'OMIT';
ON                                             : 'ON';
ONE                                            : 'ONE';
ONLY                                           : 'ONLY';
ON_ERROR                                       : 'ON_ERROR';
OPERATE                                        : 'OPERATE';
OPTIMIZATION                                   : 'OPTIMIZATION';
OPTION                                         : 'OPTION';
OR                                             : 'OR';
ORC                                            : 'ORC';
ORDER                                          : 'ORDER';
ORGADMIN                                       : 'ORGADMIN';
ORGANIZATION                                   : 'ORGANIZATION';
OUTBOUND                                       : 'OUTBOUND';
OUTER                                          : 'OUTER';
OVER                                           : 'OVER';
OVERRIDE                                       : 'OVERRIDE';
OVERWRITE                                      : 'OVERWRITE';
OWNER                                          : 'OWNER';
OWNERSHIP                                      : 'OWNERSHIP';
PACKAGES                                       : 'PACKAGES';
PARALLEL                                       : 'PARALLEL';
PARAMETERS                                     : 'PARAMETERS';
PARQUET                                        : 'PARQUET';
PARTIAL                                        : 'PARTIAL';
PARTITION                                      : 'PARTITION';
PARTITION_TYPE                                 : 'PARTITION_TYPE';
PASSWORD                                       : 'PASSWORD';
PAST                                           : 'PAST';
PATH_                                          : 'PATH';
PATTERN                                        : 'PATTERN';
PER                                            : 'PER';
PERCENT                                        : 'PERCENT';
PERIODIC_DATA_REKEYING                         : 'PERIODIC_DATA_REKEYING';
PING_FEDERATE                                  : 'PING_FEDERATE';
PIPE                                           : 'PIPE';
PIPES                                          : 'PIPES';
PIPE_EXECUTION_PAUSED                          : 'PIPE_EXECUTION_PAUSED';
PIVOT                                          : 'PIVOT';
POLICIES                                       : 'POLICIES';
POLICY                                         : 'POLICY';
PORT                                           : 'PORT';
PRECEDING                                      : 'PRECEDING';
PREFIX                                         : 'PREFIX';
PRESERVE_SPACE                                 : 'PRESERVE_SPACE';
PREVENT_UNLOAD_TO_INLINE_URL                   : 'PREVENT_UNLOAD_TO_INLINE_URL';
PREVENT_UNLOAD_TO_INTERNAL_STAGES              : 'PREVENT_UNLOAD_TO_INTERNAL_STAGES';
PRE_AUTHORIZED_ROLES_LIST                      : 'PRE_AUTHORIZED_ROLES_LIST';
PRIMARY                                        : 'PRIMARY';
PRIOR                                          : 'PRIOR';
PRIVILEGES                                     : 'PRIVILEGES';
PROCEDURE                                      : 'PROCEDURE';
PROCEDURES                                     : 'PROCEDURES';
PROCEDURE_NAME                                 : 'PROCEDURE_NAME';
PROPERTY                                       : 'PROPERTY';
PROVIDER                                       : 'PROVIDER';
PUBLIC                                         : 'PUBLIC';
PURGE                                          : 'PURGE';
PUT                                            : 'PUT';
PYTHON                                         : 'PYTHON';
QUALIFY                                        : 'QUALIFY';
QUERIES                                        : 'QUERIES';
QUERY_ACCELERATION_MAX_SCALE_FACTOR            : 'QUERY_ACCELERATION_MAX_SCALE_FACTOR';
QUERY_TAG                                      : 'QUERY_TAG';
QUEUE                                          : 'QUEUE';
QUOTED_IDENTIFIERS_IGNORE_CASE                 : 'QUOTED_IDENTIFIERS_IGNORE_CASE';
RANGE                                          : 'RANGE';
RANK                                           : 'RANK';
RAW_DEFLATE                                    : 'RAW_DEFLATE';
READ                                           : 'READ';
READER                                         : 'READER';
RECLUSTER                                      : 'RECLUSTER';
RECORD_DELIMITER                               : 'RECORD_DELIMITER';
RECURSIVE                                      : 'RECURSIVE';
REFERENCES                                     : 'REFERENCES';
REFERENCE_USAGE                                : 'REFERENCE_USAGE';
REFRESH                                        : 'REFRESH';
REFRESH_ON_CREATE                              : 'REFRESH_ON_CREATE';
REGION                                         : 'REGION';
REGIONS                                        : 'REGIONS';
REGION_GROUP                                   : 'REGION_GROUP';
RELY                                           : 'RELY';
REMOVE                                         : 'REMOVE';
RENAME                                         : 'RENAME';
REPEATABLE                                     : 'REPEATABLE';
REPLACE                                        : 'REPLACE';
REPLACE_INVALID_CHARACTERS                     : 'REPLACE_INVALID_CHARACTERS';
REPLICA                                        : 'REPLICA';
REPLICATION                                    : 'REPLICATION';
REPLICATION_SCHEDULE                           : 'REPLICATION_SCHEDULE';
REQUEST_TRANSLATOR                             : 'REQUEST_TRANSLATOR';
REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION : 'REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION';
REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION:
    'REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION'
;
RESET                                    : 'RESET';
RESOURCE                                 : 'RESOURCE';
RESOURCES                                : 'RESOURCES';
RESOURCE_MONITOR                         : 'RESOURCE_MONITOR';
RESPECT                                  : 'RESPECT';
RESPONSE_TRANSLATOR                      : 'RESPONSE_TRANSLATOR';
RESTRICT                                 : 'RESTRICT';
RESTRICTIONS                             : 'RESTRICTIONS';
RESULT                                   : 'RESULT';
RESUME                                   : 'RESUME';
RETURN                                   : 'RETURN';
RETURNS                                  : 'RETURNS';
RETURN_ALL_ERRORS                        : 'RETURN_ALL_ERRORS';
RETURN_ERRORS                            : 'RETURN_ERRORS';
RETURN_FAILED_ONLY                       : 'RETURN_FAILED_ONLY';
RETURN_N_ROWS                            : 'RETURN_' DEC_DIGIT+ '_ROWS';
RETURN_ROWS                              : 'RETURN_ROWS';
REVOKE                                   : 'REVOKE';
RIGHT                                    : 'RIGHT';
RLIKE                                    : 'RLIKE';
ROLE                                     : 'ROLE';
ROLES                                    : 'ROLES';
ROLLBACK                                 : 'ROLLBACK';
ROLLUP                                   : 'ROLLUP';
ROW                                      : 'ROW';
ROWS                                     : 'ROWS';
ROWS_PER_RESULTSET                       : 'ROWS_PER_RESULTSET';
RSA_PUBLIC_KEY                           : 'RSA_PUBLIC_KEY';
RSA_PUBLIC_KEY_2                         : 'RSA_PUBLIC_KEY_2';
RUN_AS_ROLE                              : 'RUN_AS_ROLE';
RUNTIME_VERSION                          : 'RUNTIME_VERSION';
SAML2                                    : 'SAML2';
SAML2_ENABLE_SP_INITIATED                : 'SAML2_ENABLE_SP_INITIATED';
SAML2_FORCE_AUTHN                        : 'SAML2_FORCE_AUTHN';
SAML2_ISSUER                             : 'SAML2_ISSUER';
SAML2_POST_LOGOUT_REDIRECT_URL           : 'SAML2_POST_LOGOUT_REDIRECT_URL';
SAML2_PROVIDER                           : 'SAML2_PROVIDER';
SAML2_REQUESTED_NAMEID_FORMAT            : 'SAML2_REQUESTED_NAMEID_FORMAT';
SAML2_SIGN_REQUEST                       : 'SAML2_SIGN_REQUEST';
SAML2_SNOWFLAKE_ACS_URL                  : 'SAML2_SNOWFLAKE_ACS_URL';
SAML2_SNOWFLAKE_ISSUER_URL               : 'SAML2_SNOWFLAKE_ISSUER_URL';
SAML2_SNOWFLAKE_X509_CERT                : 'SAML2_SNOWFLAKE_X509_CERT';
SAML2_SP_INITIATED_LOGIN_PAGE_LABEL      : 'SAML2_SP_INITIATED_LOGIN_PAGE_LABEL';
SAML2_SSO_URL                            : 'SAML2_SSO_URL';
SAML2_X509_CERT                          : 'SAML2_X509_CERT';
SAML_IDENTITY_PROVIDER                   : 'SAML_IDENTITY_PROVIDER';
SAMPLE                                   : 'SAMPLE';
SAVE_OLD_URL                             : 'SAVE_OLD_URL';
SCALING_POLICY                           : 'SCALING_POLICY';
SCHEDULE                                 : 'SCHEDULE';
SCHEMA                                   : 'SCHEMA';
SCHEMAS                                  : 'SCHEMAS';
SCIM                                     : 'SCIM';
SCIM_CLIENT                              : 'SCIM_CLIENT';
SEARCH                                   : 'SEARCH';
SECONDARY                                : 'SECONDARY';
SECURE                                   : 'SECURE';
SECURITY                                 : 'SECURITY';
SECURITYADMIN                            : 'SECURITYADMIN';
SEED                                     : 'SEED';
SELECT                                   : 'SELECT';
SEQUENCE                                 : 'SEQUENCE';
SEQUENCES                                : 'SEQUENCES';
SESSION                                  : 'SESSION';
SESSION_IDLE_TIMEOUT_MINS                : 'SESSION_IDLE_TIMEOUT_MINS';
SESSION_POLICY                           : 'SESSION_POLICY';
SESSION_UI_IDLE_TIMEOUT_MINS             : 'SESSION_UI_IDLE_TIMEOUT_MINS';
SET                                      : 'SET';
SETS                                     : 'SETS';
SHARE                                    : 'SHARE';
SHARES                                   : 'SHARES';
SHARE_RESTRICTIONS                       : 'SHARE_RESTRICTIONS';
SHOW                                     : 'SHOW';
SHOW_INITIAL_ROWS                        : 'SHOW_INITIAL_ROWS';
SIMPLE                                   : 'SIMPLE';
SIMULATED_DATA_SHARING_CONSUMER          : 'SIMULATED_DATA_SHARING_CONSUMER';
SIZE_LIMIT                               : 'SIZE_LIMIT';
SKIP_                                    : 'SKIP';
SKIP_BLANK_LINES                         : 'SKIP_BLANK_LINES';
SKIP_BYTE_ORDER_MARK                     : 'SKIP_BYTE_ORDER_MARK';
SKIP_FILE                                : 'SKIP_FILE';
SKIP_FILE_N                              : 'SKIP_FILE_' DEC_DIGIT+;
SKIP_HEADER                              : 'SKIP_HEADER';
SMALL                                    : 'SMALL';
SNAPPY                                   : 'SNAPPY';
SNAPPY_COMPRESSION                       : 'SNAPPY_COMPRESSION';
SNOWFLAKE_FULL                           : 'SNOWFLAKE_FULL';
SNOWFLAKE_SSE                            : 'SNOWFLAKE_SSE';
SOME                                     : 'SOME';
SOURCE                                   : 'SOURCE';
SOURCE_COMPRESSION                       : 'SOURCE_COMPRESSION';
SQL                                      : 'SQL';
SSO_LOGIN_PAGE                           : 'SSO_LOGIN_PAGE';
STAGE                                    : 'STAGE';
STAGES                                   : 'STAGES';
STAGE_COPY_OPTIONS                       : 'STAGE_COPY_OPTIONS';
STAGE_FILE_FORMAT                        : 'STAGE_FILE_FORMAT';
STANDARD                                 : 'STANDARD';
START                                    : 'START';
STARTS                                   : 'STARTS';
START_TIMESTAMP                          : 'START_TIMESTAMP';
STATE                                    : 'STATE';
STATEMENT                                : 'STATEMENT';
STATEMENT_QUEUED_TIMEOUT_IN_SECONDS      : 'STATEMENT_QUEUED_TIMEOUT_IN_SECONDS';
STATEMENT_TIMEOUT_IN_SECONDS             : 'STATEMENT_TIMEOUT_IN_SECONDS';
STATS                                    : 'STATS';
STORAGE                                  : 'STORAGE';
STORAGE_ALLOWED_LOCATIONS                : 'STORAGE_ALLOWED_LOCATIONS';
STORAGE_AWS_OBJECT_ACL                   : 'STORAGE_AWS_OBJECT_ACL';
STORAGE_AWS_ROLE_ARN                     : 'STORAGE_AWS_ROLE_ARN';
STORAGE_BLOCKED_LOCATIONS                : 'STORAGE_BLOCKED_LOCATIONS';
STORAGE_INTEGRATION                      : 'STORAGE_INTEGRATION';
STORAGE_PROVIDER                         : 'STORAGE_PROVIDER';
STREAM                                   : 'STREAM';
STREAMS                                  : 'STREAMS';
STRICT                                   : 'STRICT';
STRICT_JSON_OUTPUT                       : 'STRICT_JSON_OUTPUT';
STRIP_NULL_VALUES                        : 'STRIP_NULL_VALUES';
STRIP_OUTER_ARRAY                        : 'STRIP_OUTER_ARRAY';
STRIP_OUTER_ELEMENT                      : 'STRIP_OUTER_ELEMENT';
SUBSTRING                                : 'SUBSTRING';
SUSPEND                                  : 'SUSPEND';
SUSPENDED                                : 'SUSPENDED';
SUSPEND_IMMEDIATE                        : 'SUSPEND_IMMEDIATE';
SUSPEND_TASK_AFTER_NUM_FAILURES          : 'SUSPEND_TASK_AFTER_NUM_FAILURES';
SWAP                                     : 'SWAP';
SYNC_PASSWORD                            : 'SYNC_PASSWORD';
SYSADMIN                                 : 'SYSADMIN';
SYSTEM                                   : 'SYSTEM';
TABLE                                    : 'TABLE';
TABLEAU_DESKTOP                          : 'TABLEAU_DESKTOP';
TABLEAU_SERVER                           : 'TABLEAU_SERVER';
TABLES                                   : 'TABLES';
TABLESAMPLE                              : 'TABLESAMPLE';
TABLE_FORMAT                             : 'TABLE_FORMAT';
TABULAR                                  : 'TABULAR';
TAG                                      : 'TAG';
TAGS                                     : 'TAGS';
TARGET_LAG                               : 'TARGET_LAG';
TASK                                     : 'TASK';
TASKS                                    : 'TASKS';
TEMP                                     : 'TEMP';
TEMPORARY                                : 'TEMPORARY';
TERSE                                    : 'TERSE';
THEN                                     : 'THEN';
TIME                                     : 'TIME';
TIMEDIFF                                 : 'TIMEDIFF';
TIMESTAMP                                : 'TIMESTAMP';
TIMESTAMP_DAY_IS_ALWAYS_24H              : 'TIMESTAMP_DAY_IS_ALWAYS_24H';
TIMESTAMP_FORMAT                         : 'TIMESTAMP_FORMAT';
TIMESTAMP_INPUT_FORMAT                   : 'TIMESTAMP_INPUT_FORMAT';
TIMESTAMP_LTZ                            : 'TIMESTAMP' '_'? 'LTZ';
TIMESTAMP_LTZ_OUTPUT_FORMAT              : 'TIMESTAMP_LTZ_OUTPUT_FORMAT';
TIMESTAMP_NTZ                            : 'TIMESTAMP' '_'? 'NTZ';
TIMESTAMP_NTZ_OUTPUT_FORMAT              : 'TIMESTAMP_NTZ_OUTPUT_FORMAT';
TIMESTAMP_OUTPUT_FORMAT                  : 'TIMESTAMP_OUTPUT_FORMAT';
TIMESTAMP_TYPE_MAPPING                   : 'TIMESTAMP_TYPE_MAPPING';
TIMESTAMP_TZ                             : 'TIMESTAMP' '_'? 'TZ';
TIMESTAMP_TZ_OUTPUT_FORMAT               : 'TIMESTAMP_TZ_OUTPUT_FORMAT';
TIMEZONE                                 : 'TIMEZONE';
TIME_FORMAT                              : 'TIME_FORMAT';
TIME_INPUT_FORMAT                        : 'TIME_INPUT_FORMAT';
TIME_OUTPUT_FORMAT                       : 'TIME_OUTPUT_FORMAT';
TO                                       : 'TO';
TOP                                      : 'TOP';
TRANSACTION                              : 'TRANSACTION';
TRANSACTIONS                             : 'TRANSACTIONS';
TRANSACTION_ABORT_ON_ERROR               : 'TRANSACTION_ABORT_ON_ERROR';
TRANSACTION_DEFAULT_ISOLATION_LEVEL      : 'TRANSACTION_DEFAULT_ISOLATION_LEVEL';
TRANSIENT                                : 'TRANSIENT';
TRIGGERS                                 : 'TRIGGERS';
TRIM_SPACE                               : 'TRIM_SPACE';
TRUE                                     : 'TRUE';
TRUNCATE                                 : 'TRUNCATE';
TRUNCATECOLUMNS                          : 'TRUNCATECOLUMNS';
TRY_CAST                                 : 'TRY_CAST';
TWO_DIGIT_CENTURY_START                  : 'TWO_DIGIT_CENTURY_START';
TYPE                                     : 'TYPE';
UNBOUNDED                                : 'UNBOUNDED';
UNDROP                                   : 'UNDROP';
UNION                                    : 'UNION';
UNIQUE                                   : 'UNIQUE';
UNMATCHED                                : 'UNMATCHED';
UNPIVOT                                  : 'UNPIVOT';
UNSET                                    : 'UNSET';
UNSUPPORTED_DDL_ACTION                   : 'UNSUPPORTED_DDL_ACTION';
UPDATE                                   : 'UPDATE';
URL                                      : 'URL';
USAGE                                    : 'USAGE';
USE                                      : 'USE';
USER                                     : 'USER';
USERADMIN                                : 'USERADMIN';
USERS                                    : 'USERS';
USER_SPECIFIED                           : 'USER_SPECIFIED';
USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE : 'USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE';
USER_TASK_TIMEOUT_MS                     : 'USER_TASK_TIMEOUT_MS';
USE_ANY_ROLE                             : 'USE_ANY_ROLE';
USE_CACHED_RESULT                        : 'USE_CACHED_RESULT';
USING                                    : 'USING';
UTF8                                     : 'UTF8';
VALIDATE                                 : 'VALIDATE';
VALIDATION_MODE                          : 'VALIDATION_MODE';
VALUE                                    : 'VALUE';
VALUES                                   : 'VALUES';
VARIABLES                                : 'VARIABLES';
VERSION                                  : 'VERSION';
VIEW                                     : 'VIEW';
VIEWS                                    : 'VIEWS';
VOLATILE                                 : 'VOLATILE';
WAREHOUSE                                : 'WAREHOUSE';
WAREHOUSES                               : 'WAREHOUSES';
WAREHOUSE_SIZE                           : 'WAREHOUSE_SIZE';
WAREHOUSE_TYPE                           : 'WAREHOUSE_TYPE';
WEEKLY                                   : 'WEEKLY';
WEEK_OF_YEAR_POLICY                      : 'WEEK_OF_YEAR_POLICY';
WEEK_START                               : 'WEEK_START';
WHEN                                     : 'WHEN';
WHERE                                    : 'WHERE';
WITH                                     : 'WITH';
WITHIN                                   : 'WITHIN';
WORK                                     : 'WORK';
WRITE                                    : 'WRITE';
X4LARGE                                  : 'X4LARGE';
X5LARGE                                  : 'X5LARGE';
X6LARGE                                  : 'X6LARGE';
XLARGE                                   : 'XLARGE';
XML                                      : 'XML';
XSMALL                                   : 'XSMALL';
XXLARGE                                  : 'XXLARGE';
XXXLARGE                                 : 'XXXLARGE';
YEARLY                                   : 'YEARLY';
ZSTD                                     : 'ZSTD';

ARRAY            : 'ARRAY';
BIGINT           : 'BIGINT';
BINARY           : 'BINARY';
BOOLEAN          : 'BOOLEAN';
BYTEINT          : 'BYTEINT';
CHAR_VARYING     : 'CHAR VARYING';
DATE             : 'DATE';
DATETIME         : 'DATETIME';
DECIMAL_         : 'DECIMAL';
DOUBLE           : 'DOUBLE';
DOUBLE_PRECISION : 'DOUBLE PRECISION';
FLOAT4           : 'FLOAT4';
FLOAT8           : 'FLOAT8';
FLOAT_           : 'FLOAT';
FLOOR            : 'FLOOR';
FOLLOWING        : 'FOLLOWING';
GEOGRAPHY        : 'GEOGRAPHY';
GEOMETRY         : 'GEOMETRY';
INTEGER          : 'INTEGER';
NCHAR            : 'NCHAR';
NCHAR_VARYING    : 'NCHAR VARYING';
NUMERIC          : 'NUMERIC';
NVARCHAR2        : 'NVARCHAR2';
NVARCHAR         : 'NVARCHAR';
REAL_            : 'REAL';
RESULTSET        : 'RESULTSET';
SMALLINT         : 'SMALLINT';
STRING_          : 'STRING';
TEXT             : 'TEXT';
TINYINT          : 'TINYINT';
VARBINARY        : 'VARBINARY';
VARCHAR          : 'VARCHAR';
VARIANT          : 'VARIANT';

LISTAGG: 'LISTAGG';

DUMMY:
    'DUMMY'
; //Dummy is not a keyword but rules reference it in unfinished grammar - need to get rid

fragment SPACE:
    [ \t\r\n\u000c\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u202f\u205f\u3000]+
;

WS: SPACE -> channel(HIDDEN);

SQL_COMMENT    : '/*' (SQL_COMMENT | .)*? '*/' -> channel(HIDDEN);
LINE_COMMENT   : '--' ~[\r\n]*                 -> channel(HIDDEN);
LINE_COMMENT_2 : '//' ~[\r\n]*                 -> channel(HIDDEN);

// TODO: ID can be not only Latin.
DOUBLE_QUOTE_ID    : '"' ('""' | ~[\r\n"])* '"';
DOUBLE_QUOTE_BLANK : '""';

ID  : [A-Z_] [A-Z0-9_@$]*;
ID2 : DOLLAR [A-Z_] [A-Z0-9_]*;

DOLLAR_STRING: '$$' ('\\$' | '$' ~'$' | ~'$')*? '$$';

DECIMAL : DEC_DIGIT+;
FLOAT   : DEC_DOT_DEC;
REAL    : (DECIMAL | DEC_DOT_DEC) 'E' [+-]? DEC_DIGIT+;

fragment HexDigit  : [0-9a-f];
fragment HexString : [A-Z0-9|.] [A-Z0-9+\-|.]*;

BANG  : '!';
ARROW : '->';
ASSOC : '=>';

NE   : '!=';
LTGT : '<>';
EQ   : '=';
GT   : '>';
GE   : '>=';
LT   : '<';
LE   : '<=';

ASSIGN      : ':=';
PIPE_PIPE   : '||';
DOT         : '.';
AT          : '@';
DOLLAR      : '$';
L_PAREN     : '(';
R_PAREN     : ')';
LSB         : '[';
RSB         : ']';
LCB         : '{';
RCB         : '}';
COMMA       : ',';
SEMI        : ';';
COLON       : ':';
COLON_COLON : '::';
STAR        : '*';
DIVIDE      : '/';
MODULE      : '%';
PLUS        : '+';
MINUS       : '-';
TILDA       : '~';
AMP         : '&';

// A question mark can be used as a placeholder for a prepared statement that will use binding.
PARAM: '?';

fragment DEC_DOT_DEC : DEC_DIGIT+ DOT DEC_DIGIT+ | DEC_DIGIT+ DOT | DOT DEC_DIGIT+;
fragment DEC_DIGIT   : [0-9];

SQLCOMMAND:
    '!' SPACE? (
        'abort'
        | 'connect'
        | 'define'
        | 'edit'
        | 'exit'
        | 'help'
        | 'options'
        | 'pause'
        | 'print'
        | 'queries'
        | 'quit'
        | 'rehash'
        | 'result'
        | 'set'
        | 'source'
        | 'spool'
        | 'system'
        | 'variables'
    ) ~[\r\n]*
;

STRING_START: '\'' -> pushMode(stringMode);

// This lexer rule is needed so that any unknown character in the lexicon does not
// cause an incomprehensible error message from teh lexer. This rule will allow the parser to issue
// something more meaningful and perform error recovery as the lexer CANNOT raise an error - it
// will alwys match at least one character using this catch-all rule.
//
// !IMPORTANT! - Always leave this as the last lexer rule, before the mode definitions
BADCHAR: .;

// ================================================================================================
// LEXICAL MODES
//
// Lexical modes are used to allow the lexer to return different token types than the main lexer
// and are triggered by a main lexer rule matching a specific token. The mode is ended by matching
// a specific lexical sequence in the input stream. Note that this is a lexical trigger only and is
// not influenced by the parser state as the paresr does NOT direct the lexer:
//
// 1) The lexer runs against the entire input sequence and returns tokens to the parser.
// 2) THEN the parser uses the tokens to build the parse tree - it cannot therefore influence the
//    lexer in any way.

// In string mode we are separating out normal string literals from defined variable
// references, so that they can be translated from Snowflakey syntax to Databricks SQL syntax.
// This mode is trigered when we hit a single quote in the lexer and ends when we hit the
// terminating single quote minus the usual escape character processing.
mode stringMode;

// An element that is a variable reference can be &{variable} or just &variable. They are
// separated out in case there is any difference needed in translation/generation. A single
// & is placed in a string by using &&.

// We exit the stringMode when we see the terminating single quote.
//
STRING_END: '\'' -> popMode;

STRING_AMP    : '&' -> type(STRING_CONTENT);
STRING_AMPAMP : '&&';

// Note that snowflake also allows $var, and :var
// if they are allowed in literal strings// then they can be added here.
//
VAR_SIMPLE  : '&' [A-Z_] [A-Z0-9_]*;
VAR_COMPLEX : '&{' [A-Z_] [A-Z0-9_]* '}';

// TODO: Do we also need \xHH hex and \999 octal escapes?
STRING_UNICODE : '\\' 'u' HexDigit HexDigit HexDigit HexDigit;
STRING_ESCAPE  : '\\' .;
STRING_SQUOTE  : '\'\'';

// Anything that is not a variable reference is just a normal piece of text.
STRING_BIT: ~['\\&]+ -> type(STRING_CONTENT);