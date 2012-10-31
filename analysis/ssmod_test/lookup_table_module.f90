! A generic lookup table almost-object
! TODO: Make find_valuesN consistent with find_values2
!       (i.e. works with 
! Sam Geen, June 2010
MODULE lookup_table_module

  use amr_parameters

  implicit none

  private   ! default

  public setup_table, clear_table, find_value
  public find_value3, find_value2, find_value1 
  public lookup_table, debug_lkup

  !------------------------------------------------------------------------
  ! The table structure (should really be an object but hey ho):
  ! Contains up to 4 dimensions (more and you have to re-code it)
  ! TODO: Allow generic types in the table (if possible in FORTRAN)
  integer, parameter         :: TDIMS = 4
  logical                    :: debug_lkup=.false.
  type lookup_table
     ! Table's filename
     character(len=128)                    :: filename
     ! The table's data
     real(dp),dimension(:,:,:,:),pointer   :: table
     ! The size in each dimension
     integer*4,  dimension(TDIMS)          :: size
     ! Values along each axis
     real(dp), dimension(:), pointer       :: axis1
     real(dp), dimension(:), pointer       :: axis2
     real(dp), dimension(:), pointer       :: axis3
     real(dp), dimension(:), pointer       :: axis4
     ! Number of dimensions
     integer*4                             :: num_dims
     ! Does the table contain data?
     logical                   :: contains_data  
  end type lookup_table
  
CONTAINS
!************************************************************************
SUBROUTINE setup_table(table, filename)
!------------------------------------------------------------------------ 
  type(lookup_table) :: table
  character(len=*) :: filename

  table%filename = filename

END SUBROUTINE setup_table

!************************************************************************
! Reads the table
! This isn't public. We shouldn't need to read unless the code says so.
SUBROUTINE read_table(table)
  use amr_commons
  type(lookup_table) :: table
  integer*4          :: s1, s2, s3, s4
  logical            :: ok

  IF (.not.(table%contains_data)) THEN
     write(*,*)"Reading lookup table "//TRIM(table%filename)
     inquire(file=TRIM(table%filename), exist=ok)
     if(.not. ok)then
        if(myid.eq.1) then 
           write(*,*)'Cannot read file...'
           write(*,*)'File '//TRIM(table%filename)//' not found'
        endif
        call clean_stop
     end if
     open(unit=10,file=TRIM(table%filename),form='unformatted')
     ! Read the table's number of dimensions (can be up to 4)
     if (debug_lkup) write(*,*)"READING NDIMS"
     read(10)table%num_dims
     ! Read the table size array
     if (debug_lkup) write(*,*)"AXIS SIZES: "
     read(10)table%size(1:TDIMS)
     s1 = table%size(1)
     s2 = table%size(2)
     s3 = table%size(3)
     s4 = table%size(4)
     if (debug_lkup) write(*,*)s1, s2, s3, s4
     ! Read the axis values
     allocate(table%axis1(s1))
     allocate(table%axis2(s2))
     allocate(table%axis3(s3))
     allocate(table%axis4(s4))
     if (debug_lkup) write(*,*)"READING AXES"
     read(10)table%axis1
     read(10)table%axis2
     read(10)table%axis3
     read(10)table%axis4
     !if (debug_lkup) then write(*,*)"Axes: "
     !if (debug_lkup) then write(*,*)table%axis1
     !if (debug_lkup) then write(*,*)table%axis2
     !if (debug_lkup) then write(*,*)table%axis3
     !if (debug_lkup) then write(*,*)table%axis4
     ! Read the table
     allocate(table%table(s1,s2,s3,s4))
     if (debug_lkup) write(*,*)"READING TABLE"
     read(10)table%table
     close(10)
     if (debug_lkup) write(*,*)"DONE READING"
     ! Set contains_data flag in table
     table%contains_data = .true.
     write(*,*)"Done reading table"
  END IF
END SUBROUTINE read_table

SUBROUTINE clear_table(table)
! Clear out data in table
  type(lookup_table) :: table

  IF (debug_lkup) write(*,*)"Clearing out lookup table "//TRIM(table%filename)
  IF (table%contains_data) THEN
     ! Deallocate data
     deallocate(table%axis1)
     deallocate(table%axis2)
     deallocate(table%axis3)
     deallocate(table%axis4)
     deallocate(table%table)
     ! Reset counters
     table%size(1) = 0
     table%size(2) = 0
     table%size(3) = 0
     table%size(4) = 0
     table%num_dims = 0
     ! Reset table contains_data flag
     table%contains_data = .false.
  END IF
END SUBROUTINE clear_table

!************************************************************************
! TODO: Interpolate between values
! TODO: Do extrapolation outside data range
SUBROUTINE find_value(table, v1, v2, v3, v4, outval)
! Find result in array from input coordinates (interpolate to nearest values)
! v[1,2,3,4] - Input coordinates
! outval     - Output value
  type(lookup_table)       :: table
  real(dp), intent(in)     :: v1, v2, v3 , v4
  real(dp), intent(out)    :: outval
  integer                  :: i1, i2, i3, i4

  IF (debug_lkup) &
       write(*,*)"Finding value in lookup table "//TRIM(table%filename)
  ! Check the table is read and if not, read it
  IF (.not.(table%contains_data)) THEN 
     call read_table(table)
  END IF
  ! Get indices nearest the inputted values (now done by trili
  !call find_nearest_indices(table, v1, v2, v3, v4, i1, i2, i3, i4)
  ! Interpolate between the values
  call trilin_interpolate(table, v1, v2, v3, v4, outval)
  !write(*,*)"Getting output value at indices", i1, i2, i3, i4
  !outval = table%table(i1,i2,i3,i4)
END SUBROUTINE find_value

! The functions below do the same thing but ignore the last values
! You can optimise these if you really want to
SUBROUTINE find_value3(table, v1, v2, v3, outval)
! Find value in array (interpolate to nearest values)
  type(lookup_table)   :: table
  real(dp)             :: v1, v2, v3, v4, outval
  v4 = 1d0
  IF (debug_lkup) &
       write(*,*)"Finding value in lookup table "//TRIM(table%filename)
  call find_value(table, v1, v2, v3, v4, outval)
END SUBROUTINE find_value3

SUBROUTINE find_value2(table, v1, v2, outval)
! Find value in array (interpolate to nearest values)
  type(lookup_table)   :: table
  real(dp)             :: v1, v2, v3, v4, outval
  v3 = 1d0
  v4 = 1d0
  IF (debug_lkup) &
       write(*,*)"Finding value in lookup table "//TRIM(table%filename)
  !call find_value(table, v1, v2, v3, v4, outval)  
  IF (.not.(table%contains_data)) THEN 
     call read_table(table)
  END IF
  call bilin_interpolate(table, v1, v2, outval)
END SUBROUTINE find_value2

SUBROUTINE find_value1(table, v1, outval)
! Find value in array (interpolate to nearest values)
  type(lookup_table)   :: table
  real(dp)             :: v1, v2, v3, v4, outval
  v2 = 1d0
  v3 = 1d0
  v4 = 1d0
  IF (debug_lkup) &
       write(*,*)"Finding value in lookup table "//TRIM(table%filename)
  call find_value(table, v1, v2, v3, v4, outval)
END SUBROUTINE find_value1

!************************************************************************
SUBROUTINE find_nearest_indices(table, v1, v2, v3, v4, io1, io2, io3, io4)
! Find nearest indices to the value (will always pick below the value)
  type(lookup_table) :: table
  real(dp)           :: v1,  v2,  v3,  v4
  integer            :: io1, io2, io3, io4
  
  IF (debug_lkup) &
       write(*,*), "Find nearest indices in table "//TRIM(table%filename)
  call find_in_axis(table%axis1,v1,io1,table%size(1))
  call find_in_axis(table%axis2,v2,io2,table%size(2))
  call find_in_axis(table%axis3,v3,io3,table%size(3))
  call find_in_axis(table%axis4,v4,io4,table%size(4))
END SUBROUTINE find_nearest_indices

!************************************************************************
SUBROUTINE find_in_axis(axis, value, io, numaxis)
! Find a value in a given axis
! axis    - array containing values for this axis of the table
! value   - value along the axis to find
! io      - output coordinate on axis
! numaxis - number of elements in the axis
  real(dp)                         :: value
  integer                          :: io, numaxis
  real(dp), dimension(:), pointer  :: axis

  IF (debug_lkup) write(*,*)"Finding value in axis between ", &
       axis(1), " and ", axis(numaxis)
  ! Fix the inputted value to prevent bad extrapolation
  value = MIN(value,axis(numaxis))
  value = MAX(value,axis(1))
  io=1
  ! Find the index just above the value chosen
  ! Check: 1) value in axis is too small still and 
  !        2) that we haven't overflowed the array
  ! TODO: Add bisection/binary search (or even a tree? nah)
  IF (numaxis.gt.1) THEN
     DO WHILE ((axis(io+1).lt.value).and.(io.le.numaxis-1))
        io=io+1
     END DO
  ENDIF
  ! Check to see that we haven't fucked up the indices
  io = MIN(io,numaxis)
  io = MAX(io,1)
  ! Debug message
  IF (debug_lkup) &
       write(*,*)"Value chosen: ", axis(io), " at ",io,&
       "; (Value inputted: ", value, ")"
