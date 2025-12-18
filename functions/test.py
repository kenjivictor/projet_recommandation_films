import joblib
import pandas as pd

def recuperation_index(id):

    X= pd.read_csv("db/Features.csv")

    model_recommandation = joblib.load('model_recommandation')

    distances, indices = model_recommandation.named_steps["nn"].kneighbors(
        model_recommandation.named_steps["prep"].transform(X.iloc[[id]]))

    return indices[0]