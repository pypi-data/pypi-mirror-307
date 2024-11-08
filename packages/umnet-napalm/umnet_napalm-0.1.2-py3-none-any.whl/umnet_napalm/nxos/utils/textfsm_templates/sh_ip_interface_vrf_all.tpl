Value Filldown VRF (\S+)
Value INTERFACE (\S+)
Value IP_ADDRESS (\d+.\d+.\d+.\d+)
Value PREFIXLEN (\d+)
Value PROTOCOL_STATE (\S+)
Value LINK_STATE (\S+)
Value ADMIN_STATE (\S+)
Value MTU (\d+)

Start
  ^IP Interface Status for VRF "${VRF}"
  ^${INTERFACE}, Interface status: ${PROTOCOL_STATE}/${LINK_STATE}/${ADMIN_STATE}, iod: \d+,
  ^\s+IP address: ${IP_ADDRESS}, IP subnet: \d+.\d+.\d+.\d+\/${PREFIXLEN}( secondary)* route-preference
  ^\s+IP MTU: ${MTU} bytes -> Record

EOF
