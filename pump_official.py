from datetime import datetime
import logging
import serial
import numpy as np
from time import sleep
icc_logger = logging.getLogger("ismatecICC")
import multiprocessing

REGLO_ICC = {
    'communication' :       '%s~\r',     # [pump Addr]~[CR]                                   #
    'start':                '%sH\r',     # [Pump Addr]H[CR]                                   #   
    'stop':                 '%sI\r',     # [Pump Addr]I[CR]#
    'start_chan':           '%sH%s\r',   # [Channel]H[Pump Addr][CR] #
    'stop_chan':            '%sI%s\r',   # [Channel]I[Pump Addr][CR]   #
    'get_run_state':        '%sE\r',     # [Pump Addr]E[CR]   
    'chan_mode':            '%s~%s\r',   # Address individual channels 1, or pump 0         #+
    'set_RPM'   :           '%sL\r',     # Set pump speed in RPM mode 
    'set_mLmin' :           '%sM\r',     # Set pump speed in mL/min mode 
    'set_flow':             '%sf%s\r',   # [Channel]f[Pump Addr][CR] #
    'get_flow':             '%sf\r',     # [Channel]f[CR]
    'set_clockwise':        '%sJ\r',     # [Pump Addr]J[CR]
    'set_counterclockwise': '%sK\r',     # [Pump Addr]K[CR]
    'get_chan_run_state':   '%sE%s\r',   # [Channel]E[Pump Addr][CR]
    'get_direction':        '%sxD\r',    # [Pump Addr]xD[CR]
    'get_chan_dir':         '%sxD%s\r',  # [Channel]xD[Pump Addr][CR]
    'set_chan_flow':        '%sf%s\r',   # [Channel]f[Flow-Rate][CR]
    'get_chan_flow':        '%sf\r',     # [Channel]f[CR]
    'set_chan_clockwise':   '%sJ%s\r',   # [Channel]J[Pump Addr][CR]
    'set_chan_cntr_clkws':  '%sK%s\r',   # [Channel]K[Pump Addr][CR]
    'get_calmaxflow':       '%s?\r',     # [Channel]
    'set_disp_man':         '%sA\r',    # Set control panel, manual/normal
    'set_disp_rem':         '%sB\r',    # Set control panel, remote/disabled
    'set_display_txt':      '%sDA%s\r' ,  # [Pump Addr]DA[string (<16 char)][CR]
    'set_channel_speed':    '%sS%s\r' ,  #[Channel]S[speed_rpm][CR]  #Set channel speed in RPM
    'get_RPM'  :            '%sS\r'   , #[channel]S[CR]
    'set_vol'  :            '%sv%s\r' ,   #[channel]v[CR]
    'get_vol'  :            '%sv\r' ,    #[channel]v[CR]
    'runtime_chan' :        '%sxT%s\r',
    'set_time_mode' :       '%sN\r',
    'tube_dia' :            '%s+%s\r'
}  

