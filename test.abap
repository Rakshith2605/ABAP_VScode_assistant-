SELECT * FROM VBAK INTO TABLE @DATA(lt_vbaks).
  IF sy-subrc NE 0.
    RAISE EXCEPTION TYPE cx_sy_open_sql_error
      EXPORTING
        textid = 'VBAK_SELECT_FAILED'.
  ENDIF.