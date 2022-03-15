# Make EDID

# Overview

Given an EDID, creates a bash snippet that will apply the EDID to the user's `/dev/video0` device.

This is for TinyPilot support use. Others are welcome to use it, but it's likely to not be very useful outside of TinyPilot.

# Requirements

* Python 3.9+

# Installation

```bash
mkdir -p ./venv && \
  virtualenv --python python3 ./venv && \
  . venv/bin/activate && \
  pip install --requirement requirements.txt && \
  pip install --requirement dev_requirements.txt && \
  ./hooks/enable_hooks
```

# Usage

## Create instructions for hex-formatted EDID

```bash
$ . venv/bin/activate
$ cat /tmp/edid.hex
00ffffffffffff0052628888008888882d1e0103800000780aee91a3544c99260f505400000001010101010101010101010101010101011d007251d01e206e285500c48e2100001e8c0ad08a20e02d10103e9600138e2100001e000000fc00546f73686962612d4832430a20000000fd003b3d0f2e0f1e0a2020202020200135020321434e041303021211012021a23c3d3e1f2309070766030c00300080e3007f8c0ad08a20e02d10103e9600c48e210000188c0ad08a20e02d10103e9600138e210000188c0aa01451f01600267c4300138e210000980000000000000000000000000000000000000000000000000000000000000000000000000000000028
$ cat /tmp/edid.hex | ./app/main.py
EDID="$(mktemp -d)/tc358743-edid.hex"
echo -ne "" | sudo tee "${EDID}" && \
  echo '00ffffffffffff0052628888008888882d1e0103' | sudo tee -a "${EDID}" && \
  echo '800000780aee91a3544c99260f50540000000101' | sudo tee -a "${EDID}" && \
  echo '0101010101010101010101010101011d007251d0' | sudo tee -a "${EDID}" && \
  echo '1e206e285500c48e2100001e8c0ad08a20e02d10' | sudo tee -a "${EDID}" && \
  echo '103e9600138e2100001e000000fc00546f736869' | sudo tee -a "${EDID}" && \
  echo '62612d4832430a20000000fd003b3d0f2e0f1e0a' | sudo tee -a "${EDID}" && \
  echo '2020202020200135020321434e04130302121101' | sudo tee -a "${EDID}" && \
  echo '2021a23c3d3e1f2309070766030c00300080e300' | sudo tee -a "${EDID}" && \
  echo '7f8c0ad08a20e02d10103e9600c48e210000188c' | sudo tee -a "${EDID}" && \
  echo '0ad08a20e02d10103e9600138e210000188c0aa0' | sudo tee -a "${EDID}" && \
  echo '1451f01600267c4300138e210000980000000000' | sudo tee -a "${EDID}" && \
  echo '0000000000000000000000000000000000000000' | sudo tee -a "${EDID}" && \
  echo '00000000000000000000000000000028' | sudo tee -a "${EDID}" && \
  sudo v4l2-ctl --device=/dev/video0 --set-edid=file="${EDID}" --fix-edid-checksums
```

## Create instructions for binary-formatted EDID

```bash
$ . venv/bin/activate
$ xxd /tmp/edid.bin
00000000: 00ff ffff ffff ff00 5262 8888 0088 8888  ........Rb......
00000010: 2d1e 0103 8000 0078 0aee 91a3 544c 9926  -......x....TL.&
00000020: 0f50 5400 0000 0101 0101 0101 0101 0101  .PT.............
00000030: 0101 0101 0101 011d 0072 51d0 1e20 6e28  .........rQ.. n(
00000040: 5500 c48e 2100 001e 8c0a d08a 20e0 2d10  U...!....... .-.
00000050: 103e 9600 138e 2100 001e 0000 00fc 0054  .>....!........T
00000060: 6f73 6869 6261 2d48 3243 0a20 0000 00fd  oshiba-H2C. ....
00000070: 003b 3d0f 2e0f 1e0a 2020 2020 2020 0135  .;=.....      .5
00000080: 0203 2143 4e04 1303 0212 1101 2021 a23c  ..!CN....... !.<
00000090: 3d3e 1f23 0907 0766 030c 0030 0080 e300  =>.#...f...0....
000000a0: 7f8c 0ad0 8a20 e02d 1010 3e96 00c4 8e21  ..... .-..>....!
000000b0: 0000 188c 0ad0 8a20 e02d 1010 3e96 0013  ....... .-..>...
000000c0: 8e21 0000 188c 0aa0 1451 f016 0026 7c43  .!.......Q...&|C
000000d0: 0013 8e21 0000 9800 0000 0000 0000 0000  ...!............
000000e0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000000f0: 0000 0000 0000 0000 0000 0000 0000 0028  ...............(
$ ./app/main.py -b -i /tmp/edid.bin
EDID="$(mktemp -d)/tc358743-edid.hex"
echo -ne "" | sudo tee "${EDID}" && \
  echo '00ffffffffffff0052628888008888882d1e0103' | sudo tee -a "${EDID}" && \
  echo '800000780aee91a3544c99260f50540000000101' | sudo tee -a "${EDID}" && \
  echo '0101010101010101010101010101011d007251d0' | sudo tee -a "${EDID}" && \
  echo '1e206e285500c48e2100001e8c0ad08a20e02d10' | sudo tee -a "${EDID}" && \
  echo '103e9600138e2100001e000000fc00546f736869' | sudo tee -a "${EDID}" && \
  echo '62612d4832430a20000000fd003b3d0f2e0f1e0a' | sudo tee -a "${EDID}" && \
  echo '2020202020200135020321434e04130302121101' | sudo tee -a "${EDID}" && \
  echo '2021a23c3d3e1f2309070766030c00300080e300' | sudo tee -a "${EDID}" && \
  echo '7f8c0ad08a20e02d10103e9600c48e210000188c' | sudo tee -a "${EDID}" && \
  echo '0ad08a20e02d10103e9600138e210000188c0aa0' | sudo tee -a "${EDID}" && \
  echo '1451f01600267c4300138e210000980000000000' | sudo tee -a "${EDID}" && \
  echo '0000000000000000000000000000000000000000' | sudo tee -a "${EDID}" && \
  echo '00000000000000000000000000000028' | sudo tee -a "${EDID}" && \
  sudo v4l2-ctl --device=/dev/video0 --set-edid=file="${EDID}" --fix-edid-checksums
```
