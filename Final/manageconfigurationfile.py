import os
import ConfigParser

class Configurationfile(object):
    def __init__(self):
        self.configfolder_name = 'Configurationfile'


    def read(self, configfile_name, keywords, section = None):
        configfolder_path = os.path.join(os.getcwdu(),self.configfolder_name)
        for root, dirs, files in os.walk(self.configfolder_name):
            if not configfile_name in files:
                pass
                # logging.info('Not file [{}] in folder {}'.format(configfile_name, self.configfolder_name))
            else:
                configfile_path = os.path.join(configfolder_path, configfile_name)
                config = ConfigParser.ConfigParser()
                config.read(configfile_path)
                if not section:
                    sections = config.sections()
                    for section in sections:
                        options = config.options(section)
                        for option in options:
                            if option.lower() == keywords.lower():
                                value = config.get(section, option)
                                status = True
                                return status, value
                                break
                    status, value = False, None
                    return status, value
        
                else:
                    try:
                        value = config.get(section, keywords)
                        status = True
                    except Exception, e:
                        status, value = False, None
                    return status, value

    def write(self, configfile_name, section, keywords, values):
        configfolder_path = os.path.join(os.getcwdu(),self.configfolder_name)
        for root, dirs, files in os.walk(self.configfolder_name):
            if not configfile_name in files:
                pass
                # logging.info('Not file [{}] in folder {}'.format(configfile_name, self.configfolder_name))
            else:
                configfile_path = os.path.join(configfolder_path, configfile_name)
                config = ConfigParser.RawConfigParser()
                config.read(configfile_path)
                try:
                    config.set(section, keywords, values)
                    status = True
                    value = "1 nd"
                except ConfigParser.NoSectionError:
                    try:
                        config.add_section(section)
                        config.set(section, keywords, values)
                        status = True
                        value = "2 nd"
                    except Exception, value:
                        status = False
                    
                with open(configfile_path, 'w') as configfile:
                    config.write(configfile)
            return status, value

    def read_staticconfig(self, keywords, section = None):
        return self.read('staticconfig.cfg', keywords, section)

    def write_staticconfig(self, section, keywords, values):
        return self.write('staticconfig.cfg', section ,keywords, values)
        

if __name__ == '__main__':
    config1 = Configurationfile()
    print config1.read('staticconfig.cfg', 'date_start')
    print config1.write('staticconfig.cfg', "General2",'name','Va')