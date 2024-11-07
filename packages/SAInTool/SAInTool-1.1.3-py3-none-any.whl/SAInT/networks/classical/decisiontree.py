from typing import Union, Tuple
from fastai.tabular.all import TabularDataLoaders
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from SAInT.networks.classical.classical import ClassicalModel


class DecisionTree(ClassicalModel):

    def __init__(self,
                 dls: TabularDataLoaders,
                 name: str,
                 path: str,
                 num_features: int,
                 output_size: int,
                 target_names: list,
                 categorical_cols: list,
                 continuous_cols: list,
                 mode: str,
                 criterion: str = "gini",
                 max_depth: int = None,
                 min_samples_leaf: int = 1,
                 min_samples_split: int = 2,
                 class_weight: str = None,
                 random_seed: int = 123456,
                 model: Union[DecisionTreeRegressor,
                              DecisionTreeClassifier] = None,
                 verbose: bool = False):
        if model is None:
            kwargs = {
                "criterion": criterion,
                "max_depth": max_depth,
                "min_samples_leaf": min_samples_leaf,
                "min_samples_split": min_samples_split,
                "random_state": random_seed
            }
            if mode == "classification":
                kwargs["class_weight"] = class_weight
            model = DecisionTreeRegressor(
                **kwargs) if mode == "regression" else DecisionTreeClassifier(
                    **kwargs)
        super().__init__(model,
                         name,
                         path,
                         num_features,
                         output_size,
                         target_names,
                         categorical_cols,
                         continuous_cols,
                         mode,
                         verbose=verbose)
        self.inputs = dls.xs
        self.outputs = dls.ys.values if dls.ys.values.shape[
            1] != 1 else dls.ys.values.ravel()

    def test(self, dls: TabularDataLoaders, metric) -> Tuple[float, list]:
        return super().test_input_and_output(dls.xs, dls.ys.values, metric)

    def get_n_most_important_features(self,
                                      num_top_features: int = 20) -> list:
        self.feature_importances = dict(
            zip(self.inputs.columns, self.model.feature_importances_))

        top_features = sorted(self.feature_importances,
                              key=lambda x: x[1],
                              reverse=True)[:num_top_features]
        return top_features
