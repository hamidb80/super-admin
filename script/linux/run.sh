source "./script/linux/config.sh"

# TODO: add optional open new termianl or run direectly
# TODO: add optional run server or client or both

# open server
gnome-terminal -e "$pythonalias server/app.py"
# open client
gnome-terminal -e "$pythonalias client/app.py"