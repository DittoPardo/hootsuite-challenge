container="$1"
if [ -z $container ]; then
    container=hsc_web
fi
docker logs -f --tail=100 $container