END SUBROUTINE find_in_axis

! Bilinear interpolation *only* (i.e. only if table is 2D!)
SUBROUTINE bilin_interpolate(table, v1, v2, outval)
  ! Trilinear interpolation on values v1,v2,v3
  ! gi = distance from nearest grid cell under vi (between 0 and 1) 
  type(lookup_table)       :: table
  real(dp), intent(in)     :: v1,v2
  real(dp)                 :: v1t,v2t,v3t,v4t
  real(dp), intent(out)    :: outval
  real(dp)                 :: x0,x1, y0,y1
  integer                  :: i1, i2, i3, i4
  
  IF (debug_lkup) &
       write(*,*)"Bilinear interpolation"
  ! Get the lowest indices closest to the object
  v1t = v1
  v2t = v2
  v3t = 1d0 
  v4t = 1d0
  call find_nearest_indices(table, v1t, v2t, v3t, v4t, i1, i2, i3, i4)
  
  ! Get length along axes
  x1 = (v1t - table%axis1(i1)) / (table%axis1(i1+1) - table%axis1(i1))
  y1 = (v2t - table%axis2(i2)) / (table%axis2(i2+1) - table%axis2(i2))
  x0 = 1d0-x1
  y0 = 1d0-y1

  ! Get interpolated value
  ! We need each corner of the grid cell's contribution
  ! Think of this as like counting in binary in terms of what we add
  ! Unless that's entirely not helpful, in which case don't
  outval = &
       x0*y0 * table%table(i1  ,i2  ,i3,i4) + &
       x1*y0 * table%table(i1+1,i2  ,i3,i4) + &
       x0*y1 * table%table(i1  ,i2+1,i3,i4) + &
       x1*y1 * table%table(i1+1,i2+1,i3,i4)
  ! That's it. LEAVE NOW.
