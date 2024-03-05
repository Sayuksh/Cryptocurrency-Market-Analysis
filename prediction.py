import torch
from scaleanddescale import descaler
def prediction(data,model,model_name,index,predict_length):
    model.load_state_dict(torch.load(f'{model_name}_{predict_length}.pth'))
    model.eval()
# Make predictions
    with torch.no_grad():
        prediction = model(data)
    prediction=descaler(data,index)
    return prediction.numpy()