import os
import sys
import traceback
from flask import Blueprint, render_template_string
from flask import render_template, request, make_response
from flask_restx import Resource, Api
import pandas as pd
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from great_expectations.core import RunIdentifier, ValidationDefinition
from great_expectations.exceptions import DataContextError
from great_expectations.data_context.types.base import DataContextConfig, FilesystemStoreBackendDefaults
from great_expectations.core.batch import BatchRequest
from datetime import datetime
from cdh_lava_core.app_shared_dependencies import get_config
from cdh_lava_core.az_key_vault_service import az_key_vault as cdh_az_key_vault
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton
from cdh_lava_core.cdc_metadata_service import environment_metadata as cdc_env_metadata
import csv
from dotenv import load_dotenv
from pathlib import Path
import math
from databricks.connect import DatabricksSession


great_expectations_bp = Blueprint('great_expectations', __name__)

SERVICE_NAME = os.path.basename(__file__)
# Get the parent folder name of the running file
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
api = Api(great_expectations_bp)  # Initialize Api with the blueprint
ENVIRONMENT = "dev"  # Set the environment name
DATA_PRODUCT_ID = "lava_core"

tracer, logger = LoggerSingleton.instance(
    NAMESPACE_NAME, SERVICE_NAME, DATA_PRODUCT_ID, ENVIRONMENT
).initialize_logging_and_tracing()

def update_html(raw_html):
    # Step 1: Replace "Show Walkthrough" with "Run Tests"
    updated_html = raw_html.replace("Show Walkthrough", "Run Tests")

    # Step 2: Replace modal trigger with form submission action
    updated_html = updated_html.replace(
        'data-toggle="modal" data-target=".ge-walkthrough-modal"',
        'onclick="document.getElementById(\'myForm\').submit();"'
    )

    # Step 3: Replace "<strong>Actions</strong>" with form tag
    updated_html = updated_html.replace(
        "<strong>Actions</strong>",
        '<form id="myForm" method="post"></form>'
    )

    # Step 4: Update button type to "submit" within the form
    updated_html = updated_html.replace(
        '<button type="button" class="btn btn-info"',
        '<div><button onclick="history.back()" class="btn btn-secondary   w-200  " style="height:50px">Back</button></div><br>&nbsp;&nbsp;<br><button type="submit" style="height:50px" class="btn btn-info w-200 "'
    )

    return updated_html


