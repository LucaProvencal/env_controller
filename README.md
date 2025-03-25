Overview

Use this script to maintain optimal growing conditions for common gourmet mushroom species in a grow tent or room. It will broadcast environmental conditions to three virtual pins in Blynk 
IoT for easy real-time monitoring. 

Hardware setup instructions:
- Connect humidifier relay signal pin to `HUMIDIFIER_PIN` GPIO pin. Connect relay pins to 5V power and ground.
- Connect fan relay signal pin to `FAN_PIN` GPIO pin. Connect relay pins to 5V power and ground.
- Connect SCD41 pins to SCL, SDA, 5V power and ground.

Software Setup:
- SSH into the RPi and clone the repo.
- Run `./setup.sh`. This should set the RPi up with Python libraries and enable I2C. 
- Create a Blynk account, project, and obtain BLYNK_AUTH_TOKEN. Blynk will be used to broadcast temperature, humidity and CO2 concentration data. You can create very nice charts accessible from anywhere at any time, as long as both your iOS device and the RPi are connected to the internet.
<img src="https://github.com/user-attachments/assets/892b4a76-d861-47da-8bcf-114ac245148c" width=25% height=25%>


Summary
- Use `HUMIDITY_HIGH` and `HUMIDITY_LOW` to fine tune the desired humidity range per mushroom species.
- Use `FAN_INTERVAL` and `FAN_RUN_DURATION` to fine tune fan operation based on fresh air exchange needs.
- Run the script with access to `BLYNK_AUTH_TOKEN` in order to broadcast all data to Blynk.
  - Blynk interval can be increased for Pro version, but 2 minutes is within the range of the message limits for free tier.

TODO:
- Sometimes Blynk API goes down and the script will exit. Build error handling for this scenario. For now, it's easy to tell when this happens and I'll just restart the script.

Results:

![IMG_5150](https://github.com/user-attachments/assets/43c72a56-43e0-440a-94a7-039b4a80002e)
