NODE_NAME=TX2
DEVICES=(\
    TX2_0 \
)
TOKENS=(\
    8a88de1a-76ab-4d38-ba44-de4303918f4f \
)

# NODE_NAME=VM0
# DEVICES=(\
#     VM0_0 \
#     VM0_1 \
#     VM0_2 \
#     VM0_3 \
# )
# TOKENS=(\
#     d1b67884-54e6-4d90-9b82-7eb62b440d98 \
#     96f6c0a6-a349-40bf-8388-6f6be6354810 \
#     ae6d3949-bb96-478d-afda-4d08d80a2d9a \
#     c2d153f2-180c-40b6-a7e1-f95d4b81f23c \
# )

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
    done
done