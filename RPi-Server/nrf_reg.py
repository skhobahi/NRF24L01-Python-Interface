
CE = 15
TX = 0
RX = 1
PAYLOAD_SIZE   = 6
ADDR_LEN = 3
SMALL_PAUSE = 0.05
LONG_PAUSE=0.5

#Define settings variables for nRF:
SET_ACK        = 0x00  #Auto ack on (EN_AA) 0x01
SET_ACK_RETR   = 0x00  #15 retries, 750us paus in between in auto ack (SETUP_RETR) 0x2F
SET_DATAPIPE   = 0x01  #Datapipe 0 is used (EN_RXADDR)
SET_ADR_WIDTH  = 0x01  #5 byte address (SETUP_AW)
SET_RX_ADDR_P0 = [0x01,0x02,0x01] #Receiver address( RX_ADDR_P0)
SET_TX_ADDR    = [0x01,0x02,0x01] #Transmitter address (TX_ADDR)
SET_PAYLOAD_S  = 0x06  #3byte payload size (32byte = 0x20)(RX_PW_P0)
SET_CONFIG     = 0x1E  #1=mask_MAX_RT (IRQ-vector), E=transmitter, F= Receiver (CONFIG)

SET_FREQ       = 0x01  #2,401GHz (RF_CH)
SET_SETUP      = 0x07  #1Mbps, -0dB, (250kbps = 0x27) (RF_SETUP)
ADDRESS        = 0x12
# Registers
CONFIG      = 0x00
EN_AA       = 0x01
EN_RXADDR   = 0x02
SETUP_AW    = 0x03
SETUP_RETR  = 0x04
RF_CH       = 0x05
RF_SETUP    = 0x06
STATUS      = 0x07
OBSERVE_TX  = 0x08
CD          = 0x09
RX_ADDR_P0  = 0x0A
RX_ADDR_P1  = 0x0B
RX_ADDR_P2  = 0x0C
RX_ADDR_P3  = 0x0D
RX_ADDR_P4  = 0x0E
RX_ADDR_P5  = 0x0F
TX_ADDR     = 0x10
RX_PW_P0    = 0x11
RX_PW_P1    = 0x12
RX_PW_P2    = 0x13
RX_PW_P3    = 0x14
RX_PW_P4    = 0x15
RX_PW_P5    = 0x16
FIFO_STATUS = 0x17

READ    = 0x00
WRITE    = 0x20
RESET_STATUS = 0x70

WR_TX_PLOAD = 0xA0
RD_RX_PLOAD = 0x61

FLUSH_TX    = 0xE1
FLUSH_RX    = 0xE2
NOP         = 0xFF
