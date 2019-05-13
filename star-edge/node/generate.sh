# NODE_NAME=TX2
# DEVICES=(\
#     TX2_0 \
# )
# TOKENS=(\
#     bed7261b-d716-4615-9174-dcfebc1b0b64 \
# )

# NODE_NAME=VM0
# DEVICES=(\
#     VM0_0 \
#     VM0_1 \
#     VM0_2 \
# )
# TOKENS=(\
#     d1b67884-54e6-4d90-9b82-7eb62b440d98 \
#     96f6c0a6-a349-40bf-8388-6f6be6354810 \
#     ae6d3949-bb96-478d-afda-4d08d80a2d9a \
# )

NODE_NAME=RPi
DEVICES=(\
    RPi_0 \
)
TOKENS=(\
    3ff38357-44f0-436f-8457-5990070c5db5 \
)

##################################################

rm $NODE_NAME*.yml

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