class RegloPump:
        #Properties of the pump
    speed = np.zeros((4,1))  #RPM for each channel
    direction = np.zeros((1,4)) # 1 = counter clockwise  0 = clockwise
    tubingdiamter = np.array([(1.02, 1.02, 1.02, 1.02)])
    ser = None

    
    def __init__(self, com_port, pump_address = None, baudrate=9600,parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0.5) :
        self.port = com_port
        self.baud_rate = baudrate
        self.parity = parity
        self.stopbits =stopbits
        self.bytesize = bytesize
        self.timeout = timeout
        self.address = pump_address
        self.ser = serial.Serial(self.port, baudrate=9600, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.5)
        
        #get number of channels
        try:
            nChannels = int(self.ser.write(b'1xA\r'))    
        except ValueError:
            nChannels = 0
            
        #list of channel indices for iteration and checking
        self.channels = list(range(1, nChannels + 1))
        
    
    def connection(self):

        print("connected to: " + self.ser.portstr)
        #ser.write("2I\r".encode('ASCII'))
        command = REGLO_ICC['communication']%self.address
        self.ser.write(command.encode("ASCII"))
        sleep(1)
        a=self.ser.readline()
        print(a)
        
        self.ser.close()
        
    def start_pump(self):
        command = REGLO_ICC['start']%self.address
        self.ser.write(command.encode("ASCII"))
        sleep(1)
        print('Pump has started')
        
        
    def stop_pump(self):
        command = REGLO_ICC['stop']%self.address
        self.ser.write(command.encode("ASCII"))
        sleep(1)
        print('Pump has stopped')
        self.ser.close()
        
    def clockwise(self):
        command = REGLO_ICC['set_clockwise']%self.address
        self.ser.write(command.encode("ASCII"))
        sleep(1)
        print('Pump has set clcokwise_direction')
        
    def counter_clockwise(self):
        command = REGLO_ICC['set_counterclockwise']%self.address
        self.ser.write(command.encode("ASCII"))
        sleep(1)
        print('Pump has set clcokwise_direction')
        
    def start_chan(self, chan:int) -> int:
        '''
        Start/run pump channel.
        
        Parameters
        ----------
        chan : int
            Pump channel number

        Returns
        -------
        int
            1 == Pass

            0 == Fail

            -1 == Other error
        '''
        icc_logger.info('%s Channel %i STARTED', self.port, chan)
        #self.set_per_chan_mode(1)
        command = REGLO_ICC['start_chan'] % (chan, self.address)
        self.ser.write(command.encode("ASCII"))
        #sleep(1)
        print('Channel', chan, 'has started')
        #rsp = self.send_cmd_pass_fail(cmd_str)
        #self.set_per_chan_mode(0)
        #return rsp
        
    def stop_chan(self, chan:int) -> int:
        '''
        Start/run pump channel.
        
        Parameters
        ----------
        chan : int
            Pump channel number

        Returns
        -------
        int
            1 == Pass

            0 == Fail

            -1 == Other error
        '''
        icc_logger.info('%s Channel %i STARTED', self.port, chan)
        #self.set_per_chan_mode(1)
        command = REGLO_ICC['stop_chan'] % (chan, self.address)
        self.ser.write(command.encode("ASCII"))
        sleep(1)
        print('Channel', chan, 'has stopped')

        
        

        
    def chan_clockwise(self, chan:int) -> int: #Set direction of the channel individually in clockwise
        command = REGLO_ICC['set_chan_clockwise'] % (chan, self.address)
        self.ser.write(command.encode("ASCII"))
        #sleep(1)
        print('Channel', chan, 'set in Clockwise direction')
    
    def chan_Counterclockwise(self, chan:int) -> int: #Set direction of the channel individually in clockwise
        command = REGLO_ICC['set_chan_cntr_clkws'] % (chan, self.address)
        self.ser.write(command.encode("ASCII"))
        #sleep(1)
        print('Channel', chan, 'set in Counter Clockwise direction')
        
    def rpm_mode(self):
        command = REGLO_ICC['set_RPM'] % (self.address)
        self.ser.write(command.encode("ASCII"))
        #sleep(1)
        print('Pump set in RPM mode succesfully')
        
    def flowrate_mode(self):
        '''
        Set pump to volumetric flowrate mode.
        
        Returns
        -------
        int
            1 == pass

            0 == fail

            -1 == error
        '''
        command = REGLO_ICC['set_mLmin'] % self.address
        self.ser.write(command.encode("ASCII"))
        #sleep(1)
        code1=self.ser.readline()
        if code1 == b'*':
            print('Pump set to flowrate mode succesfully')
        else:
            print('Error in giving commands')
            
    def runstate_chan(self, chan:int) -> int:  #Get the run ste of the channel
        command = REGLO_ICC['get_chan_run_state']%(chan, self.address)
        self.ser.write(command.encode('ASCII'))
        response = self.ser.readline()
        return response
        #sleep(1)
        #self.ser.readline()
        
    def _discrete3(self, number):
        """Convert number to 'discrete type 3'.

        6 digits, 0 to 999999, left-padded with zeroes
        """
        return str(number).zfill(6)
    

    
    
    
    
    #Set the induvidual channel speed in RPM
    def set_chan_RPM(self, chan, number :float):
        
            
        if number <= 150:
            number = str(number) 
            len_num = len(number)
            n = 2   #Add two zeroes to the number at the end
            #zfill fills the number at the left
            if len_num == 1:
                number =number.zfill(len_num+3)
                number = number + '0'*n
                #number = format(number)
                #print(number)


            elif len_num == 2:
                number = number.zfill(len_num+2)
                number = number + '0'*n
                #number = format(number)
                #print(number) 

            elif len_num == 3:
                number = number.zfill(len_num+1)
                number = number + '0'*n
                #number = format(number)
                #print(number)

            else:
                print('given number is out of pump speed limit')

            #First need to set the rpm mode of the channel
            #command = REGLO_ICC['set_RPM'] % (chan)
            self.ser.write((REGLO_ICC['set_RPM'] % (chan)).encode("ASCII"))
            command = REGLO_ICC['set_channel_speed']%(chan, number)
            print(command)
            self.ser.write(command.encode("ASCII"))
            #print('Speed of the channel',chan,'set to', number )
            response = self.ser.readline()
            return command
        
        else:
            print('RPM rate is maximum please correct it')
            
            
    def get_rpm(self, chan):
        command = REGLO_ICC['get_RPM']%(chan)
        self.ser.write(command.encode('ASCII'))
        response = self.ser.readline()
        return response

    #set the individual channel in ul/mn mode
    def set_chan_flowrate(self, chan, speed_rate:float):
        # if speed_rate>100.000:
        #     speed_rate =max(min(speed_rate, 100), 0)
        # speed_string = format(speed_rate, "09.2E") 
        # speed_string = speed_string.replace("E", '').replace('.', '')
        # speed_string = speed_string[:7]+speed_string[7:]
        self.ser.write((REGLO_ICC['set_mLmin']% (chan)).encode("ASCII"))
        command = REGLO_ICC['set_chan_flow'] % (chan, self._volume2(speed_rate))
        print(command)
        self.ser.write(command.encode("ASCII"))
        
        #command = REGLO_ICC['set_channel_speed']%(chan, number)
        #print(command)
        #self.ser.write(command.encode("ASCII"))
        
        #self.ser.write(command.encode("ASCII"))
        response =self.ser.readline()
        #print(response)
        return response
        #print(response.decode('ASCII'))
        
    #Get channel flow rate in ul/min
    def get_chan_flowrate(self, chan:int) -> int:
        command = REGLO_ICC['get_flow']%(chan)
        self.ser.write(command.encode('ASCII'))
        response = self.ser.readline()
        return response
    
    # set the volume discharge of a channel in ml 
        
    def set_volume(self, chan, volume:float):
        volume_string = format(volume, "09.2E") 
        volume_string = volume_string.replace("E", '').replace('.', '')
        volume_string = volume_string[:7]+volume_string[7:]
        command = REGLO_ICC['set_vol'] % (chan, volume_string)
        self.ser.write(command.encode("ASCII"))
        response_vol =self.ser.readline()
        return response_vol
    
    
    #Get volume
    def get_volume(self, channel):
        command = REGLO_ICC['get_vol']%(channel)
        self.ser.write(command.encode('ASCII'))
        response_gvol = self.ser.readline()
        return response_gvol
    
    def _volume1(self, number):
        # convert number to "volume type 1"
        number = '%.3e' % abs(number)
        number = number[0] + number[2:5] + 'E' + number[-3] + number[-1]
        return number.encode()
    
    def _volume2(self, number):
        # convert number to "volume type 2"
        number = '%.3e' % abs(number)
        number = number[0] + number[2:5] + number[-3] + number[-1]
        return number    
    
    def set_tubing_inner_diameter(self, diam, chan= None ):
        
        """
        Set the peristaltic tubing inner diameter on the specified channel, in mm.
        
        If no channel is specified, set it on all channels.
        
        """
        self.ser.write((b'%d+%s' %(chan, self._discrete2(diam))))
        #self.ser.write((REGLO_ICC['tube_dia']%(chan, self._discrete2(diam))).encode('ASCII'))
        
        
        response = self.ser.readline()
        return response
        
        
    
    #Set the induvidual channel speed in RPM
    def set_runtime(self, rate, time, units = 's',  chan = 0):
        
        """
        Dispense at a set flowrate over time (min) on specified channel.
        Rate is specified by units, either 'ml/min' or 'rpm'.
        If no channel is specified, dispense on all channels.
        """
        assert chan in self.channels or chan == 0
        
        #set to flowrate mode first, otherwise Time modes uses RPMs
        self.ser.write((REGLO_ICC['set_mLmin']% chan).encode("ASCII"))
        
        #set time mode of the pump
        self.ser.write((REGLO_ICC['set_time_mode']%(chan)).encode('ASCII'))
        
        #Set flow rate
        self.ser.write((REGLO_ICC['set_flow']%(chan, self.volume2(rate))).encode('ASCII'))
        
  
        #Set run time
        self.ser.write((REGLO_ICC['runtime_chan']%(chan, self.time2(time, units))).encode('ASCII'))
        #self.ser.write(b'3xT00000300\r')
            
        #Start Channel
        self.ser.write((REGLO_ICC['start']%(chan)).encode("ASCII"))
            
        #self.ser.write(b'3H\r')                 
        response = self.ser.readline()
        
        # Close the serial connection
        #self.ser.close()
        
        print(f'pump has set to {time} seconds at channel {chan}')
            
        return response
    
    def time2(self, number, units ='s'):
        """Convert number to 'time type 2'.
        8 digits, 0 to 35964000 in units of 0.1s. left padded with zeroes
        (0 to 999 hr)
        """
        
        number = 10*number #0.1s
        if units =='m':
            number = 60*number
        if units == 'h':
            number = 3600* number
        return str(min(number, 35964000)).replace('.', '').zfill(8)
    
    def volume2(self, number):
        # convert number to volume 2 according to the pump icc command protocols
        
        number = '%.3e'%abs(number)
        number = number[0] + number[2:5] +number[-3] +number[-1]
        return number
    
    def _discrete2(self, number):
        
        #convert float to "discrete type 2"
        s = str(number).strip('0')
        whole, decimals = s.split('.')
        return b'%04d'% int(whole + decimals)
    

    def set_multi_processing(self, chan_list, flow_rates_list, times_list, units):

        #create a list of processes for each channel
        processes =[]

        for mchan, mrate, mtime, munit in zip(chan_list, flow_rates_list, times_list, units):

            process = multiprocessing.Process( target = self.set_runtime, args = (mrate, mtime, munit, mchan))
            processes.append(process)
        
        #start all processes concurrently
        for process in processes:    

            process.start()

        #wait for all processes to finish
        for process in processes:
            process.join()

        return "multi processing done"
    

                


    
        
 #'set_channel_speed':     '%sS0%s\r'       
        
        
            
            
            
        
    
        