END SUBROUTINE bilin_interpolate

! Trilinear interpolation *only* (i.e. only if table is 3D!)
! TODO: DO 4D INTERPOLATION
SUBROUTINE trilin_interpolate(table, v1, v2, v3, v4, outval)
  ! Trilinear interpolation on values v1,v2,v3
  ! gi = distance from nearest grid cell under vi (between 0 and 1) 
  type(lookup_table)       :: table
  real(dp)                 :: v1,v2,v3,v4
  real(dp)                 :: v1t,v2t,v3t,v4t
  real(dp), intent(out)    :: outval
  real(dp)                 :: x0,x1, y0,y1, z0,z1
  integer                  :: i1, i2, i3, i4
  
  IF (debug_lkup) &
       write(*,*)"Trilinear interpolation"
  ! Get the lowest indices closest to the object
  v1t = v1
  v2t = v2
  v3t = v3
  v4t = v4
  call find_nearest_indices(table, v1t, v2t, v3t, v4t, i1, i2, i3, i4)
  
  ! Get length along axes
  x1 = (v1t - table%axis1(i1)) / (table%axis1(i1+1) - table%axis1(i1))
  y1 = (v2t - table%axis2(i2)) / (table%axis2(i2+1) - table%axis2(i2))
  z1 = (v3t - table%axis3(i3)) / (table%axis3(i3+1) - table%axis3(i3))
  x0 = 1d0-x1
  y0 = 1d0-y1
  z0 = 1d0-z1

  ! Get interpolated value
  ! We need each corner of the grid cell's contribution
  ! Think of this as like counting in binary in terms of what we add
  ! Unless that's entirely not helpful, in which case don't
  outval = &
       x0*y0*z0 * table%table(i1  ,i2  ,i3  ,i4) + &
       x1*y0*z0 * table%table(i1+1,i2  ,i3  ,i4) + &
       x0*y1*z0 * table%table(i1  ,i2+1,i3  ,i4) + &
       x1*y1*z0 * table%table(i1+1,i2+1,i3  ,i4) + &
       x0*y0*z1 * table%table(i1  ,i2  ,i3+1,i4) + &
       x1*y0*z1 * table%table(i1+1,i2  ,i3+1,i4) + &
       x0*y1*z1 * table%table(i1  ,i2+1,i3+1,i4) + &
       x1*y1*z1 * table%table(i1+1,i2+1,i3+1,i4)
  ! That's it. LEAVE NOW.
END SUBROUTINE trilin_interpolate

END MODULE lookup_table_module
