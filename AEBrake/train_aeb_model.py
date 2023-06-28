import torch
import torch.optim as optim
import torch.nn.functional as F
import torchvision
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
import glob
import PIL.Image
import os
import numpy as np
from tqdm import tqdm

center = 224./2.


def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']

dataset = datasets.ImageFolder(
    'dataset',
    transforms.Compose([
        transforms.ColorJitter(0.1, 0.1, 0.1, 0.1),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
)

train_dataset, test_dataset = torch.utils.data.random_split(dataset, [len(dataset) - 50, 50])

train_loader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=4
)

test_loader = torch.utils.data.DataLoader(
    test_dataset,
    batch_size=16,
    shuffle=True,
    num_workers=4
)

model = models.alexnet(pretrained=True)

model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 2)

device = torch.device('cuda')
model = model.to(device)

NUM_EPOCHS = 30
BEST_MODEL_PATH = 'best_model.pth'
best_accuracy = 0.0

optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

epoch_list = []
train_loss_list = []
test_loss_list = []

for epoch in range(NUM_EPOCHS):
    train_loss = 0.0
    for images, labels in iter(train_loader):
        images = images.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = F.cross_entropy(outputs, labels)
        train_loss += float(loss)
        loss.backward()
        optimizer.step()
    train_loss /= len(train_loader)
    
    test_error_count = 0.0

    test_loss = 0.0
    for images, labels in iter(test_loader):
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        test_error_count += float(torch.sum(torch.abs(labels - outputs.argmax(1))))
        loss = F.cross_entropy(outputs, labels)
        test_loss += float(loss)
    test_loss /= len(test_loader)
    
    test_accuracy = 1.0 - float(test_error_count) / float(len(test_dataset))
    print('%d: %f' % (epoch, test_accuracy))
	
    epoch_list.append(epoch)
    train_loss_list.append(train_loss)
    test_loss_list.append(test_loss)
	
    if test_accuracy > best_accuracy:
        torch.save(model.state_dict(), BEST_MODEL_PATH)
        best_accuracy = test_accuracy


import matplotlib.pyplot as plt

plt.plot(epoch_list, train_loss_list, '-b', label='train_loss_list')
plt.plot(epoch_list, test_loss_list, '-r', label='test_loss')

plt.xlabel("n iteration")
plt.legend(loc='upper left')

# show
plt.show()        
