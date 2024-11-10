import mkdocs
import sklearn
import sklearn.datasets
import sklearn.metrics as metrics
import sklearn.model_selection
import sklearn.tree as tree
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import graphviz
import os
import statistics
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from pandas import read_csv
from sklearn.ensemble import GradientBoostingRegressor
from sklearn2pmml import PMMLPipeline, sklearn2pmml
from pypmml import Model
    

# read testing dataset
# data = read_csv(r'C:\Users\jjacq\xgrove\data\HousingData.csv')

# # create dataframe 
# df = pd.DataFrame(data)

# TODO: delete direct directory reference
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

# class grove():
#     # define xgrove-class with default values
#     # TODO add type check
#     # print("its upgraded")
#     def __init__(self, 
#                  model, 
#                  data: pd.DataFrame,
#                  ntrees: np.array = np.array([4, 8, 16, 32, 64, 128]), 
#                  pfun = None, 
#                  shrink: int = 1, 
#                  b_frac: int = 1, 
#                  seed: int = 42,
#                  grove_rate: float = 1,
#                  trained: bool = False,
#                  tar = None
#                  ):
#         self.model = model
#         self.data = self.encodeCategorical(data)
#         self.ntrees = ntrees
#         self.pfun = pfun
#         self.shrink = shrink
#         self.b_frac = b_frac
#         self.seed = seed
#         self.grove_rate = grove_rate
#         self.trained = trained
#         self.tar = tar
#         self.surrTar = self.getSurrogateTarget(pfun = self.pfun, tar=self.tar)
#         self.surrGrove = self.getGBM()
#         self.explanation = []
#         self.groves = []
#         self.rules = []
#         self.result = []

#     # get-functions for class overarching variables
    
#     def getSurrogateTarget(self, pfun, tar):
#     # Überprüfen, ob pfun None ist
#         if tar is None:
#             if self.pfun is None:
#                 # Dynamisches Entfernen des Zielattributs (surrTarName) aus den Daten
#                 # X = self.data.drop(columns=[self.surrTarName])
#                 # y = self.data[self.surrTarName]
                
#                 # Trainiere das Surrogatmodell mit den Daten
#                 # self.surrGrove.fit(X, y)
                
#                 # Mache Vorhersagen für die Zielvariable
#                 target = self.model.predict(self.data)
#             else:
#                 # Verwende die angegebene predictive function, um das Ziel zu berechnen
#                 target = pfun(model=self.model, data=self.data)
#         else: target = tar
#         return target

    
#     def getGBM(self):
#         grove = GradientBoostingRegressor(n_estimators=max(self.ntrees),
#                                           learning_rate=self.shrink,
#                                           subsample=self.b_frac)
#         grove.fit(self.data, self.surrTar)
#         return grove

#     # OHE for evaluating categorical columns
#     def encodeCategorical(self, data):
#         categorical_columns = data.select_dtypes(include=['object', 'category']).columns
#         data_encoded = pd.get_dummies(data, columns=categorical_columns)
#         return data_encoded

#     # calculate upsilon
#     def upsilon(self, pexp):
#         # Fehlerprävention durch gleichsetzen des Typs
#         surrTar_series = pd.Series(self.surrTar)
#         pexp_series = pd.Series(pexp)

#         ASE = statistics.mean((surrTar_series - pexp_series) ** 2)
#         ASE0 = statistics.mean((surrTar_series - statistics.mean(surrTar_series)) ** 2)
#         ups = 1 - ASE / ASE0
#         rho = statistics.correlation(surrTar_series, pexp_series)
#         return ups, rho

#     def get_result(self):
#         res = [self.explanation, self.rules, self.groves, self.model]
#         return res
    
#     # Plot method to visualize Upsilon vs. Rules
#     def plot(self, abs="rules", ord="upsilon"):
#         if len(self.explanation) == 0:
#             raise ValueError("No explanation data available. Please run the calculation first.")
        
