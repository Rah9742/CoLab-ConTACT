from EventbriteScraper import EventbriteScraper
import sys

def PrintHelp():
    print("Usage: PyEventbriteScraper [depth]")

def Main():
    if len (sys.argv) != 2:
        print ("Error: missing arguments\n")
        PrintHelp()
        return
    

    EventbriteScraper().ScrapeForData(int(sys.argv[1]))

if __name__ == "__main__":
    Main()
