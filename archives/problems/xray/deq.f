      DOUBLE PRECISION FUNCTION COST(V,W)                               DEQ00010
      COMMON /MSTPRM/ MSGLVL                                            DEQ00020
      COMMON /POINTS/ PHI,CHI,TWOTH,N                                   DEQ00030
      INTEGER N,MSGLVL                                                  DEQ00040
      DOUBLE PRECISION PHI(20000),CHI(20000),TWOTH(20000)               DEQ00050
      INTEGER V,W                                                       DEQ00060
      DOUBLE PRECISION DMIN1,DMAX1,DABS                                 DEQ00070
      DOUBLE PRECISION DISTP,DISTC,DISTT                                DEQ00080
      DISTP=DMIN1(DABS(PHI(V)-PHI(W)),DABS(DABS(PHI(V)-PHI(W))-360.0E+0)DEQ00090
     $        )                                                         DEQ00100
      DISTC=DABS(CHI(V)-CHI(W))                                         DEQ00110
      DISTT=DABS(TWOTH(V)-TWOTH(W))                                     DEQ00120
      COST=DMAX1(DISTP/1.00E+0,DISTC/1.0E+0,DISTT/1.00E+0)              DEQ00130
      RETURN                                                            DEQ00140
      END                                                               DEQ00150
  