#         # Get the corresponding indices for the given abs (x-axis) and ord (y-axis)
#         x_col = self.explanation[abs] if abs in self.explanation.columns else None
#         y_col = self.explanation[ord] if ord in self.explanation.columns else None
        
#         if x_col is None or y_col is None:
#             raise ValueError(f"Cannot find '{abs}' or '{ord}' in explanation columns.")
        
#         # Plot the x and y values
#         plt.plot(x_col, y_col, marker='o', linestyle='-', color='b')
#         plt.xlabel(abs)
#         plt.ylabel(ord)
#         plt.title(f'{ord} vs {abs}')
#         plt.grid(True)
#         plt.show()

#     def load_pmml_model(pmml_path):
#         """
#         Lädt ein PMML-Modell und gibt das Modellobjekt zurück.

#         Args:
#             pmml_path (str): Der Dateipfad zur PMML-Datei.

#         Returns:
#             model (pypmml.Model): Das geladene Modellobjekt.
#         """
#         try:
#             # Lade das PMML-Modell
#             model = Model.load(pmml_path)
#             return model
#         except Exception as e:
#             print(f"Fehler beim Laden des PMML-Modells: {e}")
#             return None

#     def export_to_pmml(self):
#         print("Exportiere Modelle als PMML...")
#         X = self.data.drop(columns=[self.surrTarName])
        
#         # Speichere GBM Modell
#         pipeline = PMMLPipeline([
#             ("classifier", self.surrGrove)
#         ])
#         sklearn2pmml(pipeline, "models/gbm_model.pmml")
        
#         # Speichere das RandomForest-Modell (oder anderes übergebenes Modell)
#         model_pipeline = PMMLPipeline([
#             ("classifier", self.model)
#         ])
#         sklearn2pmml(model_pipeline, "models/analyzed_model.pmml")
        
#         print("Modelle erfolgreich als PMML exportiert.")
        
#         # Speichere die Trainings- und Testdatensätze als CSV
#         self.save_datasets()

#     def save_datasets(self):
#         # Speichere den Datensatz für das Training
#         self.data.to_csv("data/training_data.csv", index=False)
#         print("Trainingsdaten als CSV gespeichert: training_data.csv")

#         # Speichere den Datensatz für das Testen (falls verfügbar)
#         if hasattr(self, 'data_test'):
#             self.data_test.to_csv("data/testing_data.csv", index=False)
#             print("Testdaten als CSV gespeichert: testing_data.csv")
        
#     def calculateGrove(self):
#         explanation = []
#         groves = []
#         interpretation = []
#         data = self.data
        
#         # for every tree
#         for nt in self.ntrees:
#             # predictions generation
#             predictions = self.surrGrove.staged_predict(data)
#             predictions = [next(predictions) for _ in range(nt)][-1]

#             rules = []
#             for tid in range(nt):
#                 # extract tree
#                 tree = self.surrGrove.estimators_[tid, 0].tree_
#                 # iterate every node of the tree
#                 for node_id in range(tree.node_count):
#                     if tree.children_left[node_id] != tree.children_right[node_id]:  #  splitsnode
#                         # save rule
#                         rule = {
#                             'feature': tree.feature[node_id],
#                             'threshold': tree.threshold[node_id],
#                             'pleft': tree.value[tree.children_left[node_id]][0][0],
#                             'pright': tree.value[tree.children_right[node_id]][0][0]
#                         }
#                         rules.append(rule)
            
#             # convert to dataframe and add to rules
#                 rules_df = pd.DataFrame(rules)
#                 groves.append(rules_df)
            
#             vars = []
#             splits= []
#             csplits_left = []
#             pleft = []
#             pright = []
#             for i in range(len(rules_df)):
#                 feature_index = int(rules_df.iloc[i]['feature'])
#                 # print("feature_index: ", feature_index)
#                 var_name = data.columns[int(feature_index)]
#                 vars.append(var_name)
#                 # print("isinstance(var_name, str): ", isinstance(var_name, str))
#                 # # Categorical columns
                
