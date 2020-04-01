
      external setpts
      c
            common /mstprm/ msglvl
            common /points/ phi, chi, twoth, n
            integer n, msglvl
            double precision  phi(20000), chi(20000), twoth(20000)
      c
            double precision orient(3,3), lambda
            integer hlo, hhi, klo, khi, llo, lhi, msglvl
      c
            msglvl = 0
            do 10 i=1,3
          read(5,*) (orient(i,j), j=1,3)
         10 continue
            read(5,*) lambda
            read(5,*) hlo, hhi, klo, khi, llo, lhi
      c
            call setpts (orient, lambda, hlo, hhi, klo, khi, llo, lhi)
            stop
            end