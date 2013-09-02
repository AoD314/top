::

    $./analyze.py --app /usr/bin/mplayer2 
    analyze : /usr/bin/mplayer2
    total count of instruction : 483174
    nop    : 13658
    call   : 21136
    cpuid  : 14
     
    MMX    : 21287
    SSE    : 12134
    SSE2   : 12512
    SSE3   : 365
    SSSE3  : 725
    SSE4.1 : 1733
    SSE4.2 : 0
    SSE4a  : 0
    AVX    : 0
    FMA3   : 0
    FMA4   : 0

::

    $ ./line_counter.py -c cpp cu p opencv/modules/core/src/ --stats short
        
    /work/opencv/opencv/modules/core/src/
    +- cuda
       +-matrix_operations.cu         (     296 lines,   12.16 KB)
       +-matrix_operations.hpp        (      57 lines,    2.75 KB)
    +-algorithm.cpp                   (   1 225 lines,   44.39 KB)
    +-alloc.cpp                       (     697 lines,   18.74 KB)
    +-arithm.cpp                      (   2 926 lines,  101.67 KB)
    +-array.cpp                       (   3 213 lines,   83.86 KB)
    +-command_line_parser.cpp         (     517 lines,   12.87 KB)
    +-convert.cpp                     (   1 379 lines,   44.86 KB)
    +-copy.cpp                        (     857 lines,   24.96 KB)
    +-datastructs.cpp                 (   4 066 lines,  111.91 KB)
    +-drawing.cpp                     (   2 521 lines,   80.10 KB)
    +-dxt.cpp                         (   2 683 lines,   94.32 KB)
    +-gl_core_3_1.cpp                 (   2 755 lines,  124.11 KB)
    +-gl_core_3_1.hpp                 (   1 373 lines,   75.05 KB)
    +-glob.cpp                        (     244 lines,    6.67 KB)
    +-gpu_cuda_mem.cpp                (     215 lines,    6.40 KB)
    +-gpu_info.cpp                    (   1 272 lines,   34.09 KB)
    +-gpu_mat.cpp                     (   1 126 lines,   38.87 KB)
    +-gpu_stream.cpp                  (     308 lines,    6.82 KB)
    +-lapack.cpp                      (   1 826 lines,   54.83 KB)
    +-mathfuncs.cpp                   (   2 561 lines,   95.40 KB)
    +-matmul.cpp                      (   3 339 lines,  112.28 KB)
    +-matop.cpp                       (   1 679 lines,   39.74 KB)
    +-matrix.cpp                      (   4 329 lines,  120.45 KB)
    +-opengl.cpp                      (   1 590 lines,   38.66 KB)
    +-out.cpp                         (     345 lines,   12.03 KB)
    +-parallel.cpp                    (     496 lines,   13.34 KB)
    +-persistence.cpp                 (   5 607 lines,  162.97 KB)
    +-precomp.cpp                     (      45 lines,    2.15 KB)
    +-precomp.hpp                     (     220 lines,    7.18 KB)
    +-rand.cpp                        (   1 008 lines,   31.14 KB)
    +-stat.cpp                        (   2 045 lines,   63.78 KB)
    +-stl.cpp                         (      69 lines,    2.63 KB)
    +-system.cpp                      (     794 lines,   21.44 KB)
    +-tables.cpp                      (   3 512 lines,  108.85 KB)
    +-types.cpp                       (     139 lines,    5.04 KB)
    
    statistics:
            folders  : 1
            files    : 36
            lines    : 57 334
            size     : 1.77 MB
    
    analyze time : 0.01808sec

::

    $ ./ttop.py
    [ 12 x Intel(R) Core(TM) i7 CPU X 980 @ 3.33GHz ]   [ GeForce GTX 560 Ti ]
                                            '+41.0°C'                '+40.0°C'

::

    $ ./executer.py run_list.txt 
    estimated tasks:  3
    estimated tasks:  2
    estimated tasks:  1
    estimated tasks:  0

::

    $ ./bigs.py /work/opencv/build/bin
    /work/opencv/build/bin : 9830 K
    2066 K    opencv_perf_imgproc
    1363 K    opencv_test_core
    1208 K    opencv_perf_core
    1028 K    opencv_perf_gpuimgproc
    1000 K    opencv_test_imgproc
     435 K    opencv_perf_gpuwarping
     342 K    opencv_perf_video
     307 K    opencv_test_highgui
     283 K    opencv_test_video
     269 K    opencv_perf_gpufilters
     227 K    opencv_perf_softcascade
     225 K    opencv_test_ml
     174 K    opencv_test_objdetect
     135 K    opencv_perf_highgui
     114 K    opencv_perf_superres
     110 K    opencv_perf_objdetect
     101 K    opencv_perf_photo
    99.2 K    opencv_test_softcascade
    98.7 K    opencv_test_photo
    83.3 K    opencv_test_superres
    52.9 K    opencv_trainsoftcascade
    24.6 K    opencv_test_gpuimgproc
    17.2 K    opencv_test_gpuwarping
    16.6 K    opencv_test_gpuarithm
    15.4 K    opencv_perf_gpucodec
    14.6 K    opencv_test_gpufilters
    14.6 K    opencv_test_gpucodec