def get_parent_directory():
    """Retrieve the parent directory of the current file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, os.pardir))

def get_csv_data(csv_path):
    """Read CSV data and return as list of dictionaries."""
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")

def initialize_context(expectations_dir, data_product_id):
    """Initialize or load a Great Expectations context."""
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory from the current directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    # Construct the relative path to the CSV file
    expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
    
    if not os.path.exists(expectations_dir):
        os.makedirs(expectations_dir, exist_ok=True)
        # Define the store backend
       # Define the validations store configuration
        validations_store_config = {
            "validations_store": {
                "class_name": "ValidationsStore",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": "uncommitted/validations/"
                }
            }
        }
        # Create DataContextConfig with the validations store
        context_config = DataContextConfig(
            stores=validations_store_config,
            expectations_store_name="expectations_store",
            data_docs_sites={
                "local_site": {
                    "class_name": "SiteBuilder",
                    "store_backend": {
                        "class_name": "TupleFilesystemStoreBackend",
                        "base_directory": "uncommitted/data_docs/local_site/"
                    },
                    "site_index_builder": {
                        "class_name": "DefaultSiteIndexBuilder"
                    }
                }
            },
            context_root_dir=expectations_directory_path
        )
        context =  gx.get_context(context_config)
        logger.info(f"Great Expectations project initialized at: {expectations_dir}")
    else:
        context =  gx.get_context(context_root_dir=expectations_directory_path)
        logger.info(f"Great Expectations project already exists at: {expectations_dir}")
    return context

def validate_with_run_id(context, dataset_name, expectation_suite, batch_definition, batch_parameters):

    # Create run_identifier with timestamp
    run_name = f"{dataset_name}_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
 

    validation_definition = ValidationDefinition(
        name=run_name,
        data=batch_definition,  # The active batch being validated
        suite=expectation_suite
    )

    # Add ValidationDefinition to the context
    context.validation_definitions.add(validation_definition)

    # Create a list of Actions for the Checkpoint to perform
    action_list = [
        # This Action updates the Data Docs static website with the Validation
        #   Results after the Checkpoint is run.
        gx.checkpoint.UpdateDataDocsAction(
            name="update_all_data_docs",
        ),
    ]


    # Create a list of one or more Validation Definitions for the Checkpoint to run
    validation_definitions = [
        context.validation_definitions.get(run_name)
    ]

    # Create the Checkpoint
    checkpoint_name = f"{run_name}_checkpoint"
    checkpoint = gx.Checkpoint(
    name=checkpoint_name,
    validation_definitions=validation_definitions,
    actions=action_list,
    result_format={"result_format": "COMPLETE"},
    )

    # Save the Checkpoint to the Data Context
    context.checkpoints.add(checkpoint)

    # Run validation
    # validation_result = validator.validate()

    # Add run_id to the meta if not present to avoid KeyError
    # if "run_id" not in validation_result.meta:
    #    validation_result.meta["run_id"] = str(run_id)

    run_id = RunIdentifier(run_name=run_name)

    validation_results = checkpoint.run(
        batch_parameters=batch_parameters,
         run_id=run_id
    )   

    return validation_results



def configure_data_docs(context, expectations_dir):
    """Configure and build Data Docs site if not already configured."""
    data_docs_sites = context.get_config().data_docs_sites
    if not data_docs_sites:
        data_docs_sites = {
            "local_site": {
                "class_name": "SiteBuilder",
                "store_backend": {
                    "class_name": "TupleFilesystemStoreBackend",
                    "base_directory": os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                },
                "site_index_builder": {
                    "class_name": "DefaultSiteIndexBuilder"
                }
            }
        }
        context.add_data_docs_site(name="local_site", site_config=data_docs_sites["local_site"])
        logger.info("Data Docs site configuration added.")
    context.build_data_docs()

def manage_expectation_suite(context, suite_name):
    """Retrieve or create an expectation suite."""
    try:
        suite = context.suites.get(suite_name)
        if suite is None:
            logger.warning(f"Suite '{suite_name}' not found; creating a new one.")
            suite = ExpectationSuite(suite_name)
            context.suites.add(suite)
            logger.info(f"Created and added new suite '{suite_name}'")
        else:
            logger.info(f"Loaded existing suite '{suite_name}'")
        return suite
    except DataContextError:
        logger.warning(f"Suite '{suite_name}' not found; creating a new one.")
        suite = ExpectationSuite(suite_name)
        context.suites.add(suite)
        return suite

def setup_spark_data_source(context, data_product_id):

    master_config = get_config()
    obj_env_metadata = cdc_env_metadata.EnvironmentMetaData()
    data_product_id_root = data_product_id.split("_")[0]
    data_product_id_individual = data_product_id.split("_")[1]
    repository_path_default = master_config.get("repository_path")
    running_local = master_config.get("running_local")
    environment = master_config.get("environment")

    parameters = {
    "data_product_id": data_product_id,
    "data_product_id_root": data_product_id_root,
    "data_product_id_individual": data_product_id_individual,
    "environment": environment,
    "repository_path": repository_path_default,
    "running_local": running_local,
    }
    config = obj_env_metadata.get_configuration_common(
    parameters, None, data_product_id, environment
    )
    
    database_name = config.get("cdh_database_name")
    catalog_name = database_name.split(".")[0]
    schema_name = database_name.split(".")[1]
    data_source_name = f"{database_name}_spark" 

    data_source = None
    try:
        # Attempt to retrieve the datasource
        data_source = context.data_sources.get(data_source_name)
        logger.info(f"Data source '{data_source_name}' already exists.")
    except (KeyError,ValueError):
        # If datasource is not found, create it
        data_source = context.data_sources.add_spark(name=data_source_name)
        logger.info(f"Created new data source '{data_source_name}'")
        
    return data_source, data_source_name, catalog_name, schema_name


def setup_sql_alchemy_data_source(context, data_product_id):
    """Retrieve or create a Databricks data source."""
    try:

        master_config = get_config()
        obj_env_metadata = cdc_env_metadata.EnvironmentMetaData()
        data_product_id_root = data_product_id.split("_")[0]
        data_product_id_individual = data_product_id.split("_")[1]
        repository_path_default = master_config.get("repository_path")
        running_local = master_config.get("running_local")
        environment = master_config.get("environment")

        parameters = {
        "data_product_id": data_product_id,
        "data_product_id_root": data_product_id_root,
        "data_product_id_individual": data_product_id_individual,
        "environment": environment,
        "repository_path": repository_path_default,
        "running_local": running_local,
        }
        config = obj_env_metadata.get_configuration_common(
        parameters, None, data_product_id, environment
        )

        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        environment = config.get("cdh_environment")
        client_secret = config.get("client_secret")
        tenant_id = config.get("az_sub_tenant_id")
        client_id = config.get("az_sub_client_id")
        az_kv_key_vault_name = config.get("az_kv_key_vault_name")
        running_interactive = False
        if not client_secret:
            running_interactive = True

        az_sub_web_client_secret_key = config.get(
        "az_sub_web_client_secret_key"
        )
        obj_az_keyvault = cdh_az_key_vault.AzKeyVault(
        tenant_id,
        client_id,
        client_secret,
        az_kv_key_vault_name,
        running_interactive,
        data_product_id,
        environment,
        az_sub_web_client_secret_key,
        )

        database_name = config.get("cdh_database_name")
        catalog_name = database_name.split(".")[0]
        schema_name = database_name.split(".")[1]

        data_source_name = database_name
        host_name = config.get("cdh_databricks_instance_id")
        token_key = config.get("cdh_databricks_pat_secret_key")
        token = obj_az_keyvault.get_secret(token_key)
        http_path = config.get("cdh_databricks_endpoint_path_sql")
        # Set environment variables dynamically
        os.environ["DATABRICKS_TOKEN"] = token
        os.environ["DATABRICKS_HTTP_PATH"] = http_path

        connection_string = (
        f"databricks://token:{token}@{host_name}:443?http_path={http_path}&catalog={catalog_name}&schema={schema_name}"
        )
        data_source = None
        try:
            # Attempt to retrieve the datasource
            data_source = context.data_sources.get(data_source_name)
            logger.info(f"Data source '{data_source_name}' already exists.")
        except (KeyError,ValueError):
            # If datasource is not found, create it
            logger.info(f"connection_string: {connection_string}")
            data_source = context.data_sources.add_databricks_sql(
                name=data_source_name,
                connection_string=connection_string
            )
            logger.info(f"Created new data source '{data_source_name}'")

    
        return data_source, data_source_name, catalog_name, schema_name
    except DataContextError as e:
        logger.error(f"Failed to retrieve or create data source '{data_source_name}': {e}")
        return None


def get_raw_file(file_system: str, file_name: str) -> str:
        """
        Reads the content of a file from the specified directory and returns it as a string.

        Args:
            file_system (str): The directory path where the file is located.
            file_name (str): The name of the file to read.

        Returns:
            str: The content of the file as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there is an error reading the file.
        """
        try:
            file_path = os.path.join(file_system, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except IOError as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
        
        
class GreatExpectationsHomeList(Resource):
    def get(self):
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        csv_path = os.path.join(parent_dir, "lava_core", "bronze_great_expectations.csv")

        # Read the CSV into a DataFrame
        df = pd.read_csv(csv_path)

        # Convert the DataFrame to a list of dictionaries
        data = df.to_dict(orient="records")

        # Retrieve other parameters if needed
        calling_page_url = request.args.get("calling_page")

        # Render the template with the data
        return make_response(render_template('great_expectations/great_expectations_home.html',
                               data=data, calling_page_url=calling_page_url))


class GreatExpectationHome(Resource):
    def get(self, data_product_id: str, text: str):
        with tracer.start_as_current_span("great_expectation"):
            try:
                # Setup paths and context
                parent_dir = get_parent_directory()
                csv_path = os.path.join(parent_dir, data_product_id, "config", "bronze_sps_config_datasets.csv")
                expectations_dir = os.path.join(parent_dir, data_product_id, "gx")
                config_data = get_csv_data(csv_path)
                

                # Initialize context and data docs
                context = initialize_context(expectations_dir, data_product_id)
                configure_data_docs(context, expectations_dir)

                default_path = os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                file_name = text
                raw_html = get_raw_file(default_path, file_name)
                updated_html_content = update_html(raw_html)
                return make_response(render_template_string(updated_html_content))

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                logger.error(error_message, exc_info=sys.exc_info())
                return make_response(render_template("error.html", error_message=error_message), 500)

    def post(self, data_product_id: str, text: str):
        with tracer.start_as_current_span("great_expectation"):
            try:
                # Setup paths and context
                parent_dir = get_parent_directory()
                csv_path = os.path.join(parent_dir, data_product_id, "config", "bronze_sps_config_datasets.csv")
                expectations_dir = os.path.join(parent_dir, data_product_id, "gx")
                config_data = get_csv_data(csv_path)
                

                # Initialize context and data docs
                context = initialize_context(expectations_dir, data_product_id)
                configure_data_docs(context, expectations_dir)

                data_access_method = "spark_dataframe"
                #data_access_method = "sql_alchemy"

                if data_access_method == "spark_dataframe":
                    data_source, data_source_name, catalog_name, schema_name = setup_spark_data_source(context, data_product_id)
                else:
                    data_source, data_source_name, catalog_name, schema_name = setup_sql_alchemy_data_source(context, data_product_id)
                
                # Manage suites and read dataset CSV
                for row in config_data:
                    
                    if data_access_method == "spark_dataframe":
                        dataset_name = row.get("dataset_name")
                        data_asset_name = f"{dataset_name}_spark"
                    else:
                        dataset_name = row.get("dataset_name")
                        data_asset_name = dataset_name

                    batch = None
                    if dataset_name:
                        if data_access_method == "spark_dataframe":
                            suite_name = f"{dataset_name}_suite_spark"
                        else:
                            suite_name = f"{dataset_name}_suite"
                            
                        expectation_suite = manage_expectation_suite(context, suite_name)
                        try:
                            data_asset = data_source.get_asset(data_asset_name)
                        except (LookupError):
                            data_asset = None
                            
                        if data_asset is None:
                            if data_access_method == "spark_dataframe":
                                data_asset = data_source.add_dataframe_asset(name=data_asset_name)
                            else:
                                data_asset = data_source.add_table_asset(name=data_asset_name, table_name=dataset_name)

                        
                        if data_access_method == "spark_dataframe":
                            batch_definition_name = f"{dataset_name}_batch_definition_spark" 
                            spark = DatabricksSession.builder.getOrCreate()
                            dataframe  = spark.read.table(f"{catalog_name}.{schema_name}.{dataset_name}")                            
                            batch_parameters = {"dataframe": dataframe}
                        else:
                            batch_definition_name = f"{dataset_name}_batch_definition" 
                            batch_parameters = {}

                        try:
                            batch_definition = data_asset.get_batch_definition(name=batch_definition_name)
                            logger.info(f"fetched batch_definition: {batch_definition_name}")
                        except (KeyError, ValueError):
                            if data_access_method == "spark_dataframe":
                                batch_definition = data_asset.add_batch_definition_whole_dataframe(
                                    batch_definition_name
                                )
                            else:
                                batch_definition = data_asset.add_batch_definition_whole_table(
                                        name= batch_definition_name
                                )
                            logger.info(f"added batch_definition: {batch_definition_name}")

                        if data_access_method == "spark_dataframe":
                            batch_request = data_asset.build_batch_request(options={"dataframe": dataframe})                       
                            batch = batch_definition.get_batch(batch_parameters=batch_parameters)
                        else:
                            batch = batch_definition.get_batch()

                        if batch is None:
                            logger.info("batch is None")

                        # Clear all expectations
                        expectation_suite.expectations = []
                        # Save the empty suite back to the data context
                        expectation_suite.save()
                        
                        row_id_keys = row.get("row_id_keys")
                        if row_id_keys and batch:
                            expected_values = row.get("expected_values")
                            if expected_values is not None and not (isinstance(expected_values, float) and math.isnan(expected_values)):
                                # Split the string and strip quotes and spaces from each item
                                expected_values_list = [item.strip(" '\t") for item in expected_values.split(",")]
                                logger.info(f"expected_values:{expected_values}")
                                expectation =   gx.expectations.ExpectColumnValuesToBeInSet(
                                column=row_id_keys,
                                value_set=expected_values_list
                                )
                               
                                expectation_suite.add_expectation(expectation)
                                expectation_suite.save()
                                
                                
                        
                        expected_row_count_min = row.get("expected_row_count_min")
                        expected_row_count_max = row.get("expected_row_count_min")
                        # Check if expected_row_count is a valid number, not NaN, and greater than 0
                        if isinstance(expected_row_count_max, (int, float)) and not math.isnan(expected_row_count_max) and expected_row_count_max > 0 and batch:
                            if isinstance(expected_row_count_min, (int, float)) and not math.isnan(expected_row_count_min) and expected_row_count_min > 0 and batch:
                                expectation =  gx.expectations.ExpectTableRowCountToBeBetween(min_value=expected_row_count_min, max_value=expected_row_count_max)
                                expectation_suite.add_expectation(expectation)
                                expectation_suite.save()


                        validation_results = validate_with_run_id(context, dataset_name, expectation_suite, batch_definition, batch_parameters)
                        
                default_path = os.path.join(expectations_dir, "uncommitted", "data_docs", "local_site")
                file_name = text
                raw_html = get_raw_file(default_path, file_name)
                raw_html = update_html(raw_html)
                return make_response(render_template_string(raw_html))

            except Exception as ex:
                trace_msg = traceback.format_exc()
                line_number = traceback.extract_tb(ex.__traceback__)[-1].lineno
                error_message = f"An unexpected error occurred: {ex} at line {line_number}\nCall Stack:{trace_msg}"
                logger.error(error_message, exc_info=sys.exc_info())
                return make_response(render_template("error.html", error_message=error_message), 500)
   

class GreatExpectationModule(Resource):
    def get(self, data_product_id: str, module: str, text: str):

        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
        file_name = os.path.basename(text)
        dir_path = module
        path = os.path.join(expectations_directory_path, "uncommitted", "data_docs", "local_site", dir_path)
        raw_html = get_raw_file(file_system=path, file_name=file_name)
        return make_response(render_template_string(raw_html))

class GreatExpectationPage(Resource):
    def get(self, data_product_id: str, module: str, suite: str, run: str, page: str, text: str):

        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go up one directory from the current directory
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

        # Construct the relative path to the CSV file
        expectations_directory_path = os.path.join(parent_dir, data_product_id, "gx")
        file_name = os.path.basename(text)
        dir_path = module
        path = os.path.join(expectations_directory_path, "uncommitted", "data_docs", "local_site", dir_path, suite, run, page)
        raw_html = get_raw_file(file_system=path, file_name=file_name)
        raw_html = update_html(raw_html)
        return make_response(render_template_string(raw_html))
