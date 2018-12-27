import gc

def get_normalized_full_name(raw):
    fullname = raw.strip()
    if fullname[0] == '(' and fullname[-1] == ')':
        return fullname[1:-1]
    return fullname

def queryset_iterator(qs, batchsize = 500, gc_collect = True):
    iterator = qs.values_list('pk', flat=True).order_by('pk').distinct().iterator()
    eof = False
    while not eof:
        primary_key_buffer = []
        try:
            while len(primary_key_buffer) < batchsize:
                primary_key_buffer.append(iterator.next())
        except StopIteration:
            eof = True
        for obj in qs.filter(pk__in=primary_key_buffer).order_by('pk').iterator():
            yield obj
        if gc_collect:
            gc.collect()