# ######################### Potentielle Fehlerquelle ####################################

#                 if pd.api.types.is_string_dtype(data.iloc[:,feature_index]) or isinstance(data.iloc[:,feature_index], str) or isinstance(data.iloc[:,feature_index], object):
#                     #print(i+": Kategorisch")
#                     levs = data[var_name].unique()
#                     lids = self.surrGrove.estimators_[0, 0].tree_.value[int(rules_df.iloc[i]['threshold'])] == -1
#                     if sum(lids) == 1: levs = levs[lids]
#                     if sum(lids) > 1: levs = " | ".join(levs[lids])
#                     csl = levs[0] if isinstance(levs, (list, pd.Index)) else levs
#                     if len(levs) > 1:
#                         csl = " | ".join(str(levs))

#                     splits.append("")
#                     csplits_left.append(csl)
                
#                 elif isinstance(data.iloc[:,i], pd.Categorical):
#                     levs = rules_df.columns[i].cat.categories
#                     lids = self.surrGrove.estimators_[0, 0].tree_.value[int(rules_df.iloc[i]['threshold'])] == -1
#                     if sum(lids) == 1: levs = levs[lids]
#                     if sum(lids) > 1: levs = " | ".join(levs[lids])
#                     csl = levs[0] if isinstance(levs, (list, pd.Index)) else levs
#                     if len(levs) > 1:
#                         csl = " | ".join(levs)

#                     splits.append("")
#                     csplits_left.append(csl)

#                 # Numeric columns   
#                 elif pd.api.types.is_numeric_dtype(data.iloc[:,i]) or np.issubdtype(data.iloc[:,i], np.number):
#                     #print(i+": Numerisch")
#                     splits = splits.append(rules_df.iloc[i]["threshold"])
#                     csplits_left.append(pd.NA)

#                 else:
#                     print(rules_df[i]+": uncaught case")
#             # # rules filled
#             # print("i: ", i)
#             # print("Länge rules_df: ", len(rules_df))

#             pleft.append(rules_df.loc[:,"pleft"])
#             pright.append(rules_df.loc[:,"pleft"])

#             # # print("pright.len: ",len(np.array(round(elem, 4) for elem in pright)))
#             # print()
#             # print("vars.len: ",len(vars))
#             # print("splits.len: ",len(splits))

#             pleft = np.array(round(elem, 4) for elem in pleft)
#             pright = np.array(round(elem, 4) for elem in pright)

#             basepred = self.surrGrove.estimators_
            
#             df = pd.DataFrame({
#                 "vars": vars,
#                 "splits": splits,
#                 "left": csplits_left,
#                 "pleft": pleft,
#                 "pright": pright
#             })
#             # print(df)
#             # print("vars: ", df.loc[:,"vars"])
#             # print("splits: ", df.loc[:,"splits"])
#             # print("left: ", df.loc[:,"left"])

#             df_small = df.groupby(["vars", "splits", "left"], as_index=False).agg({"pleft" : "sum", "pright" : "sum"})
#             # df_small.set_index(["vars", "splits", "left"], inplace=True)
#             # df_small.index.set_names(["vars", "splits", "left"], inplace=True)
#             print(df_small.shape)
#             print(df_small.columns)

#             if(len(df_small) > 1):
#                 print(len(df_small))
#                 i = 1
#                 while (i != 0):
#                     drop_rule = False
#                     # check if its numeric AND NOT categorical
#                     # all_vars = df_small.index.get_level_values('vars')

#                     # print("all_vars: ",all_vars)
#                     print("df_small: ",df_small)
#                     print("i: ",i)
#                     print("vars at ",i,": ", df_small["vars"].iloc[i])

