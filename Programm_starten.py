import bluetooth
import math
import json
import os
from datetime import datetime

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

server_sock.bind(("", bluetooth.PORT_ANY ))
port = server_sock.getsockname()[1]
server_sock.listen(1)
print("Suche nach Geraeten auf Port %d ..." % port)

uuid = "2f3b0104-fcb0-4bcf-8dda-6b06390c3c1a"
bluetooth.advertise_service( server_sock, "FooBar Service", uuid )

client_sock,address = server_sock.accept()
print("Verbindung akzeptiert von: ", address)

try:
    while True:
        data_raw = client_sock.recv(1024)
        # print "Daten bekommen: [%s]" % data_raw

        data_string = str(data_raw)
        data = data_string.replace("\n", "").replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace('"test_text":', '').lstrip(' ')
        
        dateiname = str('Daten/' + str(datetime.now().strftime('%d-%m-%Y_%H:%M:%S')) + '.txt')
        f = open(dateiname, 'w')
        f.write(data)
        f.close()
        print(dateiname + ' mit den abgefangenen Daten wurde erstellt!')

        if data == 'shutdown':
            os.system('sudo shutdown now')
        if data == 'reboot':
            os.system('sudo shutdown -r now')

except IOError:
    pass
input('\n\n\nKlicker <Enter> zum beenden!')
client_sock.close()
server_sock.close()
