from dataguard import DatabricksConnection
from dataguard import rules_master

base_url = "https://dq-dev-api.sigmoid.io"
dq_report_id = 1
table_id = 10
table_name = "customer"
schema_name = "sigma_test"
execution_type = ""
custom_filter = ""
pk_column = "customer_id"

try:
    connection_obj = DatabricksConnection(
        access_token="dapiaeb0495b58ec6e0c05bd56e76099b4e2-3",
        server_hostname="adb-1270988111630518.18.azuredatabricks.net",
        http_path="sql/protocolv1/o/1270988111630518/0731-102328-nflpsp31",
    )
except Exception as ex:
    print(ex)

engine = rules_master(
    connection_obj,
    base_url,
    dq_report_id=dq_report_id,
    table_id=table_id,
    table_name=table_name,
    schema_name=schema_name,
    execution_type=execution_type,
    custom_filter=custom_filter,
    pk_column=pk_column,
)

dq_report = engine.run_data_quality()
print(dq_report)
engine.save_report_in_backend(dq_report)
engine.send_email_alert()
