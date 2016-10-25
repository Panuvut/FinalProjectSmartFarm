from manageconfigurationfile import *

import urllib2

# str to dict 
import ast

class Update(object):
    def __init__(self):
        # self.standard_input = self.get_standard_input()
        self.standard_input = None





    def get_standard_input(self):
        try:
            response = urllib2.urlopen('http://127.0.0.1:8080/get_update_standard')
            _json = ast.literal_eval(response.read())
        except urllib2.URLError, err:
            # print type(err)
            # print err.reason
            # print str(err.reason)[1:12]
            if str(err.reason)[1:12] == 'Errno 10061':
                print 'No connection could be made because the target machine actively refused it'
            _json = None
        return _json



    def read_general_input(self, general_input, header):
        print header
        print general_input
        for group in general_input:
            for key in group.keys():
                # print  'key =',key
                pass
            for value in group.values():
                # print 'value =',value
                pass
            print 'key = {} value = {}'.format(key, value)
            Configurationfile().write_staticconfig(header, key, value)

    def update_general(self, standard_input):
        self.read_general_input(standard_input, 'General')

    def update_ph(self, standard_input):
        self.read_general_input(standard_input, 'PH')

    def update_temperature(self, standard_input):
        self.read_general_input(standard_input, 'Temperature')

    def update_moisture(self, standard_input):
        self.read_general_input(standard_input, 'Moisture')

    def update_eu_daily(self, standard_input):
        print 'EU_Daily'
        print standard_input
        for group in standard_input:
            for ec in group.keys():
                # print 'EC =', ec
                pass
            for date in group.values():
                for start_date in date.keys():
                    # print 'Start date', start_date
                    pass
                for end_date in date.values():
                    # print 'End date =', end_date
                    pass
            print 'EC = {} Start date = {} End date = {}'.format(ec, start_date, end_date)
            for dates in range(int(start_date),(int(end_date)+1)):
                Configurationfile().write_staticconfig('EU_Daily', 'Day_{}'.format(dates), ec)


    def update_status_connect(self, status):
        Configurationfile().write_staticconfig('Status_Connect', 'status_read_connect', status)

   

    def update(self):
        _json = self.get_standard_input()
        print _json
        if not _json:
            print 'No connection'
            status_read_connect = False
        else:
            status_read_connect = True
            self.standard_input = _json

            self.update_general(self.standard_input['General'])
            self.update_ph(self.standard_input['PH'])
            self.update_temperature(self.standard_input['Temperature'])
            self.update_moisture(self.standard_input['Moisture'])
            self.update_eu_daily(self.standard_input['EU_Daily'])

        self.update_status_connect(status_read_connect)

if __name__ == '__main__':
    u = Update()
    u.update()
