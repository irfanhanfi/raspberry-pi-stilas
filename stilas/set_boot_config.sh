#!/bin/bash

set_config_var() {
  lua - "$1" "$2" "$3" <<EOF > "$3.bak"
local key=assert(arg[1])
local value=assert(arg[2])
local fn=assert(arg[3])
local file=assert(io.open(fn))
local made_change=false
for line in file:lines() do
  if line:match("^#?%s*"..key.."=.*$") then
    line=key.."="..value
    made_change=true
  end
  print(line)
end

if not made_change then
  print(key.."="..value)
end
EOF
mv "$3.bak" "$3"
}


CONFIG_PATH=/boot/config.txt
[ -e $CONFIG_PATH ] || touch $CONFIG_PATH

set_config_var "$1" "$2" $CONFIG_PATH

#~ if [ "$1" -eq 0 ]; then # disable camera
	#~ set_config_var start_x 0 $CONFIG_PATH
	#~ sed $CONFIG_PATH -i -e "s/^startx/#startx/"
	#~ sed $CONFIG_PATH -i -e "s/^start_file/#start_file/"
	#~ sed $CONFIG_PATH -i -e "s/^fixup_file/#fixup_file/"
#~ else # enable camera
    #~ set_config_var start_x 1 $CONFIG_PATH
    #~ CUR_GPU_MEM=$(get_config_var gpu_mem $CONFIG_PATH)
    #~ if [ -z "$CUR_GPU_MEM" ] || [ "$CUR_GPU_MEM" -lt 128 ]; then
      #~ set_config_var gpu_mem 128 $CONFIG_PATH
    #~ fi
    #~ sed $CONFIG_PATH -i -e "s/^startx/#startx/"
    #~ sed $CONFIG_PATH -i -e "s/^fixup_file/#fixup_file/"
#~ fi
