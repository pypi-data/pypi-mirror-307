from dataguard import AnomalyDetection
from dataguard import DatabricksConnection

target_table = "sigma_test.ecomm_order_details"
target_columns = "quantity,amount"
connection_obj = DatabricksConnection(
    access_token="dapiaeb0495b58ec6e0c05bd56e76099b4e2-3",
    server_hostname="adb-1270988111630518.18.azuredatabricks.net",
    http_path="sql/protocolv1/o/1270988111630518/0731-102328-nflpsp31",
)
anomaly_obj = AnomalyDetection(connection_obj, target_columns, target_table)
result = anomaly_obj.predict_anomalies()
print(result)
