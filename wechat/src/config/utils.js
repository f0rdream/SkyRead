export const timePY2JS = (old) => {
  let newDate = ''
  old.split(/-|T|Z/).forEach(item => { newDate += `${item} ` })
  return new Date(newDate)
}
export const timeJS2PY = (old) => {
  let newDate = ''
  old = new Date(old)
  newDate = `${old.getFullYear()}-${old.getMonth()}-${old.getDate()}T${old.getHours()}:${old.getMinutes()}:${old.getSeconds()}Z`
  return newDate
}
