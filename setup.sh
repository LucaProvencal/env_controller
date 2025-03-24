#!/bin/bash

echo "----------------------------------"
echo "🔧 Setting up Raspberry Pi for Env Controller"
echo "----------------------------------"

# Update system
echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo "📦 Installing necessary packages..."
sudo apt install -y python3-pip python3-smbus i2c-tools git

# Enable I2C
echo "🛠️ Enabling I2C..."
sudo raspi-config nonint do_i2c 0
echo "✅ I2C enabled."

# Install Python libraries
echo "🐍 Installing required Python libraries..."
python3 -m venv env
source env/bin/activate
pip install adafruit-blinka adafruit-circuitpython-scd4x blynklib

# Check if SCD41 is detected
echo "🔍 Checking I2C devices..."
i2cdetect -y 1

# Set permissions
chmod +x main_scd41.py

echo "Setup complete!"