#                     if pd.api.types.is_numeric_dtype(self.data[df_small["vars"].iloc[i]])or np.issubdtype(self.data[df_small["vars"].iloc[i]], np.number) and not(isinstance(self.data[df_small["vars"].iloc[i]], pd.Categorical | object | str) or pd.api.types.is_string_dtype(self.data[df_small["vars"].iloc[i]])):
#                         #print(i+": Numerisch")
#                         for j in range(0, i):
#                             if df_small["vars"][i] == df_small["vars"][j]:
#                                 v1 = self.data[df_small["vars"][i]] <= df_small["splits"][i]
#                                 v2 = data[df_small["vars"][j]] <= df_small["splits"][j]
#                                 tab = [v1,v2]
#                                 if tab.values.trace() == tab.values.sum():
#                                     df_small.at[j, 'pleft'] = df_small.at[i, 'pleft'] + df_small.at[j, 'pleft']
#                                     df_small.at[j, 'pright'] = df_small.at[i, 'pright'] + df_small.at[j, 'pright']
#                                     drop_rule = True
#                     if drop_rule: df_small = df_small[-i,]
#                     if not drop_rule: i = i+1
#                     if i+1 > len(df_small): i = 0
#             # compute complexity and explainability statistics
#             print("predictions: ", len(predictions))
#             print("surrTar: ", len(self.surrTar))
#             upsilon, rho = self.upsilon(pexp=predictions)

#             df0 = pd.DataFrame({
#                 "vars": ["Interept"],
#                 "splits": [pd.NA],
#                 "left": [pd.NA],
#                 "pleft": [basepred],
#                 "pright": [basepred]
#             })
#             df = pd.concat([df0, df], ignore_index=True)
#             df_small = pd.concat([df0, df_small], ignore_index = True)

#             # for better
#             df = df.rename({
#                 "vars": "variable",
#                 "splits": "upper_bound_left",
#                 "left": "levels_left"
#                 }, axis=1) 
#             df_small = df_small.rename({
#                 "vars": "variable",
#                 "splits": "upper_bound_left",
#                 "left": "levels_left"
#                 }, axis=1)
            

#             groves[len(groves)-1] = df
#             interpretation.append(df_small)
#             explanation.append({
#                 "trees": nt,
#                 "rules":len(df_small),
#                 "upsilon":upsilon,
#                 "cor": rho
#                 })

#         # end of for every tree
#         # groves = pd.DataFrame(groves)
#         # interpretation = pd.DataFrame(interpretation)
#         explanation = pd.DataFrame(explanation)

#         # groves.index = self.ntrees
#         # interpretation.index = self.ntrees
#         # # explanation.columns = ["trees", "rules", "upsilon", "cor"]

#         self.explanation = explanation
#         self.rules = interpretation
#         self.groves = groves
#         self.model = self.surrGrove

#         self.result = self.get_result()
#     # end of calculateGrove()

#         # TODO add functionality of plot
import pandas as pd
import numpy as np
import statistics
from sklearn.ensemble import GradientBoostingRegressor
import matplotlib.pyplot as plt

