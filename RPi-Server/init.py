import spidev
import RPi.GPIO as GPIO
import time
import sys
from nrf_reg import *
import MySQLdb
'''
Read the data.wsn file, if the first line is R then the module will go in listening mode. Otherwise, it transmit the data
provided on line 3 to the node with the address provided in line 2.
that's all
'''
#CE Pin 15 - Used to either Trasnmitting or Listening - CE HIGH Listening\transmitting depends on SETUP_AW register
#GPIO.setwarnings(False) # Disabling the warinings. You may enable it for debugging purposes
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(15,GPIO.OUT)
#GPIO.output(15,0)

#Inititalizing SPI | Close the SPI object : spi.close()
#spi = spidev.SpiDev()
#spi.open(0,0)
#
sys.tracebacklimit = 0


class nrf24:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        # Do not forget to GPIO.cleanup() after your program ends ! it will put all ports used in this program in input mode
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(CE,GPIO.OUT) # set CE Pin as output
        GPIO.output(CE,0) #Used for debugging ->
        self.db = MySQLdb.connect(host="localhost", user="root", passwd="raspberry",db="IUTMESH")
        self.cur = self.db.cursor()

    def spi_send(self,data):
        time.sleep(SMALL_PAUSE)
        databack = self.spi.xfer2(data)
        return databack

    def print_reg(self,Register,length,Name):
        print('\033[31m'),
        # Desc : Prints the value of length \, length stored in register Register
        # Usage : msg = self.print_reg(CONFIG,1,"CONFIG")
        # Make register address ready to read -> READ|Registery
        reg_addr = [READ|Register]
        # We need to send len+1 bytes in order to read len bytes from register Register, so [reg_addr,dummy,dummy,...,dummy] len bytes of dummy
        reg_addr.extend(range(length))
        data = self.spi_send(reg_addr)
        data_hex = [hex(z)[2:] for z in data]

        while len(Name)<25: #15
            Name = Name + "."
        print("{}".format(Name)), # We add ',' at the end of print() fucntion in order to prevent a new line ;)
        for x in range(1,length+1):
            if len(data_hex[x]) == 1:
                data_hex[x] = "0" + data_hex[x]
            #print("[0x{}]".format(data_hex[x].upper()))
        print("["),
        for i in range(1,length+1):
            print("0x%s")%format(data_hex[i].upper()),
        print("]")
        print('\033[0m'),
        return data_hex #NEW

        return [hex(k) for k in data] # The first byte is always STATUS, Thank you Nordic
    def read_packet(self):
        # Desc : Reading packet(s) from the nRF24L01+ module(No IRQ, Checking STATUS register). Listen for LONG_DELAY by default
        reg_addr = [WRITE|STATUS] # First we need to reset the STATUS register to be able to read the data and make the module ready
        reg_addr.append(RESET_STATUS) # append the RESET value (0x70) on the STATUS register
        self.spi_send(reg_addr)
        try:
        # Now, we must set CE pin to HIGH to start listening to the universe : ) (multiverse ? ;), after all we are not the only universe!)
            GPIO.output(CE, 1)
            time.sleep(LONG_PAUSE)
            GPIO.output(CE,0) #Stop listening :(
        except(KeyboardInterrupt, SystemExit): # ctrl+c or shutdown: we cleanup the GPIO.
            try:
                GPIO.cleanup()
                print("\n[+] Cleaning GPIO pins ..... Cleaned")
                print("\n\t.::Good Bye My Human Friend::. \n")
            except:
                pass
                print("\n\t.::Good Bye My Human Friend::. \n")
            raise

        #Now that we have listened to the world, we need to check our packet pocket, let's see what is the STATUS register have
        spiret = self.spi_send([STATUS])
        data = [hex(z)[2:] for z in spiret]
        if len(data[0])==1:
            data = "0" + data[0]
        #data = data.upper()
        #print(data)
        # Now we check the STATUS. STATUS must be 0E by default unless we received or tranmitted a packet (un)successfully
        #print(data)
        if (data != "0e"):
            self.print_reg(STATUS,1,"\nSTATUS")
            payload = self.print_reg(RD_RX_PLOAD,PAYLOAD_SIZE,"Received") #new
            self.updatedb(payload) #NEW)
            if (data=="4e"): # if we received a packet successfully
                self.print_reg(RD_RX_PLOAD,PAYLOAD_SIZE,"\nReceived\n")
        else:
            print("."),
            sys.stdout.flush()
    def send_packet(self,packet):
        # Desc: send packet : )
        # As always we must reset the status register first
        reg_addr = [WRITE|STATUS]
        reg_addr.append(RESET_STATUS)
        self.spi_send(reg_addr)
        # There are two registers that by reading them we flush them as well.
        # Flush RX Buffer
        self.spi_send([FLUSH_TX])
        self.print_reg(STATUS,1,"STATUS Before Trasn.")
        print("Transmitting |(-- \"0x%02x\" \"0x%02x\" \"0x%02x\" \"0x%02x\" \"0x%02x\" \"0x%02x\"") % (packet[0],packet[1],packet[2],packet[3],packet[4],packet[5])
        self.print_reg(TX_ADDR,ADDR_LEN,"To.................")
        # Write data on tx Buffer -> WR_TX_PLOAD this is as the same as tx buffer and is located on top of the memory so we send it as it is
        # No WRITE|WR_TX_PLOAD
        data = [WR_TX_PLOAD]
        data.extend(packet)
        self.spi_send(data)
        try:
            GPIO.output(CE,1)
            time.sleep(0.001) # or 0.5 second
            GPIO.output(CE,0)
        except(KeyboardInterrupt, SystemExit): # ctrl+c or shutdown: we cleanup the GPIO.
            try:
                GPIO.cleanup()
                print("[+] Cleaning GPIO pins ..... Cleaned")
                print("\n\t.::Good Bye My Human Friend::. \n")
            except:
                pass
                print("\n\t.::Good Bye My Human Friend::. \n")
            raise
        self.print_reg(STATUS,1,"STATUS After:")
    def changeAddress(self,Addr,TXRX):
        if(TXRX==TX):
            data=[WRITE|TX_ADDR]
            data.extend(Addr)
            self.spi_send(data)
        if(TXRX==RX): #I do not like to use "else" statements :)
            data=[WRITE|RX_ADDR_P0]
            data.extend(Addr)
            self.spi_send(data)
    def setupRadio(self,TXRX):
        #Setup EN_AA
        data = [WRITE|EN_AA]
        data.append(SET_ACK)
        self.spi_send(data)
        #Setup ACK RETRIES
        data = [WRITE|SETUP_RETR]
        data.append(SET_ACK_RETR)
        self.spi_send(data)
        #Setup Datapipe
        data = [WRITE|EN_RXADDR]
        data.append(SET_DATAPIPE)
        self.spi_send(data)
        #Setup Address width
        data = [WRITE|SETUP_AW]
        data.append(SET_ADR_WIDTH)
        self.spi_send(data)
        #Setup Datapipe
        data = [WRITE|RF_CH]
        data.append(SET_FREQ)
        self.spi_send(data)
        #Setup Data speed and power
        data = [WRITE|RF_SETUP]
        data.append(SET_SETUP)
        self.spi_send(data)
        #Setup Receive Address
        data = [WRITE|RX_ADDR_P0]
        data.extend(SET_RX_ADDR_P0) # Be carefull with python, you must extend not append this one and the next one
        self.spi_send(data)
        #Setup Transmitter Address
        data = [WRITE|TX_ADDR]
        data.extend(SET_TX_ADDR)
        self.spi_send(data)
        #Setup Payload size
        data = [WRITE|RX_PW_P0]
        data.append(SET_PAYLOAD_S)
        self.spi_send(data)
        #Setup Transmitter Address
        if(TXRX == TX):
            SET_CONFIG = 0x1E
        if(TXRX == RX):
            SET_CONFIG = 0x1F
        data = [WRITE|CONFIG]
        data.append(SET_CONFIG)
        self.spi_send(data)
        time.sleep(LONG_PAUSE)
        print("----------REGISTERS----------")
        self.print_reg(STATUS,1,"STATUS")
        self.print_reg(EN_AA,1,"EN_AA")
        self.print_reg(SETUP_RETR,1,"SETUP_RETR")
        self.print_reg(EN_RXADDR,1,"EN_RXADDR")
        self.print_reg(SETUP_AW,1,"SETUP_AW")
        self.print_reg(RF_CH,1,"RF_CH")
        self.print_reg(RF_SETUP,1,"RF_SETUP")
        self.print_reg(RX_ADDR_P0,ADDR_LEN,"RX_ADDR_P0")
        self.print_reg(TX_ADDR,ADDR_LEN,"TX_ADDR")
        self.print_reg(RX_PW_P0,1,"RX_PW_P0")
        self.print_reg(CONFIG,1,"CONFIG")
        print("------------------------------")
    def updatedb(self,payload):
        #print(payload)
        MODE = payload[1] #01
        NODE_ADDRESS = payload[2] + payload[3] + payload[4] #010201
        NODE_DATA = payload[5] + payload[6] #8007
        #Debugging -> print("UPDATE nodes SET id=0x" + MODE + ",data=0x" + NODE_DATA + ",lastcheck=NOW() WHERE address=0x"+NODE_ADDRESS)
        self.cur.execute("UPDATE nodes SET lastcheck=NOW(), mode="+str("\""+"0x"+MODE+"\"")+",data="+str("\""+"0x"+NODE_DATA+"\"")+"WHERE address="+str("\""+"0x"+NODE_ADDRESS+"\""))
        #self.cur.execute("UPDATE nodes SET mode = \"0x5\"")
        #self.cur.execute("select * from nodes")
        #self.cur.fetchall()
        self.db.commit()
        #self.db.close()

