export const checkTcUpdate = function(tcomparison, prevtcomparison, season, prevseason){
  /* this is to check if we have to fetch data from rest */
  var mupdate = false
  if (tcomparison !== prevtcomparison && season !== 0) {
    mupdate = true
  }
  if (season !== prevseason && season !== 0){
    mupdate = true
  }
  return mupdate
}
