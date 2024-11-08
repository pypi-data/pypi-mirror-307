import warnings
import pickle

def load_model(modelname):
    # Suppress the InconsistentVersionWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        with open(modelname, 'rb') as file:
            model = pickle.load(file)
            return model
    return None

def save_model(modelname):
    # Save the updated model back to a new .pkl file
    updated_modelname = 'updated_' + modelname
    with open(updated_modelname, 'wb') as file:
        pickle.dump(model, file)


def fix_decisiontree():
    modelname='decision_tree_model.pkl'

    features = ['Age', 'contra', 'wann', 'kra', 'rei', 'zie', 'ste', 'puls', 'ber', 'dru', 'bre', 'hitz', 'blitz', \
                'Schmerzen Periode', 'Schmerzen CUB', 'Schmerzen Wasserlassen', 'Schmerzen Stuhlgang', 'Schmerzen Sex', 'Akt. Schmerz', \
                'Staerkster Schmerz in vier wochen', 'Mean Pain', 'Schmerzverlauf', 'LWS', 'Oberbauch/Mittelbauch', 'Bein/OS', 'Unterbauch', \
                'Vaginal/Mons pubis', 'Huefte Leiste Becken', 'Glutealregion', 'Endscore', 'Verstopfungen', 'Durchfall', 'Analgetika', \
                'EM Hormonbeh.', 'Myom', 'Fruchtbar', 'BMI', 'Raucher', 'Allergie', 'SUMME VAS', 'Summe SP', 'Sexuell aktiv']

    model = load_model(modelname)
    if model is not None:
        print(model.feature_names_in_)
        #print(model)
        # Assign your custom feature names to model.feature_names_in_
        model.feature_names_in_ = features
        # Check if the assignment was successful
        print(model.feature_names_in_)
        save_model(modelname)


##############################################################################

modelname='nn.pkl'
model = load_model(modelname)
#print(model.feature_names_in_)
#print(model)
print(model.summary())
