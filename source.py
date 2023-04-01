import os
#---------- Constant Values -----------
# Segment of code holding dictonaries that contain function and opcode pairs

# Function Returns the value of the register
def register_value(value):
    registers = {'$zero' : '00000','$at'  : '00001','$v0' : '00010','$v1' : '00011','$a0' : '00100',
    '$a1' : '00101','$a2' : '00110', '$a3': '00111','$t0' : '01000','$t1' : '01001','$t2' : '01010',
    '$t3' : '01011','$t4' : '01100','$t5' : '01101','$t6' : '01110','$t7' : '01111','$s0' : '10000',
    '$s1' : '10001','$s2' : '10010','$s3' : '10011','$s4' : '10100','$s5' : '10101','$s6' : '10110',
    '$s7' : '10111','$t8' : '11000','$t9' : '11001','$k0' : '11010','$k1' : '11011','$gp' : '11100',
    '$sp' : '11101','$fp' : '11110','$ra' : '11111','$0'  : '00000','$1'  : '00001','$2'  : '00010',
    '$3'  : '00011','$4'  : '00100','$5'  : '00101','$6'  : '00110', '$7' : '00111','$8'  : '01000',
    '$9'  : '01001','$10' : '01010','$11' : '01011','$12' : '01100','$13' : '01101','$14' : '01110',
    '$15' : '01111','$16' : '10000','$17' : '10001','$18' : '10010','$19' : '10011','$20' : '10100',
    '$21' : '10101','$22' : '10110','$23' : '10111','$24' : '11000','$25' : '11001','$26' : '11010',
    '$27' : '11011','$28' : '11100','$29' : '11101','$30' : '11110','$31' : '11111'}
    
    return registers[value]


# Function Returns function code for R-Type instructions
def Function_code(value):
    dict = {
        'add':'100000','addu':'100001','and':'100000','or':'100101','nor':'100111',
        'sub':'100010','subu':'100011','sll':'000000','srl':'000010','slt':'101010'
    }
    return dict[value]


# Function Returns op code for Instructions
def op_code(value):
    dict = {'addi' : '001000', 'addiu' : '001001', 'andi' : '001100', 'beq' : '000100',
        'bne' : "000101", 'lbu' : '100100', 'lhu' : '100101', 'lhu': '100101', 'll': '110000',
        'lui': '001111', 'lw': '100011', 'ori': '001101', 'slti': '001010','sltiu': '001011',
         'sb': '101000', 'sc': '111000', 'sh': '101001', 'sw': '101011'
    }
    return dict[value]

# ------------------------- Quality Control Codes ----------------------------
# Basically helps prevent repetition an a small bunch of if else statements in the code

# Checks if a value exists in the array or not
def if_exists(value,list):
    for i in list:
        if(value == i):
            return True
    return False

#Checks if a number is hexadecimal or not
def is_hex(n):
    if(n[0:2]=='0x'):
        return True
    return False

#Checks if a valid immediate is entered
#Self explainatory code
def is_valid_imm(val):
    val = str(val)
    hex = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','A','B','C','D','E','F']
    num = ['-','0','1','2','3','4','5','6','7','8','9']
    if(is_hex(val)):
        val=val.replace('0x','')
        for i in val:
            if(if_exists(i,hex)==False):
                return False
        return True
    else:
        for i in val:
            if(if_exists(i,num)==False):
                return False
        return True

# Helps print error statements whenever an error is encountered
def Error(n):
    text = "Cannot assemble the assembly code at line "
    text += str(n)
    return text


#Checks if value is register or not. Is useful to provent errors
def is_register(value):
    li = ['$zero','$at','$v0','$v1','$a0','$a1','$a2','$a3','$t0','$t1','$t2','$t3','$t4','$t5',
    '$t6','$t7','$t8','$t9','$s0','$s1','$s2','$s3','$s4','$s5','$s6','$s7','$k0','$k1','$gp',
    '$sp','$fp','$ra','$0','$1','$2','$3','$4','$5','$6','$7','$8','$9','$10','$11','$12','$13',
    '$14','$15','$16','$17','$18','$19','$20','$21','$22','$23','$24','$25','$26','$27','$28','$29',
    '$30','$31']
    return (if_exists(value,li))

# Removes comments and labels from the code. 
def remove_unused(line):        
    for i in range(len(line)):      
        if(line[i]=='#'):           # To check if a comment is present
            line = line[:i]         # Removes everything after the # including it.
            break
    for i in range(len(line)):
        if(line[i]==':'):           # To check if a label is present
            line = line[i+1:]       # Removes everything before the : including it.
            break
    return line