#         def set_flow_channel(self, chan:int):
        
    
pump_obj = RegloPump('COM14')

#pump_obj.set_multi_processing(chan_list = [2, 3], flow_rates_list= [25, 11], times_list = [120, 120], units = ['s', 's'])



#pump_obj.chan_clockwise(3)
#pump_obj.set_tubing_inner_diameter(2.54, chan =1)
#pump_obj.set_tubing_inner_diameter(2.54, chan =3)
#pump_obj.chan_Counterclockwise(3)
#pump_obj.start_chan(1)

#pump_obj.set_runtime(27, 30, units = 's', chan = 1)
# pump_obj.start_chan(1)
#pump_obj.stop_chan(1)

# pump_obj.set_chan_flowrate(3, 1)


# pump_obj.start_chan(3)
#pump_obj.chan_clockwise(3)
#pump_obj.start_chan(3)
# pump_obj.start_pump()

#pump_obj.stop_pump()


# pump_obj.rpm_mode()

# pump_obj.set_chan_RPM(3, 50)
# pump_obj.chan_clockwise(3)

# pump_obj.set_runtime(3,  38, units = 's')
#pump_obj.chan_clockwise(2)

# pump_obj.start_chan(3)


#pump_obj.start_chan(1)
# #pump_obj.start_pump()
#pump_obj.stop_chan(3)
#pump_obj.stop_chan(1)


# pump_obj.set_runtime(10, 120, units = 's', chan = 2)
# pump_obj.set_runtime(25, 120, units = 's', chan = 3)

# pump_obj.stop_chan(2)
# pump_obj.stop_chan(3)