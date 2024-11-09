from dynatrace import Dynatrace
from dynatrace.http_client import TOO_MANY_REQUESTS_WAIT
from rich.progress import track
from rich import print

from typing import Optional, List, Dict, Union
from urllib.parse import urlparse
import io

from .models import CustomDBQuery
from .utils import slugify

TIMEFRAME = "now-1y"


def lookup_columns_for_query(dt: Dynatrace, query_name: str):
    column_names = []
    query = f'custom.db.query:filter(eq(query_name,"{query_name}")):splitBy(column,query_name)'
    metric_series_collections = dt.metrics.query(
        query, time_from=TIMEFRAME, resolution="Inf"
    )
    for collection in metric_series_collections:
        for series in collection.data:
            column = series.dimension_map.get("column")
            if column:
                column_names.append(column)

    return column_names


def queries_from_ef1_config(properties: dict):
    properties.update(
        {
            "database_type": properties["database_type"],
            "group_name": properties["group_name"],
            "database_host": properties["database_host"],
            "database_name": properties["database_name"],
            "database_username": properties["database_username"],
            "custom_device_name": properties["custom_device_name"],
        }
    )

    configured_queries: List[CustomDBQuery] = []
    query_index = 1
    while query_index < 11:
        if properties[f"query_{query_index}_value"]:
            configured_queries.append(
                CustomDBQuery(
                    properties[f"query_{query_index}_name"],
                    properties[f"query_{query_index}_schedule"],
                    properties[f"query_{query_index}_value"],
                    properties[f"query_{query_index}_value_columns"],
                    properties[f"query_{query_index}_dimension_columns"],
                    properties[f"query_{query_index}_extra_dimensions"],
                )
            )
        query_index += 1
    return configured_queries


def ef2_datasource(db_type: str):
    if db_type == "Oracle":
        return "sqlOracle"
    elif db_type == "DB2":
        return "sqlDb2"
    elif db_type == "SQL Server":
        return "sqlServer"
    elif db_type == "MySQL":
        return "sqlMySql"
    elif db_type == "PostgreSQL":
        return "sqlPostgres"
    elif db_type == "SAP HANA":
        return "sqlHana"
    else:
        raise Exception(f"Unsupported database type: {db_type}")


def activation(endpoint_name: str, props: dict, version: str, credential_vault_id: str = None):

    database_type = props["database_type"]
    host = props.get("database_host") or None
    port = int(props.get("database_port")) or None
    database_name = props.get("database_name") or None
    database_username = props.get("database_username") or None
    oracle_listener_type = props.get("oracle_listener_type") or None
    jdbc_connection_string = props.get("jdbc_connection_string") or None

    endpoint = {}

    if jdbc_connection_string:
        if database_type not in ["Oracle, PostgreSQL", "SQL Server"]:
            raise Exception(f"{database_type} datasource does not currently support connection strings.")
        endpoint['useConnectionString'] = True
        endpoint['connectionString'] = jdbc_connection_string
        # try:
        #     # try parsing out some details from the connection string
        #     print(jdbc_connection_string)
        #     r = urlparse(jdbc_connection_string)
        #     print(r.scheme)
        # except Exception as e:
        #     print(f"Can't parse jdbc '{jdbc_connection_string}': {e}")
        endpoint['host'] = "SET-ME"
        endpoint['port'] = 1234
        endpoint['databaseName'] = "SET-ME"
    else:
        endpoint['host'] = host
        endpoint['port'] = port

    if credential_vault_id:
        endpoint['authentication'] = {
            "scheme": "basic",
            "useCredentialVault": True,
            "credentialVaultId": credential_vault_id
        }
    else:
        endpoint['authentication'] = {
            "scheme": "basic",
            "useCredentialVault": False,
            "username": database_username,
            "password": "changeme"
        }

    if database_type == "Oracle":
        endpoint['databaseIdentifier'] = "sid" if oracle_listener_type == "SID" else "serviceName"
        endpoint.update({"SID" if oracle_listener_type == "SID" else "serviceName": database_name})
    else:
        endpoint['databaseName'] = database_name

    activation_config = {
        "enabled": False,
        "description": f"Migrated extension from EF1 db queries config {endpoint_name}.",
        "version": version,
        f"{ef2_datasource(props['database_type'])}Remote": {
            "endpoints": [endpoint]
        }
    }

    if database_type == "Oracle":
        activation_config[f"{ef2_datasource(props['database_type'])}Remote"].update({"licenseAccepted": True})

    return activation_config


