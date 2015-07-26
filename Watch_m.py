from dns import resolver
from datetime import datetime
import sys, os, time, thread, socket, smtplib

name_servers = ["8.8.8.8","8.8.4.4"]



def SendMail(Domain, IP):
    xFROMx = "HostIPChangeNotifier"
    xTOx = ["middleeastfirst@gmail.com","waliedassar@gmail.com"]
    xSUBJECTx = "IP Change For Domain " + Domain
    dataX = Domain + " ==> " + IP
    final_data = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s\r\n" % (xFROMx,", ".join(xTOx),xSUBJECTx, dataX)
    xSERVERx = smtplib.SMTP("smtp.gmail.com",587)
    # smtp.gmail.com requires a STARTTLS session.
    xSERVERx.starttls()
    # smtp.gmail.com requires AUTH, you have to set "Access for less secure apps" to "Turn off" in gmail dashboard.
    xSERVERx.login("HostIPChangeNotifier@gmail.com","AnyPassHere")
    try:
        xSERVERx.sendmail(xFROMx,xTOx,final_data)
    except:
        time.sleep(0) 
    xSERVERx.close()

    
def Watch(Resolver,Domain):
    dom = Domain.rstrip()
    bufsize = 0
    fOut = open(dom + ".txt","w",bufsize)

    LastIP = "0.0.0.0"
    while(1):
        sIP = "0.0.0.0"
        try:
            ip = Resolver.query(dom,'A')
            sIP = str(ip[0])
        except dns.Resolver.NoAnswer:
            ip = "0.0.0.0"
        except dns.Resolver.NXDOMAIN:
            ip = "0.0.0.0"
        except:
            print "Fatal error in \"Resolver.query()\""
            sys.exit(-1)

        if sIP != LastIP:
            sTimeDate = str(datetime.now())
            fOut.write(sTimeDate + "\r\n")
            if ip != "0.0.0.0":
                fOut.write(sIP + "\r\n")
                LastIP = sIP
                SendMail(dom,sIP)
            else:
                fOut.write("0.0.0.0\r\n")
                LastIP = "0.0.0.0"
                SendMail(dom,"0.0.0.0")
            fOut.write("--------------\r\n")

def main():
    if len(sys.argv)!=2:
        print "Usage: resolve_m.py input.txt\r\n"
        sys.exit(-1)

    resolverX = resolver.Resolver()
    resolverX.nameservers = name_servers
        
    fIn = open(sys.argv[1],"r")
    for x in fIn:
        
        thread.start_new_thread(Watch,(resolverX,x))
    
    fIn.close()
    while True:
        time.sleep(1)
    sys.exit(0)
    return
    

if __name__ == "__main__":
    main()
    sys.exit(0)
