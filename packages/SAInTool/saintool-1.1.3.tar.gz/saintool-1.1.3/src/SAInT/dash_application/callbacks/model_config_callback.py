from dash import Input, Output
from SAInT.dash_application.common.dash_functions import get_pressed_buttons
from SAInT.dash_application import saint_dash_layout_components as layout

def _get_setting_for_selected_model(app, value):
    settings = app.application.settings
    trainer_data_settings = app.application.trainer.data_settings if app.application.trainer else None
    
    if value == "xgb_model_selected":
        xgboost_depth = settings.xgb_max_depth
        xgboost_n_estimators = settings.xgb_n_estimators
        setting = f"max_depth={xgboost_depth}, n_estimators={xgboost_n_estimators}"
    elif value == "rf_model_selected":
        rf_depth = settings.rf_max_depth
        rf_n_estimators = settings.rf_n_estimators
        rf_criterion = settings.rf_criterion
        if rf_criterion == "default":
            rf_criterion = "squared_error" if trainer_data_settings.mode == "regression" else "gini"
        rf_min_samples_leaf = settings.rf_min_samples_leaf
        rf_min_samples_split = settings.rf_min_samples_split
        setting = f"max_depth={rf_depth}, n_estimators={rf_n_estimators}, criterion={rf_criterion}, min_samples_leaf={rf_min_samples_leaf}, min_samples_split={rf_min_samples_split}"
    elif value == "dt_model_selected":
        dt_criterion = settings.dt_criterion
        if dt_criterion == "default":
            dt_criterion = "squared_error" if trainer_data_settings.mode == "regression" else "gini"
        dt_max_depth = settings.dt_max_depth
        dt_min_samples_leaf = settings.dt_min_samples_leaf
        dt_min_samples_split = settings.dt_min_samples_split
        dt_class_weight = settings.dt_class_weight
        setting = f"criterion={dt_criterion}, max_depth={dt_max_depth}, min_samples_leaf={dt_min_samples_leaf}, min_samples_split={dt_min_samples_split}, class_weight={dt_class_weight}"
    elif value == "svm_model_selected":
        svm_degree = settings.svm_degree
        setting = f"degree={svm_degree}"
    elif value == "mlp_model_selected":
        if trainer_data_settings:
            batchsize = trainer_data_settings.batchsize
            hidden_layers = settings.mlp_hidden_layers
            mlp_dropout = settings.mlp_dropout
            max_epochs = settings.max_epochs
            patience = settings.patience
            setting = f"hidden_layers={hidden_layers}, dropout={mlp_dropout}, batchsize={batchsize}, max_epochs={max_epochs}, patience={patience}"
        else:
            setting = ""
    elif value == "resnet_model_selected":
        if trainer_data_settings:
            batchsize = trainer_data_settings.batchsize
            resnet_layersize = settings.resnet_layersizes
            resnet_num_blocks = settings.resnet_blocks
            resnet_dropout = settings.resnet_dropout
            max_epochs = settings.max_epochs
            patience = settings.patience
            setting = f"layersize={resnet_layersize}, num_blocks={resnet_num_blocks}, dropout={resnet_dropout}, batchsize={batchsize}, max_epochs={max_epochs}, patience={patience}"
        else:
            setting = ""
    else:
        setting = ""
    return setting

def register_model_configuration_callback(dash_app, app):
    @dash_app.callback(
        Output("models-definition-configuration-input", "value"),
        Output("add_model_button", "style"),
        Input("models-definition-dropdown", "value")
    )
    def set_model_configuration_input(value):
        changed_id = get_pressed_buttons()
        if "models-definition-dropdown.value" in changed_id:
            if app.application.settings is not None:
                setting = _get_setting_for_selected_model(app, value)
                if setting:
                    return setting, {"display": "inline-block"}
                else:
                    return setting, {"display": "none"}
        return "", {"display": "none"}
