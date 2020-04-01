      DOUBLE PRECISION FUNCTION COST(V,W)                               DUN00010
      COMMON /MSTPRM/ MSGLVL                                            DUN00020
      COMMON /POINTS/ PHI,CHI,TWOTH,N                                   DUN00030
      INTEGER N,MSGLVL                                                  DUN00040
      DOUBLE PRECISION PHI(20000),CHI(20000),TWOTH(20000)               DUN00050
      INTEGER V,W                                                       DUN00060
      DOUBLE PRECISION DMIN1,DMAX1,DABS                                 DUN00070
      DOUBLE PRECISION DISTP,DISTC,DISTT                                DUN00080
      DISTP=DMIN1(DABS(PHI(V)-PHI(W)),DABS(DABS(PHI(V)-PHI(W))-360.0E+0)DUN00090
     $        )                                                         DUN00100
      DISTC=DABS(CHI(V)-CHI(W))                                         DUN00110
      DISTT=DABS(TWOTH(V)-TWOTH(W))                                     DUN00120
      COST=DMAX1(DISTP/1.25E+0,DISTC/1.5E+0,DISTT/1.15E+0)              DUN00130
      RETURN                                                            DUN00140
      END