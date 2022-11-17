IP=$(ifconfig eth0 | awk '/inet/ { print $2 }')
echo $IP

cd /root/LivingLab-CCS/server

# Check db container connection
while :
do
	# Check db container connection via ping cmd
	ping -c1 cms-main-db > /dev/null 2>&1
	if [ $? -eq 0 ];then # if cms-main-db container connected,
		sleep 7s
		python3 manage.py migrate # migrate database
		break # and brack while loop
	else
		echo "else"
	fi
done

# Create superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', '20121208')" | python3 manage.py shell

# Add admin user to custom user


# Start server
python3 manage.py runserver $IP:8000

# cd /root/LivingLab-CCS/server/ContentDownloadServer

# python3 ftpMediaDownloadServer.py &