nrf = nrf24()
#'''
nrf.setupRadio(RX)
while 1:
    f = open('data.wsn','rw')
    gui_data = f.readlines()
    gui_data2 = [gui_data[z].split() for z in range(0,len(gui_data))] #removing \n
    f.close()
    if(gui_data2[0][0] == 'R'):
        nrf.read_packet()
        time.sleep(SMALL_PAUSE)
    if(gui_data2[0][0] == 'T'):
        nrf.setupRadio(TX)
        txaddr = map(ord,gui_data2[1][0][2:].decode("hex")) #\x01\x02\x03, please note that decode() can not process 0x -> begin from [2:]
        #txaddr = [hex(txaddr[z]) for z in range(0,len(txaddr))] #In the hex form :D [0xbb, 0x...]
        GUI_PAYLOAD = map(ord,gui_data2[2][0][2:].decode("hex"))
        nrf.changeAddress(txaddr,TX)
        nrf.send_packet(GUI_PAYLOAD)
        time.sleep(SMALL_PAUSE)
        f = open('data.wsn','w')
        f.write(str('R'))
        f.close()
        nrf.setupRadio(RX)
'''
nrf.setupRadio(TX)
nrf.send_packet([0x01,0x01,0x02,0x01,0x66,0x66])
'''
#msg = nrf.spi_send()
#msg= nrf.print_reg(CONFIG,1,"CONFIG")
#msg = nrf.print_reg(STATUS,1,"STATUS")
#print(msg)
