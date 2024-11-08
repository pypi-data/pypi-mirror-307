import json
from ydata_profiling import ProfileReport
import adal
import pandas as pd
from datetime import datetime
import numpy as np
import requests
import urllib3
import json


class ProfilingException(Exception):
    pass


class Helper:
    def get_access_token():
        pass

    def save_report():
        pass


class Profiling(Helper):
    def __init__(self, connection_obj, report_id, cataloag_name, schema_name, table_name, selected_column, partition_column_name, sample_percentage):
        self.conn = connection_obj
        self.id = report_id
        self.cataloag_name = cataloag_name
        self.schema_name = schema_name
        self.table_name = table_name
        self.selected_column = selected_column
        self.partition_column_name = partition_column_name
        self.sample_percentage = sample_percentage

    def fache_data(self):
        target_table = self.schema_name + "." + self.table_name
        try:
            query = f"SELECT * FROM {target_table}"
            result = self.conn.execute_query(query)
            # resultset = json.dumps(result)
            df = pd.DataFrame(result)
        except ProfilingException as err:
            raise (f"Error while feching data {err}")
        return df

    def sampling(self):
        df = self.fache_data()
        if df.empty:
            return df
        if self.partition_column_name:

            # Calculate sample sizes per stratum
            sample_sizes = (
                df.groupby(self.partition_column_name).size().reset_index(name="count")
            )
            sample_sizes["sample_size"] = np.ceil(
                sample_sizes["count"] * self.sample_percentage / 100
            ).astype(int)

            # Perform stratified sampling
            sampled_data = (
                df.groupby(self.partition_column_name, group_keys=False)
                .apply(
                    lambda x: x.sample(
                        n=sample_sizes[
                            sample_sizes[self.partition_column_name] == x.name
                        ]["sample_size"].values[0],
                        replace=False,
                    )
                )
                .reset_index(drop=True)
            )

            return sampled_data
        else:
            raise ProfilingException(
                "Partition column name and total sample size are required for sampling."
            )
    def format_json(self, metrics):
        # Load the JSON data
        json_data = json.loads(metrics)
        # Extract specific sections from the JSON data
        variables = json_data["variables"]

        # Define the desired keys for filtering
        desired_keys = [
            "n_distinct",
            "p_distinct",
            "n_missing",
            "p_missing",
            "n_infinite",
            "p_infinite",
            "mean",
            "min",
            "max",
            "n_zeros",
            "p_zeros",
            "n_negative",
            "p_negative",
            "memory_size",
            "histogram",
            "5%",
            "25%",
            "50%",
            "75%",
            "95%",
            "range",
            "iqr",
            "std",
            "cv",
            "kurtosis",
            "mad",
            "skewness",
            "sum",
            "variance",
            "max_length",
            "mean_length",
            "median_length",
            "min_length",
            "n_characters",
            "n_characters_distinct",
            "n_unique",
            "p_unique"
        ]

        # Filter the variables based on desired keys
        filtered_variables = {}

        # Iterate over each section in variables
        for section_name, section_info in variables.items():
            temp = {
                key: value for key, value in section_info.items() if key in desired_keys
            }
            filtered_variables[section_name] = {}
            filtered_variables[section_name].update(temp)

        desired_keys_for_statistics = [
            "max_length",
            "mean_length",
            "median_length",
            "min_length",
            "n_characters",
            "n_characters_distinct",
            "n_unique",
            "p_unique",
            "5%",
            "25%",
            "50%",
            "75%",
            "95%",
            "range",
            "iqr",
            "std",
            "cv",
            "kurtosis",
            "mad",
            "skewness",
            "sum",
            "variance"
        ]

        filtered_variables_with_stats = {}

        for section_name, section_info in filtered_variables.items():
            # Start with an empty "Statistics" dictionary
            filtered_variables_with_stats[section_name] = {"Statistics": {}}

            # Add the desired keys to the "Statistics" dictionary
            for key in desired_keys_for_statistics:
                if key in section_info:
                    filtered_variables_with_stats[section_name]["Statistics"][key] = (
                        section_info[key]
                    )

            # Add the remaining keys from filtered_variables to the section
            for key, value in section_info.items():
                if key not in desired_keys_for_statistics:
                    if (
                        key != "Statistics"
                    ):  # Exclude 'Statistics' if present in filtered_variables
                        filtered_variables_with_stats[section_name][key] = value

        # missing value dict
        missing = {"count": [], "column_name": []}

        for key in filtered_variables.keys():
            missing["column_name"].append(key)
            missing["count"].append(filtered_variables[key]["n_missing"])

        # Prepare filtered data
        filtered_data = {
            "table": json_data["table"],
            "alerts": json_data["alerts"],
            "analysis": json_data["analysis"],
            "variables": filtered_variables_with_stats,
            "correlations": json_data["correlations"],
            "missing": missing,
        }

        # Add ydata_profiling_version from package to analysis
        filtered_data["analysis"]["ydata_profiling_version"] = json_data["package"][
            "ydata_profiling_version"
        ]

        rename_mapping = {
            "n_distinct": "no_of_distinct_values",
            "p_distinct": "percent_of_distinct_values",
            "n_missing": "no_of_missing_values",
            "p_missing": "percent_of_missing_values",
            "n_infinite": "no_of_infinite_values",
            "p_infinite": "percent_of_infinite_values",
            "min": "min_value",
            "max": "max_value",
            "n_zeros": "no_of_zeros",
            "p_zeros": "percent_of_zeros",
            "n_negative": "no_of_negative_values",
            "p_negative": "percent_of_negative_values",
            "5%": "5th_percentile",
            "25%": "25th_percentile",
            "50%": "50th_percentile",
            "75%": "75th_percentile",
            "95%": "95th_percentile",
            "iqr": "interquartile_range",
            "std": "standard_deviation",
            "cv": "coefficient_of_variation",
            "mad": "mean_absolute_deviation",
            "n_characters": "no_of_characters",
            "n_characters_distinct": "no_of_distinct_characters",
            "n_unique": "no_of_unique_values",
            "p_unique": "percent_of_unique_values",
            "n": "no_of_rows",
            "n_var": "no_of_variables",
            "n_cells_missing": "no_of_cells_missing",
            "n_vars_with_missing": "no_of_variables_with_missing_values",
            "n_vars_all_missing": "no_of_variables_all_missing_values",
            "p_cells_missing": "percent_of_cells_with_missing_values",
            "types": "data_types",
            "n_duplicates": "no_of_duplicates",
            "p_duplicates": "percent_of_duplicates"

        }
        def rename_keys(d, mapping):
            if isinstance(d, dict):
                return {mapping.get(k, k): rename_keys(v, mapping) for k, v in d.items()}
            elif isinstance(d, list):
                return [rename_keys(i, mapping) for i in d]
            else:
                return d
            
        filtered_data["variables"] = rename_keys(filtered_data["variables"], rename_mapping)
        filtered_data["table"] = rename_keys(filtered_data["table"], rename_mapping)
        return filtered_data
    
    def profiler(self):
        data_frame = self.sampling()
        if data_frame is None:
            raise ProfilingException("No DataFrame provided for profiling.")
        if data_frame.empty:
            return {}
        if self.selected_column:
            self.selected_column = [col for col in self.selected_column if col in data_frame.columns]
            data_frame = data_frame[self.selected_column]

        profile = ProfileReport(data_frame)
        metrics = profile.to_json()
        result = self.format_json(metrics)
        print(result)
        return result
