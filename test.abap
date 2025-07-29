DATA: lv_number TYPE i,
      lv_is_prime TYPE abap_bool VALUE abap_true,
      lv_divisor  TYPE i.

DO 200 TIMES.
  lv_number = sy-index.
  lv_is_prime = abap_true.

  IF lv_number < 2.
    lv_is_prime = abap_false.
  ELSE.
    DO lv_divisor = 2 TO lv_number - 1.
      IF lv_number MOD lv_divisor EQ 0.
        lv_is_prime = abap_false.
        EXIT.
      ENDIF.
    ENDDO.
  ENDIF.

  IF lv_is_prime = abap_true.
    WRITE: / lv_number.
  ENDIF.
ENDDO.