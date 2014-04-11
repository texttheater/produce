Desiderata
==========

* make requested files based on their dependencies
* don't do unneccesary work (use timestamps)
* intermediate files can be deleted later without affecting up-to-dateness

Target status taxonomy (draft)
==============================

 status
  error
   cyclic
    is_own_ddep
    has_ddep_with_status_cyclic
   missing_deps
    no_matching_rule
    has_ddep_with_status_missing_deps
  unavailable
   out_of_date
    task
    out_of_date_through_age
     has_ddep_with_status_existent_which_is_younger
     has_ddep_with_status_out_of_date
   nonexistant
  existant
   out_of_date
   up_to_date
