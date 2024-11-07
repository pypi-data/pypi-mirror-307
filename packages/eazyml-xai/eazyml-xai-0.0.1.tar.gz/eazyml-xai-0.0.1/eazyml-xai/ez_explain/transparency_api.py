VALID_DATATYPE_LIST = '''The valid datatype for this parameter is a list'''
VALID_DATATYPE_DICT = '''The valid datatype for this parameter is a dict'''
VALID_DATATYPE = '''The valid datatype for this parameter is a %s.'''
INVALID_DATATYPE_PARAMETER = '''The parameter %s has invalid data type or values.'''
INVALID_MODEL_NAME_PARAMETER = '''The model name in %s has been spelt wrongly or not given in string format..'''
INVALID_WEIGHTS = '''Please provide positive integer weight for the ensemble constituents in place of %s.'''
WEIGHTS_MISMATCH = '''The weights given by the user in %s are not matching in number with models given.'''
ENSEMBLE_MODEL_TYPE_ALLOWED = '''%s is not a predictive model. EazyML supports ensembles for Predictive Classification and Regression models only.'''
EXPORT_MODEL_TYPE_ALLOWED = '''%s is not a predictive/timeseries model. EazyML supports export for Predictive and Timeseries models only.'''
EXPORT_MODEL_TYPE_FOR_DI_ALLOWED = '''%s is not a augmented intelligence model. export_augi and docker_augi are only supported for Augmented Intelligence models only.'''
ENSEMBLE_CONSTITUENT_EMPTY = '''%s is an empty list. Please provide constituent model names to build ensemble.'''
INVALID_DICT = '''One or more dictionary specified in the parameters is not valid. A valid dictionary should have a list of strings as valid values for each key. The key should be a string'''
ERROR_MESSAGE_YES_NO_ONLY = '''The parameter %s has invalid data type or values. The valid set of values are yes or no.'''
ERROR_MESSAGE_MODEL_TYPE = '''The parameter %s has invalid data type or values. The valid set of values are predictive or timeseries.'''
OUTCOME_NOT_PRESENT_IN_DATA = '''The outcome column is either not present in the dataset or has been dropped as part of discard columns or id column'''
ERROR_MESSAGE_OUTCOME_TYPE = '''The parameter %s has invalid data type or values. The valid set of values are categorical or numeric'''
MANDATORY_PARAMETER = '''The request must have the parameter %s.'''
BAD_JSON = ''' Bad JSON format '''
INVALID_CREDENTIALS = "Invalid Credentials"
INTERNAL_SERVER_ERROR = "Internal Server Error"
INVALID_FILE = "Please upload a valid file"
DATASET_UPLOAD_SUCCESS = "Dataset is uploaded successfully!"
OUTCOME_SET_SUCCESS = "Outcome has been set successfully!"
DATASET_NOT_FOUND = "No dataset found for the given dataset_id"
COLUMN_NOT_FOUND = ''' Cannot find the column %s '''
TYPE_CONVERSION_FAILED = ''' %s could not be converted to %s '''
TYPE_CONVERSION_SUCCESSFULL = "The type conversion is successful!"
MODEL_NOT_BUILT = ''' Please build the model before calling this API'''
MODEL_BUILT = "The model has been built."
MODEL_NOT_FOUND = "The model_id entered is not valid"
NOT_AUGI_MODEL = "Model ID - %s is not a augmented intelligence model. Please provide an augmented intelligence Model ID to do validations on test data."
NOT_PREDICTIVE_MODEL = "Model ID - %s is not a predictive model. Please provide a predictive Model ID to generate predictions."
NOT_PREDICTIVE_MODEL_LE = "Model ID - %s is not a predictive model. Please provide a predictive Model ID to get the explanations."
INVALID_MODEL_CHOSEN = ''' Please choose a valid model. Model should be one of %s  '''
INCONSISTENT_DATASET = "The uploaded dataset is not consistent with the training dataset."
PREDICTION_PROGRESS = " The Prediction is ongoing"
PREDICTION_SUCCESS = " The Prediction is successful"
VALIDATION_SUCCESS = " AUGI validation is finished"
PREDICTION_FAILED = "Prediction Failed"
VALIDATION_FAILED = "Validation Failed"
UNAUTHORIZED_ACCESS = "Unauthorized Access"
DATA_HAS_MISSING_VALUES = "Dataset has missing values. Please call /ez_impute first or call /ez_load with impute as yes."
IMPUTE_SUCCESS = "Imputation is successful."
EMPTINESS_QUALITY_SUCCESS = "Emptiness quality has been calculated successfully."
OUTLIER_QUALITY_SUCESS = "Outliers has been detected successfully."
MODEL_BUILD_NOT_POSSIBLE = "Model Building is not possible. The reasons could be: 1) The number of numeric columns after encoding is zero. 2)All the models are disabled in the config file."
MODEL_BUILDING_PROGRESS = "Model Building is in progress."
MODEL_BUILDING_INIT = "Model initialization done. Please call build model API to initiate build models."
FEATURE_EXTRACTION_PROGRESS = "Feature extraction is in progress."
DATA_HAS_MISSING_VALUES = "Dataset has missing values. Please call /ez_impute first"
IMPUTE_SUCCESS = "Imputation is successful"
LOGIN_SUCCESS = "Authentication successful"
OUTCOME_COULD_NOT_BE_SET = ''' Could not set %s as outcome '''
TEXT_OUTCOME_NOT_POSSIBLE = ''' Could not set %s as outcome as it is of text type '''
NO_MISSING_VALUES = "There are no missing values present in the training data that was uploaded. Hence no records were imputed."
POSSIBLE_DATATYPES = ''' The data types must be one of [%s, %s, %s, %s] '''
ALL_STR_PARAM = "All the parameters should be of type string."
PARAM_SHOULD_BE_NUMERIC =  "Parameters cannot be decoded. It should only be a numeric string."
TEST_DATASET_NOT_FOUND =  "No prediction dataset found with such id."
EXPLANATION_SUCCESS = "Explanation of the prediction point is as follows"
EXPLANATION_FAILURE= "Explanation of the prediction point cannot be fetched."
DATASET_FETCH_SUCCESS = "The dataset is as shown"
DATASET_FETCH_FAIL = "The processed data could not be fetched."
MODEL_STATUS_FAIL = "The model status could not be fetched. Please try again after some time."
DT_COLUMN_INVALID = "The column name that you have specified as date_time_column is not a valid Date/Time column."
MODEL_BUILDING_REGISTERED = "Model Building process is registered. Use the model_id for the other processes."
DERIVED_NOT_REMOVED_TIMESERIES = "Dependent predictors are not removed for time series models."
DEPENDENT_NOT_REMOVED_TIMESERIES = "Dependent predictors are not removed for time series models."
DERIVED_NOT_REMOVED_THRESHOLD = "Dependent predictors are not removed as the number of columns after encoding is greater than the threshold that you have provided."
DERIVED_NOT_ADDED_TIMESERIES = "Derived predictors are not added for time series models."
NO_NUMERIC_PRESENT = "Numeric columns are not present in your dataset."
DERIVED_NUMERIC_FAIL = "Derived predictors are not added. The possible reasons can be: 1) the number of columns after encoding is greater than the threshold that you have provided 2) non-numeric features were chosen in the expression list 3) features are not present in the processed dataset 4) If column names have space\s, in that case, supply column name in quotes e.g. '\"<col 1>\" <operator> \"<col 2>\"'"
NO_TEXT_PRESENT = "Text columns are not present in your dataset."
DERIVED_TEXT_FAIL = "Derived predictors are not added. The possible reasons are: 1) the number of columns after encoding is greater than the threshold that you have provided. 2) The text column cannot be derived 3) The text_type specified is not one among (sentiments, glove, topic extraction, concept extraction)"
FEAT_SELECT_NOT_POSSIBLE_TIME_SERIES = "Feature selection is not done for time series models."
FEAT_SELECT_NOT_POSSIBLE_NO_NUMERIC="Feature selection is not possible as there is no numeric columns left after encoding."
DATASET_INSERT_SUCCESS = "The processed data is overwritten."
DATASET_INSERT_FAIL = "The processed data could not be overwritten."
CONFIG_FILE_FAIL = "The configuration change is not applied. The parameter/s changed are either not spelled correctly or the value is not in the correct data type format. Please correct and re-apply."
CONFIG_FILE_SUCCESS = "The config is set."
CONFIG_FILE_NOT_FOUND = "No such configuration file found to validate against"
CONFIG_VARIABLE_NOT_VALID = "The configuration parameter %s is not a valid parameter"
CONFIG_VARIABLE_TYPE_MISMATCH = "The configuration parameter %s is not having the expected type"
CONFIG_VARIABLE_NOT_IN_RANGE = "The configuration parameter %s is not in the expected range"
MODEL_BUILD_NOT_POSSIBLE = "Model Building is not possible as the number of numeric columns after encoding is zero."
OUTCOME_NOT_PRESENT_IN_INSERTED_DATA = "The outcome variable is not present in the data frame that you have inserted."
NUMERIC_NOT_PRESENT_IN_INSERTED_DATA = "The inserted data should only contain numeric values if it is inserted using a model_id."
MODEL_ALREADY_BUILT = "This operation is not permitted as the model for this model_id has already been built."
EZ_EXPORT_MODEL_ONE_OPTION = 'Please select one of model_name or export_all or docker options in post request.'
EZ_EXPORT_MODEL_WRONG_OPTION = 'Please unselect docker_augi, export_augi since this is not augmented intelligence model.'
EZ_EXPORT_MODEL_MULTIPLE_OPTION = 'Please select either model_name or export_all or docker options in post request.'
EZ_AUGI_EXPORT_MODEL_ONE_OPTION = 'Please select one of export_augi or docker_augi options in post request.'
EZ_AUGI_EXPORT_MODEL_WRONG_OPTION = 'Please unselect model_name, export_all, docker since this is augmented intelligence model.'
EZ_AUGI_EXPORT_MODEL_MULTIPLE_OPTION = 'Please select either export_augi or docker_augi option, but not both.'
EZ_INIT_MODEL_OPTIONS_KEYS_LIST = ["model_type", "accelerate", "date_time_column", "remove_dependent", "derive_numeric", "derive_text", "phrases", "text_types", "expressions", "feature_selection", "validate_insights", "outcome_label"]
EZ_GET_DATASETS_KEYS_LIST = ['options']
EZ_GET_DATASETS_OPTIONS_KEYS_LIST = []
EZ_GET_MODELS_KEYS_LIST = ['options']
EZ_GET_MODELS_OPTIONS_KEYS_LIST = ['dataset_id', 'model_type']
EZ_GET_TEST_DATASETS_KEYS_LIST = ['options']
EZ_GET_TEST_DATASETS_OPTIONS_KEYS_LIST = ['model_id']
EZ_DELETE_DATASETS_KEYS_LIST = ['options', 'dataset_id']
EZ_DELETE_DATASETS_OPTIONS_KEYS_LIST = []
EZ_DELETE_MODELS_KEYS_LIST = ['options', 'model_id']
EZ_DELETE_MODELS_OPTIONS_KEYS_LIST = []
EZ_DELETE_TEST_DATASETS_KEYS_LIST = ['options', 'prediction_dataset_id']
EZ_DELETE_TEST_DATASETS_OPTIONS_KEYS_LIST = []
EZ_INIT_MODEL_KEYS_LIST = ['dataset_id', 'options']
EZ_REMOVE_DEPENDENT_OPTIONS_KEYS_LIST = []
EZ_REMOVE_DEPENDENT_KEYS_LIST = ['model_id', 'options']
EZ_DERIVE_NUMERIC_OPTIONS_KEYS_LIST = ["expressions", "return_dataset", "return_columns"]
EZ_DERIVE_NUMERIC_KEYS_LIST = ['model_id', 'options']
EZ_DERIVE_TEXT_OPTIONS_KEYS_LIST = ["phrases", "text_types", "return_dataset", "return_columns"]
EZ_DERIVE_TEXT_KEYS_LIST = ['model_id', 'options']
EZ_SELECT_FEATURES_OPTIONS_KEYS_LIST = []
EZ_SELECT_FEATURES_KEYS_LIST = ['model_id', 'options']
EZ_BUILD_MODELS_OPTIONS_KEYS_LIST = ["features", "validate_insights"]
EZ_BUILD_MODELS_KEYS_LIST = ['model_id', 'options']
EZ_BUILD_ENSEMBLE_KEYS_LIST = ['model_id', 'ensemble_constituents', 'options']
EZ_BUILD_ENSEMBLE_OPTIONS_KEYS = ['ensemble_constituents_weights']
EZ_LOAD_OPTIONS_KEYS_LIST = ["outcome", "accelerate", "id", "discard", "impute", "outlier", "shuffle", "data_source", "filename", "ez_dtypes"]
EZ_EXPORT_MODEL_KEYS_LIST = ['model_id', 'options']
EZ_EXPORT_MODEL_OPTIONS_KEYS = ['model_name', 'export_all', 'docker', 'export_augi', 'docker_augi']
EZ_LOAD_KEYS_LIST = ["filename", "options"]
EZ_LOAD_BIG_DATA_KEYS_LIST = ["dataset_id", "file_path", "options"]
EZ_IMPUTE_KEYS_LIST = ["dataset_id", "options"]
EZ_IMPUTE_OPTIONS_KEYS_LIST = ["impute"]
EZ_SET_OUTCOME_KEYS_LIST = ["dataset_id", "outcome", "options"]
EZ_SET_OUTCOME_OPTIONS_KEYS_LIST = ["outcome_type"]
EZ_OUTLIER_KEYS_LIST = ["dataset_id", "options"]
EZ_OUTLIER_OPTIONS_KEYS_LIST = ["remove_outliers"]
EZ_TYPES_KEYS_LIST = ["dataset_id", "options"]
EZ_TYPES_OPTIONS_KEYS_LIST = ["ez_dtypes"]
EZ_PREDICT_OPTIONS_KEYS_LIST = ["model_name", "data_source", "filename"]
EZ_PREDICT_KEYS_LIST = ["filename", "model_id", "options"]
EZ_GET_PREDICT_KEYS_LIST = ["model_id", "prediction_dataset_id", "options"]
EZ_VALIDATE_KEYS_LIST = ["filename", "model_id", "options"]
EZ_VALIDATE_OPTIONS_KEYS_LIST = ['filename', 'data_source']
EZ_GET_BIAS_KEYS_LIST = ["model_id", "prediction_dataset_id", "options"]
EZ_GET_BIAS_OPTIONS_KEYS_LIST = []
EZ_EXPLAIN_KEYS_LIST = ["model_id", "prediction_dataset_id", "options"]
EZ_SHOW_VALIDATION_KEYS_LIST = ["model_id", "validation_dataset_id", "options"]
EZ_EXPLAIN_PDF_KEYS_LIST = [
    "training_samples_with_predictions", "test_data_with_prediction", "options", "mode",
    "outcome", "scaler", "record_numbers"
]
EZ_EXPLAIN_PDF_OPTIONS_KEYS_LIST = ["scaler", "data_source", "record_number"]
EZ_EXPLAIN_OPTIONS_KEYS_LIST = ["record_number", "scaler"]
EZ_SHOW_VALIDATION_OPTIONS_KEYS_LIST = ["record_number"]
EZ_FETCH_KEYS_LIST = ["dataset_id", "options"]
EZ_FETCH_OPTIONS_KEYS_LIST = ["return_dataset", "return_columns", "model_id"]
EZ_GET_MODEL_STATUS_KEYS_LIST = ["dataset_id", "model_id", "options"]
EZ_GET_MODEL_STATUS_OPTIONS_KEYS_LIST = ["return_models"]
EZ_CONFIG_KEYS_LIST = ["filename", "options"]
EZ_CONFIG_OPTIONS_KEYS_LIST = ["dataset_id", "model_id", "prediction_dataset_id"]
EZ_INSERT_KEYS_LIST = ["filename", "dataset_id", "options"]
EZ_INSERT_OPTIONS_KEYS_LIST = ["model_id"]
EZ_SHUFFLE_KEYS_LIST = ["dataset_id", "options"]
EZ_SHUFFLE_OPTIONS_KEYS_LIST = ["shuffle"]
EZ_DRIFT_KEYS_LIST = [ "filename", "dataset_id", "options"]
EZ_DRIFT_OPTIONS_KEYS_LIST = ["data_drift", "model_drift"]
EZ_DATA_BALANCE_KEYS_LIST = ["dataset_id", "options"]
EZ_DATA_BALANCE_OPTIONS_KEYS_LIST = ["class_count"]
EZ_DATA_DUPLICATES_KEYS_LIST = ["dataset_id", "options"]
EZ_DATA_DUPLICATES_OPTIONS_KEYS_LIST = []
EZ_SHAPE_KEYS_LIST = ["dataset_id", "options"]
EZ_SHAPE_OPTIONS_KEYS_LIST = []
EZ_CORRELATION_KEYS_LIST = ["dataset_id", "options"]
EZ_CORRELATION_OPTIONS_KEYS_LIST = []
INVALID_KEY = '''The parameter %s is invalid'''
OUTCOME_NOT_SET = '''There is no outcome variable set for this dataset id'''
DID_MID_MISMATCH = "The dataset id-model id pair that you have provided is incorrect"
DATATYPES_MESSAGE_API = "The datatypes of the variables are as follows"
DEPENDENT_PREDICTORS_CANNOT_BE_REMOVED_AFTER_FEATURE_SELECTION = 'Dependent predictors cannot be removed after feature selection is done.'
DEPENDENT_PREDICTORS_CANNOT_BE_REMOVED_AFTER_DERIVED_PREDICTORS ='Dependent predictors cannot be removed after derived predictors are added.'
DERIVE_FEATURES_CANNOT_BE_ADDED_AFTER_FEATURE_SELECTION = 'Derived predictors cannot be added after feature selection is done.'
TEXT_TYPES_NOT_ALLOWED = "For your current subscription only %s are allowed. Please upgrade to derive the other text types"
EZ_GET_DATASETS_RETURN_MESSAGE = 'The datasets that you have uploaded are as shown'
EZ_GET_MODELS_RETURN_MESSAGE = 'The models that you have built are as shown'
EZ_GET_TEST_DATASETS_RETURN_MESSAGE = 'The test datasets that you have uploaded are as shown'
EZ_DELETE_DATASETS_RETURN_MESSAGE = 'The dataset %s (%s) has been deleted successfully.'
EZ_DELETE_MODELS_RETURN_MESSAGE = 'The model %s (%s) has been deleted successfully.'
EZ_DELETE_TEST_DATASETS_RETURN_MESSAGE = 'The test dataset %s (%s) has been deleted successfully.'
UID_OR_MID_WRONG = 'Given uid or mid is wrong'
NOT_VALID_CLASSIFICATION_MODEL = 'The model_name is not valid for given classification model'
NOT_VALID_REGRESSION_MODEL = 'The model_name is not valid for given regression model'
INVALID_MODEL_NAME_EXPORT_PARAMETER = '''The model name %s does not exist for the given model_id or has been spelt incorrectly'''
NOT_VALID_MODEL = 'The model_name is not valid'
DATASET_DRIFT_SUCCESS = 'Drift has been calculated successfully'
DATASET_DRIFT_FAIL = 'Drift calculation has been failed'
DRIFT_NOT_SUPPORTED = 'Currently, we are supporting only numeric and categorical datatypes to investigate a drift'
DATA_BALANCE_SUCCESS = 'Data balance has been checked successfully'
DATA_INCOMPLETENESS_SUCCESS = 'Data incompleteness has been checked successfully'
DATA_DUPLICATES_SUCCESS = 'Data duplication has been checked successfully'
DATA_BALANCE_FAIL = 'Failed to check the data balance'
DATA_BALANCE_OUTCOME_CHECK = 'Please check the outcome variable. Data balance is only applicable for categorical outcome'
DATA_INCOMPLETENESS_OUTCOME_CHECK = 'Please check the outcome variable. Data incompleteness is only applicable for categorical outcome'
DATA_ROWS_NOT_ACCEPTED = 'No of rows in dataset is not adequate because no of rows is less than 100'
DATA_COLUMNS_NOT_ACCEPTED = 'No of columns in dataset is not adequate because the no of rows in the dataset is less than the no of columns'
DATA_SHAPE_ACCEPTED = 'Dataset dimension is adequate for further processing'
EZ_CORRELATION_SUCCESS = 'Correlation has been calculated successfully between all features and all features with outcome'
EZ_DATA_QUALITY_KEYS_LIST = [
                "filename",
                "outcome",
                "options"]
