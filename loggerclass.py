import logging
from logging.handlers import SysLogHandler
import sys
from pprint import pprint

class logclass(logging.Logger):
    def __init__(self, name):
        self.siteId = "1"
        self.stationId = "1"
        self.Subsys = "RestAPI"
        self.systype= "StationController"
        self.sevinfo = None
        self.mydict = {'siteId': self.siteId, 'stationId': self.stationId, 'Subsys': self.Subsys, 'systype': self.systype, 'sevinfo': self.sevinfo}
        return super(logclass, self).__init__(name)
    
    logging.CRIT = 2
    logging.crit = lambda x: logging.log(logging.crit, x) 
    logging.addLevelName(logging.CRIT, "CRIT") 
    
    logging.WARNING = 4
    logging.warning = lambda x: logging.log(logging.WARNING, x) 
    logging.addLevelName(logging.WARNING, "WARNING") 

    logging.WARN = 4
    logging.warn = lambda x: logging.log(logging.WARN, x) 
    logging.addLevelName(logging.WARN, "WARN") 
    
    logging.NOTICE = 5
    logging.notice = lambda x: logging.log(logging.NOTICE, x)
    logging.addLevelName(logging.NOTICE, "NOTICE") 

    logging.INFO = 6
    logging.info = lambda x: logging.log(logging.INFO, x)
    logging.addLevelName(logging.INFO, "INFO") 
    
    logging.DEBUG = 7
    logging.debug = lambda x: logging.log(logging.DEBUG, x)
    logging.addLevelName(logging.DEBUG, "DEBUG")
    
    def crit(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        if extra_dict == {}:
            extra_dict = self.mydict
        extra_dict['sevinfo'] = "maj"
        sevnote = "Major Alarm"
        self.log(logging.CRIT, msg, extra=extra_dict, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        if extra_dict == {}:
            extra_dict = self.mydict
        extra_dict['sevinfo'] = "min"
        sevnote = "Minor Alarm"
        return super(logclass, self).warn(msg, extra=extra_dict, *args, **kwargs)
    
    def notice(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        if extra_dict == {}:
            extra_dict = self.mydict
        extra_dict['sevinfo'] = "clr"
        sevnote = "Clear Alarm"
        self.log(logging.NOTICE, msg, extra=extra_dict, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        if extra_dict == {}:
            extra_dict = self.mydict
        extra_dict['sevinfo'] = "info"
        sevnote = "Information Log"
        return super(logclass, self).info(msg, extra=extra_dict, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        extra_dict = kwargs.pop('extra', {} )
        if extra_dict == {}:
            extra_dict = self.mydict
        extra_dict['sevinfo'] = "dbg"
        sevnote = "Debug Log"
        return super(logclass, self).debug(msg, extra=extra_dict, *args, **kwargs)

    
class myFormatter(logging.Formatter):
    logfmt = '<local0.2> %(asctime)-15s  station.viasat.io DeviceFactory[22222]:[level="%(levelname)s" siteId="%(siteId)s" stationId="%(stationId)s" Subsys="%(Subsys)s" systype="%(systype)s" sevinfo="%(sevinfo)s"] %(message)s'
    def __init__(self, *args, **kwargs):
        super().__init__()

    def format(self, record):
        format_orig = self._style._fmt
        self._style._fmt = myFormatter.logfmt
        return super().format(record)

class UpperThresholdFilter(logging.Filter):
        def __init__(self, threshold, *args, **kwargs):
            self._threshold = threshold
            super(UpperThresholdFilter, self).__init__(*args, **kwargs)

        def filter(self, rec):
            return rec.levelno <= self._threshold

def main(argv):
    logger = logclass() #works
    logger.setLevel(logging.CRIT)
    handler = logging.handlers.SysLogHandler('/dev/log')
    handler.setLevel(logging.CRIT)
    handler.addFilter(UpperThresholdFilter(logging.DEBUG))
    logger.addHandler(handler)

    fmt = myFormatter()
    handler.setFormatter(fmt)
    
    logger.debug('---DEBUG LOG')
    logger.warn('------WARN LOG')
    logger.crit('---------CRIT LOG')
    logger.info('------------INFO LOG')
    logger.notice('---------------NOTICE LOG')

    siteId = "2"
    stationId = "2"
    Subsys = "RestAPI__2"
    systype= "StationController__2"
    sevinfo = None
    d = {'siteId': siteId, 'stationId': stationId, 'Subsys': Subsys, 'systype': systype, 'sevinfo': sevinfo }

    logger.debug('---DEBUG LOG__2', extra=d)
    logger.warn('------WARN LOG__2', extra=d)
    logger.crit('---------CRIT LOG__2', extra=d)
    logger.info('------------INFO LOG__2', extra=d)
    logger.notice('---------------NOTICE LOG__2', extra=d)



    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))


