# install jetson-inference libraris

# clone the repo and submodules

cd

git clone https://github.com/dusty-nv/jetson-inference

cd jetson-inference

# In Case Of Jetpack 4.5.1 
git checkout 19ed62150b3e9499bad2ed6be1960dd38002bb7d 

# In Case Of Jetpack 4.6.1 
git checkout 01a395892ecc8acdbec4d8e9d6e8ac676416a507   --
git checkout 0f1f328f0d4c24dfb4074a1d0d8e06a3d6c60ee4

git submodule update --init

# build from source
mkdir build
cd build

# In Case Of Jetpack 4.5.1 
cmake ../

# In Case Of Jetpack 4.6.1 
cmake -DENABLE_NVMM=OFF ../

make

# install libraries
sudo make install
sudo ldconfig

* keep build terminal !! (Don't close!!)

# test at new test terminal !!

detectnet csi://0

=====================

# modify camera at new terminal 

cd ~/jetson-inference/utils

gedit camera/gstCamera.cpp

# In Case Of Jetpack 4.5.1 
Comments 139, 140, 141 line 

# In Case Of Jetpack 4.6.1 
# Modify 141 line 
mOptions.flipMethod = videoOptions::FLIP_HORIZONTAL;

gedit camera/gstCamera.h

modify DefaultWidth (196 line) -> 224
modify Defaultheight (201 line) -> 224 

# at build terminal 

make ; sudo make install; sudo ldconfig

# at test terminal 

detectnet csi://0

=====================================

# now object following folder

cd ~/jetbot_new/object_following

# detect python example

python3 detectnet_test.py

===============
# object following

python3 following_test.py

cd  ~/pytorch-ssd

python3 following_test.py --model=onnx/ssd-mobilenet.onnx --labels=onnx/labels.txt  --input-blob=input_0 --output-cvg=scores --output-bbox=boxes


