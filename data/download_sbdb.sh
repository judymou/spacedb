#!/bin/bash -e

pushd $(dirname $0) &>/dev/null

curl -v 'https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=full_name,pdes,name,class,neo,pha,moid,moid_jup,epoch,e,a,q,i,om,w,ma,tp,per,n,ad,first_obs,last_obs,n_obs_used,H,M1,diameter,density,extent,rot_per,GM,pole,albedo,BV,UB,IR,spec_T,spec_B' -o rawdata/sbdb.json
gzip -f rawdata/sbdb.json

popd &>/dev/null
