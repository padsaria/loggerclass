import logging
from logging.handlers import RotatingFileHandler
import sys
import os
import syslog
from pprint import pprint

class logclass(logging.Logger):
    global siteId 
    global stationId 
    global systype 
    global Subsys
    siteId = "  "
    stationId = "  "
    systype = "  "
    Subsys = "   " 
    global sevinfo
    global logfmt
    sevinfo = "   "
    global mydict

    def __init__(self, name="testin1"):
        self.siteId = 1
        self.stationId = 2
        self.systype = 3
        self.Subsys = 4
        self.sevinfo = None
        self.mydict = {'siteId': self.siteId, 'stationId': self.stationId, 'Subsys': self.Subsys, 'systype': self.systype, 'sevinfo': self.sevinfo}
        return super(logclass, self).__init__(name)

    if systype == "system":
        Subsys = "SystemApp"
    elif systype == "portal":
        Subsys = "RestAPI"
    elif systype == "stationController":
        Subsys = "MsgBroker"

    def info(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        extra_dict = self.mydict
        extra_dict['sevinfo'] = "info"
        return super(logclass, self).info(msg, extra=extra_dict, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        extra_dict = self.mydict
        extra_dict['sevinfo'] = "error"
        return super(logclass, self).error(msg, extra=extra_dict, *args, **kwargs)

    
    def debug(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        extra_dict = self.mydict
        extra_dict['sevinfo'] = "debug"
        return super(logclass, self).debug(msg, extra=extra_dict, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        extra_dict = self.mydict
        extra_dict['sevinfo'] = "warnnn"
        return super(logclass, self).warn(msg, extra=extra_dict, *args, **kwargs)

class myFormatter(logging.Formatter):
    logfmt = '<local0.2> %(asctime)-15s  station.viasat.io DeviceFactory[22222]:[level= " %(levelname)s siteId="%(siteId)s " stationId="%(stationId)s"  Subsys="%(Subsys)s" systype="%(systype)s", sevinfo= "%(sevinfo)s"] %(message)s'
    def __init__(self, *args, **kwargs):
        super().__init__(fmt="%(levelno)d: %(msg)s", datefmt=None, style='%')

    def format(self, record):
        print("in myFormatter")
        format_orig = self._style._fmt
        self._style._fmt = myFormatter.logfmt
        return super().format(record)

def main(argv):
    logging.setLoggerClass(logclass)
    logger = logging.getLogger('pls workkk2')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler('/dev/log')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    FORMAT = '<local0.2> %(asctime)-15s  station.viasat.io DeviceFactory[22222]:[severity= " %(levelname)s " siteId="%(siteId)s " stationId="%(stationId)s"  Subsys="%(Subsys)s" systype="%(systype)s" sevinfo="%(sevinfo)s"] %(message)s'
    handler.setFormatter(logging.Formatter(FORMAT))
    fmt = myFormatter()
    handler.setFormatter(fmt)
    #logger = logclass("pls work")   
    #logger.configure_logging()

    #print(type(logger))
   #mydict = logger.metadata()

    logger.debug('2nd warning')
    logger.warn('1st warning')
    logger.error('1st warning')
    logger.info("3rd INFO ?????")
    return 0

if __name__ == "__main__":
    #main(sys.argv)
    sys.exit(main(sys.argv))


