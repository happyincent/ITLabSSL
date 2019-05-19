DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

OUTDIR=$DIR/config

mkdir -p $OUTDIR

BASE=(edge.yml ffmpeg.yml)

for FILE in "$@"; do
    echo "Gernerating ymls from config: $FILE ..."

    NODE_NAME=$(cat $FILE | jq '.NODE_NAME' | xargs)
    rm -f $OUTDIR/[$NODE_NAME]*.yml

    cat $FILE | jq -r '.DEVICES' | jq -c '.[]' | while read i; do

        id=$(echo $i | jq '.id' | xargs)
        token=$(echo $i | jq '.token' | xargs)
        
        for f in "${BASE[@]}"; do
            sed "\
                s|\${NODE_NAME}|${NODE_NAME}|g; \
                s|\${id}|${id}|g; \
                s|\${token}|${token}|g" \
                $DIR/$f > $OUTDIR/${NODE_NAME}_${id}-$f
        
            # For VM* use live555 rtsp proxy server
            if [[ ${id} = VM* ]] && [[ $f = ffmpeg.yml ]] ; then
                sed -i "s|\${RTSP_URI}|\${RTSP_PROXY_URI}|;" $OUTDIR/${NODE_NAME}_${id}-$f
            fi
        done

    done
done