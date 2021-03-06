#IMPORTS
import os as os
from time import sleep as sleep

def welcome():
    print("Welcome to the chroot help installer\nWe presume that you have arch linux already installed...")
    input("Press enter to continue...")
    print("Lets start!")
    
def Time_zone():
    region_and_city = input("What is your Region/city? Put write like this, exemple: Europe/Lisbon\nRegion/city: ")
    os.system("ln -sf /usr/share/zoneinfo/" + region_and_city + " /etc/localtime")

    os.system("hwclock --systohc")

def localization():
    print("First and first we need to install the editor nano")
    os.system("pacman -S nano")
    print("Remove the # of your location and press Ctrl + X and enter")
    input("Press enter to continue...")
    os.system("nano /etc/locale.gen")
    print("Installing language...")
    os.system("locale-gen")

    lang_var = input("One question...\nWrite the line that you remove the #\nLine: ")
    os.system("touch /etc/locale.conf")
    os.system("echo LANG=" + lang_var + " > /etc/locale.conf")
    

    print("Now write the layout of the keyboard again to make it persistent...")
    layout = input("Layout: ")
    os.system("touch /etc/vconsole.conf")
    os.system("echo KEYMAP=" + layout + " > /etc/vconsole.conf")


def network_config():
    hostname = input("Enter the hostname: ")
    os.system("touch /etc/hostname")
    os.system("echo " + hostname + " > /etc/hostname")


def set_pass_root():
    print("Lets set the root password!")
    os.system("passwd")

def bootloader():
    efi_bios = input("Is your system efi-gpt or bios-mbr\nbios or efi: ")
    if efi_bios == "bios":
        os.system("pacman -S grub ntfs-3g")
        os.system("fdisk -l")
        disk_partition = input("enter the last latter of the disk that you have installed arch: ")
        disk = ("dev/sd" + disk_partition)
        os.system("grub-install --target=i386-pc " + disk)
        pass
    if efi_bios == "efi":
        os.system("pacman -S grub efibootmgr ntfs-3g")
        os.system("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=GRUB")
        pass
    print("Now, this is the final step of the installation of bootloader...\nBut this step needs to be you...\nThe system will open the editor nano and you need to remove # of the final line of the file that is '#GRUB_DISABLE_OS_PROBER=false', remove the #, needs to be like this 'GRUB_DISABLE_OS_PROBER=false'\nThen press Ctrl+X and press enter")
    input("Press enter to continue...")
    os.system("nano /etc/default/grub")
    os.system("grub-mkconfig -o /boot/grub/grub.cfg")


def users():
    print("Lets create a user!")
    name = input("Name: ")
    os.system("useradd -m -g users -G wheel " + name)
    print("Insert the password")
    os.system("passwd " + name)
def additional_packages():
    os.system("pacman -S dosfstools os-prober mtools network-manager-applet networkmanager wpa_supplicant wireless_tools dialog sudo nano xorg xorg-server")
    os.system("systemctl enable NetworkManager")
    os.system("pacman -S firefox neofetch")
    os.system("echo neofetch >> /etc/bash.bashrc")

def interface():
    os.system("clear")
    choose = input("\n1. None: Does nothing\n2. i3-gaps\n3. KDE\n4. Gnome\n5. xfce4\nOption: ")
    if choose == "1":
        print("Please run now reboot")
        os.system("exit")
    if choose == "2":
        os.system("pacman -S i3-gaps i3-status dmenu lightdm lightdm-gtk-greeter")
        os.system("systemctl enable lightdm")
        print("Please run now reboot")
        os.system("exit")
    if choose == "3":
        os.system("pacman -S plasma")
        os.system("systemctl enable sddm")
        print("Please run now reboot")
        os.system("exit")
    if choose == "4":
        os.system("pacman -S gnome gnome-extra")
        os.system("systemctl enable gdm")
        print("Please run now reboot")
        os.system("exit")
    if choose == "5":
        os.system("pacman -S xfce4 xfce4-goodies lightdm lightdm-gtk-greeter")
        os.system("systemctl enable lightdm")
        print("Please run now reboot")
        os.system("exit")
def order():
    welcome()
    Time_zone()
    localization()
    network_config()
    set_pass_root()
    bootloader()
    users()
    additional_packages()
    interface()

order()