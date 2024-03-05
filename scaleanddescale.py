from sklearn.preprocessing import MinMaxScaler, StandardScaler
scaler=MinMaxScaler()
scaler2=StandardScaler()
def data_scaler(data):
    data=scaler.fit_transform(data)
    data=scaler2.fit_transform(data)
    return data
def data_descaler(prediction,index):
    standard_values=1/(scaler2.scale_[index])
    minmax_values=1/(scaler.scale_[index])
    
    prediction=prediction*standard_values*minmax_values
    
    return prediction