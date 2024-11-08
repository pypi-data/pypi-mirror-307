import os
from pint import UnitRegistry
import pyanimalconverter.convert as convert

ureg = UnitRegistry()
Q_ = ureg.Quantity

def talk(rightText="",leftText=""):
    bubbleBottomLine = "-" * (len(rightText)-4)
    bubbleTopLine = "-" * (len(rightText))
    one_speechBubbleTop = f'''
                                              /{bubbleTopLine}
   
                                               {rightText}

                                              |   _{bubbleBottomLine}
                                              / _/
                                             //
    '''
    # middleText = f'''
    #           {leftText}                                   {rightText}
    # '''
    # both_speechBubbleTop = '''
    #     -----------------------------       ----------------------------------
    # '''
    # both_speechBubbleBottom = '''
    #     ----_   ---------------------       ---   _---------------------------
    #         \\ _\\                              / _/
    #             \\                           //
    # '''
    animal = '''
                        _           _ 
            __   ___.--'_`.       .'_`--.___   __
            ( _`.'. -   'o` )     ( 'o`   - .`.'_ )
            _\\.'_'      _.-'       `-._      `_`./_
            ( \\`. )    //\\`           '/\\    ( .'/ )
             \\_`-'`---'\\__,         ,__//`---'`-'_/
              \\`        `-\\           /-'        '/
               `                                 '   
    '''

    return one_speechBubbleTop + animal

def askAnimal():
    navigation = "menu";
    while(True):
        os.system('clear');
        if(navigation=="done"):
            print(talk("Ok, bye. Ribbit.","I have nothing left to ask!"))
            break
        if(navigation=="menu"):
            print(talk("Ribbit, what do you want?"))
            menuInput = input("I want to (CONVERT/COMPARE) some numbers (type DONE to exit): ").upper()
            print(menuInput);
            if(menuInput=="CONVERT"):
                navigation="convert";
            elif(menuInput=="COMPARE"):
                navigation="compare";
            elif(menuInput=="DONE"):
                navigation="done";
        if(navigation=="convert"):
            os.system('clear');
            print(talk("Ribbit, ok, what number do you want to convert?","I want to convert a number!"));
            while(True):
                convertFrom = input("Enter the number with units (e.g. 1 kg, 5 kg) you want to convert (or MENU to cancel): ");
                if convertFrom == "menu":
                    navigation="menu";
                    break;
                try:
                    convertFrom_num = Q_(convertFrom);
                    if not(len(convertFrom.split(" "))==2):
                        raise ValueError;
                    fromUnit = convertFrom.split(" ")[1]
                except Exception as e:
                    os.system('clear');
                    print(e);
                    print(talk("I don't understand, please tell me a number with the right format - ribbit!"));
                    continue;
                else:
                    os.system('clear');
                    print(talk("What do you want to convert this number to?",f"{convertFrom_num.magnitude} {convertFrom_num.units}"))
                    while(True):
                        try:
                            convertTo = input("Enter unit type (e.g. kg, cm, lb): ")
                            finalAnswer = convert.convert(convertFrom_num.magnitude, fromUnit, convertTo)
                        except SystemExit: # catches the SystemExit errors out of convert() (specifically scenario where units not compatible)
                            os.system('clear');
                            print(talk(f"Stupid! I can't convert {fromUnit} to {convertTo}. Give me a number I can actually convert {fromUnit} to!"));
                            continue;
                        except Exception:  # catches exception if input not typed properly/using unsupported unit
                            os.system('clear');
                            print(talk("I don't know what that number or unit are. Make sure you've typed with the proper format! (e.g. 5 kg)"))
                            continue;
                        else:
                            os.system('clear')
                            print(talk(f"{convertFrom} in {convertTo} is {finalAnswer} {convertTo}"));
                            break;
                    menuInput = input("Ask the frog to convert another number? (Y/N): ").upper();
                    if(menuInput == "N"):
                        navigation="menu"
                        break
                    elif(menuInput == "Y"):
                        os.system('clear')
                        print(talk("What number do you want to convert this time?"));

        if(navigation == "compare"):
            os.system('clear')
            print(talk("What's the first number?"));
            while(True):
                compareFirst = input("Enter a number with units (e.g. 1 kg, 5 kg) you want to compare: ");
                # if "MENU" or "menu" in compareFirst:
                #     navigation="menu";
                #     break;
                try:
                    compareFirst_num = Q_(compareFirst);
                    compareFirst_unit = compareFirst.split(" ")[1]
                except Exception as e:
                    os.system('clear');
                    print(e);
                    print(talk("I don't understand, please tell me a number with the right format - ribbit!"));
                    continue;
                else:
                    os.system('clear');
                    print(talk(f"What number do you want me to compare {compareFirst} with?",f"{compareFirst_num.magnitude} {compareFirst_num.units}"))
                    while(True):
                        try:
                            compareSecond = input("Enter a number with units (e.g. 1 kg, 5 kg) you want to compare with: ")
                            compareSecond_num = Q_(compareSecond);  # check if user input in the right format: [number] [units] -> 10 kg, 1 cm
                            compareSecond_unit = compareSecond.split(" ")[1]    # to extract the unit from the original input str
                            # print(convert.convert(convertFrom_num.magnitude, "km", "meter"))
                            finalAnswer = convert.compare(compareFirst_num.magnitude, compareSecond_num.magnitude, compareFirst_unit, compareSecond_unit)
                        except SystemExit as e: # catches the SystemExit errors that might come out of compare (specifically scenario where units not comparable)
                            os.system('clear');
                            print(talk(f"Stupid! I can't compare {compareFirst_unit} with {compareSecond_unit}. Give me a number I can actually compare with {compareFirst_unit}!"));
                            continue;
                        except Exception as e:  # catches the exception raised if the second number input is not properly formatted
                            os.system('clear');
                            print(talk(f"I'm not sure I understand what you just said. Make sure you've typed with the proper format! (e.g. 5 kg)"))
                            continue;
                        else:
                            os.system('clear')
                            if(finalAnswer==1):
                                print(talk(f"{compareFirst} is larger than {compareSecond}."))
                            elif(finalAnswer==0):
                                print(talk(f"{compareFirst} is equal to {compareSecond}."))
                            elif(finalAnswer==-1):
                                print(talk(f"{compareFirst} is smaller than {compareSecond}."))
                            break;
                    menuInput = input("Ask the frog to compare more numbers? (Y/N): ").upper()
                    if(menuInput == "N"):
                        navigation="menu"
                        break
                    elif(menuInput == "Y"):
                        os.system('clear')
                        print(talk("Ribbit, ok.. what's your first number?","'Scuse me, can you compare some more numbers?"));
                    

# askAnimal();
