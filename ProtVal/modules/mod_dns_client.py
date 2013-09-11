def getModuleName():
    return "DNS Client Validator"

def getModuleDescription():
    return "A dummy DNS Client Validator"

def initMod():
    print("Inside DNS Client validator")
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
    
    

    for answers in answer:
        print(answers)
    
    if str(host_by_name) == str(answer[0]):
        print("Answer is the same")
    else:
        print("Answer is not the same. This doesn't have to mean that your settings are incorrect.")
        print("Some websites can be reached using different IP-adresses")
        
    print("Check MX records")
    answer = my_resolver.query(input_user, "MX")
    for answers in answer:
        print(answers)
    
    
            
if __name__ == "__main__":
    main()        
