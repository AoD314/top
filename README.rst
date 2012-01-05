==========
Example 00
==========

::

    $ python3.2 analyze.py --app /usr/bin/ffmpeg
    analyze : /usr/bin/ffmpeg                                                                                           
    total count of instruction : 11849  
    nop    : 266                                                                                                        
    call   : 924                                                                                                        
    cpuid  : 0                                                                                                          
                                                                                                                   
    MMX    : 39                                                                                                         
    SSE    : 79                                                                                                         
    SSE2   : 238                                                                                                        
    SSE3   : 4                                                                                                          
    SSSE3  : 0                                                                                                          
    SSE4.1 : 0                                                                                                          
    SSE4.2 : 0                                                                                                          
    SSE4a  : 0                                                                                                          
    AVX    : 0                                                                                                          
    FMA3   : 0                                                                                                          
    FMA4   : 0 

==========
Example 01
==========

::

$ python line_counter.py -c py
.
+- __init__.py     (2 lines, 82  B)
+- colors.py       (31 lines, 818  B)
+- converter.py    (4 lines, 4  B)
+- file.py         (29 lines, 597  B)
+- filters.py      (41 lines, 942  B)
+- line_counter.py (42 lines, 2.00 KB)
+- num.py          (14 lines, 281  B)
+- size.py         (33 lines, 824  B)
+- tree.py         (205 lines, 7.65 KB)

statistics:
    folders  : 0
    files    : 9
    lines    : 401
    size     : 13.11 KB

analyze time : 0.00121sec

