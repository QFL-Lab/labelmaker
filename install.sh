#!/bin/bash
echo "Installing drivers..."
sudo apt install ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

echo "Installing Pyhton 3 and virtualenv..."
sudo apt install python3-venv

echo "Creating virtual environment..."
python3 -m venv .venv-labelmaker
source .venv-labelmaker/bin/activate
pip install -r req.txt

echo "Creating udev rules..."
echo 'ACTION=="add",'\
         'SUBSYSTEMS=="usb",'\
         'ATTRS{idVendor}=="0922",'\
         'ATTRS{idProduct}=="1002",'\
         'MODE="0666"' \
      | sudo tee /etc/udev/rules.d/91-labelle-0922-1002.rules
sudo udevadm control --reload-rules
sudo udevadm trigger --attr-match=idVendor="0922"

echo "Creating and starting systemd service..."
mkdir -p ~/.config/systemd/user
# Define the new ExecStart path
NEW_EXECSTART=$(find "$PWD" -name start.sh)

# Write the service file with the new ExecStart line
cat > ~/.config/systemd/user/labelmaker.service << EOF
[Unit]
Description=labelmaker
After=network.target

[Service]
Type=simple
ExecStart=$NEW_EXECSTART

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload 
systemctl --user enable labelmaker.service
systemctl --user start labelmaker.service

echo "Finished installation. Rebooting in 5s..."
duration=$(( SECONDS - 5 ))
sudo reboot