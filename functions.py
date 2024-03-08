from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

data = 0
model1 = LogisticRegression(solver="liblinear", random_state=0)
model2 = RandomForestClassifier(n_estimators=1000, random_state=0)
features2 = ['ejection_fraction','serum_creatinine','creatinine_phosphokinase', 'serum_sodium','platelets','high_blood_pressure', 'smoking', 'diabetes','time']

def m1(Z):
    print(pd.DataFrame(Z,index=[0]))
    data = pd.read_csv("data1.csv")
    y = data['target']
    features = data.columns[1:-1]
    X = data[features]
    model1.fit(X,y)
    r = model1.predict(pd.DataFrame(Z,index=[0]))
    return r[0]


def m2(Z):
    print(pd.DataFrame(Z,index=[0]))
    data = pd.read_csv("/data2.csv")
    X = data[features2]
    scaler = MinMaxScaler()
    # X = pd.DataFrame(scaler.fit_transform(X), columns=features2)
    print(X)
    y = data['DEATH_EVENT']
    model2.fit(X,y)
    r = model2.predict(pd.DataFrame(Z,index=[0]))
    print(r)
    return r[0]
