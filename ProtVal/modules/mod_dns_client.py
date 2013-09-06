def getModuleName():
    return "DNS Client Validator"

def getModuleDescription():
    return "A TCP server to validate TCP clients against"

def initMod():
    print("Inside TCP Client Validator")
    main()

import socket
import dns.resolver

    
    
def main():
    input_user = input("Which DNS records do you want to test?")
    host_by_name = socket.gethostbyname(input_user)
    print('Information received from local DNS:', host_by_name)
    
    print("Now we are going to verify the answer using Google DNS")
    
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = ['8.8.8.8']
    
    answer = my_resolver.query(input_user)
    print(type(my_resolver.nameservers))
    print(type(answer))

    print(answer[0])
    
    if str(host_by_name) == str(answer[0]):
        print("Answer is the same")
    else:
        print("Answer is not the same. This doesn't have to mean that your settings are incorrect.")
        print("Some websites can be reached using different IP-adresses")
            
if __name__ == "__main__":
    main()        
