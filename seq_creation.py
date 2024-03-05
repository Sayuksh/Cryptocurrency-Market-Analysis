import torch
import numpy as np
def sequence_define(data,seq_length,index_of_Y,predict_length):

    #tail of train data is need as the model requires the seq_length of data to predict
    X=[]
    Y=[]
    for i in range(seq_length,data.shape[0]):
            X.append(data[i-seq_length:i])
            Y.append(data[i:i+predict_length,index_of_Y])
    # for i in range(seq_length,data.shape[0]-(data.shape[0]%seq_length)):
    #         X.append(data[i-seq_length:i])
    #         Y.append(data[i:i+predict_length,index_of_Y])
    X=torch.tensor(np.array(X),dtype=torch.float32)
    Y=torch.tensor(np.array(Y),dtype=torch.float32)
    
    return X,Y
