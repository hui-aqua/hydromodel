meshinfo = {
    "horizontalElementLength": float(60),
    "verticalElementLength": float(15),
}
netinfo = {
    'Sn': 0.194,
    'twineDiameter': 2.42e-3,
    'meshLength': 0.0255,
    'netYoungmodule': 40000000,
    'netRho': 1140.0,
}
f = open("meshinfomation.txt", "w")
f.write(str(meshinfo))
f.write(str(netinfo))
f.close()

with open('cageDict', 'r') as f:
    content = f.read()
    reread = eval(content)
