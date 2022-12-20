echo "recording startet" > runLog.log

lastDate=0

while true
do
    (date +%s) - lastDate >> runLog.log
    lastDate = (date +%s)
    sleep 10
done

