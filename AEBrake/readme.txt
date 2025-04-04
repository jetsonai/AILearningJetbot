* YOU MUST INSTALL PYTORCH BEFORE START THIS.!!

* 딥러닝 패키지 설치가 아직 되지 않았다면 먼저 설치가 필요합니다.: 
   go to tis page to Install DL setting 
   
   https://github.com/jetsonai/AILearningJetbot/tree/main/StartDL
   

1. data_collection

save_block=0 # 0: free, 1:block


1) Take Blocked Picture

python3 aeb_data_collection.py 1

# press 's' to take picture
(collect picture more than 40)

# Ctl-C to finish it

2) Take Free Picture

python3 aeb_data_collection.py 0

# press 's' to take picture
(collect picture more than 40)

# Ctl-C to finish it

----------------------------------------
2. train_fca_model

python3 train_aeb_model.py                                                                                                                                                     

----------------------------------------

* YOU MUST set power mod 5W !!

model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 38)

3. fca_live_demo

python3 aeb_live_demo.py
