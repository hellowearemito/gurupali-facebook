import pandas as pd


def normalize_node_weights():
    node_data = pd.read_csv("nodes.csv")
    sums = node_data.groupby(by=["year", "month"], as_index=False).sum()
    new_df = pd.merge(node_data, sums, how='left', left_on=["year", "month"], right_on=["year", "month"])

    def f(x):
        return float(x["weight_x"]) / float(x["weight_y"])

    new_df["weight"] = new_df.apply(f, axis=1)

    narrowed_df = new_df[["id_x", "year", "month", "group_x", "weight"]]

    narrowed_df = narrowed_df.rename(columns={'id_x': 'id', 'group_x': 'group'})

    narrowed_df.to_csv("nodes2.csv", index=False)
    return True


def normalize_edge_weights():
    edge_data = pd.read_csv("edges.csv")
    sums = edge_data.groupby(by=["year", "month"], as_index=False).sum()
    new_df = pd.merge(edge_data, sums, how='left', left_on=["year", "month"], right_on=["year", "month"])

    def f(x):
        return float(x["weight_x"]) / float(x["weight_y"])

    new_df['weight'] = new_df.apply(f, axis=1)

    narrowed_df = new_df[["from_x", "to_x", "year",  "month", "weight"]]

    narrowed_df = narrowed_df.rename(columns={'from_x': 'from', 'to_x': 'to'})

    narrowed_df.to_csv("edges2.csv", index=False)
    return True


