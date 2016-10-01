container="$1"
if [ -z $container ]; then
    container=hsc_web
fi
docker-compose -f docker-compose.yml -f debug.yml -f test.yml up -d && docker attach $container