class grove():
    def __init__(self, 
                 model, 
                 data: pd.DataFrame,
                 ntrees: np.array = np.array([4, 8, 16, 32, 64, 128]), 
                 pfun=None, 
                 shrink: int = 1, 
                 b_frac: int = 1, 
                 seed: int = 42,
                 grove_rate: float = 1,
                 trained: bool = False,
                 tar=None):
        self.model = model
        self.data = self.encodeCategorical(data)
        self.ntrees = ntrees
        self.pfun = pfun
        self.shrink = shrink
        self.b_frac = b_frac
        self.seed = seed
        self.grove_rate = grove_rate
        self.trained = trained
        self.tar = tar
        self.surrTar = self.getSurrogateTarget(pfun=self.pfun, tar=self.tar)
        self.surrGrove = self.getGBM()
        self.explanation = []
        self.groves = []
        self.rules = []
        self.result = []

    def encodeCategorical(self, data):
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns
        return pd.get_dummies(data, columns=categorical_columns)

    def getSurrogateTarget(self, pfun, tar):
        if tar is None:
            return self.model.predict(self.data) if self.pfun is None else pfun(model=self.model, data=self.data)
        else:
            return tar

    def getGBM(self):
        grove = GradientBoostingRegressor(n_estimators=max(self.ntrees), learning_rate=self.shrink, subsample=self.b_frac)
        grove.fit(self.data, self.surrTar)
        return grove

    def upsilon(self, pexp):
        surrTar_series = pd.Series(self.surrTar)
        pexp_series = pd.Series(pexp)
        ASE = statistics.mean((surrTar_series - pexp_series) ** 2)
        ASE0 = statistics.mean((surrTar_series - statistics.mean(surrTar_series)) ** 2)
        ups = 1 - ASE / ASE0
        rho = statistics.correlation(surrTar_series, pexp_series)
        return ups, rho

    def get_result(self):
        return [self.explanation, self.rules, self.groves, self.model]

    def calculateGrove(self):
        explanation = []
        groves = []
        interpretation = []
        data = self.data

        # Start with an empty DataFrame for rules
        cumulative_rules = pd.DataFrame()

        # For every tree count (nt)
        for nt in self.ntrees:
            rules = []  # List to store rules for the current tree

            # Generate predictions (this part stays the same)
            predictions = self.surrGrove.staged_predict(data)
            predictions = [next(predictions) for _ in range(nt)][-1]

            # For every tree (for nt trees, we calculate rules for each tree)
            for tid in range(nt):
                tree = self.surrGrove.estimators_[tid, 0].tree_

                # Iterate through every node of the tree
                for node_id in range(tree.node_count):
                    if tree.children_left[node_id] != tree.children_right[node_id]:  # split node
                        rule = {
                            'feature': tree.feature[node_id],
                            'threshold': tree.threshold[node_id],
                            'pleft': tree.value[tree.children_left[node_id]][0][0],
                            'pright': tree.value[tree.children_right[node_id]][0][0]
                        }
                        rules.append(rule)

            # Convert the current tree's rules to a DataFrame
            rules_df = pd.DataFrame(rules)

            # Add the current tree's rules to the cumulative rules
            cumulative_rules = pd.concat([cumulative_rules, rules_df], ignore_index=True)

            # Save the cumulative rules as the current "grove" (add it to groves)
            groves.append(cumulative_rules)

            # Calculate the complexity and explanation (same as before)
            upsilon, rho = self.upsilon(pexp=predictions)

            # Interpret the rules (same as before)
            # Leere Listen für die gesammelten Variablen und anderen Werte
            interpretation = []
            explanation = []

            # Iteriere über jede Grove (jede Anzahl an Bäumen)
            for nt, grove in enumerate(groves, 1):  # nt ist die Anzahl der Bäume für diese Grove
                # Zunächst leere Daten für die aktuellen Bäume der Grove
                cumulative_rules = pd.DataFrame()

                # Iteriere über alle Bäume in der aktuellen Grove
                for baum in grove:
                    # Falls baum keine DataFrame-Struktur ist, konvertiere es dazu
                    if isinstance(baum, str):
                        print(f"Error: Unexpected data format for baum: {type(baum)}")
                        continue  # Überspringe diesen Baum, wenn er nicht im richtigen Format ist

                    # Hier nehmen wir an, dass baum ein DataFrame ist
                    rules = baum  # Setze die Regeln des aktuellen Baums in das DataFrame rules

                    # Bereite die temporären Listen vor
                    vars_temp = []
                    splits_temp = []
                    csplits_left_temp = []
                    pleft_temp = []
                    pright_temp = []

                    for i in range(len(rules)):
                        feature_index = int(rules.iloc[i]['feature'])
                        var_name = data.columns[feature_index]
                        vars_temp.append(var_name)

                        if pd.api.types.is_string_dtype(data.iloc[:, feature_index]) or isinstance(data.iloc[:, feature_index], str) or isinstance(data.iloc[:, feature_index], object):
                            levs = data[var_name].unique()
                            csl = " | ".join(map(str, levs))
                            splits_temp.append("")
                            csplits_left_temp.append(csl)
                        elif pd.api.types.is_numeric_dtype(data.iloc[:, feature_index]) or np.issubdtype(data.iloc[:, feature_index], np.number):
                            splits_temp.append(rules.iloc[i]["threshold"])
                            csplits_left_temp.append(pd.NA)

                        pleft_temp.append(rules.loc[i, "pleft"])
                        pright_temp.append(rules.loc[i, "pright"])

                    # Erstelle DataFrame für diesen Baum
                    df_tree = pd.DataFrame({
                        "vars": vars_temp,
                        "splits": splits_temp,
                        "left": csplits_left_temp,
                        "pleft": pleft_temp,
                        "pright": pright_temp
                    })

                    # Füge dieses Baum-DataFrame der kumulierten Liste der Regeln hinzu
                    cumulative_rules = pd.concat([cumulative_rules, df_tree], ignore_index=True)

                # Intercept hinzufügen für die Basisregel
                df0 = pd.DataFrame({
                    "vars": ["Intercept"],
                    "splits": [pd.NA],
                    "left": [pd.NA],
                    "pleft": [self.surrGrove.estimators_[0, 0].tree_.value[0][0]],
                    "pright": [self.surrGrove.estimators_[0, 0].tree_.value[0][0]]
                })

                cumulative_rules = pd.concat([df0, cumulative_rules], ignore_index=True)

                # Umbenennen der Spalten für mehr Klarheit
                cumulative_rules = cumulative_rules.rename(columns={"vars": "variable", "splits": "upper_bound_left", "left": "levels_left"})

                # Kumulative Aggregation der Regeln für diese Grove
                df_small = cumulative_rules.groupby(["variable", "upper_bound_left", "levels_left"], as_index=False).agg({"pleft": "sum", "pright": "sum"})

                # Speichern der Interpretation für diese Grove
                interpretation.append(df_small)
                
                # Erklärung für diese Grove (Anzahl der Regeln, upsilon, correlation)
                explanation.append({
                    "trees": nt,
                    "rules": len(df_small),
                    "upsilon": upsilon,
                    "cor": rho
                })

            # Jetzt enthält `interpretation` alle kumulierten DataFrames für jede Grove, und `explanation` enthält die Erklärungen zu jeder Grove.

