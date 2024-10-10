import sys
import argparse
from argparse import RawTextHelpFormatter
from uni import *

class CustomParser(argparse.ArgumentParser):
    def error(self, message):
        print ("Error: " + message + "\n")
        self.print_help()
        sys.exit(2)


class PyUniScraper(object):
    unis = {
        "manchester": Manchester.Manchester(),
        "birmingham": Birmingham.Birmingham(),
        "surrey": Surrey.Surrey(),
        "portsmouth": Portsmouth.Portsmouth(),
        "rmit": RMIT.RMIT(),
        "sheffield": Sheffield.Sheffield(),
        "leeds": Leeds.Leeds(),
        "york": York.York(),
        "uwe": UWE.UWE(),
        "lancaster": Lancaster.Lancaster(),
        "aberdeen": Aberdeen.Aberdeen(),
        "bathspa": BathSpa.BathSpa(),
        "exeter": Exeter.Exeter(),
        "wolverhampton": Wolverhampton.Wolverhampton(),
        "solent": Solent.Solent(),
        "warwick": Warwick.Warwick(),
        "liverpool": Liverpool.Liverpool(),
        "winchester": Winchester.Winchester(),
        "ulster": Ulster.Ulster(),
        "bristol": Bristol.Bristol(),
        "uws": UWS.UWS(),
        "standrews": StAndrews.StAndrews(),
        "swansea": Swansea.Swansea(),
        "southampton": Southampton.Southampton()
    } 
    # perhaps not the best to initialize all these classes that won't be used

    def __init__(self):
        parser = CustomParser(description='''Parses for research output from selected Universities

supported universities:
  manchester
  birmingham
  surrey
  portsmouth
  rmit
  sheffield
  leeds
  york
  uwe
  lancaster
  aberdeen
  bathspa
  exeter
  wolverhampton
  solent
  warwick
  liverpool                            
  winchester
  standrews
  swansea
  southampton''', formatter_class=RawTextHelpFormatter)

        parser.add_argument('university', help='University to get information for')
        parser.add_argument('depth', type=int, default=1, help='Number of pages')
        parser.add_argument('keywords', metavar='K', type=str, nargs='+', help='Keywords to search for')
        parser.add_argument('--raw', dest='raw', action='store_const', const=True, default=False, help='Output to console instead of csv')
        parser.add_argument('-v', '--version', action='version', version='PyUniScraper v0.1.4')
        args = parser.parse_args()

        if args.university in self.unis:
            print ("Scraping for data... this might take a while!")
            self.unis[args.university].ScrapeForData(args.raw, args.depth, args.keywords)
            print ("---DONE---")
        else:
            print("Error: university not supported\n")
            parser.print_help();
