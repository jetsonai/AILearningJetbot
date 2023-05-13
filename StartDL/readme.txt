-----------------------------------------------------------------------------------------------------
## 만약 5장에서 딥러닝 세팅을 모두 마쳤다면 8장과 9장을 위해 아래의 두가지 패키지만 반드시 설치하고 가세요.
   
pip3 install tqdm

pip3 install packaging
---------------------------------------------------------------------------------------------------

## 만약 새로운 sd 카드에서 8장과 9장 실습을 하고자 한다면 아래의 설치를 모두 해주세요.

cd
cd AILearningJetbot/StartDL

chmod 777 *.sh

./install-pytorch.sh
   -> It might take more than 40 minutes.
   
   
pip3 install tqdm

pip3 install packaging

   
./install_torch2trt.sh

# To Check

python3

import torch
import torchvision

git clone https://github.com/JetsonHacksNano/installSwapfile

cd installSwapfile

./installSwapfile.sh

sudo reboot

리부팅 후 jtop 으로 스왑 상태 확인해주세요.




