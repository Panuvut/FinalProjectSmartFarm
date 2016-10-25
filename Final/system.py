import datetime
import time
from datetime import date
from manageconfigurationfile import *
from updateconfigurationfile import *

class System(object):
    def __init__(self):

        self.updateconfig()

        self.current_day = self.get_day()
        self.current_date = self.get_date()

        self.standard_high_temperature = None
        self.standard_low_temperature = None
        self.standard_high_moisture = None
        self.standard_low_moisture = None
        self.standard_high_ph = None
        self.standard_low_ph = None
        self.standard_ec = None


        self.current_temperature = self.get_temperature()
        self.current_moisture = self.get_moisture()
        # Potential of Hydrogen ion
        self.current_ph = self.get_ph()
        # Electric Conductivity
        self.current_ec = self.get_ec()
        
        
    # ******************** manage configuration file ****************** 

    # ***** < write file.cfg > *****

    def update_writeconfig(self):
        Update().update()

    # ***** > write file.cfg < *****


    # ***** < read file.cfg > *****

    def readconfig(self, keywords, section):
        status, value = Configurationfile().read_staticconfig(keywords, section)
        if not status:
            print "Error : read Configurationfile [keywords {}, section {}]".format(keywords, section)
        else:
            return value
    
    def update_readconfig(self):
        self.standard_high_temperature = self.readconfig('high','Temperature')
        self.standard_low_temperature = self.readconfig('low','Temperature')
        self.standard_high_moisture = self.readconfig('high', 'Moisture')
        self.standard_low_moisture = self.readconfig('low', 'Moisture')
        self.standard_high_ph = self.readconfig('high','PH')
        self.standard_low_ph = self.readconfig('low','PH')
        self.standard_ec = self.readconfig('Day_{}'.format(self.current_day),'EU_Daily')
    
    # ***** > read file.cfg < *****




    # ***** Init Get *****
    # Number of day
    def get_day(self):
        status, value = Configurationfile().read_staticconfig('start_date', 'General')
        if status:
            start_dates = value.split('-')
        now_date = datetime.datetime.date(datetime.datetime.now())
        start_date = date(int(start_dates[0]),int(start_dates[1]),int(start_dates[2]))
        days = now_date - start_date
        return days.days

    def get_date(self):
        return datetime.datetime.date(datetime.datetime.now())

    # ***** Init Set *****
    # def set_startdate(self):
    #    return datetime.datetime.date(datetime.datetime.now())



    # ***** Get *****
    def get_temperature(self):
        temperature = 24.0
        return temperature

    def get_moisture(self):
        moisture = 5.0
        return moisture

    def get_ph(self):
        ph = 6.0
        return ph

    def get_ec(self):
        ec = 0.5
        return ec

   

    # ***** Set *****
    #  on/off fan and motor
    def set_poweron(self):
        pass

    def set_poweroff(self):
        pass
        

    # def admix_solution_A(self):
    #     pass

    # def admix_solution_B(self):
    #     pass

    # def admix_solution_water(self):
    #     pass





    # ****** process *****
    def process_temperature(self, current_temperature, standard_high_temperature, standard_low_temperature):
        if float(current_temperature) > float(standard_high_temperature):
            print 'Over high temperature'
        elif float(current_temperature) < float(standard_low_temperature):
            print 'Over low temperature'
        else:
            print 'temperature correct'

    def process_moisture(self, current_moisture, standard_high_moisture, standard_low_moisture):
        if float(current_moisture) > float(standard_high_moisture):
            print 'Over high moisture'
        elif float(current_moisture) < float(standard_low_moisture):
            print 'Over low moisture'
        else:
            print 'moisture correct'

    def process_ph(self, current_ph, standard_high_ph, standard_low_ph):
        if float(current_ph) > float(standard_high_ph):
            print 'Over high ph'
        elif float(current_ph) < float(standard_low_ph):
            print 'Over low ph'
        else:
            print 'ph correct'

    def process_ec(self, current_ec, standard_ec):
        standard_high_ec = float(standard_ec) + 0.2
        standard_low_ec = float(standard_ec) - 0.2
        if float(current_ec) > float(standard_high_ec):
            print 'Over high ec'
        elif float(current_ec) < float(standard_low_ec):
            print 'Over low ec'
        else:
            print 'ec correct'



    def runsystem(self):
        while True:
            self.update_writeconfig()
            self.update_readconfig()
            self.process_temperature(self.current_temperature, self.standard_high_temperature, self.standard_low_temperature)
            self.process_moisture(self.current_moisture, self.standard_high_moisture, self.standard_low_moisture)
            self.process_ph(self.current_ph, self.standard_high_ph, self.standard_low_ph)
            self.process_ec(self.current_ec, self.standard_ec)

            time.sleep(10)

if __name__ == '__main__':
    system = System()

    print system.current_day
    print system.standard_high_temperature
    print system.standard_low_temperature
    print system.standard_high_moisture
    print system.standard_low_moisture
    print system.standard_high_ph
    print system.standard_low_ph
    print system.standard_ec 
    system.runsystem()