import torch
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt
from dataset import load_siamese_data
from modules import SiameseNetwork, ContrastiveLoss

SNN_PATH = 'SNN.pth'  # Path to save the trained Siamese Network model

def train():

    siamese_fit = trainSNN()
    torch.save(siamese_fit['model'].state_dict(), SNN_PATH)

    # Plot Accuracy and Loss
    plot_data(siamese_fit['loss'], 'Siamese Network')
    plt.show()

def trainSNN(epochs=30):
    
    siamese_train_loader = load_siamese_data(batch_size=32)
    model = SiameseNetwork()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    criterion = ContrastiveLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    siamese_fit = {'model': model, 'loss': {'train': [], 'val': []}}

    for epoch in range(epochs):
        model.train()
        train_loss = 0
        for batch_idx, (img1, img2, labels) in enumerate(siamese_train_loader):
            optimizer.zero_grad()
            
            img1, img2, labels = img1.to(device), img2.to(device), labels.to(device)
            
            output1, output2 = model(img1, img2)
            loss = criterion(output1, output2, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        siamese_fit['loss']['train'].append(train_loss / len(siamese_train_loader))

        print(f'Epoch {epoch + 1}/{epochs}, Loss: {siamese_fit["loss"]["train"][-1]}')

    return siamese_fit

def plot_data(data, title):
    
    plt.figure()
    plt.plot(data['train'], label='Train Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title(title)

if __name__ == '__main__':
    train()
