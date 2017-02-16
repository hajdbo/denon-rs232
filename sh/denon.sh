stty -F /dev/ttyS0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts hupcl
echo -ne PWON\\r > /dev/ttyS0

# PWON
# PWSTANDBY
