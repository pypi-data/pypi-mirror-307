import pickle
import joblib
from xgboost import XGBClassifier, XGBRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from SAInT.networks import MLP, TabResNet

def get_model_type_from_file(file_path):
    try:
        print("Try to open file ", file_path)
        with open(file_path, 'rb') as file:
            #model = pickle.load(file)
            model = joblib.load(file)
        #[STDOUT]: /home/schuler/Repositories/c3di/SAInT/outputs/titanic/models/models/titanic_fastai_mlp_bs_8_lr_default_wd_default_mae_hidden_64_32_32_32_p0.00_max_epochs_50_patience_10.pkl
        #[STDOUT]: Error loading file: persistent IDs in protocol 0 must be ASCII strings
        #[STDOUT]: internal model_type = error
        print("Get type of ", model)
        print(type(model))
        # keras.src.models.sequential.Sequential
        # numpy.ndarray
        if isinstance(model, (XGBClassifier, XGBRegressor)):
            return "xgb"
        elif isinstance(model, (RandomForestClassifier, RandomForestRegressor)):
            return "rf"
        elif isinstance(model, (DecisionTreeClassifier, DecisionTreeRegressor)):
            return "dt"
        elif isinstance(model, (SVC, SVR)):
            return "svm"
        elif isinstance(model, (MLP)):
            return "mlp"
        elif isinstance(model, (TabResNet)):
            return "res"
        else:
            return "unknown"

    except Exception as e:
        print(f"Error loading file: {e}")
        return "error"