# Jetzt enthält `interpretation` alle kumulierten DataFrames für jede Grove, und `explanation` enthält die Erklärungen zu jeder Grove.


        # Store the final results
        explanation = pd.DataFrame(explanation)
        self.explanation = explanation
        self.rules = interpretation
        self.groves = groves

        # Final result
        self.result = self.get_result()

# import pandas as pd
# from pypmml import Model  # Importiere pypmml für das Modell
# #import xgrove.grove as grove

# # Definiere den PMML-Dateipfad und den CSV-Datenpfad
# pmml_path = "../models/linear_model.pmml"
# data_path = "../models/generated_data.csv"

# # Lade das trainierte PMML-Modell (aus R gespeichert)
# pmml_model = Model.load(pmml_path)  # Laden des trainierten Modells

# # Lade die Eingabedaten aus der CSV-Datei
# input_data = pd.read_csv(data_path)

# # Entferne die Zielvariable 'Target' aus den Eingabedaten
# input_data = input_data.drop(columns=["Target"])

# # Erstelle ein grove-Objekt mit dem geladenen Modell und den bearbeiteten Eingabedaten
# grove_instance = grove(model=pmml_model, data=input_data, trained=True)

# # Führe die Berechnung durch
# grove_instance.calculateGrove()

# # Ausgabe des Resultats und der Explanation
# print("Result:")
# print(grove_instance.result)

# print("\nExplanation:")
# print(grove_instance.explanation)

