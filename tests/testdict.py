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
f = open("meshinfomation1.txt", "w")
f.write(str(meshinfo))
f.write(str(netinfo))
f.close()

with open('../benchMarkTests/moe2016/cageDict', 'r') as f:
    content = f.read()
    reread = eval(content)
print(reread['Environment']['fluidDensity'])
with open('meshinfomation.txt', 'r') as f:
    content = f.read()
    mesh = eval(content)
