case "$NODE_ENV" in
    production )
        npm run build
        ;;
    development )
        exec npm start
        ;;
esac