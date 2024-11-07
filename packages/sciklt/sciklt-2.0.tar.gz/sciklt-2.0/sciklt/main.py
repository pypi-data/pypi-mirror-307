from sciklt.aids import *
from sciklt.cn import *
import os
import shutil
import subprocess


available = {'-1  ' : "AIDS CN NLP(Folder)",
             '\nAIDS' : "",
             '0   ' : "All",
             '1   ' : "Breadth First Search",
             '2   ' : "Depth First Search",
             '3   ' : "Uniform Cost Search",
             '4   ' : "Depth Limited Search", 
             '5   ' : "Iterative Deepening Search(IDDFS)", 
             '6   ' : "A*", 
             '7   ' : "Iterative Deepening A*", 
             '8   ' : "Simplified Memory Bounded A*",
             '9   ' : "Genetic Algorithm", 
             '10  ' : "Simulated Annealing",
             '11  ' : "Solving Sudoku(Simulated Annealing)",
             '12  ' : "Alpha-Beta Pruning",
             '13  ' : "Map Coloring(Constraint Satisfaction Problem)",
             '14  ' : "House Allocation(Constraint Satisfaction Problem)",
             '15  ' : "Random Sampling",
             '16  ' : "Z Test",
             '17  ' : "T Test",
             '18  ' : "ANOVA",
             '19  ' : "Linear Regression",
             '20  ' : "Logistic Regression",
             '\nCN' : "",
             '21  ' : "Chat Application JAVA",
             '22  ' : "File Transfer JAVA",
             '23  ' : "RMI(Remote Method Invocation) JAVA",
             '24  ' : "wired.tcl     (Wired Network)",
             '25  ' : "wired.awk     (Wired Network)",
             '26  ' : "wireless.tcl  (Wireless Network)",
             '27  ' : "Wireless.awk  (Wireless Network)",
             '28  ' : "tahoe.tcl     (TCP Congestion Control)",
             '29  ' : "reno.tcl      (TCP Congestion Control)",
             '30  ' : "sack.tcl      (TCP Congestion Control)",
             '31  ' : "vegas.tcl     (TCP Congestion Control)",
             '32  ' : "flow.tcl      (TCP Flow Control)",
             '33  ' : "analysis.awk  (TCP Flow & Congestion Control)",
             '34  ' : "LS.tcl        (Link State & Distance Vector Routing)",
             '35  ' : "DV.tcl        (Link State & Distance Vector Routing)",
             '36  ' : "analysis.awk  (Link State & Distance Vector Routing)",
             '37  ' : "multicast.tcl (Multicast & Broadcast Routing)",
             '38  ' : "broadcast.tcl (Multicast & Broadcast Routing)",
             '39  ' : "analysis.awk  (Multicast & Broadcast Routing)",
             '40  ' : "DHCP JAVA",
             '41  ' : "LAN.tcl       (Ethernet LAN IEEE 802.3)",
             '42  ' : "analysis.awk  (Ethernet LAN IEEE 802.3)",
             '43  ' : "complexdcf.tcl(Wireless LAN IEEE 802.11)"}

def get(name = None, open = False):
    try:
        if name is not None:
            name = str(name)
        if   name in ['1']      :   print(bfs)
        elif name in ['2']      :   print(dfs)
        elif name in ['3']      :   print(ucs)
        elif name in ['4']      :   print(dls)
        elif name in ['5']      :   print(ids)
        elif name in ['6']      :   print(astar)
        elif name in ['7']      :   print(idastar)
        elif name in ['8']      :   print(smastar)
        elif name in ['9']      :   print(genetic)
        elif name in ['10']     :   print(sa)
        elif name in ['11']     :   print(sudoku)
        elif name in ['12']     :   print(alphabeta)
        elif name in ['13']     :   print(csp_map)
        elif name in ['14']     :   print(csp_house)
        elif name in ['15']     :   print(random_sampling)
        elif name in ['16']     :   print(z_test)
        elif name in ['17']     :   print(t_test)
        elif name in ['18']     :   print(anova)
        elif name in ['19']     :   print(linear)
        elif name in ['20']     :   print(logistic)
        elif name in ['21']     :   print(chat)
        elif name in ['22']     :   print(file_transfer)
        elif name in ['23']     :   print(rmi)
        elif name in ['24']     :   print(wired_tcl)
        elif name in ['25']     :   print(wired_awk)
        elif name in ['26']     :   print(wireless_tcl)
        elif name in ['27']     :   print(wireless_awk)
        elif name in ['28']     :   print(tahoe_tcl)
        elif name in ['29']     :   print(reno_tcl)
        elif name in ['30']     :   print(sack_tcl)
        elif name in ['31']     :   print(vegas_tcl)
        elif name in ['32']     :   print(flow_tcl)
        elif name in ['33']     :   print(tcp_flow_congestion_awk)
        elif name in ['34']     :   print(LS_tcl)
        elif name in ['35']     :   print(DV_tcl)
        elif name in ['36']     :   print(link_state_distance_vector_awk)
        elif name in ['37']     :   print(multicast_tcl)
        elif name in ['38']     :   print(broadcast_tcl)
        elif name in ['39']     :   print(multicast_broadcast_awk)
        elif name in ['40']     :   print(dhcp)
        elif name in ['41']     :   print(LAN_tcl)
        elif name in ['42']     :   print(ethernet_LAN_awk)
        elif name in ['43']     :   print(complexdcf_tcl)
        elif name in ['0']      :   print(code)
        elif name in ['-1']     :   get_folder(loc = True)
        else:
            for k, v in available.items():
                sep = " : " if v else ""
                print(k,v,sep = sep)
    except:
        pass

def get_folder(loc = False, i = 0, j = 0):
    src = os.path.realpath(__file__)[:-7]+"\\data\\AIDS CN NLP"
    src = src.replace("\\\\","\\")
    try:
        dest = os.getcwd()+"\\AIDS CN NLP"+(f" ({i})" if i != 0 else "")
        shutil.copytree(src, dest, symlinks=False,
                        copy_function = shutil.copy2,
                        ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__init__.py', '__pycache__'),
                        ignore_dangling_symlinks=False, 
                        dirs_exist_ok=False)
        if loc:
            print("Path:",dest.replace("\\\\","\\"))
    except FileExistsError:
        get_folder(loc, i + 1, j)
    except:
        try:
            dest = os.path.expanduser('~')+"\\Downloads\\AIDS CN NLP"+(f" ({j})" if j != 0 else "")
            shutil.copytree(src, dest, symlinks=False,
                            copy_function = shutil.copy2,
                            ignore=shutil.ignore_patterns('.ipynb_checkpoints', '__init__.py', '__pycache__'),
                            ignore_dangling_symlinks=False, 
                            dirs_exist_ok=False)
            if loc:
                print("Path:",dest.replace("\\\\","\\"))
        except FileExistsError:
            get_folder(loc, i, j + 1)
        except:
            pass