import sys
import threading

from time import sleep
from os import path, system

PIN = "" # Set default PIN


class Loading(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)

        self.name = name
        self.running = True
        self.loading = "/-\|"

    def stop(self):
        self.running = False

    def run(self):
        while True:
            for i in self.loading:
                sys.stdout.write("\rInstalling: %s %s " % (self.name, i))
                sys.stdout.flush()
                sleep(0.1)

            if not self.running:
                print("\rInstalling: %s complete" % (self.name))
                break


class RDP:
    def __init__(self, code):
        self.code = code
        self.install_crd()
        self.install_desktop_environment()
        self.install_firefox()
        self.finish(self.code)
        print("\nRDP created succesfully move to https://remotedesktop.google.com/access")

    @staticmethod
    def install_crd():
        l = Loading("Chrome Remote Desktop")
        l.start()

        if not path.exists("chrome-remote-desktop_current_amd64.deb"):
            system("wget https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb &> /dev/null")

        system("sudo dpkg --install chrome-remote-desktop_current_amd64.deb &> /dev/null")
        system("sudo apt install --assume-yes --fix-broken &> /dev/null")

        l.stop()

    @staticmethod
    def install_desktop_environment():
        l = Loading("Desktop Environment")
        l.start()

        system("export DEBIAN_FRONTEND=noninteractive")
        system("sudo apt install -y mate-desktop-environment &> /dev/null")
        system("sudo bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/mate-session\" > /etc/chrome-remote-desktop-session'")
        system("sudo apt remove --assume-yes gnome-terminal &> /dev/null")
        system("sudo apt install --assume-yes xscreensaver &> /dev/null")
        system("systemctl disable lightdm.service &> /dev/null")

        l.stop()

    @staticmethod
    def install_firefox():
        l = Loading("Firefox")
        l.start()

        system("sudo apt install -y firefox-esr &> /dev/null")

        l.stop()

    @staticmethod
    def finish(crp):
        system("%s &> /dev/null" % (crp))
        system("service chrome-remote-desktop start &> /dev/null")


if __name__ == "__main__":
    system("clear")
    print("      _           _          _")
    print("  ___| |___ _ _ _| |   ___ _| |___")
    print(" |  _| | . | | | . |  |  _| . | . |")
    print(" |___|_|___|___|___|  |_| |___|  _|")
    print("                              |_|\n")

    print(" Visit http://remotedesktop.google.com/headless and copy the command after Authentication\n")
    CRP = input(" CRP: ")

    print("\n Enter a Pin (more or equal to 6 digits)")
    if PIN:
        print(" PIN: %s" % (PIN))
    elif not PIN:
        PIN = input(" PIN: ")

    CRP = CRP.replace("$(hostname)", '"RDP"')
    CRP = ("%s --pin=%s") % (CRP, PIN)

    print("")
    RDP(CRP)
