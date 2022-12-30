RaspiImager
hostname: weatherpi
user: weather
pw: ...
WIFI: your wifi credentials


sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip fail2ban ntpdate git

pip3 install -r requirements.txt
