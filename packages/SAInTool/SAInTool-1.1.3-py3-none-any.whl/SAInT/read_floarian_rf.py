import warnings
import pickle

modelname='decision_tree_model.pkl'
#modelname='endometriose_2024_10_29_trainValidTest_FeatureNames_dt_max_depth_5_min_samples_split_5_min_samples_leaf_2_criterion_entropy_class_weight_balanced.pkl'
#modelname='nn.pkl'
#modelname='randomforrest.pkl'

features = ['Age', 'contra', 'wann', 'kra', 'rei', 'zie', 'ste', 'puls', 'ber', 'dru', 'bre', 'hitz', 'blitz', \
            'Schmerzen Periode', 'Schmerzen CUB', 'Schmerzen Wasserlassen', 'Schmerzen Stuhlgang', 'Schmerzen Sex', 'Akt. Schmerz', \
            'Staerkster Schmerz in vier wochen', 'Mean Pain', 'Schmerzverlauf', 'LWS', 'Oberbauch/Mittelbauch', 'Bein/OS', 'Unterbauch', \
            'Vaginal/Mons pubis', 'Huefte Leiste Becken', 'Glutealregion', 'Endscore', 'Verstopfungen', 'Durchfall', 'Analgetika', \
            'EM Hormonbeh.', 'Myom', 'Fruchtbar', 'BMI', 'Raucher', 'Allergie', 'SUMME VAS', 'Summe SP', 'Sexuell aktiv']

# Suppress the InconsistentVersionWarning
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    with open(modelname, 'rb') as file:
        model = pickle.load(file)
    print(model.feature_names_in_)
    #print(model)

    # Assign your custom feature names to model.feature_names_in_
    model.feature_names_in_ = features
    # Check if the assignment was successful
    print(model.feature_names_in_)

    # Save the updated model back to a new .pkl file
    updated_modelname = 'updated_decision_tree_model.pkl'
    with open(updated_modelname, 'wb') as file:
        pickle.dump(model, file)

# Check if model loaded correctly
print("Model loaded successfully.")
