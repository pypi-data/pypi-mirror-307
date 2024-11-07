import pandas as pd
import numpy as np
import re
from . import transparency_api as tr_api
from . import exai
import traceback
import pickle
from . import globals as gbl
g = gbl.config_global_var()
try:
    from werkzeug import secure_filename
except:
    from werkzeug.utils import secure_filename


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def get_records_list(record_number):
    final_rec = []
    if any(["-" in str(x) for x in record_number]):
        for x in record_number:
            if "-" not in x and len(x.strip().split(" ")) == 1:
                final_rec.append(int(x))
            elif len(str(x).strip().split(" ")) == 1:
                l = [range(int(x.split("-")[0]), int(x.split("-")[1])+1)]
                final_rec.extend(l[0])
            else:
                return -1
        return [i for n, i in enumerate(final_rec) if i not in final_rec[:n]]
    elif any([len(str(x).strip().split(" ")) > 1 for x in record_number]):
        return -1
    else:
        return [int(i) for i in record_number]


def get_df(uploaded_file, data_source="system", is_api=False,
           ip_fname=None, full_path=False):
    if "system" == data_source:
        if ip_fname is not None:
            fname = ip_fname
        else:
            fname = secure_filename(uploaded_file)
        ext = get_extension(fname)
        tmp_path = uploaded_file
        try:
            if ext == "csv":
                df = pd.read_csv(tmp_path, na_values=[
                    'n/a', 'na', 'nan', 'null'])
            if ext == "xlsx" or ext == "xls":
                df = pd.read_excel(tmp_path, na_values=[
                    'n/a', 'na', 'nan', 'null'])
            if ext == "tsv":
                df = pd.read_table(tmp_path, na_values=[
                    'n/a', 'na', 'nan', 'null'])
            if ext == "parquet":
                df = pd.read_parquet(tmp_path)
            if ext == "txt":
                with open(tmp_path) as myfile:
                    head = list(islice(myfile, g.DELIMITER_ROWS_COUNT))
                delimiter = find_delimiter(head)[0]
                if delimiter in g.ALLOWED_DELIMITERS:
                    df = pd.read_csv(tmp_path, sep=delimiter,na_values=[
                        'n/a', 'na', 'nan', 'null'])
                else:
                    print ('Error in loading txt file. Delimiter not found.')
                    return None, None
            if is_api:
                return df, tmp_path
        except Exception as e:
            print ("Exception in loading csv: ", e)
            print (traceback.print_exc())
            return None, None
    else:
        try:
            df = pd.read_parquet(uploaded_file)
            tmp_path = uploaded_file
            if is_api:
                if df.shape[0] >= 1000 or df.shape[1] >= 100:
                    df.to_csv(tmp_path, index=False)
                return df, tmp_path
        except Exception as e:
            print ("Exception in reading parquet file: ", e)
            print (traceback.print_exc())
            return None, None
    df = df.replace(r'^\s*$', np.nan, regex=True)
    columns = list(df.columns)
    try:
        columns_stripped = [re.sub('\s+', ' ', str(col)).strip().replace(
            '()','(.)') for col in columns]
    except Exception as e:
        print ("Exception in converting column text to str", e)
        columns_stripped = [re.sub('\s+', ' ', str(col.encode(
            'ascii', 'ignore').decode('ascii'))).strip().replace(
            '()','(.)') for col in columns]
    sql_escape_sequences = g.SQL_ESCAPE_SEQUENCES 
    for i, elem in enumerate(columns_stripped):
        for esc_seq in sql_escape_sequences:
            if esc_seq in elem:
                columns_stripped[i] = elem.replace(esc_seq, '')
    df.columns = columns_stripped
    if any(("[" in x or "]" in x or "<" in x for x in columns_stripped)):
        return g.COLUMN_NAMES_INCOMPATIBLE, None
    return df, None


def call_explainable_ai(train_data, outcome, test_data, model, 
                        scaler, criterion, record_numbers, extra_info):

    body = dict(
        train_data = train_data,
        test_data = test_data,
        outcome = outcome,
        criterion = criterion,
        scaler = scaler,
        model = model,
        record_numbers = record_numbers
    )
    g = extra_info["g"]

    body["g"] = dict(
        (name, getattr(g, name))
        for name in dir(g)
        if not name.startswith("__") and type(getattr(g, name)) in [
            bool, int, str, bytes, float]
    )
    return call_exai_post(body)


