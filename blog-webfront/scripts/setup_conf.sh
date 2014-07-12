CONFIG_FILES=( blog.nginx )
CERT_FILE=xxx.com.crt
KEY_FILE=xxx.com.key

ENABLE_CONFIG=/etc/nginx/sites-enabled
SSL_DIR=/etc/nginx/ssl

for CONFIG_FILE in ${CONFIG_FILES[@]}; do
	cp -lf ${CONFIG_FILE} ${ENABLE_CONFIG}/${CONFIG_FILE/.nginx/} 
done

mkdir -p $SSL_DIR
cp $CERT_FILE $SSL_DIR/
cp $KEY_FILE $SSL_DIR/

if [ -f "${ENABLE_CONFIG}/default" ] ; then
    rm "${ENABLE_CONFIG}/default"
fi