EZ_FETCH_DATA_QUALITY_KEYS_LIST = [
                "dataset_id",
                "outcome",
                "options"]
EZ_DATA_QUALITY_OPTIONS_KEYS_LIST = [
                "data_shape",
                "data_balance",
                "data_emptiness",
                "impute",
                "data_outliers",
                "remove_outliers",
                "data_drift",
                "model_drift",
                "data_duplication",
                "influential_features",
                "data_completeness",
                "data_correctness",
                "outcome_correlation",
                "data_quality_options",
                "bigdata_accelerate",
                "filename",
                "prediction_filename"]
EZ_DATA_QUALITY_OPTIONS_OPTIONS_KEYS_LIST = [
                "data_load_options",
                "influential_features_options"]
DATA_QUALITY_SUCCESS = "Data quality checks according to given options have been calculated successfully"
EZ_DATA_BIAS_KEYS_LIST = [
                "filename",
                "outcome",
                "options"]
EZ_DATA_BIAS_OPTIONS_KEYS_LIST = [
                "data_balance",
                "data_outliers",
                "data_duplication",
                "impute",
                "influential_features",
                "data_incompleteness",
                "data_bias_options",
                "prediction_filename"]
EZ_DATA_INCOMPLETENESS_OPTIONS_KEYS_LIST = []
EZ_DATA_BIAS_OPTIONS_OPTIONS_KEYS_LIST = [
                "data_load_options",
                "influential_features_options"]
