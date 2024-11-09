
import jittor as jt
from jittor import nn
from jittor import Module
from aim import Run
from MMonitor.mmonitor.monitor import Monitor  
from MMonitor.visualize import Visualization 
import jittor.transform as transforms
from jittor.dataset.cifar import CIFAR10
import time
from jittor.models.resnet import *
from transformers import ResNetForImageClassification
import numpy as np

def prepare_data(batch_size,num_workers=2):
    transform_train = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.RandomCrop(32),
        transforms.ToTensor(),
        transforms.ImageNormalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.ImageNormalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    # 加载数据集
    trainset = CIFAR10(train=True, transform=transform_train)
    trainloader = trainset.set_attrs(batch_size=batch_size, shuffle=True, num_workers=2)
    testset = CIFAR10(train=False, transform=transform_test)
    testloader = testset.set_attrs(batch_size=batch_size, shuffle=False, num_workers=2)
    return trainloader,testloader

def prepare_config(model):
    # model.layer1[0].bn1
    # model.layer1[0].conv2
    #
    config_mmonitor = {
        model.layer1[0].bn1:['VarTID','InputSndNorm']
    }
    return config_mmonitor
if __name__=='__main__':
    model = Resnet18(pretrained=False)
    print('模型已经引入')
    batch_size=32
    train_loader,test_loader = prepare_data(batch_size)
    print('数据已引入')
    criterion = nn.CrossEntropyLoss()
    opt = nn.Adam(model.parameters(), lr=0.001)
    num_epochs = 10
    config_mmonitor = prepare_config(model)
    monitor = Monitor(model,config_mmonitor)
    vis = Visualization(monitor, project=config_mmonitor.keys(), name=config_mmonitor.values())
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for i,(inputs,labels) in enumerate(train_loader):
            outputs = model(inputs)
            loss = criterion(outputs,labels)
            running_loss += loss.item()
        opt.step(running_loss)
        monitor.track(epoch)
        logs = vis.show(epoch)
        aim_run.track(logs,context={'subset':'train'})
        print(f"Epoch: {epoch}, Loss: {loss.item()}")
            