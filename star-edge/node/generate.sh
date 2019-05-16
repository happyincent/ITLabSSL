# NODE_NAME=TX2
# DEVICES=(\
#     ncku_1 \
#     TX2_0 \
# )
# TOKENS=(\
#     4c499276-db27-4fce-a2bf-292dc19641a5 \
#     a5d36f41-7892-46f8-a290-275313bcd920 \
# )

NODE_NAME=VM0
DEVICES=(\
    VM0_0 \
    VM0_1 \
    VM0_2 \
    VM0_3 \
    VM0_4 \
    VM0_5 \
    VM0_6 \
    VM0_7 \
    VM0_8 \
    VM0_9 \
    VM0_10 \
    VM0_11 \
    VM0_12 \
    VM0_13 \
    VM0_14 \
    VM0_15 \
)
TOKENS=(\
    d1b67884-54e6-4d90-9b82-7eb62b440d98 \
    96f6c0a6-a349-40bf-8388-6f6be6354810 \
    ae6d3949-bb96-478d-afda-4d08d80a2d9a \
    c2d153f2-180c-40b6-a7e1-f95d4b81f23c \
    91584ea8-ae3d-4bf2-bd3c-a6192887801b \
    2fe2d423-2445-4897-a196-8cfd27e6d132 \
    39159d54-8fbf-4002-b3c9-bfabf4231ed9 \
    a91efb2c-38d0-4693-93f8-77887a0771c6 \
    7081800d-223a-4c4b-aea3-3cc7921672c4 \
    aea79365-411c-449b-a68a-8a5edf78158a \
    605f3092-72c8-4ee5-9d5d-339df02b0aab \
    afa6e2d4-9f4d-438d-aaf3-589529f5c7d7 \
    868b4fd9-fe5a-4bed-a25d-bced14912e10 \
    8c596179-5017-4925-93c3-3b219a9cd7cd \
    5a041e68-c787-4325-a7db-5d4ddce8afb9 \
    5db90c58-ed03-4edf-8b72-89d3fcbf2018 \
)

# NODE_NAME=RPi
# DEVICES=(\
#     ncku_2 \
#     RPi_0 \
# )
# TOKENS=(\
#     f64a2406-2eff-4301-b594-d07621e988e9 \
#     31243347-3a25-499b-a584-61623dff1168 \
# )

##################################################

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ -z "$NODE_NAME" ]] || [[ -z "$DEVICES" ]] || [[ -z "$TOKENS" ]]; then
    echo Empty \$NODE_NAME or \$DEVICES or \$TOKENS
    exit 1
fi

rm $DIR/[!_][$NODE_NAME]*.yml

FILES=(edge.yml ffmpeg.yml)

for i in "${!DEVICES[@]}"; do
    for f in "${FILES[@]}"; do
        sed "\
            s|\${NODE_NAME}|${NODE_NAME}|g; \
            s|\${DEVICE}|${DEVICES[$i]}|g; \
            s|\${TOKEN}|${TOKENS[$i]}|g" \
            $DIR/_$f > $DIR/${NODE_NAME}_${DEVICES[$i]}-$f
    
        if [[ ${DEVICES[$i]} = VM* ]] && [[ $f = ffmpeg.yml ]] ; then
            sed -i "s|\${RTSP_URI}|\${RTSP_PROXY_URI}|;" $DIR/${NODE_NAME}_${DEVICES[$i]}-$f
        fi
    done
done