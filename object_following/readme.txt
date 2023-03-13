# install jetson-inference libraris

# clone the repo and submodules

cd

git clone https://github.com/dusty-nv/jetson-inference

cd jetson-inference

git checkout 19ed62150b3e9499bad2ed6be1960dd38002bb7d

git submodule update --init

# build from source
mkdir build
cd build
cmake ../
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

139, 140, 141 line comments

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


