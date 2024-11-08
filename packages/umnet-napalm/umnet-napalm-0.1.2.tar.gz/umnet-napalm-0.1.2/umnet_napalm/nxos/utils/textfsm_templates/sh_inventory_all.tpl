Value NAME (".+"|\S+)
Value DESC (".+"|\S+)
Value PID (\S+)
Value SN (\S+)

Start
  ^NAME: ${NAME},\s+DESCR:\s+${DESC}
  ^PID:\s+,\s+VID:.+,\s+SN:\s+${SN} -> Record
  ^PID: ${PID}\s+,\s+VID:.+,\s+SN:\s+${SN} -> Record