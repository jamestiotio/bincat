import idc
import idautils
import idaapi

fname = idaapi.askfile_c(1, "*.*", "Save to binary")

max_addr = 0
# Check if we have a buggy IDA or not
buggy = False
try:
    idaapi.get_many_bytes_ex(0, 1)
except TypeError:
    buggy = True

if buggy:
    f = idaapi.qfile_t()
    f.open(fname, 'wb+')
    segments = [x for x in idautils.Segments()]
    max_addr = idc.GetSegmentAttr(segments[-1], idc.SEGATTR_END)
    # TODO check max_addr to see if it's sane to write such a big file
    idaapi.base2file(f.get_fp(), 0, 0, max_addr)
    f.close()

else:
    f = open(fname, 'wb+')
    # over all segments
    for s in idautils.Segments():
        start = idc.GetSegmentAttr(s, idc.SEGATTR_START)
        end = idc.GetSegmentAttr(s, idc.SEGATTR_END)
        # print "Start: %x, end: %x, size: %x" % (start, end, end-start)
        max_addr = max(max_addr, end)
        f.seek(start, 0)
        # Only works with fixed IDAPython.
        f.write(idaapi.get_many_bytes_ex(start, end-start)[0])
    f.close()

print "section[dump] = 0, 0x%x, 0, 0x%x" % (max_addr, max_addr)
