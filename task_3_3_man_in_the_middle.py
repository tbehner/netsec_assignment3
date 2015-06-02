import telnetlib
from time import sleep
import math

class ManInTheMiddleHandler():
    def __init__(self):
        # settings for encryption keys
        self.key_prime = -1
        self.key_generator = -1
        self.key_exponent = 3
        self.key = -1

    # receive message (only one line) over telnet, set timeout to 100ms, in case there is no message sent
    def receiveMessage(self, tn):
        message = tn.read_until("\n", 0.1)
        return message

    # find word "prime" and "generator" in message, after that always the prime n and generator g appears in message
    def findPrimeAndGeneratorInMessage(self, message):
        message_parts = message.split(" ")
        for i in xrange(len(message_parts)):
            if message_parts[i] == "prime":
                self.key_prime = long(message_parts[i+1])
            if message_parts[i] == "generator":
                self.key_generator = long(message_parts[i+1])

    # find word "be" in message, after that always the public key "g^x mod n" or "g^y mod n" is sent
    # replace this key by own key "(public_key)^z mod n"
    def exchangeKeyMessages(self, message):
        message_parts = message.split(" ")
        for i in xrange(len(message_parts)):
            if message_parts[i] == "be":
                # consider that one person sends "!" after the public key and also remove line breaks
                put_exclamation_mark_at_end = False
                if "!" in message_parts[i+1]:
                    message_parts[i+1] = message_parts[i+1].replace("!", "")
                    put_exclamation_mark_at_end = True
                message_parts[i+1] = message_parts[i+1].strip()
                
                # exchange key
                public_key = long(message_parts[i+1])
                manipulated_public_key = math.pow(public_key, self.key_exponent) % self.key_generator
                message_parts[i+1] = str(manipulated_public_key)
                self.printMessage("Attacker", "public key:\r\n\t%s\r\nwas replaced by manipulated key:\r\n\t%s" % (public_key, manipulated_public_key))
                self.printMessage("Attacker", "(exponent: %s, generator: %s)" % (self.key_exponent, self.key_generator))
                
                # add "!" again at end
                if put_exclamation_mark_at_end:
                    message_parts[i+1] += "!"
                
                # reconstruct message
                return " ".join(message_parts)
        return message

    # print message
    def printMessage(self, sender_name, message):
        print "##################################################"
        print "%s:" % sender_name
        print message
        print "##################################################"

    # receive message from one client, exchange keys with own and relay manipulated message to other client
    def handleSendingAndReceiving(self, tn_A, tn_B, client_number):
        # get message
        message = self.receiveMessage(tn_A)
        if message != "":
            # find 
            self.findPrimeAndGeneratorInMessage(message)
            message = self.exchangeKeyMessages(message)
            self.printMessage(client_number, message)
            tn_B.write(message)
        sleep(0.05)
    
    # start attack
    def startManInTheMiddleAttack(self, host_1, port_1, host_2, port_2):
        # open telnet connection to both
        tn_1 = telnetlib.Telnet(host_1, port_1)
        tn_2 = telnetlib.Telnet(host_2, port_2)
        
        # run forever and receive/send messages from one client to the other
        #try:
        while 1==1:
            self.handleSendingAndReceiving(tn_1, tn_2, "Diffie")
            self.handleSendingAndReceiving(tn_2, tn_1, "Hellman")
        #except:
        #    print "exception"


# create ManInTheMiddleHandler and start attack
manInTheMiddleHandler = ManInTheMiddleHandler()
manInTheMiddleHandler.startManInTheMiddleAttack("10.0.0.12", 3333, "10.0.0.12", 4444)