import os

def find_serialport():
    read = os.popen('python3 -m serial.tools.list_ports').read()
    serialport_list = read.split()
    i=0
    for str in serialport_list:    
        print(f'{i}:{str}')
        i+=1
    if(serialport_list.count == 0):
        return 0
    else:        
        return serialport_list
        
if __name__ == '__main__':
    find_serialport()
        