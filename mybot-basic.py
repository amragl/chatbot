import re

import ImageClassification
import inference
import BagOfWords

#######################################################
# remove warnings
#######################################################
import warnings
warnings.filterwarnings("ignore")

#######################################################
#  Initialise AIML agent
#######################################################
import aiml
# Create a Kernel object. No string encoding (all I/O is unicode)
kern = aiml.Kernel()
kern.learn("info/std-startup.xml")
kern.respond("load aiml kb")
#kern.setTextEncoding(None)
# Use the Kernel's bootstrap() method to initialize the Kernel. The
# optional learnFiles argument is a file (or list of files) to load.
# The optional commands argument is a command (or list of commands)
# to run after the files are loaded.
# The optional brainFile argument specifies a brain file to load.
#kern.bootstrap(learnFiles="mybot-basic.xml")


#######################################################
# Welcome user
#######################################################
print("Hi I am Joe, What can I help you with!")

#######################################################
# Main loop
#######################################################
while True:
    #get user input
    try:
        userInput = input("> ")
        userInput = re.sub(r'\W+', ' ', userInput)
        print (userInput)
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye!")
        break
    #pre-process user input and determine response agent (if needed)
    responseAgent = 'aiml'
    #activate selected response agent
    if responseAgent == 'aiml':
        answer = kern.respond(userInput)
       # print(answer +" aiml")
    #post-process the answer for commands
    if answer[0] == '#':
        params = answer[1:].split('$')
        cmd = int(params[0])
        if cmd == 0:
            print(params[0], " starting with # params[0]")
            break
        elif cmd == 1:
            bad_value = '  #99'
            if bad_value in params[1]:
                params[1] = params[1].replace(bad_value, "")
            image_url = params[1] +"."+ params[2]
            ImageClassification.FindTheImage(image_url)
            #FindTheImage(image_url)
        elif cmd == 2:
            inference.inference_kb()
        elif cmd == 3:
            print(params[1])
            inference.inference_check(params[1])
            #inference_check2()
        elif cmd == 99:
            BagOfWords.bag_of_words(params[1])
            #print("cmd 99 ","I did not get that, please try again.")
            #print(answer)
    else:
        print(" aiml Joe: ",answer)
        
    



