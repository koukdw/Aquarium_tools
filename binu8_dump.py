import struct,os


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

def int2byte(num):
	return struct.pack('L',num)

def FormatString(string, count):
	res = "○%08d○\n%s\n●%08d●\n%s\n\n"%(count, string, count, string)
	
	return res

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
		dst = open(dstname, 'w', encoding='utf-8')

		src.seek(4)
		entry_count = byte2int(src.read(4))
		str_offset = (entry_count << 1) * 4 + 8
		src.seek(str_offset)
		print(hex(src.tell()))
		print(dstname)
		str_count = byte2int(src.read(4))

		str_list = dumptxt(src, src.tell()+5, str_count-1)
		i = 0
		for string in str_list:
			dst.write(FormatString(string, i))
			i += 1

		src.close()
		dst.close()
main()
