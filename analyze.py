#!/usr/bin/env python3
# coding: utf-8

""" 
    Copyright (c) 2011, Andrey Morozov <morozov.andrey.vmk@gmail.com>
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, 
    are permitted provided that the following conditions are met:

        Redistributions of source code must retain the above copyright notice, this 
        list of conditions and the following disclaimer.

        Redistributions in binary form must reproduce the above copyright notice, 
        this list of conditions and the following disclaimer in the documentation 
        and/or other materials provided with the distribution.

        Neither the name of the <ORGANIZATION> nor the names of its contributors 
        may be used to endorse or promote products derived from this software without
        specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, 
    INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
    OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import argparse
from subprocess import Popen, PIPE

i_MMX   = set(b'emms movd movq packssdw packsswb packuswb paddb paddd paddsb paddsw paddusb paddusw paddw pand pandn pcmpeqb pcmpeqd pcmpeqw pcmpgtb pcmpgtd pcmpgtw pmaddwd pmulhw pmullw por pslld psllq psllw psrad psraw psrld psrlq psrlw psubb psubd psubsb psubsw psubusb psubusw psubw punpckhbw punpckhdq punpckhwd punpcklbw punpckldq punpcklwd pxor'.split())
i_SSE1  = set(b'addps addss cmpps cmpss comiss cvtpi2ps cvtps2pi cvtsi2ss cvtss2si cvttps2pi cvttss2si divps divss ldmxcsr maxps maxss minps minss movaps movhlps movhps movlhps movlps movmskps movntps movss movups mulps mulss rcpps rcpss rsqrtps rsqrtss shufps sqrtps sqrtss stmxcsr subps subss ucomiss unpckhps unpcklps andnps andps orps pavgb pavgw pextrw pinsrw pmaxsw pmaxub pminsw pminub pmovmskb pmulhuw psadbw pshufw xorps prefetchnta prefetch0 prefetch1 prefetch2 ldmxcsr sfence movntq maskmovq fxrstor fxsave'.split())
i_SSE2  = set(b'addpd addsd subpd subsd mulpd mulsd divpd divsd maxpd maxsd minpd minsd paddb paddw paddd paddq paddsb paddsw paddusb paddusw psubb psubw psubd psubq psubsb psubsw psubusb psubusw pmaddwd pmulhw pmullw pmuludq rcpps rcpss sqrtpd sqrtsd andnpd andnps andpd pand pandn por pslldq psllq pslld psllw psrad psraw psrldq psrlq psrld psrlw pxor orpd xorpd cmppd cmpsd comisd ucomisd pcmpxxb pcmpxxw pcmpxxd Compare eq lt le ne nlt nle ord unord cvtdq2pd cvtdq2ps cvtpd2pi cvtpd2dq cvtpd2ps cvtpi2pd cvtps2dq cvtps2pd cvtsd2si cvtsd2ss cvtsi2sd cvtsi2ss cvtss2sd cvtss2si cvttpd2pi cvttpd2dq cvttps2dq cvttps2pi cvttsd2si cvttss2si movq movsd movapd movupd movhpd movlpd movdq2q movq2dq movntpd movntdq movnti maskmovdqu pmovmskb pshufd pshufhw pshuflw unpckhpd unpcklpd punpckhbw punpckhwd punpckhdq punpckhqdq punpcklbw punpcklwd punpckldq punpcklqdq packssdw packsswb packuswb clflush lfence mfence pause'.split())
i_SSE3  = set(b'addsubpd addsubps haddpd haddps hsubpd hsubps lddqu movddup movshdup movsldup fisttp monitor mwait'.split())
i_SSSE3 = set(b'psignd psignw psignb phaddd phaddw phaddsw phsubd phsubw phsubsw  pmaddubsw pabsd pabsw pabsb pmulhrsw pshufb palignr'.split())
i_SSE41 = set(b'mpsadbw phminposuw pmuldq pmulld dpps dppd blendps blendpd blendvps blendvpd pblendvb pblendw pminsb pmaxsb pminuw pmaxuw pminud pmaxud pminsd pmaxsd roundps roundss roundpd roundsd inserps pinsrb pinsrd pinsrq extractps pextrb pextrw pextrd pextrq pmovsxbw pmovzxbw pmovsxbd pmovzxbd pmovsxbq pmovzxbq pmovxswd pmovzxwd pmovsxwq pmovzxwq pmovsxdq pmovzxdq ptest pcmpeqq packusdw movntdqa'.split())
i_SSE42 = set(b'crc32 pcmpestri pcmpestrm pcmpistri pcmpistrm pcmpgtq popcnt'.split())
i_SSE4a = set(b'lzcnt popcnt extrq inserq movntsd movntss'.split())
i_AVX   = set(b'vfmaddpd vfmaddps vfmaddsd vfmaddss vfmaddsubpd vfmaddsubps vfmsubaddpd vfmsubaddps vfmsubpd vfmsubps vfmsubsd vfmsubss vfnmaddpd vfnmaddps vfnmaddsd vfnmaddss vfnmsubpd vfnmsubps vfnmsubsd vfnmsubss vbroadcastss vbroadcastsd vbroadcastf128 vinsertf128 vextractf128 vmaskmovps vmaskmovpd vpermilps vpermilpd vperm2f128 vzeroall vzeroupper'.split())
i_FMA3  = set(b'vfmadd132pdy vfmadd132psy vfmadd132pdx vfmadd132psx vfmadd132sd vfmadd132ss vfmadd213pdy vfmadd213psy vfmadd213pdx vfmadd213psx vfmadd213sd vfmadd213ss vfmadd231pdy vfmadd231psy vfmadd231pdx vfmadd231psx vfmadd231sd vfmadd231ss'.split())
i_FMA4  = set(b'vfmaddpdx vfmaddpdy vfmaddpsx vfmaddpsy vfmaddsd vfmaddss'.split())
i_nop   = set(b'nop nopl nopw'.split())
i_call  = set(b'call callq'.split())

class Analyze:
    def __init__(self, app):
        self.app = app
        pass

    def info(self):
        print("analyze : " + str(self.app))

        p1 = Popen(['objdump', '-d', str(self.app)], stdout=PIPE)
        p2 = Popen(['cut', '-f3'], stdin=p1.stdout, stdout=PIPE)
        p3 = Popen(['cut', '-d ', '-f1'],stdin=p2.stdout, stdout=PIPE)
        li = p3.communicate()[0].split()

        self.mmx = self.sse1 = self.sse2 = self.sse3 = self.ssse3 = self.sse41 = self.sse42 = 0
        self.sse4a = self.avx = self.fma3 = self.fma4 = 0
        self.count = self.nop = self.call = self.cpuid = 0

        a_z = set(range(ord('a'), ord('z') + 1))

        for i in li:
            if i[-1] in a_z: 
                self.count += 1;
                if i == b'cpuid':  self.cpuid+=1; continue
                if i in i_nop:     self.nop+=1;   continue
                if i in i_call:    self.call+=1;  continue

                if i in i_MMX:     self.mmx+=1;   continue
                if i in i_SSE1:    self.sse1+=1;  continue
                if i in i_SSE2:    self.sse2+=1;  continue
                if i in i_SSE3:    self.sse3+=1;  continue
                if i in i_SSSE3:   self.ssse3+=1; continue
                if i in i_SSE41:   self.sse41+=1; continue
                if i in i_SSE42:   self.sse42+=1; continue
                if i in i_SSE4a:   self.sse4a+=1; continue
                if i in i_AVX:     self.avx+=1;   continue
                if i in i_FMA3:    self.fma3+=1;  continue
                if i in i_FMA4:    self.fma4+=1;  continue

        self.message_print() 

    def message_print(self):
        print("total count of instruction : " + str(self.count))
        print("nop    : " + str(self.nop))
        print("call   : " + str(self.call))
        print("cpuid  : " + str(self.cpuid))
        print(" ")
        print("MMX    : " + str(self.mmx))
        print("SSE    : " + str(self.sse1))
        print("SSE2   : " + str(self.sse2))
        print("SSE3   : " + str(self.sse3))
        print("SSSE3  : " + str(self.ssse3))
        print("SSE4.1 : " + str(self.sse41))
        print("SSE4.2 : " + str(self.sse42))
        print("SSE4a  : " + str(self.sse4a))
        print("AVX    : " + str(self.avx))
        print("FMA3   : " + str(self.fma3))
        print("FMA4   : " + str(self.fma4))

def main():
    parser = argparse.ArgumentParser(description='analyze of application')
    parser.add_argument('--version', action='version', version='%(prog)s v1.0')
    parser.add_argument('--app', required=True, help='application name')
    args = parser.parse_args()

    a = Analyze(args.app)
    a.info()

if __name__ == "__main__":
    main()

