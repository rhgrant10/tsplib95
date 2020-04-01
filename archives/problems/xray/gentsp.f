      external setpts
c
      common /mstprm/ msglvl
      common /points/ phi, chi, twoth, n
      integer n, msglvl
      double precision  phi(20000), chi(20000), twoth(20000)
c
      character(len=3) lvlarg
      double precision orient(3,3), lambda
      integer hlo, hhi, klo, khi, llo, lhi
c
      if (iargc() == 0) then
            msglvl = 0
      else
            call getarg (1, lvlarg)
            read (lvlarg, *)msglvl
      end if
      do i=1,3
            read(5,*) (orient(i,j), j=1,3)
      end do
      read(5,*) lambda
      read(5,*) hlo, hhi, klo, khi, llo, lhi
c
      call setpts (orient, lambda, hlo, hhi, klo, khi, llo, lhi)
      stop
      end