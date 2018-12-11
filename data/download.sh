#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

cd rawdata

echo 'Downloading SBDB...'
curl 'https://ssd.jpl.nasa.gov/sbdb_query.cgi' -o sbdb.csv -H 'Origin: https://ssd.jpl.nasa.gov' -H 'Upgrade-Insecure-Requests: 1' -H 'DNT: 1' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryI5CMg9fifgJnfvc6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36' -H 'X-DevTools-Emulate-Network-Conditions-Client-Id: F64DB139B75061A6BE276315A7C5AC1D' -H 'Referer: https://ssd.jpl.nasa.gov/sbdb_query.cgi' --data-binary $'------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="obj_group"\r\n\r\nall\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="obj_kind"\r\n\r\nall\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="obj_numbered"\r\n\r\nall\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="OBJ_field"\r\n\r\n0\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="OBJ_op"\r\n\r\n0\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="OBJ_value"\r\n\r\n\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="ORB_field"\r\n\r\n0\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="ORB_op"\r\n\r\n0\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="ORB_value"\r\n\r\n\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="c_fields"\r\n\r\nAaAbAcAdAeAfAgAhAiAjAkAlAmAnAoApAqArAsAtAuAvAwAxAyAzBaBbBcBdBeBfBgBhBiBjBkBlBmBnBoBpBqBrBsBtBuBvBwBxByBzCaCbCcCdCeCfCgChCiCjCkClCmCnCoCpCqCrCsCtCuCvCw\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="table_format"\r\n\r\nCSV\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="max_rows"\r\n\r\n10\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="format_option"\r\n\r\ncomp\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name="query"\r\n\r\nGenerate Table\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nformat_option\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nfield_list\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nobj_kind\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nobj_group\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nobj_numbered\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nast_orbit_class\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\ntable_format\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nOBJ_field_set\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\nORB_field_set\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\npreset_field_set\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6\r\nContent-Disposition: form-data; name=".cgifields"\r\n\r\ncom_orbit_class\r\n------WebKitFormBoundaryI5CMg9fifgJnfvc6--\r\n' --compressed

echo 'Downloading close approaches...'
curl 'https://ssd-api.jpl.nasa.gov/cad.api?dist-max=10LD&date-min=2019-01-01&date-max=2100-01-01&sort=dist&fullname=true' -o close_approach.json

popd &>/dev/null