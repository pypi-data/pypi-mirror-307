from functools import reduce
from .sigmadq_core_functions import sigmadq_core_functions as core
from .sigmadq_helper_functions import sigmadq_helper_functions as helper

helper = helper()
core = core("target_table", {"report": "report_only"})


class rules_master:
    def __init__(self, connection_obj, base_url, **kwargs):
        self.base_url = base_url
        if connection_obj._is_mysql():
            pass
        elif connection_obj._is_postgres():
            pass
        elif connection_obj._is_snowflake():
            self.dq_report_id = kwargs["dq_report_id"]
            self.table_id = kwargs["table_id"]
            self.table_name = kwargs["table_name"]
            self.schema_name = kwargs["schema_name"]
            self.execution_type = kwargs["execution_type"]
            self.custom_filter = kwargs["custom_filter"]
            self.pk_column = kwargs["pk_column"]
            self.conn = connection_obj
        elif connection_obj._is_bigquery():
            self.dq_report_id = kwargs["dq_report_id"]
            self.table_id = kwargs["table_id"]
            self.table_name = kwargs["table_name"]
            self.dataset_name = kwargs["dataset_name"]
            self.execution_type = kwargs["execution_type"]
            self.custom_filter = kwargs["custom_filter"]
            self.pk_column = kwargs["pk_column"]
            self.conn = connection_obj
        elif connection_obj._is_databricks():
            self.dq_report_id = kwargs["dq_report_id"]
            self.table_id = kwargs["table_id"]
            self.table_name = kwargs["table_name"]
            self.schema_name = kwargs["schema_name"]
            self.execution_type = kwargs["execution_type"]
            self.custom_filter = kwargs["custom_filter"]
            self.pk_column = kwargs["pk_column"]
            self.conn = connection_obj
        elif connection_obj._is_redshift():
            pass
        elif connection_obj._is_mssql():
            pass

    def get_access_token(self):
        return helper.sigma_dq_helper_get_access_token()

    def get_validation_suite(self):
        access_token = self.get_access_token()
        url = self.base_url
        target_table_id = self.table_id
        return helper.sigma_dq_helper_get_validation_suite(
            url, target_table_id, access_token
        )

    def run_data_quality(self):
        conn = self.conn
        case_when_list = []
        save_result = []
        target_column_list = []
        responses = self.get_validation_suite()
        dq_score = {}

        if not responses:
            dq_result = {"id": self.dq_report_id, "run_status": "FAILED", "result": {}}
            helper.sigma_dq_helper_save_report(
                self.dq_report_id,
                dq_result,
                self.base_url,
                self.table_id,
                self.get_access_token(),
            )
            print("No validation suite found for this table")
        else:
            target_table = f"{self.schema_name}.{self.table_name}"
            for rules in responses:
                rules = rules.replace("brand_x-riff", "`brand_x-riff`")
                if "sigma_dq_check_timeliness" in rules:
                    rules = rules.replace(
                        "target_table,",
                        'conn, target_table, {"report": "comprehensive"}, ',
                    )
                    rules = "core." + rules
                    print(rules)
                    dq_report = eval(rules)
                    save_result.append(dq_report)
                elif "sigma_dq_check_schema_binding" in rules:
                    rules = rules.replace(
                        "target_table,",
                        'conn, target_table, {"report": "comprehensive"}, ',
                    )
                    rules = "core." + rules
                    print(rules)
                    dq_report = eval(rules)
                    save_result.append(dq_report)
                elif "sigma_dq_check_isDuplicate" in rules:
                    rules = rules.replace(
                        "target_table,",
                        'conn, target_table, {"report": "comprehensive"}, ',
                    )
                    rules = "core." + rules
                    rules = rules.replace(
                        ")",
                        f', execution_type="{self.execution_type}", custom_filter="{self.custom_filter}")',
                    )
                    print(rules)
                    dq_report = eval(rules)
                    save_result.append(dq_report)
                else:
                    rules = rules.replace(
                        "target_table,",
                        'conn, target_table, {"report": "comprehensive"}, ',
                    )
                    rules = "core." + rules
                    rules = rules.replace(
                        ")",
                        f', execution_type="{self.execution_type}", custom_filter="{self.custom_filter}")',
                    )
                    print(rules)
                    dq_report = eval(rules)
                    case_when_list.append(dq_report[0])
                    save_result.append(dq_report[1])
                    target_column_list.append(dq_report[2])
            if case_when_list:
                case_when_string = reduce(lambda x, y: x + " ," + y, case_when_list)
                dq_score = helper.sigma_dq_calculate_dq_score(
                    conn,
                    target_table,
                    case_when_string,
                    target_column_list,
                    self.execution_type,
                    self.custom_filter,
                    self.pk_column,
                )
            print(save_result)
            self.dq_result = helper.sigma_dq_generate_dq_json(
                self.dq_report_id,
                dq_score,
                save_result,
                self.base_url,
                self.get_access_token(),
            )
            return self.dq_result
            # helper.sigma_dq_helper_save_report(dq_report_id, dq_result, base_url, table_id, token)

    def save_report_in_backend(self, dq_report):
        helper.sigma_dq_helper_save_report(
            self.dq_report_id,
            dq_report,
            self.base_url,
            self.table_id,
            self.get_access_token(),
        )

    def send_email_alert(self):
        dq_score = self.dq_result['result']["DQ"]['dqScore']
        attribute_score = self.dq_result['result']["Attributes"]
        sorted_by_score_desc = sorted(attribute_score, key=lambda d: d['DQscore'])

        top_failed = []
        for sc in sorted_by_score_desc:
            if sc['DQscore'] < 100:
                top_failed.append(sc)
            if len(sorted_by_score_desc) == 5:
                break

        top_failed_str = ''
        for i in top_failed:
            top_failed_str += f"{i['Attribute/column']}: {i['Rule']} <br>"
        print(top_failed_str)
        app_filters = ""
        if self.execution_type == "":
            app_filters = "Full run"
        elif self.execution_type == "incremental":
            app_filters = self.execution_type
        elif self.execution_type == "custom":
            app_filters = "Filter: " + self.custom_filter
        else:
            app_filters = self.execution_type

        helper.sendemail_alerts(
                    url="https://dq-qa.sigmoid.io/",
                    support_email_id="pratchav@sigmoidanalytics.com",
                    link="https://dq-qa.sigmoid.io/",
                    powerbi_link="",
                    list_of_emails=[],
                    appl_filter=app_filters,
                    target_table=self.target_table,
                    list_of_tables=[],
                    team="",
                    dq_score = dq_score,
                    top_failed = top_failed_str
                )