class EF2SqlExtension:
    def __init__(
        self, dt: Dynatrace, endpoint_name: str, ef1_config_properties: Union[Dict, List], log_file: io.TextIOWrapper, credential_vault_id = None, pre_cron = False
    ) -> None:
        
        extension_name = f"custom:db.query.{slugify(endpoint_name)[:30] if len(slugify(endpoint_name)) > 30 else slugify(endpoint_name)}"
        try:
            current_versions = dt.extensions_v2.list_versions(extension_name)
            for version in current_versions:
                version = version.version.split(".")
                version[2] = str(int(version[2])+1)
                version = '.'.join(version)
        except Exception as e:
            version = "1.0.0"
        

        if type(ef1_config_properties) == list:
            # have to merge queries from multiple configs into one
            queries = []
            db_type = ef2_datasource(ef1_config_properties[0]["database_type"])
            for conf_prop in ef1_config_properties:
                queries.extend(queries_from_ef1_config(conf_prop))
            self.activation_config = activation(endpoint_name, ef1_config_properties[0], version, credential_vault_id)
        else:
            db_type = ef2_datasource(ef1_config_properties["database_type"])
            queries = queries_from_ef1_config(ef1_config_properties)
            self.activation_config = activation(endpoint_name, ef1_config_properties, version, credential_vault_id)

        extension = {
            "name": extension_name,
            "version": version,
            "minDynatraceVersion": "1.301" if not pre_cron else "1.299",
            "author": {"name": "Dynatrace"},
            db_type: [],
        }

        group_number = 1
        subgroup_number = 0

        group = {
                "group": f"queries-{group_number}",
                "dimensions": [
                    {"key": "db.query", "value": f"const:{slugify(endpoint_name)[:240]}"}
                ],
                "subgroups": []
            }

        for query in queries:
            if subgroup_number == 10:
                extension[db_type].append(group)
                group_number+=1
                group = {
                    "group": f"queries-{group_number}",
                    "subgroups": []
                }
            metric_columns = query.value_columns
            if not metric_columns:
                metric_columns = lookup_columns_for_query(dt, query.name)
            else:
                metric_columns = metric_columns

            safe_query_name = slugify(query.name)

            subgroup = {
                "subgroup": query.name,
                "query": query.value,
                "metrics": [],
                "dimensions": [{"key": "query_name", "value": f"const:{query.name}"}],
            }

            if not pre_cron:
                subgroup.update({"schedule": query.schedule})

            for column in metric_columns:
                subgroup["metrics"].append(
                    {
                        "key": f"{safe_query_name}.{slugify(column)}",
                        "value": f"col:{column}",
                        "type": "gauge",
                    }
                )

            for column in query.dimension_columns:
                subgroup['dimensions'].append(
                    {
                        "key": column.lower() ,
                        "value": f"col:{column}"
                    }
                )

            for dimension_pair in query.extra_dimensions:
                key, value = dimension_pair.split("=")
                subgroup['dimensions'].append(
                    {
                        "key": key.lower(),
                        "value": f"const:{value}"
                    }
                )

            subgroup_number += 1
            group['subgroups'].append(subgroup)


        extension[db_type].append(group)

        self.name = "custom:" + extension["name"].split(":")[1]
        self.version = extension["version"]
        self.dictionary = extension
