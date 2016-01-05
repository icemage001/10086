import ConfigParser
import mprequest
from sys import argv

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


if __name__ == '__main__':
    Config = ConfigParser.ConfigParser()
    exeruningpath=os.path.dirname(sys.executable)
    Config.read(exeruningpath + "\\Config.ini")
    Config.read("Config.ini")
    Config.sections()
    mpusername = ConfigSectionMap('ACCOUNT')['username']
    mppassword = ConfigSectionMap('ACCOUNT')['password']
    newrequest = mprequest.WhiteList()
    newrequest.setusername(mpusername)
    newrequest.setpassword(mppassword)
    newrequest.addmobile(argv[0])
    newrequest.savemobile()
    newrequest.close()
