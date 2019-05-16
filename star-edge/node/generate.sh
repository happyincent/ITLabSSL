# NODE_NAME=TX2
# DEVICES=(\
#     TX2_0 \
# )
# TOKENS=(\
#     8a88de1a-76ab-4d38-ba44-de4303918f4f \
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
    fea16d76-3500-4d29-84d5-67201c154bf8 \
    6fd52eb2-df01-4772-b855-80283797e690 \
)

# NODE_NAME=RPi
# DEVICES=(\
#     RPi_0 \
# )
# TOKENS=(\
#     f1a05c9f-87d7-4618-9831-47fb1aa2507a \
# )

##################################################

if [[ -z "$NODE_NAME" ]] || [[ -z "$DEVICES" ]] || [[ -z "$TOKENS" ]]; then
    echo Empty \$NODE_NAME or \$DEVICES or \$TOKENS
    exit 1
fi

rm [!_][$NODE_NAME]*.yml

FILES=(edge.yml ffmpeg.yml)

for i in "${!DEVICES[@]}"; do
    for f in "${FILES[@]}"; do
        sed "\
            s|\${NODE_NAME}|${NODE_NAME}|g; \
            s|\${DEVICE}|${DEVICES[$i]}|g; \
            s|\${TOKEN}|${TOKENS[$i]}|g" \
            _$f > ${NODE_NAME}_${DEVICES[$i]}-$f
    
        if [[ ${DEVICES[$i]} = VM* ]] && [[ $f = ffmpeg.yml ]] ; then
            sed -i "s|\${RTSP_URI}|\${RTSP_PROXY_URI}|;" ${NODE_NAME}_${DEVICES[$i]}-$f
        fi
    done
done