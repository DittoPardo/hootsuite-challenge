container="$1"
if [ -z $container ]; then
    container=hsc_web
fi

docker exec -it $container bash
