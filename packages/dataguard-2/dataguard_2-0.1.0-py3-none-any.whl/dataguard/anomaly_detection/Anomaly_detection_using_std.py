import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class AnomalyDetection:
    def __init__(
        self, connection_obj, numeric_features, target_table, sample_percentage=None
    ):
        self.numeric_features = numeric_features
        self.target_table = target_table
        self.sample_percentage = 20
        self.conn = connection_obj

    def load_dataset(self):
        query = f"select {self.numeric_features} from {self.target_table}"
        data = self.conn.execute_query(query)
        # df = pd.read_json(data)
        return data

    def sampling(self):
        data = self.load_dataset()
        df = pd.DataFrame(data)
        sample_fraction = self.sample_percentage / 100.0
        sample_size = int(len(df) * sample_fraction)
        sampled_data = df.sample(n=sample_size, replace=False)
        return sampled_data

    def preprocess_data(self):
        """Preprocess the data by handling missing values and scaling."""
        df = self.sampling()
        self.df = df.dropna()
        return self.df

    def train_model(self):
        df = self.preprocess_data()
        meta = {}
        self.column_names = df.columns.tolist()
        for column in self.column_names:
            meta[column] = {}
            mean = df[column].mean()
            std = df[column].std()
            std_div = std * 2
            lower_limit, upper_limit = mean - std_div, mean + std_div
            meta[column]["mean"] = mean
            meta[column]["std"] = std
            meta[column]["lower_limit"] = lower_limit
            meta[column]["upper_limit"] = upper_limit
        return meta

    def result_json(self, dfX, meta):
        column = []

        for col in dfX.columns:
            column.append({"name": col, "datatype": str(dfX[col].dtype)})

        # extracting the row data from data frame
        rows = []
        rows_meta = dfX.to_dict(orient="records")
        for r in rows_meta:
            rows.append(r)

        # extracting actual count of an anomalies and normal data points
        value_count = dfX["anomaly_label"].value_counts()
        count = {
            "normal_data": str(
                value_count.get(1, 0)
            ),  # Count for normal data (value 1)
            "anomalies": str(
                value_count.sum() - value_count.get(1, 0)
            ),  # All others are anomalies
        }
        column_list = self.numeric_features.split(",")
        count["column_name"] = column_list
        # merge all the dictionaries to create a json
        result = {"column": column, "row": rows, "count": count, "meta": meta}
        return result

    def predict_anomalies(self):
        model = self.train_model()
        for column in model.keys():
            self.df[f"anomaly_label_{column}"] = self.df[column].apply(
                lambda x: (
                    -1
                    if x < model[column]["lower_limit"]
                    or x > model[column]["upper_limit"]
                    else 1
                )
            )

        column_anomaly = [f"anomaly_label_{item}" for item in self.column_names]
        self.df["anomaly_label"] = self.df.apply(
            lambda row: 1 if all(row[col] == 1 for col in column_anomaly) else -1,
            axis=1,
        )
        self.df = self.df.drop(column_anomaly, axis=1)
        result = self.result_json(self.df, model)
        return result
