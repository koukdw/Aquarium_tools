# -*- coding:utf-8 -*-

import struct
import os
import pathlib

path = pathlib.Path('./Output/')

def walk(adr):
	mylist=[]
	for root,dirs,files in os.walk(adr):
		for name in files:
			if name[-6:] != '.binu8':
				continue
			if name == '__global.binu8':
				continue
			adrlist=os.path.join(root, name)
			mylist.append(adrlist)
	return mylist

def byte2int(byte):
	long_tuple=struct.unpack('<L',byte)
	long = long_tuple[0]
	return long

def dumpstr(src):
    bstr = b''
    len = src.read(4)
    c = src.read(1)
    while c != b'\x00':
        bstr += c
        c = src.read(1)
    return bstr.decode('utf-8')

def dumptxt(src, offset, count):
	src.seek(offset)
	str_list = []
	for i in range(0, count):
		str_list.append(dumpstr(src))
	return str_list

def main():
	f_lst = walk('Script')

	for fn in f_lst:
		src = open(fn, 'rb')
		dstname = fn[:-6] + '.txt'
		txt = open(dstname, 'r', encoding='utf-8')
		filesize=os.path.getsize(fn)
		src.seek(4)
		entry_count = byte2int(src.read(4))
		str_offset = (entry_count << 1) * 4 + 8
		src.seek(0)
		data=src.read(str_offset+9)
		dst = open(path.joinpath(fn[:-6]+'.binu8'),'wb')
		dst.write(data)
		for rows in txt:
			if rows[0] != '●':
				continue
			row = txt.readline().rstrip('\r\n')

			str = bytes(row, 'utf-8')
			dst.write(struct.pack('L', len(str)+1))
			dst.write(struct.pack("%ds" % len(str), str))
			dst.write(struct.pack('B',0))

		src.seek(str_offset)
		str_count = byte2int(src.read(4))
		dumptxt(src, src.tell()+5, str_count-1)
		data=src.read(filesize-src.tell())
		dst.write(data)
		src.close()
		dst.close()
		txt.close()

main()