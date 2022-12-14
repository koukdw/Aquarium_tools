# -*- coding:utf-8 -*-

import struct
import os
import pathlib

path = pathlib.Path(
    './Output/')


def walk(adr):
    mylist = []
    for root, dirs, files in os.walk(adr):
        for name in files:
            if name[-6:] != '.datu8':
                continue
            if not (os.path.isfile(os.path.join(root, name[:-6] + '.txt'))):
                continue  
            adrlist=os.path.join(root, name)
            mylist.append(adrlist)
    return mylist

def byte2int(byte):
	long_tuple=struct.unpack('L',byte)
	long = long_tuple[0]
	return long

def dumpstr(src):
    bstr = b''
    #len = src.read(4)
    c = src.read(1)
    while c != b'\x00':
        bstr += c
        c = src.read(1)
    return bstr.decode('utf-8')

def int2byte(num):
	return struct.pack('L',num)

def main():
    f_lst = walk('Config')

    for fn in f_lst:
        fs = open(fn, 'rb')
        dstname = fn[:-6] + '.txt'
        txt = open(dstname, 'r', encoding='utf-8')
        filesize=os.path.getsize(fn)
        dst = open(path.joinpath(fn[:-6]+'.datu8'), 'wb')
        count = byte2int(fs.read(4))
        types=[byte2int(fs.read(4)) for i in range(count)]
        dst.write(int2byte(count))
        for t in types:
            dst.write(int2byte(t))
        str_list = []
        for rows in txt:
            if rows[0] != '●':
                continue
            row = txt.readline().rstrip('\r\n').replace('\\n','\n')
            str_list.append(row)
        i = 0
        while fs.tell() < filesize:
            for t in types:
                if t == 2:
                    dst.write(fs.read(4))
                elif t == 1:
                    value = byte2int(fs.read(4))
                    l = dumpstr(fs)
                    if len(l) != 0:
                        str = bytes(str_list[i], 'utf-8')
                        dst.write(struct.pack('L', len(str)+1))
                        dst.write(struct.pack("%ds" % len(str), str))
                        dst.write(struct.pack('B',0))
                        i += 1
                    elif value == 1:
                        dst.write(struct.pack('L', 1))
                        dst.write(struct.pack('B', 0))
                    else:
                        dst.write(struct.pack('B', 0))
        fs.close()
        dst.close()
        txt.close()
main()