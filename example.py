import kramer

### Default IP and port, Machine id 1 (default), Kramer Protocol 3000
kramer = kramer.Kramer_switch('192.168.1.39', 5000, 1)

### Check if switch answers
if kramer.checkConnection() == 0: print('Connection successful.')

### Switch output 1 to input 7 and print status
status = kramer.setVideoSwitchState(7, 1)
print(status)