#----------- Functions to deal with number conversion and sign extensions ----------------


# This function converts a decimal number to a 16 bit 2's complement signed number
# Self explanatory algorithgm
def twosComplement (value, bitLength) :
    return (bin(value & (2**bitLength - 1)).replace('0b','')).zfill(16)


# This function sign extends a binary string to 16 bits
# Self explanatory algorithgm
def sign_extend(value):
    if(value[0]== '0'):
        value = ('0'*(16-len(value))) + value
        return value
    else:
        value = ('1'*(16-len(value))) + value
        return value


# This function deals with converting an input number(as string) to a 16 bit 
# immediate depending on whether it is signed or unsigned
# Self explanatory algorithgm
def imm_value(value,type):
    if(type=='s'):
        if(is_hex(value)):
            value = int(value,base=16)
            value = bin(value).replace('0b','')
            return sign_extend(value)
        else:
            return twosComplement(int(value),16)
    else:
        if(is_hex(value)):
            value = int(value,base=16)
            value = bin(value).replace('0b','')
            return value.zfill(16)
        else:
            value = bin(int(value)).replace('0b','')
            return value.zfill(16)

# This function sign converts and extends a decimal to 5 bits
# Self explanatory algorithgm
def extend_to_5_bit(n):
    temp = bin(n).replace("0b", "")
    if(len(temp) < 5 ):
        t = ("0"*(5-len(temp)))
        temp = t+temp
    return temp

# This function converts a binary strig to a 8 digit hex string
# Self explanatory algorithgm
def to_hex(str):
    num = int(str,2)
    num = hex(num).replace('0x','')
    num = num.zfill(8)
    num = '0x' + num
    return num



# ---------------------------- Code for R type instructions ----------------------------

# Compares the values of registers and the function code
def R_to_hex(list,n):
    opcode = "000000"
    if(is_register(list[1]) and is_register(list[2]) and is_register(list[3])):     #Check to see if registers exist
        rs = register_value(list[1])    #Find equivalent binary of register
        rt = register_value(list[2])    #Find equivalent binary of register
        rd = register_value(list[3])    #Find equivalent binary of register
    else:
        return Error(n)               #Return Error statement
    shamt = "00000"                     #Since Shamt for arethmetic functions is zero
    fun = Function_code(list[0])        #Find equivalent function code of instruction
    machine_binary = opcode + rs + rt + rd + shamt + fun    #club all to 32 bit binary
    return (to_hex(machine_binary))     #Convert to hex and return

#Check For syntax errors in the form of incorrect input parameters.
#Else split to list and assemble
def assemble_Rtype(value,n):
    value = value.replace(',',' ')
    value = value.split()
    if(len(value)!=4):                  
        return Error(n)
    else:
        inter = []
        inter.append(value[0])
        inter.append(value[2])
        inter.append(value[3])
        inter.append(value[1])
        return R_to_hex(inter,n)

# ---------------------- Code to deal with Shift instructions ------------------------

# Compares the values of registers and the function code
def Shift_to_hex(list,n):
    opcode = '000000'
    if(is_register(list[1]) and is_register(list[3])):      #Check to see if registers exist
        rt = register_value(list[1])        #Find equivalent binary of register
        rs = '00000'                        #Since rs is not used in shift instructions
        rd = register_value(list[3])        #Find equivalent binary of register
        if(is_valid_imm(list[2])):
            if(is_hex(list[2])):                #Find 5 bit binary of shamt
                shamt = extend_to_5_bit(int(list[2],base=16))
            else:
                shamt = extend_to_5_bit(int(list[2]))
        else:
            return Error(n)
        func = Function_code(list[0])       #Find equivalent function code of instruction
        machine_binary = opcode + rs + rt + rd + shamt + func   #club all to 32 bit binary
        return(to_hex(machine_binary))      #Convert to hex and return
    else:
        return Error(n)         #Return Error statement
        
#Check For syntax errors in the form of incorrect input parameters.
#Else split to list and assemble
def assemble_Shift(value,n):
    value = value.replace(',',' ')
    value = value.split()
    if(len(value)!=4):
        return Error(n)
    else:
        inter = []
        inter.append(value[0])
        inter.append(value[2])
        inter.append(value[3])
        inter.append(value[1])
        return Shift_to_hex(inter,n)

#------------------- Code for I type instructions ----------------