DATA_BIAS_SUCCESS = "Data bias checks according to given options have been calculated successfully"
UNSUPPORTED_OPERATION_SMALL_DATA = "This operation is not supported for small dataset for current version of EazyML."
UNSUPPORTED_OPERATION_BIG_DATA = 'This operation is not supported for large dataset in current version of EazyML.'
EZ_FETCH_INSIGHTS_KEYS_LIST =["model_id","options"]
EZ_FETCH_INSIGHTS_OPTIONS_KEYS_LIST=["model_type"]
FETCH_INSIGHTS_SUCCESS_MESSAGE='The data insights has fetched successfully'
ONLINE_LEARNING_SUCCESS =  "The information recorded while training the model is as follows"
ACTIVE_LEARNING_SUCCESS =  "The query information is as follows"
EZ_TRANSFER_KEYS_LIST = ["filename", "options"]
EZ_TRANSFER_OPTIONS_KEYS_LIST = ["filename", "overwrite","foldername", "createfolder"]
FILE_ALREADY_EXISTS = "The provided file already exists."
FOLDER_ALREADY_EXISTS = "The provided folder already exists."
FILE_SAVE_SUCCESSFUL = "The file %s has been saved successfully."
CONVERSION_DONE = "Text to audio conversion has been done successfully. The audio file %s has been saved successfully."
FILE_NOT_PRESENT = "Requested resource doesn't exist in your account" 
EZ_UPLOAD_DOCUMENT_OPTIONS_KEYS_LIST = ["overwrite"]
EZ_UPLOAD_DOCUMENT_KEYS_LIST=["document_path", "index_name", "options"]
INVALID_DOCUMENT_FORMAT = "This operation is not supported for %s uploaded document format."
INVALID_INPUT_FORMAT = "Your current provided input format is not correct for %s. Please provide your input in string format."
INVALID_SUB_TYPE = "Your current subscription plan is %s. Please upgrade to premium subscription plan for using this API."
INDEX_NOT_FOUND = "Please provide an existing index_name which was mentioned while uploading the document."
EZ_EXTRACT_INFORMATION_KEYS_LIST = ["query", "index_name", "options"]
EZ_EXTRACT_INFORMATION_OPTIONS_KEYS_LIST = ["explainable_ai"]
EZ_TEXT_TO_AUDIO_CONVERSION_KEYS_LIST = ["text", "options"]
EZ_GET_INDICES_DETAILS_KEYS_LIST = ["options"]
EZ_GET_INDICES_DETAILS_OPTIONS_KEYS_LIST = []
PREMIUM_DOC_TOKEN_LIMIT = '''You have exceeded the allowed limit of number of tokens for the document. Please upload document containing lesser than %s number of tokens.'''
EZ_TEXT_TO_AUDIO_CONVERSION_OPTIONS_KEYS_LIST = ["rate", "voice_id", "volume", "accent", "filename", "overwrite"]
FREE_TRIAL_TOKEN_LIMIT = '''You have exceeded the allowed limit of tokens you can use for trial period. Please upgrade your plan to be able to ask more questions.'''
STANDARD_TOKEN_LIMIT = '''You have exceeded limits for the number of tokens you can use for the month. Please upgrade your plan to be able to ask more questions.'''
DELUXE_TOKEN_LIMIT = '''<p>You have exceeded limits for the number of tokens you can use for the month. Please upgrade your plan to be able to ask more questions.'''
PREMIUM_TOKEN_LIMIT = '''<p>You have exceeded limits for the number of tokens you can use for the month. Please contact us for requesting additional quota.'''
BIG_DATA_IMPUTE = "The imputation operation is not supported for big data in current version of EazyML. Please provide no for impute parameter"
EZ_BIG_DATA_ACCELERATE = "Please use the ez_fetch_bigdata_quality with the dataset_id provided and the necessary quality parameters."
EZ_BIG_DATA_PATH = "Please use ez_data_quality for Big data to store the dataset_id and data path"
EZ_DATASET_ID = "Please provide the dataset_id"
EZ_DATAQUALITY_PROGRESS = "The Task is still running in the background. Please try after sometime"
EZ_DRIFT_MANDATORY_PARAMETER = '''For drift analysis the request must have the parameter %s.'''