def call_exai_post(body):
    try:
        response = exai.get_explainable_ai(body)
    except Exception as e:
        print ("Exception in call_ai")
        traceback.print_exc()
    if response is not None:
        return response


def ez_explain(auth_token, mode, outcome, train_file_path,
                      test_file_path, model, options={}):
    """EazyML Explanation API. 
        Accepts a JSON request which should have "train_file_path",
        "test_file_path", "mode", "outcome" and "model_name" as keys.
        train_file_path: Train file on which the the model build.
        test_file_path: Test file on which you want the prediction.
        record_number: The record whose prediction needs to be explained.
        mode: "Classification / Regression"
        outcome: Outcome column which you want to predict.
        model_name: Model which you use for the prediction.
    
    Returns
    -------
    [On success]
        Returns a JSON response with the keys "success" which tells the user
        if the API was successful in fetching the explanation
        "message" to convey additional information and "explanations" which is
        a python dictionary
        containing information about the explanation string, local importance
        dataframe.
    [On Failure]
        Only success and message is returned.
    """
    try:
        data_source = "system"
        if ("data_source" in options and options[
            "data_source"] == "parquet"):
            data_source = "parquet"
        train_data, _ = get_df(train_file_path, data_source=data_source) 
        test_data, _ = get_df(test_file_path, data_source=data_source)
        if outcome not in train_data.columns:
            return {
                    "success": False,
                    "message": "Outcome is not present in training data columns"
                    }
        if mode not in ['classification', 'regression']:
            return {
                    "success": False,
                    "message": "Please provide valid mode.('classification'/'regression')"
                    }
        if not isinstance(options, dict):
            return {
                    "success": False,
                    "message": tr_api.VALID_DATATYPE_DICT.replace(
                        "this", "options"),
                    }
        #Check for valid keys in the options dict
        is_list = lambda x: type(x) == list
        is_string = lambda x: isinstance(x, str)
        if (
            not is_string(mode)
            or not is_string(outcome)
            or not is_string(train_file_path)
            or not is_string(test_file_path)
        ):
            return {
                        "success": False,
                        "message": tr_api.ALL_STR_PARAM
                    }
        if "scaler" in options:
            scaler = options["scaler"]
        else:
            scaler = None
        for key in options:
            if key not in tr_api.EZ_EXPLAIN_OPTIONS_KEYS_LIST:
                return {"success": False, "message": tr_api.INVALID_KEY % (key)}

        if "record_number" in options and options["record_number"]:
            record_number = options["record_number"]

            if is_string(record_number):
                record_number = record_number.split(',')
            if is_list(record_number):
                rec_n = get_records_list(record_number)
                if rec_n != -1:
                    record_number = rec_n
                else:
                    return {"success": False,
                            "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}

            if not is_list(record_number) and not is_string(
                record_number) and not isinstance(record_number, int):
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif is_list(record_number) and not all([(is_string(
                x) and x.isdigit()) or isinstance(x, int) for x in record_number]):
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif is_string(record_number) and not record_number.isdigit():
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif isinstance(record_number, int) and record_number < 0:
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            elif is_list(record_number) and any([isinstance(
                x, int) and x < 0 for x in record_number]):
                return {"success": False,
                        "message": "'record_number' in the 'options' parameter has either negative values or invalid data types."}
            if is_list(record_number):
                record_number = record_number
            elif isinstance(record_number, int):            
                record_number = [str(record_number)]
            else:
                record_number = [record_number]
            test_data_rows_count = test_data.shape[0]
            for rec_number in record_number:
                if int(rec_number) > test_data_rows_count:
                    return {
                            "success": False,
                            "message": "'record_number' in the 'options' parameter has values more than number of rows in the prediction dataset."
                            }
        else:
            record_number = [1]
        
        ## Cache g, misc_data_model, model_data in extra_info
        extra_info =dict()
        extra_info["g"] = g

        results = []
        results = call_explainable_ai(train_data, outcome, test_data, model, 
                                      scaler, mode, record_number, extra_info)
        if type(results) != list:
            return {
                        "success": False,
                        "message": tr_api.EXPLANATION_FAILURE
                    }
        return {
                    "success": True,
                    "message": tr_api.EXPLANATION_SUCCESS,
                    "explanations": results,
                }

    except Exception as e:
        print (traceback.print_exc())
        return {"success": False, "message": tr_api.INTERNAL_SERVER_ERROR}