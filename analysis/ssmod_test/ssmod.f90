program ramses
  use single_star_module
  use starpop_wind_module
  use hydro_parameters
  implicit none
  
  real(dp) ::ageIn
  real(dp) ::spdout,mlout,tempout,radout,momout,teout,keout
  character(len=128) :: dir

  logical  ::plotstarpop,plotsinglestar

  plotstarpop=.false.
  plotsinglestar=.true.
  !debug_lkup=.true.

  ! Read run parameters
  call read_params

  IF (plotstarpop) THEN
  
     ! Open diagnostic file
     open(unit=20,file='teststarpop.dat')
     
     ! Debug the lookup file
     
     ! SAM GEEN HACK - TEST WIND PARAMETERS
     call setup_starpop
     do ageIn=1d-7,20d0,1d-2
        ! Input parameters: mass, age, metallicity, speedout, masslossout
        call starpop_values(1.0d0, ageIn, 1.5d-3, &
             spdout, mlout, tempout, radout)
        write(20,*)ageIn,mlout,tempout
     end do
     call cleanup_starpop
     close(20)

  ENDIF


  IF (plotsinglestar) THEN

     ! Open diagnostic file
     open(unit=20,file='testsinglestar.dat')
     !open(unit=30,file='testsinglestar2.dat')
     
     ! Debug the lookup file
      debug_lkup=.true.
     
     ! SAM GEEN HACK - TEST WIND PARAMETERS
     write(*,*)'Gamma = ',gamma
     dir = '.'
     call setup_single_star(dir)
     do ageIn=0d0,20d0,1d-1
        ! Input parameters: mass, age, metallicity, speedout, masslossout
        call star_wind_values(15.0d0, ageIn, 1d-2, &
             mlout, momout, keout, teout, tempout)
        write(20,'(100(1d14.4))')ageIn,mlout,momout/1d51,keout/1d51,teout/1d51,&
             tempout
     end do
     call cleanup_single_star
     close(20)

  ENDIF

  !close(30)
  ! Start time integration
  !call adaptive_loop

end program ramses
