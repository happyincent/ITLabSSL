DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

OUTDIR=$DIR/yml

mkdir -p $OUTDIR

BASE_YMLS=(edge.yml ffmpeg.yml)

for JSON in "$@"; do
    echo "Gernerating yml from config: $JSON ..."

    NODE_NAME=$(cat $JSON | jq '.NODE_NAME' | xargs)
    rm -f $OUTDIR/$NODE_NAME*.yml

    cat $JSON | jq -r '.DEVICES' | jq -c '.[]' | while read i_device; do

        id=$(echo $i_device | jq '.id' | xargs)
        token=$(echo $i_device | jq '.token' | xargs)
        rtsp_uri=$(echo $i_device | jq '.rtsp_uri' | xargs)
        postinfo_timetout=$(echo $i_device | jq '.postinfo_timetout' | xargs)
        serial_port=$(echo $i_device | jq '.serial_port' | xargs)
        serial_baud=$(echo $i_device | jq '.serial_baud' | xargs)
        
        for YML in "${BASE_YMLS[@]}"; do
            sed "\
                s|\${NODE_NAME}|${NODE_NAME}|g; \
                s|\${id}|${id}|g; \
                s|\${token}|${token}|g; \
                s|\${postinfo_timetout}|${postinfo_timetout}|g; \
                s|\${serial_port}|${serial_port}|g; \
                s|\${serial_baud}|${serial_baud}|g; \
                s|\${rtsp_uri}|${rtsp_uri}|g;" \
                $DIR/$YML > $OUTDIR/${NODE_NAME}_${id}-$YML
        done

    done
done