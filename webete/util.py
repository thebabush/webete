
def strip_file_ext_from_list(fname, exts):
    for ext in exts:
        ext = '.' + ext
        if fname.endswith(ext):
            return fname[:-len(ext)]
    return fname

