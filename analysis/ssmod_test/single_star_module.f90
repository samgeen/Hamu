MODULE single_star_module

! Obtains values for stellar winds based on:
! Stellar mass (Msolar)
! Stellar age (Myears)
! Stellar metallicity (absolute metallicity, so Zsolar = 0.02)
! Outputs (all cumulative from age=0):
! Mass loss (Msolar)
! Momentum in g.cm/s
! Energy (kinetic, thermal) in ergs
! Created by Sam Geen, June 2010
! Edited by Sam Geen, December 2010

! Use lookup table module for speed, mass-loss arrays
use amr_parameters
use hydro_parameters
use lookup_table_module

implicit none

public

type(lookup_table) :: massloss_table
type(lookup_table) :: momentum_table
type(lookup_table) :: kenergy_table ! kinetic
type(lookup_table) :: tenergy_table ! thermal

CONTAINS

!************************************************************************
! Sets up the tables, and then clears them (e.g. on program exit)
SUBROUTINE setup_single_star(dir)
  character(len=128)              ::dir,filename
  write(filename,'(a,a)') trim(dir),'/starwind_masslosstable.dat'
  call setup_table(massloss_table, filename)
  write(filename,'(a,a)') trim(dir),'/starwind_momentumtable.dat'
  call setup_table(momentum_table, filename)
  write(filename,'(a,a)') trim(dir),'/starwind_kenergytable.dat'
  call setup_table(kenergy_table, filename)
  write(filename,'(a,a)') trim(dir),'/starwind_tenergytable.dat'
  call setup_table(tenergy_table, filename)
END SUBROUTINE setup_single_star

SUBROUTINE cleanup_single_star
  call clear_table(massloss_table)
  call clear_table(momentum_table)
  call clear_table(kenergy_table)
  call clear_table(tenergy_table)
END SUBROUTINE cleanup_single_star

!************************************************************************
! Finds the wind parameters for a given star (mass, age, metallicity)
! Note: mass is *initial* mass, *not* current mass
! Values from Padova model (e.g. Girardi et al 2008)
! Inputs:
! Stellar mass (Msolar)
! Stellar age (Myears)
! Stellar metallicity (absolute metallicity, so Zsolar = 0.02)
! Outputs (all cumulative from age=0):
! Mass loss (Msolar)
! Momentum in g.cm/s
! Energy (kinetic, thermal) in ergs
! Sam Geen, June 2010
SUBROUTINE star_wind_values(mass, age, metal, masslossout, &
                            momentumout, kenergyout, tenergyout)
  real(dp)::mass, age, metal,logage
  real(dp),intent(out)::masslossout, momentumout, kenergyout, tenergyout
  real(dp)::ageInternal

  ! If age is zero, set to a very low value to prevent confusing the log fn
  if (age.eq.0d0) then
     ageInternal = 1d-20
  else
     ageInternal = age
  end if
  ! Lookup table contains time data based on log(years)
  ! Convert input time in Myr --> log(yr)
  logage = DLOG10(ageInternal)+6d0
  ! Find values in the tables
  call find_value3(massloss_table, mass, logage, metal, masslossout)
  call find_value3(momentum_table, mass, logage, metal, momentumout)
  call find_value3(kenergy_table,   mass, logage, metal, kenergyout)
  call find_value3(tenergy_table,   mass, logage, metal, tenergyout)
  ! Scale thermal energy by degrees of freedom
  tenergyout = tenergyout / (gamma - 1d0)
  ! Uh, yeah. That's basically it.

END SUBROUTINE star_wind_values

!************************************************************************
! How long before a star croaks it, and what is its final mass and energy?
! Note: "mass" is *initial* mass, *not* current mass
! Mass in Msolar, time in Myr, energy in 10^51 ergs
! Values from Smartt et al 2009, Kovetz et al 2009
SUBROUTINE star_snparams(mass, metal, fmassout, lifetimeout, snenergyout)
  ! HACK! HACK! HORRIBLE HACK! ONLY VALUES FOR 15Msolar
  real(dp)::mass, metal
  real(dp),intent(out)::fmassout, lifetimeout, snenergyout
  ! HACK! HARD-CODED VALUES FOR STAR OF 15 Msolar
  fmassout = 1.5d0
  lifetimeout = 14.125d0
  snenergyout = 1.2d0 ! This is a total guess
END SUBROUTINE star_snparams

END MODULE
