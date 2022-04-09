#IMPORTS 
import os as os
from time import sleep

#Welcome

def welcome():
    sleep(2)
    print("Hello there! It seems you choose my installer to have the mission to install your own custom Arch Distro!")
    input("Press enter to continue...")
    print("Lets start imediately!")
    input("Press enter to start...")
    os.system("clear")
def layout():
    sleep(2)
    print("Enter your the layout of your keyboard")
    layout_keyboard = input("Layout: ")
    os.system("loadkeys " + layout_keyboard)
    sleep(2)
    os.system("clear")
def system_clock():
    sleep(2)
    print("Activating system clock ntp...")
    os.system("timedatectl set-ntp true")
def partitioning_and_mouting():
    sleep(2)
    print("This step is very important! Be carefull!\nIf you have a Windows installed in a diferent disk and you choose the wrong one, you may lose your windows. So whe placed very secure confirmation (i think i put a more thant expected... Oh well...)")
    print("In this part will be asked the disk, put the letter, EXEMPLE: sda or sdb\nWhat it matters is the last letter that distingues to the otheres so put sdX. The x you put the disk")
    input("Press enter to choose the disk...")

    print("Choose the disk...")
    os.system("fdisk -l")
    disk_to_partition = input("Enter the disk, sdX, only the last letter required: ")
    print("Are you sure this is the disk. The disk choose is " + disk_to_partition + "?")
    confirmation = input("y or n")
    if confirmation == "y":
        pass
    else:
        partitioning_and_mouting()
    
    print("Now you need to choose the layouts or you can create your custom layout if you have more experience with partitions...")
    sleep(2)
    print("You have many layouts...")
    sleep(1)
    print("Layout UEFI with GPT: \nMount point      Partition       Partition type      Size\n/mnt/efi      /dev/sdX3       EFI system partition        512Mib\n[Swap]      /dev/sdX2       Linux Swap      4Gib\n/mnt      /dev/sdX1       Linux x86-64-root (/)       Rest of the device")
    print("Or you have the layout BIOS with MBR: \nMount point      Partition       Partition type      Size\n[Swap]        /dev/sdX2       Linux Swap      4Gib\n/mnt      /dev/sdX1       Linux       Rest of the device")
    print("Or you can create your own custom layout with cfdisk")

    layout = input("Layout 1, 2 or custom: ")
    disk = ("/dev/sd" + disk_to_partition)
    if layout == "1":
        print("building partitions...")
        os.system("parted " + disk + " -- mklabel gpt")
        os.system("parted " + disk + " -- mkpart primary 512Mib -4Gib")
        os.system("parted " + disk + " -- mkpart primary linux-swap -4Gib 100%")
        os.system("parted " + disk + " -- mkpart ESP fat32 1Mib 512Mib")
        os.system("parted " + disk + " -- set 3 esp on")
        os.system("fdisk " + disk + " -l")
        input("Press enter to format the partitions...")
        print("Formating...")

        os.system("mkfs.ext4 " + disk + "1")
        os.system("mkswap " + disk + "2")
        os.system("mkfs.fat -F 32 " + disk + "3")
        

        print("Mouting partitions...")

        os.system("mount " + disk + "1 /mnt")
        os.system("mkdir -pv /mnt/boot/efi")
        os.system("mount " + disk + "3 /mnt/boot/efi")
        os.system("swapon " + disk + "2")
        print("DONE")
        pass
    if layout == "2":
        print("building partitions...")
        os.system("parted " + disk + " -- mklabel mbr")
        os.system("parted " + disk + " -- mkpart primary 512Mib -4Gib")
        os.system("parted " + disk + " -- mkpart primary linux-swap -4Gib 100%")
        os.system("fdisk " + disk + " -l")
        input("Press enter to format the partitions...")
        print("Formating...")
        os.system("mkfs.ext4 " + disk + "1")
        os.system("mkswap " + disk + "2")
        

        print("Mouting partitions...")

        os.system("mount " + disk + "1 /mnt")
        os.system("swapon " + disk + "2")
        print("DONE")
        pass
    if layout == "custom":
        os.system("cfdisk " + disk)

        print("Because this is a custom layout you need to set the partitions...")

        root_partition = input("ROOT: " + disk + "X: ")
        swap_partition = input("SWAP: "+ disk + "X: ")
        ask_efi_partition_exists = input("Is a BIOS or EFI: y or n\nAnswer: ")
        if ask_efi_partition_exists == "y":
            efi_partition = input("EFI: " + disk + "X: ")
        if ask_efi_partition_exists == "n":
            pass

        print("Formatting...")

        if ask_efi_partition_exists == "n":
            os.system("mkfs.ext4 " + disk + root_partition)
            os.system("mkswap " + disk + swap_partition)

            print("Mouting partitions...")

            os.system("mount " + disk + root_partition + " /mnt")
            os.system("swapon " + disk + swap_partition)
            print("DONE")
            pass
        if ask_efi_partition_exists == "y":
            os.system("mkfs.ext4 " + disk + root_partition)
            os.system("mkswap " + disk + swap_partition)
            os.system("mkfs.fat -F 32 " + disk + efi_partition)

            print("Mouting partitions...")

            os.system("mount " + disk + root_partition + " /mnt")
            os.system("mkdir -pv /mnt/boot/efi")
            os.system("mount " + disk + efi_partition + " /mnt/boot/efi")
            os.system("swapon " + disk + swap_partition)
            print("DONE")
            pass


def installing_base():
    os.system("clear")
    print("Now i will begin installing the base of the system...")
    input("Press enter to start installing...")
    os.system("pacstrap /mnt base linux linux-firmware")

def fstab():
    os.system("clear")
    print("Configurating fstab")
    os.system("genfstab -U /mnt >> /mnt/etc/fstab")

def finish_and_chroot():
    print("And its done!\nNow i will chroot you in and you can start configuration your own system!\nBut if you want help you can install the command git and do\n'git clone https://github.com/Devvilas/arch-chroot-py.git'")
    input("Press enter to chroot...")
    os.system("mv -v /root/arch-py-installer/Arch\ chroot\ py/src/main.py /mnt/root")
    os.system("arch-chroot /mnt")
        

def order():
    welcome()
    layout()
    system_clock()
    partitioning_and_mouting()
    installing_base()
    fstab()
    finish_and_chroot()

order()