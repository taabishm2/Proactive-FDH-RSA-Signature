import fdh

save_path = 'C:/Users/Tabish/Desktop/Github/Crypto/FDH_RSA/Files/'

def write_list(filename,l):
    '''write a list l into file'''

    completeName = save_path + filename + '.txt'
    file = open(str(completeName),'w')
    file.write(str(l)[1:-1])
    file.close()

def read_list(filename):
    '''return data from file read as list, READS ONLY INTEGERS'''

    completeName = save_path + filename + '.txt'
    

    file = open(completeName,'r')
    arr = file.read().split(',')
    return (list(map(int,arr)))

def read_list_noint(filename):
    '''return data from file read as list, READS NON INTEGERS'''

    completeName = save_path + filename + '.txt'

    file = open(completeName,'r')
    arr = file.read().split(',')
    return (arr)

def read_large_data(filename):
    '''reads basic data from file'''

    msg = ""
    
    with open(save_path + filename + ".txt") as infile:
        for line in infile:
            msg += line
    return (msg)