#Code to assemble I type instructions
def assemble_I(value,n,type):
    value = value.replace(',',' ')      #Removes unwanted items
    value = value.split()       #converts to list
    if(len(value)!=4):          #checks if we have correct number of parameters
        if(len(value)==3 and value[0]=='lui'):      #since lui has a specical syntax
            if(is_register(value[1]) and is_valid_imm(value[2])):   #check if register and immediate are valid
                opcode = op_code(value[0])      #return opcode
                rs = '00000'                    #since rs is not used in lui
                rt = register_value(value[1])   #return register value
                imm = imm_value(value[2],type)  #return immediate value
                machine_binary = opcode + rs + rt + imm #club to binary
                return to_hex(machine_binary)   #convert to hex and return
            return Error(n) # Register does not exist
        return Error(n) # Wrong number of parameters
    else:
        if(is_register(value[1]) and is_register(value[2]) and is_valid_imm(value[3])):   #check if register and immediate are valid
            opcode = op_code(value[0])          #return opcode
            rs = register_value(value[2])       #return register value
            rt = register_value(value[1])       #return register value
            imm = imm_value(value[3],type)      #return immediate value
            machine_binary = opcode + rs + rt + imm     #club to binary
            return to_hex(machine_binary)       #return after conversion to hex
        return Error(n) # Register does not exist

#------------------- Code for Base-Offset type instructions ----------------

def assemble_Offset(value,n,type):
    value = value.replace(',',' ').replace('(',' ').replace(')',' ')    #Removes unwanted items
    value = value.split()       #Convert to list
    if(len(value)!=4):          #check for correct number of parameters
            return Error(n)     #wrong syntax
    else:
        if(is_register(value[1]) and is_register(value[3]) and is_valid_imm(value[2])):   #check if register and immediate are valid            
            opcode = op_code(value[0])                  #return opcode
            rs = register_value(value[3])               #return register value
            rt = register_value(value[1])               #return register value
            imm = imm_value(value[2],type)              #return immediate velue
            machine_binary = opcode + rs + rt + imm     #club to binary
            return to_hex(machine_binary)   #return after converting to hex
        else:
            return Error(n)


#------------------- Code to control various cases for assembly ---------------

#checks for different types of instructions and calls respective function for 
#further type specific operations
def assemble(line,n):
    R_type = ['add','addu','and','nor','or','sub','subu','slt']
    Shift_Ins = ['sll','srl']
    I_type_signed = ['addi','lhu','ll','lui','slti']
    I_type_unsigned = ['addiu','andi','ori','sltiu']
    Offset_type_signed = ['lw','sb','sc','sh','sw']
    Offset_type_unsigned = ['lbu']

    line = remove_unused(line)          # Remove comments and labels
    temp = (((line.replace(',','')).replace(')','')).replace('(','')).split()

    if(len(temp)==0):
        return Error(n)                 #Empty line, No instructions
    elif(if_exists(temp[0],R_type)):
        return assemble_Rtype(line,n)
    elif(if_exists(temp[0],Shift_Ins)):
        return assemble_Shift(line,n)
    elif(if_exists(temp[0],I_type_signed)):
        return assemble_I(line,n,'s')
    elif(if_exists(temp[0],I_type_unsigned)):
        return assemble_I(line,n,'u')
    elif(if_exists(temp[0],Offset_type_signed)):
        return assemble_Offset(line,n,'s')
    elif(if_exists(temp[0],Offset_type_unsigned)):
        return assemble_Offset(line,n,'u')
    else:
        return Error(n)             #Syntax error
    return hex

#---------- Other Functions ----------


def openfile():                         #function to open asm file for assembling
    inp = input("myAssembler ")         #take file name for input
    file_name =inp + '.asm'             #add asm extension to the file name
    if(os.path.exists(file_name)):      #check if file exists
        file=open(file_name)            #open file
        content=file.read()             #read contents of the file
        file.close()                    #close the opened file to save memory
        content=content.splitlines()    #split the document to a list containing indivudial lines
        return content,inp              #return the list amd file name
    else:                                       
        print("File does not exist !")  #print Error text if file does not exist  
        return None,None

def controller():     #Function to control all the various functions and implement the code
    lines,file_name = openfile()
    output = []
    #code to asemble the lines indivudially
    if(lines != None):
        for i in range(len(lines)):
            hex = assemble(lines[i],i+1)
            output.append(hex)
    else:
        return
    #code to write output to text file
    file_name+='.txt'
    temp = open(file_name,'w')
    for i in output:
        temp.write(i+'\n')
    temp.close()

controller()  #Main function starts the program