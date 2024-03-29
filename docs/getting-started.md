# Getting Started

## General Cheat Sheet

Raspberry Pi **IP**: `pi@raspberrypi.local`
Raspberry Pi **Password**: `raspberry`

## Set up the project on your computer

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt` on windows and `make install` on macOS and Linux (including the raspberry pi linux)
3. Run the `main_test.py` file to run it on pc and test the software. Test options are in the works too.

## Set-Up the rasberry Pi for Windows 10

### Installing ssh

Please keep in mid that those instructions are if you have a recent version of windows 10, if you don't have anything that is more recent than a 2019 version, please update your Windows 10.

Windows does not come pre-installed with ssh, which is what we will be using to access the pi. Fortunately now with Windows 10, you can install ssh quite easily.

Open a new PowerShell windows as an administrator (right-click the powershell icon and select "Run as an administrator")

Copy and paste the command
```powershell
Add-WindowsCapability -Online -Name OpenSSH.Client*
```

Congrats you now have ssh!

### Sharing your internet connection the Pi

If your raspberry Pi does not have a wifi card and you are connecting to it over USB, you can share your computer's internet connection with it.


1. Plug in your raspberry pi, ensure that the green LED is on and wait for like a minute.
2. Open the *Control Panel*.
3. Go to *Network and Internet*.
4. Go to *Network Sharing Center*. The network underlined in red is your **internet network**, the network underlined in orange will be your **raspberry pi network**.
   ![image](res/getting-started-1.jpg)
5. Click on your **internet network**, then click on *Properties* (requires admin permissions), then go to the *Sharing* tabs.
6. Enable "Allow other network users to connect through this computer's Internet connection" adn in the dropdown menu select the network that corresponds to your **raspberry pi network**. 
   ![image](res/getting-started-2.jpg)

You should be good to go now, give the pi a minute to connect.

## Connecting to the Pi (macOS and Windows 10)

0. Make sure to connect your pi is connected and the green LED is on.
1. Open a PowerShell window and type in:
    ```powershell
    ssh pi@raspberrypi.local
    ```
2. The password you will have to enter will be queenseng
3. Test the internet connection by typing `ping google.com`, if you get no error you are good to go!

## Copying the code

There are many ways to copy the code but here are two examples:
- Download [WinSCP](https://winscp.net/eng/download.php) connect to the Pi and copy paste it
- clone the repository on the Pi Using git
