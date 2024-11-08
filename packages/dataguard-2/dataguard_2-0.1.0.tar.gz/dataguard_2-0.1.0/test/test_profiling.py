from dataguard import Profiling
from dataguard import DatabricksConnection

try:
    connection_obj = DatabricksConnection(
        access_token="dapiaeb0495b58ec6e0c05bd56e76099b4e2-3",
        server_hostname="adb-1270988111630518.18.azuredatabricks.net",
        http_path="sql/protocolv1/o/1270988111630518/0731-102328-nflpsp31",
    )
except Exception as ex:
    print(ex)

engine = Profiling(
    connection_obj,
    report_id=1,
    cataloag_name="",
    schema_name="sigma_test",
    table_name="customer",
    selected_column="",
    partition_column_name="country",
    sample_percentage=70,
)

print(engine.profiler())
