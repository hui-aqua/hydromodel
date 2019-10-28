import os

os.system("clear")
modellist = [
    "fishcagewithbottom",
    "fishcagewithoutbottom",
    "trawlnet",
    "fishcagewithmooringsystem"]  # add more models if it is ready


def printmodel():
    print("Currently, the available numerical models are:")
    for model in modellist:
        print(str(modellist.index(model)) + " " + model)


appath = input(
    "The default path for salome2019 is: \t/opt/salome2019/appli_V2019_univ/salome \n"
    "If your salome is located in this path, you can press '1' and enter \n\n"
    "The default path for salome2018 is: \t/opt/salome2018/appli_V2018.0.1_public/salome \n"
    "If your salome is located in this path, you can press '2' and enter \n\n"
    "Please input you path to salome in your computer \n")
if appath == str(1):
    appath = "/opt/salome2019/appli_V2019_univ/salome"
if appath == str(2):
    appath = "/opt/salome2018/appli_V2018.0.1_public/salome"
while not os.path.isfile(appath):
    appath = input("Sorry, I cannot find salome in your given path, please input it again \n")
    if appath == str(1):
        appath = "/opt/salome2019/appli_V2019_univ/salome"
    if appath == str(2):
        appath = "/opt/salome2018/appli_V2018.0.1_public/salome"
os.system("clear")
print("This program is not ready to release for commercial usages.\n"
      "Any questions about this program, please email: hui.cheng@uis.no\n")
printmodel()
modelkey = input("\nPress the index number to choose the model or 'CTRL+C' to exit: ")
while not int(modelkey) in range(len(modellist)):
    modelkey = input("\nPlease choose the model in the above list: ")

os.system("clear")
modelbank = "/home/hui/GitCode/aqua/hydromodel/Meshcreater/"
os.system(appath + " -t " + modelbank + modellist[int(modelkey)] + ".py")
