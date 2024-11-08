from datetime import datetime
from .sigmadq_helper_functions import sigmadq_helper_functions
import time 
from collections import Counter


# COMMAND ----------

from_date = 0
to_date = 0
helper = sigmadq_helper_functions()

# COMMAND ----------


class sigmadq_core_functions:
    # TODO email, phone number - to be added from GE
    def __init__(self, target_table, meta) -> None:
        self.target_table = target_table
        self.meta = meta

    # COMMAND ----------

    def sigma_helper_add_execution_filter(
        self,
        execution_type,
        custom_filter,
        target_table,
        target_column=None,
        column_name="update_ts",
    ):
        filter_string = ""
        if execution_type == "incremental":
            filter_string = (
                f" {column_name} = (select MAX({column_name}) from {target_table})"
            )
        elif execution_type == "custom":
            filter_string = f" {custom_filter}"
        return filter_string

    # COMMAND ----------

    def sigma_dq_check_leadingZero(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        minimum_zeros,
        execution_type="",
        custom_filter="",
    ):
        leading_zeros = ""
        column = target_column
        conn = connection_obj
        dq_rule = "leadingZero"
        StrSQl = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table, target_column
        )
        for i in range(minimum_zeros):
            leading_zeros += "0"
        leading_zeros += "%"

        if conn._is_mysql() or conn._is_databricks():
            logic = f"case when {target_column} is not null and {target_column} like '{leading_zeros}'"
            StrSQl = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        elif conn._is_postgres():
            logic = f"case when {target_column} is not null and cast({target_column} as text) like '{leading_zeros}'"
            StrSQl = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        elif conn._is_snowflake():
            logic = "case when {target_column} is not null and {target_column} like '{leading_zeros}'"
            StrSQl = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        elif conn._is_bigquery():
            logic = f"case when {target_column} is not null and cast({target_column} as string) like '{leading_zeros}'"
            StrSQl = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        if applied_filters != "":
            StrSQl += f" WHERE {applied_filters}"

        casewhen_logic = (
            f" {logic} THEN '' ELSE '"
            + target_column
            + " for rule "
            + dq_rule
            + " Failed, ' END "
        )

        dq_apply_column_data = conn.execute_query(StrSQl)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isExisting(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        and_logic = "#and#"
        or_logic = "%OR%"
        userinput = ">0"
        column = target_column
        conn = connection_obj
        dq_rule = "isExisting"
        casewhenlogic = " case when "

        target_table_for_join = target_table.split(".")
        schema = target_table_for_join[0]
        modified_target_column = target_table_for_join[1] + "." + target_column

        # get correct pass count
        if api_response.__contains__("%OR%"):
            table_list = api_response.split("%OR%")
            sub_query = ""
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += " OR "
                sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "

        elif api_response.__contains__("#AND#"):
            table_list = api_response.split("#AND#")
            sub_query = ""
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += " AND "
            sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "

        elif (
            not api_response.__contains__("%OR%")
            and not api_response.__contains__("#AND#")
            and api_response != ""
        ):
            single_table = api_response
            left_join_table = schema + "." + single_table.split(".")[0]
            left_join_column = single_table.split(".")[1]
            sub_query = f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "

        else:
            return "Error please check the input dqRule:sigma_dq_check_isExisting"

        if execution_type == "incremental":
            if api_response == "":
                sub_query += (
                    " UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "
                    + target_table
                    + ") "
                )
            else:
                sub_query = (
                    "( "
                    + sub_query
                    + " ) and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "
                    + target_table
                    + ") "
                )

        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            if api_response == "":
                sub_query += f" {between_condition} "
            else:
                sub_query = "( " + sub_query + " ) and " + between_condition

        elif execution_type == "custom":
            if api_response == "":
                sub_query += " where " + custom_filter
            else:
                print("Line No 63")
            sub_query = "( " + sub_query + " )  and " + custom_filter

        pass_count_query = (
            f"select count({modified_target_column}) from {target_table} "
        )
        if sub_query != "":
            pass_count_query += f" where {sub_query}"

        casewhenlogic += sub_query
        total_count_query = f"select count(*) from {target_table} "
        if execution_type == "incremental":
            total_count_query += (
                " WHERE UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from "
                + target_table
                + ") "
            )

        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            total_count_query += f" {between_condition} "

        elif execution_type == "custom":
            print("Line No 82")
            total_count_query += " where " + custom_filter
        # get failed values
        if api_response.__contains__("%OR%"):
            modifiedApiOR_Res = api_response.split("%OR%")
            modifiedORFinal = ""
            modifiedORLeftjoin = ""
            left_join_singleTable = ""
            for singleTable in modifiedApiOR_Res:
                left_join_singleTable = singleTable.split(".")
                index = modifiedApiOR_Res.index(singleTable)
                if index >= 1:
                    modifiedORFinal += (
                        " OR " + modified_target_column + " = " + singleTable
                    )  # operator goes here
                    if modifiedORLeftjoin.__contains__(left_join_singleTable[0]):
                        modifiedORLeftjoin += (
                            " AND " + modified_target_column + " = " + singleTable
                        )
                    else:
                        modifiedORLeftjoin += (
                            " left join "
                            + target_table_for_join[0]
                            + "."
                            + left_join_singleTable[0]
                            + " on "
                            + modified_target_column
                            + " = "
                            + singleTable
                        )
                else:
                    modifiedORFinal += (
                        modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedORLeftjoin = (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedORFinal
                + " \
                        THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
            )

        elif api_response.__contains__("#and#"):
            modified_api_and_res = api_response.split("#and#")
            modifiedANDFinal = ""
            modifiedANDLeftjoin = ""
            left_join_singleTable = ""
            for singleTable in modified_api_and_res:
                left_join_singleTable = singleTable.split(".")
                index = modified_api_and_res.index(singleTable)
                if index >= 1:
                    modifiedANDFinal += (
                        " AND " + modified_target_column + " = " + singleTable
                    )  # operator goes here
                    if modifiedANDLeftjoin.__contains__(left_join_singleTable[0]):
                        modifiedANDLeftjoin += (
                            " AND " + modified_target_column + " = " + singleTable
                        )
                    else:
                        modifiedANDLeftjoin += (
                            " left join "
                            + target_table_for_join[0]
                            + "."
                            + left_join_singleTable[0]
                            + " on "
                            + modified_target_column
                            + " = "
                            + singleTable
                        )
                else:
                    modifiedANDFinal += (
                        modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedANDLeftjoin = (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedANDFinal
                + " \
                    THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedANDLeftjoin
            )

        elif (
            not api_response.__contains__("%OR%")
            and not api_response.__contains__("#AND#")
            and api_response != ""
        ):
            modifiedAPIResponsefirnotcontain = api_response
            modifiedORFinal = ""
            left_join_singleTable = modifiedAPIResponsefirnotcontain.split(".")
            modifiedORFinal += (
                modified_target_column + " = " + api_response
            )  # operator goes here
            modifiedORLeftjoin = (
                " left join "
                + target_table_for_join[0]
                + "."
                + left_join_singleTable[0]
                + " on "
                + modified_target_column
                + " = "
                + api_response
            )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedORFinal
                + " \
                        THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
            )

        else:
            return "Error please check the input dqRule:sigma_dq_check_isExisting"

        if execution_type == "incremental":
            StrSQl += (
                " WHERE "
                + target_table
                + ".UPDATE_RUN_TS = (select MAX("
                + target_table
                + ".UPDATE_RUN_TS) from "
                + target_table
                + ") "
            )

        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' WHERE cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            StrSQl += between_condition

        elif execution_type == "custom":
            print("Line No 149" + custom_filter)
            StrSQl += " where " + target_table + "." + custom_filter

        # print("Before dq_apply_column_data " + StrSQl)
        dq_apply_column_data = conn.execute_query(StrSQl)
        # print("total_count_query. " + total_count_query)
        total_count = conn.execute_query(total_count_query)
        # print("pass_count_query  " + pass_count_query)
        pass_count = conn.execute_query(pass_count_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]
        key = [key for key in pass_count[0].keys()]
        pass_count = pass_count[0][f"{key[0]}"]
        # print(total_count, pass_count)
        dq_report = helper.sigma_dq_generate_dq_report_for_joins(
            dq_apply_column_data, column, dq_rule, total_count, pass_count, meta={}
        )
        # return dq_report

        # Generate DQ report based on the isExisting check
        # dq_report = helper.sigma_dq_generate_dq_report(dq_apply_column_data, column, dq_rule)

        casewhenlogic += f" THEN '' ELSE '{column} for rule {dq_rule} Failed,'  END "
        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhenlogic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_core_isExisting(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isExisting"
        casewhenlogic = " case when "
        target_table_for_join = target_table.split(".")
        schema = target_table_for_join[0]
        modified_target_column = target_table_for_join[1] + "." + target_column
        sql_str = ""

        applied_filters = helper.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if api_response.__contains__("%OR%"):
            sub_query = ""
            table_list = api_response.split("%OR%")
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += "OR"
                sub_query += f" {target_column} in (select distinct {left_join_column} from {left_join_table}) "

        elif api_response.__contains__("#AND#"):
            sub_query = ""
            table_list = api_response.split("#AND#")
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += "AND"
                sub_query += f" {target_column} in (select distinct {left_join_column} from {left_join_table}) "

        elif (
            not api_response.__contains__("%OR%")
            and not api_response.__contains__("#AND#")
            and api_response != ""
        ):
            sub_query = ""
            left_join_table = schema + "." + api_response.split(".")[0]
            left_join_column = api_response.split(".")[1]
            sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table})"

        else:
            return "Error please check the input dqRule:sigma_dq_check_isExisting"

        sql_str += f"select {column}, case when {sub_query} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        if applied_filters != "":
            sql_str += f" WHERE {applied_filters}"

        casewhen_logic = (
            f"{casewhenlogic}"
            + f" {sub_query} "
            + " then '' else '"
            + f" {column} for {dq_rule} Failed ' end "
        )

        dq_apply_column_data = conn.execute_query(sql_str)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isBlank(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isBlank"
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql() or conn._is_snowflake():
            logic = (
                f"case when {target_column} is not null AND TRIM({target_column}) <> ''"
            )
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS' "
                f"else 'FAIL' end as dq_status from  {target_table} "
            )
        elif conn._is_postgres():
            logic = f"case when {target_column} is not null AND TRIM(cast({target_column} as text)) <> ''"
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS' "
                f"else 'FAIL' end as dq_status from  {target_table} "
            )
        elif conn._is_bigquery():
            logic = f"case when {target_column} is not null AND TRIM(cast({target_column} as string)) <> ''"
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS'"
                f"else 'FAIL' end as dq_status from  `{target_table}` "
            )
        elif conn._is_databricks():
            logic = (
                f"case when {target_column} is not null AND TRIM({target_column}) <> ''"
            )
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS' "
                f"else 'FAIL' end as dq_status from  {target_table} "
            )

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        casewhen_logic = (
            logic
            + "THEN '' ELSE '"
            + target_column
            + " for rule "
            + dq_rule
            + " Failed, ' END "
        )

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isNull(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        conn = connection_obj
        column = target_column
        dq_rule = "isNull"
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        if conn._is_mysql() or conn._is_snowflake():
            logic = (
                f"case when {target_column} is not null AND TRIM({target_column}) <> ''"
            )
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS' "
                f"else 'FAIL' end as dq_status from  {target_table} "
            )
        elif conn._is_postgres():
            logic = f"case when {target_column} is not null AND TRIM(cast({target_column} as text)) <> ''"
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS' "
                f"else 'FAIL' end as dq_status from  {target_table} "
            )
        elif conn._is_bigquery():
            logic = f"case when {target_column} is not null AND TRIM(cast({target_column} as string)) <> ''"
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS'"
                f"else 'FAIL' end as dq_status from  `{target_table}` "
            )
        elif conn._is_databricks():
            logic = (
                f"case when {target_column} is not null AND TRIM({target_column}) <> ''"
            )
            str_sql = (
                f"select {target_column} ,{logic} then 'PASS' "
                f"else 'FAIL' end as dq_status from  {target_table} "
            )

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        casewhen_logic = (
            f" {logic} THEN '' ELSE '{target_column} for rule {dq_rule} Failed, ' END"
        )
        dq_apply_column_data = conn.execute_query(str_sql)
        # print(dq_apply_column_data)
        # t.sleep(30)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_core_isDecimalCond(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isDecimalWithCondition"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            logic = f"case when {target_column} like '%.%'"
            str_sql = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"
        elif conn._is_postgres():
            logic = f"case when cast({target_column} as text) like '%.%'"
            str_sql = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"
        elif conn._is_bigquery():
            logic = f"case when cast({target_column} as string) like '%.%'"
            str_sql = f"select {target_column}, {logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        condition = (
            api_response.replace("#AND#", " AND ")
            .replace("%OR%", " OR ")
            .replace("%=%", " = ")
            .replace("%>%", " > ")
            .replace("%<%", " < ")
            .replace("%>=%", " >= ")
            .replace("%<=%", " <= ")
            .replace("%!=%", " != ")
        )
        str_sql += f" WHERE {condition}"

        if applied_filters != "":
            str_sql += f" AND {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhen_logic = f" {logic} AND {condition} THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END"
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isPositiveNumber(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isPositiveNumber"

        ## create temp view for running complex select queries

        casewgenlogic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        # SQL query to check isPositiveNumber for the target_column and generate DQ_Status

        StrSQl = f"SELECT {target_column}, CASE WHEN {target_column} >= 0 THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        if applied_filters != "":
            StrSQl += f" WHERE {applied_filters}"
        # Generate DQ report based on the isPositiveNumber check
        dq_apply_column_data = conn.execute_query(StrSQl)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return ("", dq_report)

        elif meta["report"] == "comprehensive":
            # SQL query to generate comprehensive report with dqMessage_
            casewgenlogic = f" CASE WHEN {target_column} >= 0 THEN '' ELSE '{column} for rule {dq_rule} Failed, ' end"
            return (casewgenlogic, dq_report, target_column)
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isInNotList(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        list_of_values,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        dq_rule = "isNotInList"
        conn = connection_obj
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        list_of_values = [value.strip() for value in list_of_values.split(",")]
        str_sql = (
            "select "
            + target_column
            + ", case when "
            + target_column
            + " not in ("
            + ",".join(["'" + item + "'" for item in list_of_values])
            + ") then 'PASS' else 'FAIL' end as dq_status from "
            + target_table
        )

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        casewhen_logic = (
            "case when "
            + target_column
            + " not in ("
            + ",".join(['"' + item + '"' for item in list_of_values])
            + ") then '' else ' "
            + target_column
            + "for rule"
            + dq_rule
            + "Failed, ' end"
        )
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isInList(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        comma_separated_values,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isInList"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        list_of_values = [value.strip() for value in comma_separated_values.split(",")]

        str_sql = (
            "select "
            + target_column
            + ", case when "
            + target_column
            + " in ("
            + ",".join(["'" + item + "'" for item in list_of_values])
            + ") then 'PASS' else 'FAIL' end as dq_status from "
            + target_table
        )

        # str_sql = f"select {target_column}, case when {target_column} in ('{','.join(list_of_values)}') then 'PASS' else 'FAIL' end as dq_status from {target_table} "
        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"
        # casewhen_logic = f"CASE WHEN {target_column} in ('{','.join(list_of_values)}') THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END"
        casewhen_logic = (
            "case when "
            + target_column
            + " in ("
            + ",".join(['"' + item + '"' for item in list_of_values])
            + ") then '' else ' "
            + target_column
            + " for rule "
            + dq_rule
            + " Failed, ' end"
        )
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_customPatternCheck(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "customPatternCheck"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            logic = f"CASE WHEN {target_column} REGEXP '{api_response}'"
            str_sql = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table} "
        elif conn._is_postgres():
            logic = f"CASE WHEN cast({target_column} as text) ~ '{api_response}'"
            str_sql = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table} "
        elif conn._is_bigquery():
            logic = f"CASE WHEN REGEXP_CONTAINS(cast( {target_column} as string), r'{api_response}')"
            str_sql = f"SELECT  {target_column},{logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table} "

        casewhen_logic = (
            f" {logic} THEN '' ELSE '{target_column} for rule {dq_rule} Failed, ' END"
        )

        if target_column == "C_GLOBAL_ITEM_NUMBER" and "fsitem" in target_table.lower():
            str_sql += f" WHERE ITEM_CODE not ilike '%ALT%' and STATUS_IND IN (200,230,500) and CLASS NOT IN ('CAF','CUF','LGA','TPI','PMI') "
            casewhen_logic = f" CASE WHEN {target_column} NOT REGEXP '{api_response}' and ITEM_CODE not ilike '%ALT%' and STATUS_IND IN (200,230,500) and CLASS NOT IN ('CAF','CUF','LGA','TPI','PMI') THEN '{target_column} for rule {dq_rule} Failed, ' ELSE '' END "

        elif (
            target_column == "C_GLOBAL_ITEM_NUMBER"
            and "fsformula" in target_table.lower()
        ):
            str_sql += f" WHERE FORMULA_CODE not ilike '%ALT%' and STATUS_IND IN (200,230,500) and CLASS NOT IN ('CAF','CUF','LGA')"
            casewhen_logic = f" CASE WHEN {target_column} NOT REGEXP '{api_response}' and FORMULA_CODE not ilike '%ALT%' and STATUS_IND IN (200,230,500) and CLASS NOT IN ('CAF','CUF','LGA') THEN '{target_column} for rule {dq_rule} Failed, ' ELSE '' END "

        elif (
            target_column == "C_GLOBAL_ITEM_NO"
            and "fsspecification" in target_table.lower()
        ):
            str_sql += f" WHERE SPECIFICATION_CODE not ilike '%ALT%' and STATUS_IND IN (200,230,500) and CLASS NOT IN ('CAF','CUF','LGA')"
            casewhen_logic = f" CASE WHEN {target_column} NOT REGEXP '{api_response}' and SPECIFICATION_CODE not ilike '%ALT%' and STATUS_IND IN (200,230,500) and CLASS NOT IN ('CAF','CUF','LGA') THEN '{target_column} for rule {dq_rule} Failed, ' ELSE '' END "

        if applied_filters and "WHERE" in applied_filters:
            str_sql += f" AND {applied_filters}"
        elif applied_filters:
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isNullCondition(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):

        column = target_column
        conn = connection_obj
        dq_rule = "isNullCond"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        main_condition = f"({target_column} is null or trim({target_column}) = '') "
        conditions = api_response.replace("#and#", " AND ").replace("%OR%", " OR ")

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            str_sql = f"select {target_column},case when {main_condition} then 'FAIL' else 'PASS' end as dq_status from {target_table} where {conditions}"
            casewhen_logic = f" case when {conditions} and {main_condition} then '{target_column} for rule {dq_rule} Failed, ' else '' end "
        elif conn._is_postgres():
            str_sql = f"select {target_column},case when {target_column} is null or trim(cast({target_column} as text)) = '' then 'FAIL' else 'PASS' end as dq_status from {target_table} where {conditions}"
            casewhen_logic = f" case when {conditions} and {target_column} is null or trim(cast({target_column} as text)) = '' then '{target_column} for rule {dq_rule} Failed, ' else '' end "
        elif conn._is_bigquery():
            str_sql = f"select {target_column},case when {target_column} is null or trim(cast({target_column} as string)) = '' then 'FAIL' else 'PASS' end as dq_status from {target_table} where {conditions}"
            casewhen_logic = f" case when {conditions} and {target_column} is null or trim(cast({target_column} as string)) = '' then '{target_column} for rule {dq_rule} Failed, ' else '' end "

        if applied_filters:
            str_sql += f" and {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isAscii(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isASCII"
        case_when_logic = ""

        StrSQl = f"select {target_column}, case when {target_column} between 0 and 127 then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        case_when_logic = (
            "  CASE WHEN "
            + target_column
            + " between 0 and 127 "
            + " THEN ''"
            + " ELSE '"
            + column
            + " for rule "
            + dq_rule
            + " Failed, "
            + "' END"
        )

        if applied_filters != "":
            StrSQl += f" where {applied_filters}"

        dq_apply_column_data = conn.execute_query(StrSQl)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )
        if meta["report"] == "report_only":
            return ("", dq_report)

        elif meta["report"] == "comprehensive":
            # SQL query to generate comprehensive report with dqMessage_

            return (case_when_logic, dq_report, target_column)
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_column_value_lengthCheck(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        dq_rule = "lengthCheck"
        conn = connection_obj
        api_response = api_response.split("#AND#")
        casewhen_logic = ""
        str_sql = ""

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            logic = f"CASE WHEN LENGTH({target_column}) >= {api_response[0]} AND LENGTH({target_column}) <= {api_response[1]}"
            str_sql = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"
        elif conn._is_postgres():
            logic = f"CASE WHEN LENGTH(cast({target_column} as text)) >= {api_response[0]} AND LENGTH(cast({target_column} as text)) <= {api_response[1]}"
            str_sql = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"
        elif conn._is_bigquery():
            logic = f"CASE WHEN LENGTH(cast({target_column} as string)) >= {api_response[0]} AND LENGTH(cast({target_column} as string)) <= {api_response[1]}"
            str_sql = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"

        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if applied_filters:
            str_sql += f" where {applied_filters}"

        casewhen_logic = (
            logic
            + " THEN '' ELSE '"
            + target_column
            + " for rule "
            + dq_rule
            + " Failed, ' END"
        )

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_mathematicalOperationsWithColumn(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        target_column_operation,
        execution_type="",
        custom_filter="",
    ):
        columns = []
        dq_rule = "mathematicalOperationsWithColumn"
        conn = connection_obj
        total_rows_query = ""
        str_sql = ""
        casewhenlogic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if target_column_operation.__contains__("=="):
            columns.extend(target_column_operation.split("=="))
        elif target_column_operation.__contains__(">"):
            columns.extend(target_column_operation.split(">"))
        elif target_column_operation.__contains__("<"):
            columns.extend(target_column_operation.split("<"))
        elif target_column_operation.__contains__(">="):
            columns.extend(target_column_operation.split(">="))
        elif target_column_operation.__contains__("<="):
            columns.extend(target_column_operation.split("<="))
        else:
            raise Exception("target_column_operation is invalid or incorrect")
        columns = [columns[0]]

        # split based on operators
        addition = []
        if target_column_operation.__contains__("#+#"):
            for c in columns:
                addition.extend(c.split("#+#"))
                columns = addition
        subtraction = []
        if target_column_operation.__contains__("#-#"):
            for a in columns:
                subtraction.extend(a.split("#-#"))
                columns = subtraction
        division = []
        if target_column_operation.__contains__("#/#"):
            for s in columns:
                division.extend(s.split("#/#"))
                columns = division
        multiply = []
        if target_column_operation.__contains__("#*#"):
            for d in columns:
                multiply.extend(d.split("#*#"))
                columns = multiply
        query_columns = ", ".join([x.strip() for x in columns])
        column_operation = (
            target_column_operation.replace("#+#", "+")
            .replace("#-#", "-")
            .replace("#/#", "/")
            .replace("#*#", "*")
        )

        str_sql = f"select {query_columns}, case when {column_operation} then 'PASS' else 'FAIL' end as dq_status from {target_table} "

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        list_of_columns = []
        for c in columns:
            list_of_columns.append(c.strip())
        # print(list_of_columns)
        total_rows_query = f"select count(*) from {target_table}"
        if applied_filters != "":
            total_rows_query += f" WHERE {applied_filters}"
        total_count = conn.execute_query(total_rows_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]

        # additional handling required for list of columns as main argument
        failed_values_dict = {}
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = {}
        dq_report["column"] = target_column
        dq_report["rule"] = dq_rule
        dq_report["total_rows_checked"] = total_count
        total_DQ_Pass_count = sum(
            1 for item in dq_apply_column_data if item.get("dq_status") == "PASS"
        )
        dq_report["total_rows_failed"] = sum(
            1 for item in dq_apply_column_data if item.get("dq_status") == "FAIL"
        )
        if dq_report["total_rows_failed"] > 0:
            dq_report["success"] = False
            dq_report["failed_percent"] = (
                dq_report["total_rows_failed"] / dq_report["total_rows_checked"]
            ) * 100

            raw_fail_list = [
                item.get(target_column)
                for item in dq_apply_column_data
                if item.get("dq_status") == "FAIL"
            ]
            # dq_apply_column_data_ = dq_apply_column_data.filter(
            #     dq_apply_column_data.DQ_Status == "FAIL"
            # ).toPandas()
            # failed_values_dict = dq_apply_column_data_.to_dict(orient="list")

            # for i in dq_apply_column_data.columns:
            #     if i not in list_of_columns:
            #         del failed_values_dict[i]

            raw_fail_list_ = list(set(raw_fail_list))
            dq_report["failed_values"] = raw_fail_list_
        elif dq_report["total_rows_failed"] == dq_report["total_rows_checked"]:
            dq_report["success"] = False
            try:
                dq_report["failed_percent"] = (
                    dq_report["total_rows_failed"] / dq_report["total_rows_checked"]
                ) * 100
            except:
                dq_report["failed_percent"] = 0
                dq_report["failed_values"] = []
        else:
            dq_report["success"] = True
            dq_report["passed_percent"] = (
                total_DQ_Pass_count / dq_report["total_rows_checked"]
            ) * 100

        dq_report["meta"] = meta

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhenlogic = f"case when {column_operation} THEN '' ELSE '{target_column} for rule {dq_rule} Failed, ' END "
            return casewhenlogic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_mathematicalCalculations(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        left_join_table,
        api_response2,
        execution_type="",
        custom_filter="",
    ):

        column = target_column
        conn = connection_obj
        target_column_operation = api_response
        dq_rule = "fieldCompareWithMathematicalOperations"
        target_table_for_join = target_table.split(".")
        schema = target_table_for_join[0]
        str_sql = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        # split based on comparator
        columns = []
        total_rows_query = ""
        total_rows_query = f"select count(*) from {target_table}"
        if applied_filters != "":
            total_rows_query += f" WHERE {applied_filters} "
        if target_column_operation.__contains__("#+#"):
            columns.extend(target_column_operation.split("#+#"))
        elif target_column_operation.__contains__("#-#"):
            columns.extend(target_column_operation.split("#-#"))
        elif target_column_operation.__contains__("#/#"):
            columns.extend(target_column_operation.split("#/#"))
        elif target_column_operation.__contains__("#*#"):
            columns.extend(target_column_operation.split("#*#"))
        else:
            raise Exception("target_column_operation is invalid or incorrect")
        columns.append(target_column)
        query_columns = ", ".join([x.strip() for x in columns])

        api_response = (
            api_response.replace("#+#", "+")
            .replace("#-#", "-")
            .replace("#*#", "*")
            .replace("#/#", "/")
        )
        if api_response2 == "":
            if (
                conn._is_mysql()
                or conn._is_snowflake()
                or conn._is_bigquery()
                or conn._is_databricks()
            ):
                logic = f"case when round({target_column},2) = round({api_response},2)"
                str_sql = (
                    f"select {query_columns}, {logic} "
                    f"then 'PASS' else 'FAIL' end as dq_status from {target_table} "
                )
            elif conn._is_postgres():
                logic = f"case when round(cast({target_column} as numeric),2) = round(cast({api_response} as numeric),2)"
                str_sql = (
                    f"select {query_columns}, {logic} "
                    f"then 'PASS' else 'FAIL' end as dq_status from {target_table} "
                )

            if applied_filters != "":
                str_sql += f" WHERE {applied_filters} "
        else:
            if api_response2.__contains__("="):
                modifiedApiORR_Res = target_table.split("#AND#")  # No need
                lsTempTargetTable = "".join(modifiedApiORR_Res)
                modifiedApiResForCaseWhen = api_response.replace("=", "==")
                modifiedAPIResponseForEqualTo = api_response2.split("=")
                stripmodifiedAPIResponseForEqualTo = []  # stripping
                tableNameInApi_response = []
                modifiedAPIResponseForEqualToTemp = ""
                onStringquery = ""
                onStringquery1 = ""

                for index in modifiedAPIResponseForEqualTo:  # APIResponse  #No need
                    stripmodifiedAPIResponseForEqualTo.append(index.strip())
                    tableNameInApi_response.append(index.split(".")[1])
                    if onStringquery == "":
                        onStringquery = (
                            schema
                            + "."
                            + tableNameInApi_response[0]
                            + "."
                            + index.split(".")[2].strip()
                        )
                        # if onStringquery == 'ITEM_CODE':
                        if onStringquery.__contains__("ITEM_CODE"):
                            onStringquery = onStringquery.replace(
                                "ITEM_CODE", "regexp_replace(ITEM_CODE, '^0+', '')"
                            )
                    else:
                        onStringquery1 = (
                            schema
                            + "."
                            + tableNameInApi_response[1]
                            + "."
                            + index.split(".")[2].strip()
                        )
                        if onStringquery1.__contains__("ITEM_CODE"):
                            onStringquery1 = onStringquery1.replace(
                                "ITEM_CODE", "regexp_replace(ITEM_CODE, '^0+', '')"
                            )
                        onStringquery += " = " + onStringquery1

                for item in modifiedAPIResponseForEqualTo:
                    if lsTempTargetTable in item.strip():
                        continue
                    else:
                        modifiedAPIResponseForEqualToTemp = item.strip()
                index = modifiedAPIResponseForEqualToTemp.index(".")
                dot_count = modifiedAPIResponseForEqualToTemp.count(".")
                if dot_count == 2:
                    modifiedAPIResponseForEqualToTemp = (
                        modifiedAPIResponseForEqualToTemp.rsplit(".", 1)
                    )
                    # if lsTempTargetTable in modifiedAPIResponseForEqualToTemp
                else:
                    modifiedAPIResponseForEqualToTemp = (
                        modifiedAPIResponseForEqualToTemp[:index]
                    )

                for (
                    singleTable
                ) in (
                    modifiedApiORR_Res
                ):  # leftjointable #targettable and leftjointable connection
                    index = modifiedApiORR_Res.index(singleTable)
                    api_responseSecond = targetTableAPI + " = " + target_table
                    api_response_added = api_response + " and " + api_responseSecond
                    temp1 = modifiedApiORR_Res[0].split(".")

                if (
                    target_table.split(".")[0] in tableNameInApi_response
                ):  # checking leftjoin table isin apiResponse
                    andClause = ""
                    leftjointabledetails = (
                        "left join " + target_table_for_join[0] + "." + temp1[0]
                    )
                    modifiedORLeftjoin = (
                        leftjointabledetails + " on " + api_responseSecond
                    )
                    # if tableNameInApi_response not in modifiedORLeftjoin
                    for stv in tableNameInApi_response:
                        if stv in leftjointabledetails:
                            continue
                        else:
                            stv = stv.strip()
                            if stv != target_table_for_join[1]:
                                andClause = (
                                    " left join "
                                    + target_table_for_join[0]
                                    + "."
                                    + stv
                                    + " on "
                                    + api_response
                                )
                                # andClause = " and "+api_response

                else:
                    modifiedORLeftjoin = (
                        " left join "
                        + modifiedAPIResponseForEqualToTemp[0]
                        + " on "
                        + onStringquery
                    )

                if (
                    conn._is_mysql()
                    or conn._is_snowflake()
                    or conn._is_bigquery()
                    or conn._is_databricks()
                ):
                    logic = (
                        f"case when round({target_column},2) = round({api_response},2)"
                    )
                    str_sql = (
                        f" select {query_columns}, {logic}"
                        f" then 'PASS' else 'FAIL' end as dq_status from {target_table} {modifiedORLeftjoin}"
                    )
                elif conn._is_postgres():
                    logic = f"case when round(cast({target_column} as numeric),2) = round(cast({api_response} as numeric),2)"
                    str_sql = (
                        f" select {query_columns}, {logic}"
                        f" then 'PASS' else 'FAIL' end as dq_status from {target_table} {modifiedORLeftjoin}"
                    )
                if applied_filters != "":
                    str_sql += f" WHERE {applied_filters} "

        list_of_columns = []
        for c in columns:
            list_of_columns.append(c.strip())
        # print(list_of_columns)

        dq_apply_column_data = conn.execute_query(str_sql)
        ## additional handling required for list of columns as main argument
        failed_values_dict = {}
        dq_report = {}
        dq_report["column"] = target_column
        dq_report["rule"] = dq_rule
        total_count = conn.execute_query(total_rows_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]
        dq_report["total_rows_checked"] = total_count
        total_DQ_Pass_count = sum(
            1 for item in dq_apply_column_data if item.get("dq_status") == "PASS"
        )
        dq_report["total_rows_failed"] = sum(
            1 for item in dq_apply_column_data if item.get("dq_status") == "FAIL"
        )
        if dq_report["total_rows_failed"] > 0:
            dq_report["success"] = False
            dq_report["failed_percent"] = (
                dq_report["total_rows_failed"] / dq_report["total_rows_checked"]
            ) * 100
            raw_fail_list = [
                item.get(target_column)
                for item in dq_apply_column_data
                if item.get("dq_status") == "FAIL"
            ]
            # dq_apply_column_data_ = dq_apply_column_data.filter(
            #     dq_apply_column_data.DQ_Status == "FAIL"
            # ).toPandas()
            # failed_values_dict = dq_apply_column_data_.to_dict(orient="list")
            # for i in dq_apply_column_data.columns:
            #     if i not in list_of_columns:
            #         del failed_values_dict[i]

            raw_fail_list_ = list(set(raw_fail_list))
            # raw_fail_list_ = sigma_dq_helper_unique_elements_in_list(raw_fail_list)
            dq_report["failed_values"] = raw_fail_list_
        elif dq_report["total_rows_failed"] == dq_report["total_rows_checked"]:
            dq_report["success"] = False
            try:
                dq_report["failed_percent"] = (
                    dq_report["total_rows_failed"] / dq_report["total_rows_checked"]
                ) * 100
            except:
                dq_report["failed_percent"] = 0
            dq_report["failed_values"] = []
        else:
            dq_report["success"] = True
            try:
                dq_report["passed_percent"] = (
                    total_DQ_Pass_count / dq_report["total_rows_checked"]
                ) * 100
            except:
                dq_report["passed_percent"] = 0

        dq_report["meta"] = meta

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            # SQL query to generate comprehensive report with dqMessage_
            casewhenlogic = (
                f"{logic} then '' ELSE '{column} for rule {dq_rule} Failed, ' END"
            )
            return casewhenlogic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isExistingCond(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        api_response2,
        rule_id=0,
        execution_type="",
        custom="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isExistingCond"
        target_table_for_join = target_table.split(".")
        modified_target_column = target_table_for_join[1] + "." + target_column
        modifiedapi_response = ""
        modifiedapi_responseSplit = api_response.split(".")
        modifiedapi_leftJoinresponse2 = ""
        schema = target_table_for_join[0]
        casewhenlogic = ""
        sub_query3 = ""
        # pass count
        if api_response.__contains__("%OR%"):
            table_list = api_response.split("%OR%")
            sub_query = ""
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += " OR "
                sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "
            sub_query3 = f" not exists (select distinct {left_join_column} from {left_join_table} where {target_column} = {left_join_column}) "

        elif api_response.__contains__("#AND#"):
            table_list = api_response.split("#AND#")
            sub_query = ""
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                # print(left_join_column)
                if table_list.index(single_table) > 0:
                    sub_query += " AND "
                sub_query += f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "
            sub_query3 = f" not exists (select distinct {left_join_column} from {left_join_table} where {target_column} = {left_join_column})"

        elif (
            not api_response.__contains__("%OR%")
            and not api_response.__contains__("#AND#")
            and api_response != ""
        ):
            single_table = api_response
            left_join_table = schema + "." + single_table.split(".")[0]
            left_join_column = single_table.split(".")[1]
            sub_query = f"{target_column} in (select distinct {left_join_column} from {left_join_table}) "
            sub_query3 = f" not exists (select distinct {left_join_column} from {left_join_table} where {target_column} = {left_join_column}) "

        else:
            return "Error please check the input dqRule:sigma_dq_check_isExisting"

        subquery2 = ""
        if api_response2 != "":
            subquery2 = api_response2.replace("#AND#", " AND ").replace("%OR%", " OR ")
            # if subquery2.__contains__(" AND ") or subquery2.__contains__(" OR "):
            # subquery2 = schema + "." + subquery2
            # print(subquery2)
            sub_query = f" ({sub_query}) AND ({subquery2}) "
            sub_query3 = f" ({sub_query3}) AND ({subquery2}) "
        casewhenlogic = sub_query3

        if execution_type == "incremental":
            sub_query = f" ({sub_query}) and UPDATE_RUN_TS = (select MAX(UPDATE_RUN_TS) from {target_table}) "
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(UPDATE_RUN_TS as string) between "{from_date_str}" AND "{to_date_str}"'
            sub_query = f" ({sub_query}) and {between_condition} "

        pass_count_query = (
            f"select count({modified_target_column}) from {target_table} "
        )
        if sub_query != "":
            pass_count_query += f"where {sub_query}"

        # Total count query
        total_count_query = (
            f"select count({modified_target_column}) from {target_table} "
        )

        total_count_query += f" WHERE {subquery2}"
        total_count_subquery = ""

        if execution_type == "incremental":
            total_count_subquery += (
                " update_ts = (select MAX(update_ts) from " + target_table + ") "
            )
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            total_count_subquery += between_condition

        if total_count_subquery != "":
            total_count_query += " AND " + total_count_subquery

        # query for failed values
        StrSQl = ""
        if api_response.__contains__("%OR%"):
            modifiedApiOR_Res = api_response.split("%OR%")
            modifiedORFinal = ""
            modifiedORLeftjoin = ""
            left_join_singleTable = ""
            for singleTable in modifiedApiOR_Res:
                left_join_singleTable = singleTable.split(".")
                index = modifiedApiOR_Res.index(singleTable)
                if index >= 1:
                    modifiedORFinal += (
                        " OR " + modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedORLeftjoin += (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )
                else:
                    modifiedORFinal += (
                        modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedORLeftjoin = (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )

            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedORFinal
                + "THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
            )

        elif api_response.__contains__("#AND#"):
            modifiedApiAND_Res = api_response.split("#AND#")
            modifiedANDFinal = ""
            modifiedANDLeftjoin = ""
            left_join_singleTable = ""
            for singleTable in modifiedApiAND_Res:
                left_join_singleTable = singleTable.split(".")
                index = modifiedApiAND_Res.index(singleTable)
                if index >= 1:
                    modifiedANDFinal += (
                        " AND " + modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedANDLeftjoin += (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )
                else:
                    modifiedANDFinal += (
                        modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedANDLeftjoin = (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )

            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedANDFinal
                + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedANDLeftjoin
            )

        else:  # When my api_response    = 'JDE_VENDOR.global_vendor_number
            modifiedapi_response += (
                modified_target_column + " = " + api_response
            )  # operator goes here
            modifiedORLeftjoin = (
                " left join "
                + target_table_for_join[0]
                + "."
                + modifiedapi_responseSplit[0]
                + " on "
                + modified_target_column
                + " = "
                + api_response
            )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedapi_response
                + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + modifiedORLeftjoin
            )

        if api_response2 != "":
            lsmodifiedApliResponse = ""
            if not api_response2.__contains__("#AND#") and api_response2.__contains__(
                "%OR%"
            ):
                lsmodifiedApliResponse = (
                    # target_table_for_join[0]
                    # + "."
                    api_response2.replace(
                        "%OR%", " OR "  # + target_table_for_join[0] + "."
                    )
                )
            elif not api_response2.__contains__("%OR%") and api_response2.__contains__(
                "#AND#"
            ):
                lsmodifiedApliResponse = (
                    # target_table_for_join[0]
                    # + "."
                    api_response2.replace(
                        "#AND#", " AND "  # + target_table_for_join[0] + "."
                    )
                )
            elif api_response2.__contains__("%OR%") and api_response2.__contains__(
                "#AND#"
            ):
                lsmodifiedApliResponse = (
                    # target_table_for_join[0]
                    # + "."
                    api_response2.replace(
                        "#AND#", "AND "  # + target_table_for_join[0] + "."
                    ).replace(
                        "%OR%", " OR "  # + target_table_for_join[0] + ".")
                    )
                )

            else:
                lsmodifiedApliResponse = api_response2
            StrSQl += " WHERE " + lsmodifiedApliResponse

        else:
            print("Invalid Input")

        if execution_type == "incremental":
            StrSQl += (
                " AND "
                + target_table
                + ".update_ts = (select MAX(update_ts) from "
                + target_table
                + ") "
            )
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            StrSQl += f" AND {between_condition}"

        dq_apply_column_data = conn.execute_query(StrSQl)
        # print("dq_apply_column_data passed")
        # print(total_count_query)
        # print(pass_count_query)
        total_count = conn.execute_query(total_count_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]
        pass_count = conn.execute_query(pass_count_query)
        key = [key for key in pass_count[0].keys()]
        pass_count = pass_count[0][f"{key[0]}"]

        dq_report = helper.sigma_dq_generate_dq_report_for_joins(
            dq_apply_column_data, column, dq_rule, total_count, pass_count, meta={}
        )
        # dq_report["meta"]["rule_id"] = rule_id
        dq_report["meta"]["condition"] = lsmodifiedApliResponse
        # Generate DQ report based on the check
        if meta["report"] == "report_only":
            return ("", dq_report)

        elif meta["report"] == "comprehensive":
            # SQL query to generate comprehensive report with dqMessage_
            CaseStrSQL_ = f" CASE WHEN {casewhenlogic}  THEN '{column} for rule {dq_rule} Failed,' ELSE ''  END "
            # print("sigma_dq_check_isExistingCond "+CaseStrSQL_)
            return (CaseStrSQL_, dq_report, target_column)
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isNotExisting(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        and_logic = "#and#"
        or_logic = "%OR%"
        userinput = ">0"
        column = target_column
        conn = connection_obj
        dq_rule = "isNotExisting"
        casewhenlogic = " case when "
        target_table_for_join = target_table.split(".")
        schema = target_table_for_join[0]
        modified_target_column = target_table_for_join[1] + "." + target_column
        CaseStrSQL_ = ""

        # get correct pass count
        if api_response.__contains__("%OR%"):
            table_list = api_response.split("%OR%")
            sub_query = ""
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += " OR "
                sub_query += f"{target_column} not in (select distinct {left_join_column} from {left_join_table}) "

        elif api_response.__contains__("#AND#"):
            table_list = api_response.split("#AND#")
            sub_query = ""
            for single_table in table_list:
                left_join_table = schema + "." + single_table.split(".")[0]
                left_join_column = single_table.split(".")[1]
                if table_list.index(single_table) > 0:
                    sub_query += " AND "
                sub_query += f"{target_column} not in (select distinct {left_join_column} from {left_join_table}) "

        elif (
            not api_response.__contains__("%OR%")
            and not api_response.__contains__("#AND#")
            and api_response != ""
        ):
            single_table = api_response
            left_join_table = schema + "." + single_table.split(".")[0]
            left_join_column = single_table.split(".")[1]
            sub_query = f"{target_column} not in (select distinct {left_join_column} from {left_join_table}) "

        else:
            return "Error please check the input dqRule:sigma_dq_check_isExisting"

        if execution_type == "incremental":
            if api_response == "":
                sub_query += (
                    " update_ts = (select MAX(update_ts) from " + target_table + ") "
                )
            else:
                sub_query = (
                    "( "
                    + sub_query
                    + " ) and update_ts = (select MAX(update_ts) from "
                    + target_table
                    + ") "
                )

        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            if api_response == "":
                sub_query += f" {between_condition} "
            else:
                sub_query = "( " + sub_query + " ) and " + between_condition

        pass_count_query = (
            f"select count({modified_target_column}) from {target_table} "
        )
        if sub_query != "":
            pass_count_query += f"where {sub_query}"
        casewhenlogic += sub_query
        # Total pass count query
        total_count_query = (
            f"select count({modified_target_column}) from {target_table} "
        )
        if execution_type == "incremental":
            total_count_query += (
                " WHERE source_datetime = (select MAX(source_datetime) from "
                + target_table
                + ") "
            )
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' WHERE cast(source_datetime as string) between "{from_date_str}" AND "{to_date_str}"'
            total_count_query += f" {between_condition} "

        # get failed values
        if api_response.__contains__("%OR%"):
            modifiedApiOR_Res = api_response.split("%OR%")
            modifiedORFinal = ""
            modifiedORLeftjoin = ""
            left_join_singleTable = ""
            for singleTable in modifiedApiOR_Res:
                left_join_singleTable = singleTable.split(".")
            index = modifiedApiOR_Res.index(singleTable)
            if index >= 1:
                modifiedORFinal += (
                    " OR " + modified_target_column + " = " + singleTable
                )  # operator goes here
                if modifiedORLeftjoin.__contains__(left_join_singleTable[0]):
                    modifiedORLeftjoin += (
                        " AND " + modified_target_column + " = " + singleTable
                    )
                else:
                    modifiedORLeftjoin += (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )
            else:
                modifiedORFinal += (
                    modified_target_column + " = " + singleTable
                )  # operator goes here
                modifiedORLeftjoin = (
                    " left join "
                    + target_table_for_join[0]
                    + "."
                    + left_join_singleTable[0]
                    + " on "
                    + modified_target_column
                    + " = "
                    + singleTable
                )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedORFinal
                + " \
                    THEN 'FAIL' ELSE 'PASS' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
            )

        elif api_response.__contains__("#and#"):
            modifiedApiAND_Res = api_response.split("#and#")
            modifiedANDFinal = ""
            modifiedANDLeftjoin = ""
            left_join_singleTable = ""
            for singleTable in modifiedApiAND_Res:
                left_join_singleTable = singleTable.split(".")
                index = modifiedApiAND_Res.index(singleTable)
                if index >= 1:
                    modifiedANDFinal += (
                        " AND " + modified_target_column + " = " + singleTable
                    )  # operator goes here
                    if modifiedANDLeftjoin.__contains__(left_join_singleTable[0]):
                        modifiedANDLeftjoin += (
                            " AND " + modified_target_column + " = " + singleTable
                        )
                    else:
                        modifiedANDLeftjoin += (
                            " left join "
                            + target_table_for_join[0]
                            + "."
                            + left_join_singleTable[0]
                            + " on "
                            + modified_target_column
                            + " = "
                            + singleTable
                        )
                else:
                    modifiedANDFinal += (
                        modified_target_column + " = " + singleTable
                    )  # operator goes here
                    modifiedANDLeftjoin = (
                        " left join "
                        + target_table_for_join[0]
                        + "."
                        + left_join_singleTable[0]
                        + " on "
                        + modified_target_column
                        + " = "
                        + singleTable
                    )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedANDFinal
                + " \
                THEN 'FAIL' ELSE 'PASS' END as dq_status from "
                + target_table
                + " "
                + modifiedANDLeftjoin
            )

        elif (
            not api_response.__contains__("%OR%")
            and not api_response.__contains__("#AND#")
            and api_response != ""
        ):
            modifiedAPIResponsefirnotcontain = api_response
            modifiedORFinal = ""
            left_join_singleTable = modifiedAPIResponsefirnotcontain.split(".")
            modifiedORFinal += (
                modified_target_column + " = " + api_response
            )  # operator goes here
            modifiedORLeftjoin = (
                " left join "
                + target_table_for_join[0]
                + "."
                + left_join_singleTable[0]
                + " on "
                + modified_target_column
                + " = "
                + api_response
            )
            StrSQl = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedORFinal
                + " \
                    THEN 'FAIL' ELSE 'PASS' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
            )

        else:
            return "Error please check the input dqRule:sigma_dq_check_isExisting"

        if execution_type == "incremental":
            StrSQl += (
                " WHERE "
                + target_table
                + ".source_datetime = (select MAX("
                + target_table
                + ".source_datetime) from "
                + target_table
                + ") "
            )
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' WHERE cast(source_datetime as string) between "{from_date_str}" AND "{to_date_str}"'
            StrSQl += between_condition

        dq_apply_column_data = conn.execute_query(StrSQl)
        total_count = conn.execute_query(total_count_query)
        pass_count = conn.execute_query(pass_count_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]
        key = [key for key in pass_count[0].keys()]
        pass_count = pass_count[0][f"{key[0]}"]

        dq_report = helper.sigma_dq_generate_dq_report_for_joins(
            dq_apply_column_data, column, dq_rule, total_count, pass_count, meta={}
        )

        casewhenlogic += f" THEN '' ELSE '{column} for rule {dq_rule} Failed,'  END "
        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhenlogic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isSpace(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isSpace"
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        # SQL query to check isSpace for the target_column and generate DQ_Status
        if conn._is_mysql() or conn._is_databricks():
            logic = f"CASE WHEN {target_column} IS NOT NULL AND {target_column} <> '' AND TRIM({target_column}) = {target_column}"
            StrSQl = f"SELECT {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_postgres():
            logic = f"CASE WHEN {target_column} IS NOT NULL AND cast({target_column} as text) <> '' AND TRIM(cast({target_column} as text)) = cast({target_column} as text)"
            StrSQl = f"SELECT {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_snowflake():
            logic = f"CASE WHEN {target_column} IS NOT NULL AND cast({target_column} as string) <> '' AND TRIM({target_column}) = {target_column}"
            StrSQl = f"SELECT {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_bigquery():
            logic = f"CASE WHEN {target_column} IS NOT NULL AND cast({target_column} as string) <> '' AND TRIM(cast({target_column} as string)) = cast({target_column} as string)"
            StrSQl = f"SELECT {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"

        case_when_logic = (
            logic
            + " THEN '' ELSE '"
            + target_column
            + " for rule "
            + dq_rule
            + " Failed,' END "
        )

        if applied_filters != "":
            StrSQl += f" WHERE {applied_filters}"
        dq_apply_column_data = conn.execute_query(StrSQl)
        # Generate DQ report based on the isSpace check
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )
        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isAlphabet(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isAlphabet"
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            logic = f"case when {target_column} REGEXP '^[a-zA-Z]+$'"
            StrSQl = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"
        elif conn._is_postgres():
            logic = f"case when cast({target_column} as text) ~ '^[a-zA-Z]+$'"
            StrSQl = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"
        elif conn._is_bigquery():
            logic = f"case when REGEXP_CONTAINS(cast( {target_column} as string), r'^[a-zA-Z]+$')"
            StrSQl = f"select {target_column}, {logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"

        if applied_filters != "":
            StrSQl += f" where {applied_filters}"

        dq_apply_column_data = conn.execute_query(StrSQl)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhen_logic = (
                f"{logic} THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END "
            )
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isDate(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isDate"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if (
            api_response == "dd.mm.YYYY"
            or api_response == "dd/mm/YYYY"
            or api_response == "dd-mm-YYYY"
        ):
            if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
                logic = (
                    " CASE WHEN "
                    + target_column
                    + " REGEXP '^([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_postgres():
                logic = (
                    " CASE WHEN "
                    + f"cast({target_column} as text)"
                    + " ~ '^([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_bigquery():
                logic = (
                    " CASE WHEN "
                    + f"REGEXP_CONTAINS(cast({target_column} as string),"
                    + " r'^([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0-9]{4}|[0-9]{2})$') "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic} "
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )

        elif (
            api_response == "mm.dd.YYYY"
            or api_response == "mm/dd/YYYY"
            or api_response == "mm-dd-YYYY"
        ):
            if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
                logic = (
                    " CASE WHEN "
                    + target_column
                    + " REGEXP '^([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_postgres():
                logic = (
                    " CASE WHEN "
                    + f"cast({target_column} as text)"
                    + " ~ '^([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_bigquery():
                logic = (
                    " CASE WHEN "
                    + f"REGEXP_CONTAINS(cast({target_column} as string),"
                    + " r'^([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])[.\/-]([0-9]{4}|[0-9]{2})$') "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )

        elif (
            api_response == "YYYY.mm.dd"
            or api_response == "YYYY/mm/dd"
            or api_response == "YYYY-mm-dd"
        ):
            if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
                logic = (
                    " CASE WHEN "
                    + target_column
                    + " REGEXP '^([0-9]{4}|[0-9]{2})[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_postgres():
                logic = (
                    "CASE WHEN "
                    + f"cast({target_column} as text)"
                    + " ~ '^([0-9]{4}|[0-9]{2})[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_bigquery():
                logic = (
                    " CASE WHEN "
                    + f"REGEXP_CONTAINS(cast({target_column} as string),"
                    + " r'^([0-9]{4}|[0-9]{2})[.\/-]([0]?[1-9]|[1][0-2])[.\/-]([0]?[1-9]|[1|2][0-9]|[3][0|1])$') "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )

        elif api_response == "YYYYmmdd":
            if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
                logic = (
                    " CASE WHEN "
                    + target_column
                    + " REGEXP '^([0-9]{4}|[0-9]{2})([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f",{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_postgres():
                logic = (
                    " CASE WHEN "
                    + f"cast({target_column} as text)"
                    + " ~ '^([0-9]{4}|[0-9]{2})([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_bigquery():
                logic = (
                    " CASE WHEN "
                    + f"REGEXP_CONTAINS(cast({target_column} as string),"
                    + " r'^([0-9]{4}|[0-9]{2})([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])$') "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f"{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )

        elif api_response == "ddmmYYYY":
            if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
                logic = (
                    " CASE WHEN "
                    + target_column
                    + " REGEXP '^([0]?[1-9]|[1|2][0-9]|[3][0|1])([0]?[1-9]|[1][0-2])([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f",{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_postgres():
                logic = (
                    " CASE WHEN "
                    + f"cast({target_column} as text)"
                    + " ~ '^([0]?[1-9]|[1|2][0-9]|[3][0|1])([0]?[1-9]|[1][0-2])([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f", {logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_bigquery():
                logic = (
                    " CASE WHEN "
                    + f"REGEXP_CONTAINS(cast({target_column} as string),"
                    + " r'^([0]?[1-9]|[1|2][0-9]|[3][0|1])([0]?[1-9]|[1][0-2])([0-9]{4}|[0-9]{2})$') "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f",{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )

        elif api_response == "mmddYYYY":
            if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
                logic = (
                    "CASE WHEN "
                    + target_column
                    + " REGEXP '^([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f" ,{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_postgres():
                logic = (
                    " CASE WHEN "
                    + f"cast({target_column} as text)"
                    + " ~ '^([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])([0-9]{4}|[0-9]{2})$' "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f",{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )
            elif conn._is_bigquery():
                logic = (
                    " CASE WHEN "
                    + f"REGEXP_CONTAINS(cast({target_column} as string),"
                    + " r'^([0]?[1-9]|[1][0-2])([0]?[1-9]|[1|2][0-9]|[3][0|1])([0-9]{4}|[0-9]{2})$') "
                )
                str_sql = (
                    "select "
                    + target_column
                    + f",{logic}"
                    + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                    + target_table
                    + "  "
                )

        else:
            print("Incorrect/Unsupported Format Selected")

        # condition = (
        #     api_response.replace("#AND#", " AND ")
        #     .replace("%OR%", " OR ")
        #     .replace("%=%", " = ")
        #     .replace("%>%", " > ")
        #     .replace("%<%", " < ")
        #     .replace("%>=%", " >= ")
        #     .replace("%<=%", " <= ")
        #     .replace("%!=%", " != ")
        # )
        # str_sql += f" WHERE {condition}"

        if applied_filters != "":
            str_sql += f" where {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":

            # casewhen_logic = f" {logic} AND {api_response} THEN '{column} for rule {dq_rule} Failed, ' ELSE '' END"
            casewhen_logic = (
                f" {logic} THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END"
            )

            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isEmail(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isEmail"
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            logic = (
                " CASE WHEN "
                + target_column
                + " is not null and "
                + target_column
                + " REGEXP '[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}' "
            )
            str_sql = (
                "select "
                + target_column
                + f", {logic}"
                + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + "  "
            )
        elif conn._is_postgres():
            logic = (
                " CASE WHEN "
                + target_column
                + " is not null and "
                + " ~ '[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}' "
            )
            str_sql = (
                "select "
                + target_column
                + f", {logic}"
                + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + "  "
            )
        elif conn._is_bigquery():
            logic = (
                " CASE WHEN "
                + target_column
                + " is not null and "
                + f"REGEXP_CONTAINS(cast({target_column} as string),"
                + " r[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}') "
            )
            str_sql = (
                "select "
                + target_column
                + f", {logic}"
                + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + "  "
            )
        case_when_logic = (
            logic
            + " THEN '' else '"
            + target_column
            + " for rule "
            + dq_rule
            + " Failed,' END"
        )
        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )
        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isInListCond(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        list_of_values,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isInListWithCondition"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        str_sql = (
            "select "
            + target_column
            + ", case when "
            + target_column
            + " in ("
            + ",".join(["'" + item + "'" for item in list_of_values])
            + ") then 'PASS' else 'FAIL' end as dq_status from "
            + target_table
            + " "
        )

        condition = (
            api_response.replace("#AND#", " AND ")
            .replace("%OR%", " OR ")
            .replace("%=%", " = ")
            .replace("%>%", " > ")
            .replace("%<%", " < ")
            .replace("%>=%", " >= ")
            .replace("%<=%", " <= ")
            .replace("%!=%", " != ")
        )
        str_sql += f" WHERE {condition}"

        if applied_filters != "":
            str_sql += f" and {applied_filters}"
        # print(str_sql)
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhen_logic = (
                "case when "
                + target_column
                + " in ("
                + ",".join(["'" + item + "'" for item in list_of_values])
                + f") and {condition} THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END"
            )

            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isNegativeNumber(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        dq_rule = "isNegativeNumber"
        conn = connection_obj
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        str_sql = f"SELECT {target_column}, CASE WHEN {target_column} < 0 THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        casewhen_logic = f"CASE WHEN {target_column} < 0 THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END"
        casewhen_dqrule = (
            f"CASE WHEN {target_column} < 0 THEN '' ELSE '{column}-{dq_rule} , ' END"
        )

        if applied_filters:
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isNumber(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isNumber"
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            logic = "CASE WHEN " + target_column + " REGEXP '^[0-9]+$' "
            str_sql = (
                "SELECT "
                + target_column
                + f", {logic}"
                + "THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM "
                + target_table
                + " "
            )
        elif conn._is_postgres():
            logic = "CASE WHEN " + f"cast({target_column} as text)" + " ~ '^[0-9]+$' "
            str_sql = (
                "SELECT "
                + target_column
                + f", {logic}"
                + "THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM "
                + target_table
                + " "
            )
        elif conn._is_bigquery():
            logic = (
                "CASE WHEN "
                + f"REGEXP_CONTAINS(cast({target_column} as string),"
                + " r'^[0-9]+$') "
            )
            str_sql = (
                "SELECT "
                + target_column
                + f", {logic}"
                + "THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM "
                + target_table
                + " "
            )
        casewhen_logic = (
            f"{logic} then '' ELSE '{column} for rule {dq_rule} Failed, ' END"
        )

        if applied_filters:
            applied_filters = f" WHERE {applied_filters}"
            str_sql += applied_filters

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isURL(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isURL"
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            case_when_logic = (
                f"CASE WHEN {target_column} "
                + "REGEXP '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'"
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_postgres():
            case_when_logic = (
                f"CASE WHEN cast({target_column} as text)"
                + " ~ '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'"
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_bigquery():
            case_when_logic = (
                f"CASE WHEN REGEXP_CONTAINS(cast({target_column} as string),"
                + " r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$') "
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        case_when_logic = (
            " CASE WHEN "
            + target_column
            + " REGEXP '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$' THEN '' ELSE '"
            + target_column
            + " for rule "
            + dq_rule
            + " Failed, ' END"
        )

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_startsWith(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        prefix,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "startswith"
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        # SQL query to check isNull for the target_column and generate DQ_Status
        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            case_when_logic = f"CASE WHEN {target_column} LIKE '{prefix}%'"
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_postgres():
            case_when_logic = (
                f"CASE WHEN cast({target_column} as text) LIKE '{prefix}%'"
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_bigquery():
            case_when_logic = (
                f"CASE WHEN cast({target_column} as string) LIKE '{prefix}%'"
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        case_when_logic = f"{case_when_logic} THEN '' ELSE '{target_column} for rule {dq_rule} Failed,' END"
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isBoolean(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isBoolean"
        boolean_values = ["TRUE", "FALSE", "true", "false", "True", "False", "0", "1"]
        boolean_string = "'" + "','".join(boolean_values) + "'"
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql():
            case_when_logic = f"case when {target_column} in ({boolean_string})"
            str_sql = f"select {target_column}, {case_when_logic} then 'PASS' else 'FAIL' end as dq_status from  {target_table}"
        elif conn._is_postgres():
            case_when_logic = (
                f"case when cast({target_column} as text) in ({boolean_string})"
            )
            str_sql = f"select {target_column}, {case_when_logic} then 'PASS' else 'FAIL' end as dq_status from  {target_table}"
        elif conn._is_databricks() or conn._is_bigquery() or conn._is_snowflake():
            case_when_logic = (
                f"case when cast({target_column} as string) in ({boolean_string})"
            )
            str_sql = f"select {target_column}, {case_when_logic} then 'PASS' else 'FAIL' end as dq_status from  {target_table}"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )
        case_when_logic = f"{case_when_logic} THEN '' ELSE '{target_column} for rule {dq_rule} Failed,' END"

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isUpperCase(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isUpperCase"
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        str_sql = (
            f"SELECT {target_column}, CASE WHEN {target_column} = upper({target_column}) "
            f"THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table} "
        )
        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )
        case_when_logic = (
            f"CASE WHEN {target_column} == upper({target_column}) THEN '' ELSE '{target_column} "
            f"for rule {dq_rule} Failed,' END"
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_endswith(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        suffix,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "endswith"
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            case_when_logic = f"CASE WHEN {target_column} LIKE '%{suffix}'"
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_postgres():
            case_when_logic = (
                f"CASE WHEN cast({target_column} as text) LIKE '%{suffix}'"
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"
        elif conn._is_bigquery():
            case_when_logic = (
                f"CASE WHEN cast({target_column} as string) LIKE '%{suffix}'"
            )
            str_sql = f"SELECT {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END AS dq_status FROM {target_table}"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        case_when_logic = f" {case_when_logic} THEN '' ELSE '{target_column} for rule {dq_rule} Failed,' END"
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    # 100            #120
    def sigma_dq_check_isTimestamp(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isTimestamp"
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql():
            casewhen_logic = f"case when {target_column} = timestamp({target_column})"
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"
        elif conn._is_postgres():
            casewhen_logic = f"case when {target_column} = to_timestamp(cast({target_column} as text))"
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"
        elif conn._is_snowflake():
            casewhen_logic = (
                f"case when {target_column} = to_timestamp({target_column})"
            )
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"
        elif conn._is_bigquery():
            casewhen_logic = f"case when {target_column} = timestamp({target_column})"
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"
        elif conn._is_databricks():
            casewhen_logic = (
                f"CASE WHEN " + target_column + " = to_timestamp(" + target_column + ")"
            )
            str_sql = f"select {target_column}, {casewhen_logic} THEN 'PASS' ELSE 'FAIL' END as dq_status from {target_table}"

        if applied_filters:
            applied_filters = f" WHERE {applied_filters}"
            str_sql += applied_filters

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        casewhen_logic = (
            f"{casewhen_logic} THEN '' ELSE '{column} for rule {dq_rule} Failed, ' END "
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_fieldCompare_with_current_date(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "fieldCompare_date"
        source_table_with_column = target_table + "." + target_column
        source_table = target_table
        case_when_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        operator = api_response.split(" ")[0]
        if operator in ["<", ">", "<=", ">=", "=", "!="]:
            if conn._is_mysql():
                case_when_logic = f"CASE WHEN STR_TO_DATE({source_table_with_column}, '%Y-%m-%d') {operator} current_date()"
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table}"
                )
            elif conn._is_postgres():
                case_when_logic = (
                    f"CASE WHEN to_date(cast({source_table_with_column} as text), 'yyyy-mm-dd') "
                    f"{operator} current_date"
                )
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table}"
                )
            elif conn._is_snowflake():
                case_when_logic = f"CASE WHEN to_date({source_table_with_column}) {operator} current_date"
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table} "
                )
            elif conn._is_bigquery():
                case_when_logic = (
                    f"CASE WHEN cast({target_column} as date) {operator} current_date"
                )
                str_sql = (
                    f"select {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END as dq_status"
                    f" from {source_table} "
                )
            elif conn._is_databricks():
                case_when_logic = f"CASE WHEN to_date({source_table_with_column}, 'yyyy-MM-dd') {operator} current_date()"
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table} "
                )
            # print(str_sql)

            case_when_logic = f"{case_when_logic} THEN '' ELSE '{column} for rule {dq_rule} Failed,' END "
        else:
            return "Error please check the input dqRule:sigma_dq_check_fieldCompare_with_current_date"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_fieldCompare_with_current_timestamp(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "fieldCompare_with_current_timestamp"
        source_table_with_column = target_table + "." + target_column
        source_table = target_table
        case_when_logic = ""

        operator = api_response.split(" ")[0]
        if operator in (">", "<", ">=", "<=", "!=", "="):
            if conn._is_mysql():
                case_when_logic = f"CASE WHEN timestamp({source_table_with_column}) {operator} current_timestamp()"
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table}"
                )
            elif conn._is_postgres():
                case_when_logic = f" CASE WHEN cast({source_table_with_column} as timestamp) {operator} current_timestamp"
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table}"
                )
            elif conn._is_snowflake():
                case_when_logic = f"CASE WHEN to_timestamp({source_table_with_column}) {operator} current_timestamp()"
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from {source_table}"
                )
            elif conn._is_bigquery():
                case_when_logic = f"CASE WHEN timestamp({target_column}) {operator} current_timestamp()"
                str_sql = (
                    f"select {target_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END as dq_status "
                    f"from {source_table}"
                )
            elif conn._is_databricks():
                case_when_logic = (
                    f"CASE WHEN to_timestamp({source_table_with_column}, 'yyyy-MM-dd HH:mm:ss.SSS') "
                    f"{operator} current_timestamp()"
                )
                str_sql = (
                    f"select {source_table_with_column}, {case_when_logic} THEN 'PASS' ELSE 'FAIL' END "
                    f"as dq_status from  {source_table}"
                )
        else:
            return "Error please check the input dqRule:sigma_dq_check_fieldCompare_with_current_timestamp"

        case_when_logic = (
            f"{case_when_logic} THEN '' ELSE '{column} for rule {dq_rule} Failed,' END "
        )

        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return dq_report
        elif meta["report"] == "comprehensive":
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_fieldCompareWithCondition(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        api_response2,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "fieldCompareWithCondition"
        source_table_with_column = target_table + "." + target_column
        source_table = target_table
        operator = "".join(api_response.split("%")[1:-1])
        value = "".join(api_response.split("%")[::-3])
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        try:
            value = float(value)
        except:
            return "Insert valid number"
        else:
            value = float(value)

        if operator == ">":
            operator = "> " + str(value)
            rev_op = "<= " + str(value)
        elif operator == ">=":
            operator = ">= " + str(value)
            rev_op = "< " + str(value)
        elif operator == "<":
            operator = "< " + str(value)
            rev_op = ">= " + str(value)
        elif operator == "<=":
            operator = "<= " + str(value)
            rev_op = "> " + str(value)
        elif operator == "<>":
            operator = "<> " + str(value)
            rev_op = "= " + str(value)
        elif operator == "=":
            operator = "= " + str(value)
            rev_op = "<> " + str(value)
        else:
            return "Error please check the input"

        str_sql = (
            "select "
            + source_table_with_column
            + ", CASE WHEN "
            + source_table_with_column
            + " "
            + operator
            + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
            + source_table
            + "  "
        )
        casewhen_logic = source_table_with_column + " " + rev_op

        api_response_condition = api_response2.replace("#AND#", "AND").replace(
            "%OR%", "OR"
        )
        str_sql += " WHERE " + api_response_condition
        casewhen_logic += " AND " + api_response_condition

        total_rows_query = (
            f"select * from {target_table} WHERE {api_response_condition}"
        )
        if applied_filters != "":
            str_sql += f" AND {applied_filters}"
            total_rows_query += f" AND {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        total_DQ_Pass_count = sum(
            1 for item in dq_apply_column_data if item.get("dq_status") == "PASS"
        )
        total_count = conn.exexute_query(total_rows_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]

        dq_report = helper.sigma_dq_generate_dq_report_for_joins(
            dq_apply_column_data,
            column,
            dq_rule,
            total_count,
            total_DQ_Pass_count,
            meta={},
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhen_logic = f"case when {casewhen_logic} then '{column} for rule {dq_rule} Failed, ' else '' END"
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_fieldCompare_with_value(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "fieldCompare_zero"
        source_table_with_column = target_table + "." + target_column
        source_table = target_table
        operator = "".join(api_response.split("%")[1:-1])
        value = "".join(api_response.split("%")[::-3])
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        try:
            value = float(value)
        except:
            return "Insert valid number"
        else:
            value = float(value)

        if operator in (">", ">=", "<", "<=", "<>", "="):
            operator = f"{operator} {str(value)}"
            str_sql = (
                f"select {source_table_with_column}, CASE WHEN {source_table_with_column} {operator} "
                f"THEN 'PASS' ELSE 'FAIL' END as dq_status from {source_table}  "
            )
            casewhen_logic = f"{source_table_with_column} {operator}"
        else:
            return "Error please check the input dqRule:sigma_dq_check_fieldCompare_with_value"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhen_logic = f" case when {casewhen_logic} then '' else '{column} for rule {dq_rule} Failed, ' end "
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_fieldCompare_with_field(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "fieldCompare_with_field"
        source_table_with_column = target_table + "." + target_column
        source_table = target_table
        str_sql = ""
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if api_response.__contains__("%>=%"):  # Greater than eqaul to
            compare_table_with_column = api_response.split("%>=%")[-1]
            compare_table = ".".join(compare_table_with_column.split(".")[:-1])
            operator = ">="
        elif api_response.__contains__("%>%"):  # Greater Than
            compare_table_with_column = api_response.split("%>%")[-1]
            compare_table = ".".join(compare_table_with_column.split(".")[:-1])
            operator = ">"
        elif api_response.__contains__("%<=%"):  # Less than equal to
            compare_table_with_column = api_response.split("%<=%")[-1]
            compare_table = ".".join(compare_table_with_column.split(".")[:-1])
            operator = "<="
        elif api_response.__contains__("%<%"):  # Less than
            compare_table_with_column = api_response.split("%<%")[-1]
            compare_table = ".".join(compare_table_with_column.split(".")[:-1])
            operator = "<"
        elif api_response.__contains__("%=%"):  # equalTo
            compare_table_with_column = api_response.split("%=%")[-1]
            compare_table = ".".join(compare_table_with_column.split(".")[:-1])
            operator = "="
        elif api_response.__contains__("%<>%"):  # NotEqualTo
            compare_table_with_column = api_response.split("%<>%")[-1]
            compare_table = ".".join(compare_table_with_column.split(".")[:-1])
            operator = "!="
        else:
            return " Error please check the input dqRule : fieldCompare_with_field"

        if source_table == compare_table:
            str_sql = (
                f"select {source_table_with_column}, case when {source_table_with_column} {operator} {compare_table_with_column} "
                f"then 'PASS' else 'FAIL' end as dq_status from {source_table}"
            )
            casewhen_logic = f"CASE WHEN {source_table_with_column} {operator} {compare_table_with_column} then '' ELSE '{column} for rule {dq_rule} Failed, ' END"
        else:
            str_sql = (
                "select "
                + source_table_with_column
                + ",case when "
                + source_table_with_column
                + " "
                + operator
                + " "
                + compare_table_with_column
                + " then 'PASS' else 'FAIL' end as dq_status from "
                + source_table
                + " left join "
                + compare_table
                + " on "
                + source_table_with_column
                + " = "
                + compare_table_with_column
                + " "
            )
            casewhen_logic = f"CASE WHEN {source_table_with_column} {operator} {compare_table_with_column} then '' ELSE '{column} for rule {dq_rule} Failed, ' END"

        if applied_filters:
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isDuplicate(
        self,
        connection_obj,
        target_table,
        meta,
        columns_str,
        execution_type="",
        custom_filter="",
    ):
        dq_rule = "isDuplicate"
        conn = connection_obj
        # column = target_column
        str_sql = ""
        casewhen_logic = ""
        column_list = columns_str.split(",")
        applied_filters = self.sigma_helper_add_execution_filter(execution_type, custom_filter, target_table)
 
        str_sql = f"select {columns_str}, count(1) as cnt, case when count(1) > 1 then 'FAIL' else 'PASS' end"\
                f" as dq_status from {target_table}"
            
        if applied_filters != "":
            str_sql += f" WHERE {applied_filters} "
        str_sql += f" group by {columns_str} ORDER BY {len(column_list) + 1} DESC "

        # print(str_sql)
        dq_apply_column_data = conn.execute_query(str_sql)
        dq_message = ""
        for row in dq_apply_column_data:
            if row['dq_status'] == 'FAIL':
                dq_message = f"Duplicate records found for {columns_str}. "
                break

        failed_record = "Top error - ["
        for a in column_list:
            a = a.strip()
            failed_record += f"{dq_apply_column_data[0][a]}, "
        failed_record = failed_record[:-2] + "]" + str(dq_apply_column_data[0]['cnt'])
        
        dq_action = "PASS"
        if dq_message != "":
            dq_action = "FAIL"
            dq_message += failed_record

        # additional handling required for list of columns as main argument
        failed_values_dict = {}
        dq_report = {}
        dq_report = {}
        dq_report['rule'] = dq_rule
        dq_report['table_name'] = target_table
        dq_report['dq_message'] = dq_message
        dq_report['dq_action'] = dq_action
        
        if meta["report"] == "report_only":
            return dq_report
        elif meta["report"] == "comprehensive":
            return dq_report
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isExistingCondAdvanced(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        api_response2,
        left_join_tables,
        execution_type="",
        custom_filter="",
    ):
        api_responseSecond = ""
        dq_rule = "isExistingCondAdvanced"
        conn = connection_obj
        column = target_column
        target_table_for_join = target_table.split(".")
        modified_target_column = target_table + "." + target_column
        modifiedapi_response = ""
        modifiedapi_responseSplit = api_response.split(".")
        andClause = ""
        secondLeftJoin = ""
        schema = target_table.split(".")[0]
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        subquery2 = ""
        # calculate pass count
        pass_count_query = ""
        table_list = api_response.split("=")
        subquery_tables = []
        for table in table_list:
            subquery_tables.append(table.strip())
        for x in subquery_tables:
            if x.split(".")[0] in target_table:
                from_table = x
            else:
                to_table = x
        subquery = f" {from_table} in (select distinct {to_table} from {schema}.{to_table.split('.')[0]} ) "
        if api_response2.split(".")[0] in to_table:
            subquery = subquery.replace(
                ")",
                f" where {api_response2.replace('%OR%', ' OR ').replace('#AND#', ' AND ')} ",
            )

        if left_join_tables != "":
            if subquery2 != "":
                subqueryforcaselogicupdate = f" NOT EXITS (select distinct {left_join_tables} from {schema}.{left_join_tables.split('.')[0]} WHERE {target_column} = {left_join_tables} "
                casewhenlogic = subquery + "" + subqueryforcaselogicupdate
                subquery += f" {target_column} in (select distinct {left_join_tables} from {schema}.{left_join_tables.split('.')[0]}  "
                subquery += " ) "
            else:
                subqueryforcaselogicupdate = f" and {target_column} not in (select distinct {left_join_tables} from {schema}.{left_join_tables.split('.')[0]} ) "
                casewhenlogic = subquery + "" + subqueryforcaselogicupdate
                subquery += f" and {target_column} in (select distinct {left_join_tables} from {schema}.{left_join_tables.split('.')[0]}  "
                subquery += " ) "

        if api_response2 != "":
            if api_response2.split(".")[0] in target_table:
                subquery += f" and {api_response2.replace('%OR%', ' OR ').replace('#AND#', ' AND ')} "
                casewhenlogic += f" and {api_response2.replace('%OR%', ' OR ').replace('#AND#', ' AND ')} "

        if execution_type == "incremental":
            subquery = f" ({subquery}) and {applied_filters} "
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            subquery = f" ({subquery}) and {between_condition} "
        elif execution_type == "custom":
            subquery = custom_filter
        pass_count_query = f" select count({target_column}) from {target_table}"
        if subquery != "":
            pass_count_query += f" where {subquery} "

        # calculate total count
        total_subquery = ""
        if execution_type == "1 month":
            total_subquery = f" {applied_filters} "
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            total_subquery = between_condition
        elif execution_type == "custom":
            total_subquery = custom_filter
            total_count_query = f"select count({target_column}) from {target_table}"
        if total_subquery != "":
            total_count_query += f" where {total_subquery}"

        # calculate failed values
        str_sql = ""
        targetTableAPI = target_table_for_join[1] + "." + target_column
        modifiedORLeftjoin = ""
        if api_response.__contains__("="):
            modifiedApiORR_Res = left_join_tables.split("#AND#")
            modifiedApiResForCaseWhen = api_response.replace("=", "==")
            modifiedAPIResponseForEqualTo = api_response.split("=")
            stripmodifiedAPIResponseForEqualTo = []  # stripping
            tableNameInApi_response = []

            for index in modifiedAPIResponseForEqualTo:
                stripmodifiedAPIResponseForEqualTo.append(index.strip())
                tableNameInApi_response.append(index.split(".")[0])

            modifiedAPIResponseForEqualToTemp = modifiedAPIResponseForEqualTo[1].strip()
            index = modifiedAPIResponseForEqualToTemp.index(".")
            modifiedAPIResponseForEqualToTemp = modifiedAPIResponseForEqualToTemp[
                :index
            ]

            for singleTable in modifiedApiORR_Res:
                index = modifiedApiORR_Res.index(singleTable)
                api_responseSecond = targetTableAPI + " = " + left_join_tables
                api_response_added = api_response + " and " + api_responseSecond
                temp1 = modifiedApiORR_Res[0].split(".")

            if left_join_tables.split(".")[0] in tableNameInApi_response:
                modifiedORLeftjoin = (
                    " left join "
                    + target_table_for_join[0]
                    + "."
                    + temp1[0]
                    + " on "
                    + api_responseSecond
                )
                andClause = " and " + api_response

            else:
                modifiedORLeftjoin = (
                    " left join "
                    + target_table_for_join[0]
                    + "."
                    + modifiedAPIResponseForEqualToTemp
                    + " on "
                    + api_response
                )
                secondLeftJoin = (
                    " left join "
                    + target_table_for_join[0]
                    + "."
                    + left_join_tables.split(".")[0]
                    + " on "
                    + api_responseSecond
                    + " "
                )

            str_sql = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + api_response_added
                + " \
                THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
                + secondLeftJoin
                + andClause
            )

        else:  # When my api_response    = 'JDE_VENDOR.global_vendor_number
            temp1 = left_join_tables.split(".")
            modifiedapi_response += (
                modified_target_column + " == " + api_response
            )  # operator goes here
            modifiedORLeftjoin = (
                " left join "
                + target_table_for_join[0]
                + "."
                + modifiedapi_responseSplit[0]
                + " on "
                + modified_target_column
                + " = "
                + api_response
            )
            modifiedORLeftjoin += (
                " left join " + target_table_for_join[0] + "." + temp1[0]
            )
            str_sql = (
                "select distinct "
                + modified_target_column
                + ", CASE WHEN "
                + modifiedapi_response
                + " THEN 'PASS' ELSE 'FAIL' END as dq_status from "
                + target_table
                + " "
                + modifiedORLeftjoin
            )

        if api_response2 != "":
            lsmodifiedApliResponse = ""
            if not api_response2.__contains__("#AND#") and api_response2.__contains__(
                "%OR%"
            ):
                lsmodifiedApliResponse = (
                    target_table_for_join[0]
                    + "."
                    + api_response2.replace(
                        "%OR%", " OR " + target_table_for_join[0] + "."
                    )
                )
            elif not api_response2.__contains__("%OR%") and api_response2.__contains__(
                "#AND#"
            ):
                lsmodifiedApliResponse = (
                    target_table_for_join[0]
                    + "."
                    + api_response2.replace(
                        "#AND#", " AND " + target_table_for_join[0] + "."
                    )
                )
            elif api_response2.__contains__("%OR%") and api_response2.__contains__(
                "#AND#"
            ):
                lsmodifiedApliResponse = (
                    target_table_for_join[0]
                    + "."
                    + api_response2.replace(
                        "#AND#", "AND " + target_table_for_join[0] + "."
                    ).replace("%OR%", " OR " + target_table_for_join[0] + ".")
                )
            else:
                lsmodifiedApliResponse = target_table_for_join[0] + "." + api_response2
            str_sql += " WHERE " + api_response2

        else:
            print("Invalid Input")

        if execution_type == "1 month":
            str_sql += " AND " + applied_filters
        elif execution_type == "date_range":
            from_timestamp = datetime.fromtimestamp(from_date)
            from_date_str = from_timestamp.strftime("%Y-%m-%d")
            to_timestamp = datetime.fromtimestamp(to_date)
            to_date_str = to_timestamp.strftime("%Y-%m-%d")
            between_condition = f' cast(update_run_ts as string) between "{from_date_str}" AND "{to_date_str}"'
            str_sql += f" AND {between_condition}"
        elif execution_type == "custom":
            str_sql += " AND " + custom_filter

        print(str_sql)

        dq_apply_column_data = conn.execute_query(str_sql)
        total_count = conn.execute_query(total_count_query)
        pass_count = conn.execute_query(pass_count_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]
        key = [key for key in pass_count[0].keys()]
        pass_count = pass_count[0][f"{key[0]}"]
        dq_report = helper.sigma_dq_generate_dq_report_for_joins(
            dq_apply_column_data, column, dq_rule, total_count, pass_count, meta={}
        )
        dq_report["meta"]["condition"] = lsmodifiedApliResponse
        if meta["report"] == "report_only":
            return dq_report
        elif meta["report"] == "comprehensive":
            # SQL query to generate comprehensive report with dqMessage_
            case_when_logic = f" CASE WHEN {casewhenlogic}  THEN '{column} for rule {dq_rule} Failed,' ELSE ''   END "
            # print("Comprehensive report query:", StrSQL_)
            return case_when_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_isMapped(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        api_response,
        api_response2,
        rule_id,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isMapped"
        leftjoinTbaledetails = api_response2
        str_sql = ""
        target_table_for_join = target_table.split(".")
        schema = target_table_for_join[0]
        modified_target_column = target_table + "." + target_column
        targetTableAPI = (
            schema + "." + target_table_for_join[1] + "." + target_column
        )  # add schema 'product_mapping.SUB_RGM_PPG'
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        total_rows_query = f"select * from {target_table}"

        if leftjoinTbaledetails == "":
            str_sql = (
                f"select {target_column}, count(distinct {api_response}) as response_col, "
                f"case when count(distinct {api_response}) > 1 then 'FAIL' else 'PASS' end as dq_status from {target_table} "
            )

            if applied_filters != "":
                str_sql += f" WHERE {applied_filters}"
                total_rows_query += f" WHERE {applied_filters}"

            str_sql += f" group by {target_column}"
        else:
            print("Else")
            if api_response2.__contains__("="):
                modifiedApiORR_Res = target_table.split("#AND#")  # No need
                lsTempTargetTable = "".join(modifiedApiORR_Res)
                modifiedApiResForCaseWhen = api_response.replace("=", "==")
                modifiedAPIResponseForEqualTo = api_response2.split("=")
                stripmodifiedAPIResponseForEqualTo = []  # stripping
                tableNameInApi_response = []
                modifiedAPIResponseForEqualToTemp = ""
                onStringquery = ""
                for index in modifiedAPIResponseForEqualTo:  # APIResponse  #No need
                    stripmodifiedAPIResponseForEqualTo.append(index.strip())
                    tableNameInApi_response.append(index.split(".")[1])
                    if onStringquery == "":
                        onStringquery = (
                            schema
                            + "."
                            + tableNameInApi_response[0]
                            + "."
                            + index.split(".")[2].strip()
                        )
                        # if onStringquery == 'ITEM_CODE':
                        if onStringquery.__contains__("ITEM_CODE"):
                            onStringquery = onStringquery.replace(
                                "ITEM_CODE", "regexp_replace(ITEM_CODE, '^0+', '')"
                            )  # "regexp_replace(ITEM_CODE, '^0+', '')"
                    else:
                        onStringquery1 = (
                            schema
                            + "."
                            + tableNameInApi_response[1]
                            + "."
                            + index.split(".")[2].strip()
                        )
                        if onStringquery1.__contains__("ITEM_CODE"):
                            onStringquery1 = onStringquery1.replace(
                                "ITEM_CODE", "regexp_replace(ITEM_CODE, '^0+', '')"
                            )  # "regexp_replace(ITEM_CODE, '^0+', '')"
                        onStringquery += " = " + onStringquery1

                for item in modifiedAPIResponseForEqualTo:
                    if lsTempTargetTable in item.strip():
                        continue
                    else:
                        modifiedAPIResponseForEqualToTemp = item.strip()
                index = modifiedAPIResponseForEqualToTemp.index(".")
                dot_count = modifiedAPIResponseForEqualToTemp.count(".")
                if dot_count == 2:
                    modifiedAPIResponseForEqualToTemp = (
                        modifiedAPIResponseForEqualToTemp.rsplit(".", 1)
                    )
                    # if lsTempTargetTable in modifiedAPIResponseForEqualToTemp
                else:
                    modifiedAPIResponseForEqualToTemp = (
                        modifiedAPIResponseForEqualToTemp[:index]
                    )

                for (
                    singleTable
                ) in (
                    modifiedApiORR_Res
                ):  # leftjointable #targettable and leftjointable connection
                    index = modifiedApiORR_Res.index(singleTable)
                    api_responseSecond = targetTableAPI + " = " + target_table
                    api_response_added = api_response + " and " + api_responseSecond
                    temp1 = modifiedApiORR_Res[0].split(".")

                if (
                    target_table.split(".")[0] in tableNameInApi_response
                ):  # checking leftjoin table isin apiResponse
                    andClause = ""
                    leftjointabledetails = (
                        "left join " + target_table_for_join[0] + "." + temp1[0]
                    )
                    modifiedORLeftjoin = (
                        leftjointabledetails + " on " + api_responseSecond
                    )
                    # if tableNameInApi_response not in modifiedORLeftjoin
                    for stv in tableNameInApi_response:
                        if stv in leftjointabledetails:
                            continue
                        else:
                            stv = stv.strip()
                            if stv != target_table_for_join[1]:
                                andClause = (
                                    " left join "
                                    + target_table_for_join[0]
                                    + "."
                                    + stv
                                    + " on "
                                    + api_response
                                )
                                # andClause = " and "+api_response

                else:
                    modifiedORLeftjoin = (
                        " left join "
                        + modifiedAPIResponseForEqualToTemp[0]
                        + " on "
                        + onStringquery
                    )

                str_sql = (
                    f"select {target_column}, count(distinct {api_response}) as response_col, "
                    f"case when count(distinct {api_response}) = 1 then 'PASS' else 'FAIL' end "
                    f"as dq_status from {target_table} {modifiedORLeftjoin} group by {target_column} "
                )

        # print(str_sql)
        dq_apply_column_data = conn.execute_query(str_sql)
        total_DQ_Pass_count = sum(
            1 for item in dq_apply_column_data if item.get("dq_status") == "PASS"
        )
        total_count = conn.execute_query(total_rows_query)
        key = [key for key in total_count[0].keys()]
        total_count = total_count[0][f"{key[0]}"]

        dq_report = helper.sigma_dq_generate_dq_report_for_joins(
            dq_apply_column_data,
            column,
            dq_rule,
            total_count,
            total_DQ_Pass_count,
            meta={},
        )
        dq_report["meta"]["rule_id"] = rule_id
        failed_values = []
        if dq_report["success"] == True:
            failed_values = []
        else:
            failed_values = dq_report["failed_values"]

        if len(failed_values) > 1:
            cleaned_failed_values = [
                value for value in failed_values if value is not None
            ]
            casewhen_logic = (
                "case when "
                + target_column
                + ' in ("'
                + '","'.join(cleaned_failed_values)
                + '"'
                + ") THEN '"
                + target_column
                + " for rule "
                + dq_rule
                + " Failed, ' ELSE '' END "
            )
        else:
            casewhen_logic = f"case when {target_column} is null THEN '{target_column} for rule {dq_rule} Failed, ' ELSE '' END"

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isDecimal(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
        from_date=0,
        to_date=0,
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "isDecimal"
        target_table_for_join = target_table.split(".")
        modified_target_column = target_table + "." + target_column
        casewhen_logic = ""
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if conn._is_mysql() or conn._is_snowflake() or conn._is_databricks():
            casewhen_logic = f"case when {target_column} like '%.%'"
            str_sql = (
                f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end "
                f"as dq_status from {target_table}"
            )
        elif conn._is_postgres():
            casewhen_logic = f"case when cast({target_column} as text) like '%.%'"
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table} "
        elif conn._is_bigquery():
            casewhen_logic = f"case when cast({target_column} as string) like '%.%'"
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table}"

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            casewhen_logic = f" {casewhen_logic} THEN '' ELSE '{column} for rule {dq_rule} Failed,' END "
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    # COMMAND ----------

    def sigma_dq_check_isExistingFilter(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        target_conditions,
        lookup_tables,
        lookup_logic=" AND ",
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "is_existing_in_filter"
        casewhen_logic = ""
        target_cond_string = ""
        # execution_filter = ""

        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )

        if target_conditions != "":
            target_cond_string = target_conditions.replace("#AND#", " AND ").replace(
                "%OR%", " OR "
            )
        case_when = ""
        if target_cond_string != "":
            case_when += target_cond_string + " and "

        lookup_array = []
        for t in lookup_tables:
            sub_query = f"(select distinct {t['column_name']} from {t['table_name']})"
            if t["filter_condition"] != "":
                sub_query = sub_query[:-1]
                sub_query += f" where {t['filter_condition']} )"
            lookup_array.append(sub_query)

        main_condition = ""
        for arr in lookup_array:
            if lookup_array.index(arr) > 0:
                if "AND" in lookup_logic.upper():
                    main_condition += " or "
                else:
                    main_condition += " and "
            main_condition += f"{target_column} not in {arr} "

        str_sql = f"select {target_column}, case when {main_condition} then 'FAIL' else 'PASS' end as dq_status from {target_table} "
        if target_cond_string != "":
            str_sql += f" where {target_cond_string} "

        if applied_filters != "":
            str_sql += f" WHERE {applied_filters}"

        # print(str_sql)

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return "", dq_report
        elif meta["report"] == "comprehensive":
            # target condition is already included in {case_when}
            casewhen_logic = f"case when {case_when} {main_condition} then '{target_column} for rule {dq_rule} Failed, ' else '' END"
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option: 'report_only' or 'comprehensive'"
            )

    # COMMAND ----------

    def sigma_dq_check_textToNumberCheck(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        execution_type="",
        custom_filter="",
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "textToNumberCheck"
        applied_filters = self.sigma_helper_add_execution_filter(
            execution_type, custom_filter, target_table
        )
        str_sql = ""
        casewhen_logic = ""

        if conn._is_mysql():
            casewhen_logic = (
                f"case when cast(replace(replace({target_column}, ',', ''), ' ', '') as unsigned) > 0 and "
                f"{target_column}%1 == 0"
            )
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table} "
        elif conn._is_postgres():
            casewhen_logic = (
                f"case when cast(replace(replace(cast({target_column} as text), ',', ''), ' ', '') as numeric) > 0"
                f" and cast(replace(replace(cast({target_column} as text), ',', ''), ' ', '') as numeric)%1 = 0"
            )
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table} "
        elif conn._is_snowflake():
            casewhen_logic = (
                f"case when cast(replace(replace({target_column}, ',', ''), ' ', '') as integer) > 0"
                f" and cast(replace(replace({target_column}, ',', ''), ' ', '') as integer)%1 = 0"
            )
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table} "
        elif conn._is_bigquery():
            casewhen_logic = f"case when mod(cast(replace(replace(cast({target_column} as string), ',', ''), ' ', '') as numeric), 1) = 0"
            str_sql = (
                f"select {target_column}, {casewhen_logic} "
                f"then 'PASS' else 'FAIL' end as dq_status from {target_table}"
            )
        elif conn._is_databricks():
            casewhen_logic = (
                f"case when cast(replace(replace({target_column}, ',', ''), ' ', '') as INT) > 0"
                f" and {target_column}%1 = 0"
            )
            str_sql = f"select {target_column}, {casewhen_logic} then 'PASS' else 'FAIL' end as dq_status from {target_table} "

        casewhen_logic = (
            f"{casewhen_logic} then '' else '{column} for rule {dq_rule} Failed, ' end"
        )

        if applied_filters:
            str_sql += f" WHERE {applied_filters}"

        dq_apply_column_data = conn.execute_query(str_sql)
        dq_report = helper.sigma_dq_generate_dq_report(
            dq_apply_column_data, column, dq_rule
        )

        if meta["report"] == "report_only":
            return ("", dq_report)
        elif meta["report"] == "comprehensive":
            return casewhen_logic, dq_report, target_column
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    def sigma_dq_check_timeliness(
        self,
        connection_obj,
        target_table,
        meta,
        target_column,
        exception,
        expected_count,
        rule_id=0,
    ):
        column = target_column
        conn = connection_obj
        dq_rule = "timeliness"
        expected_count = expected_count.split("-")
        exception = exception.split(",")

        day_of_week = datetime.now().strftime("%A")
        day_of_month = datetime.now().strftime("%d")
        day_str = ("0" + day_of_month) if int(day_of_month) < 10 else day_of_month

        if day_of_week in exception or day_str in exception:
            return {
                "rule": dq_rule,
                "table_name": target_table,
                "dq_message": "Job skipped",
                "dq_action": "PASS",
            }
        str_sql = f"select distinct {target_column} from {target_table} order by {target_column} desc limit 10"
        ingestion_timestamp = conn.execute_query(str_sql)
        # print(ingestion_timestamp)
        timestamp_list = []
        for i in ingestion_timestamp:
            ts = i[f"{target_column}"]
            epoch_time = time.mktime(ts.timetuple())
            timestamp_list.append(epoch_time)
        print(timestamp_list)
        time_diff = []
        for i in range(len(timestamp_list) - 1):
            diff = (timestamp_list[i] - timestamp_list[i + 1]) / 3600
            time_diff.append(diff)

        time_diff = [round(time) for time in time_diff]
        time_diff = Counter(time_diff).most_common(1)[0][0]
        str_sql = f"SELECT (unix_timestamp(current_timestamp()) - unix_timestamp(MAX({target_column}))) / 3600 AS hours_difference, count(*) as row_count FROM {target_table} WHERE {target_column} = (SELECT MAX({target_column})FROM {target_table});"
        time_diff_hours = conn.execute_query(str_sql)
        row_count = time_diff_hours[0]["row_count"]
        time_diff_hours = round(time_diff_hours[0]["hours_difference"])
        dq_report = {}
        if time_diff_hours >= time_diff:
            dq_massage = f"No data has been ingested in the past {time_diff} hours."
        elif int(expected_count[0]) >= row_count <= int(expected_count[1]):
            dq_massage = f"Data ingested is out of range {expected_count[0]} - {expected_count[1]}"
        else:
            dq_massage = ""
        dq_report["rule"] = dq_rule
        dq_report["table_name"] = target_table
        dq_report["dq_message"] = dq_massage
        dq_report["dq_action"] = "PASS" if dq_report["dq_message"] == "" else "FAIL"

        if meta["report"] == "report_only":
            return dq_report
        elif meta["report"] == "comprehensive":
            return dq_report
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )

    def sigma_dq_check_schema_binding(
        self, connection_obj, target_table, meta, target_column_list, rule_id=0
    ):
        column_list = target_column_list.replace(" ", "").split(",")
        conn = connection_obj
        dq_rule = "schema_binding"
        table = target_table.split(".")

        if conn._is_mysql() and conn._is_snowflake():
            str_sql = f"show columns from {target_table}"
        elif conn._is_postgres():
            str_sql = f"show columns from {target_table}"
        elif conn._is_bigquery():
            str_sql = f"show columns from {target_table}"
        elif conn._is_databricks():
            str_sql = f"show columns from {target_table}"

        dq_apply_column_data = conn.execute_query(str_sql)
        result = {
            column: (
                "PASS"
                if any(
                    col_dict["col_name"] == column for col_dict in dq_apply_column_data
                )
                else "FAIL"
            )
            for column in column_list
        }

        dq_message = ""
        for column in result.keys():
            if result[column] == "FAIL":
                dq_message += f"Column {column} is missing from table, "
        dq_message = dq_message[:-2]

        dq_report = {"rule": dq_rule, "table_name": table[1], "dq_message": dq_message}
        dq_report["dq_action"] = (
            "FAIL" if "missing" in dq_report["dq_message"] else "PASS"
        )

        if meta["report"] == "report_only":
            return dq_report
        elif meta["report"] == "comprehensive":
            return dq_report
        else:
            raise Exception(
                "Mention Report type in meta option : 'report_only' or 'comprehensive' "
            )
