import summonAuto as summonAuto
import sys

if __name__ =="__main__":
    sell = 0
    auto = 0    
    if len(sys.argv) > 1 and sys.argv[1] == 1:
        sell =1
    if len(sys.argv) > 2 and sys.argv[2] == 1:
        auto = 1
    summonAuto.run_by_piont(sell,auto)