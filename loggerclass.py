import logging
from logging.handlers import RotatingFileHandler
import sys
import os
import syslog
from pprint import pprint

class logclass(logging.Logger):
    siteId = "  "
    stationId = "  "
    systype = "  "
    Subsys = "   " 
    global sevinfo
    global logfmt
    sevinfo = "   "

    def __init__(self, name="testin"):
        self.siteId = 1
        self.stationId = 2
        self.systype = 3
        self.Subsys = 4
        print("in here")

        return super(logclass, self).__init__(name)

    if systype == "system":
        Subsys = "SystemApp"
    elif systype == "portal":
        Subsys = "RestAPI"
    elif systype == "stationController":
        Subsys = "MsgBroker"
    
    def metadata(self):
        mydict = {'siteId': self.siteId, 'stationId': self.stationId, 'Subsys': self.Subsys, 'systype': self.systype, 'sevinfo': sevinfo}
        return mydict
    
    def info(self, msg, extra):
        #extra_dict = kwargs.pop('extra')
        extra_dict['sevinfo'] = "dbg"
        print("we got here boiiiii")
        pprint(extra_dict)
        super().info(msg, extra=extra_dict)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        msg, kwargs = self.process(msg, kwargs)
        self.logger.debug(msg, extra=extra)
    
    def debug(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        extra_dict['siteId'] = self.siteId
        extra_dict['stationId'] = self.stationId
        extra_dict['Subsys'] = self.Subsys
        extra_dict['systype'] = self.systype
        extra_dict['sevinfo'] = "5"
        print("we got here boiiiii")
        pprint(extra_dict)
        return super(logclass, self).debug(msg, extra=extra_dict, *args, **kwargs)

    def warn(self, msg, extra=None):
        self.logger.warn(msg, extra=extra)

    def configure_logging(self):
        self.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler('/dev/log')
        handler.setLevel(logging.DEBUG)
        self.addHandler(handler)
        FORMAT = '<local0.2> %(asctime)-15s  station.viasat.io DeviceFactory[22222]:[severity= " %(levelname)s " siteId="%(siteId)s " stationId="%(stationId)s"  Subsys="%(Subsys)s" systype="%(systype)s" sevinfo="%(sevinfo)s"] %(message)s'
        handler.setFormatter(logging.Formatter(FORMAT))
        print("end of configure_logging")
  





def main(argv):
    logging.setLoggerClass(logclass)
    #logging.basicConfig()
    logger = logging.getLogger("testin")
    logger.configure_logging()
    
    print(type(logger))
    print("here2")
   #mydict = logger.metadata()

    logger.debug('2nd warning')
    return 0

if __name__ == "__main__":
    #main(sys.argv)
    sys.exit(main(sys.argv))