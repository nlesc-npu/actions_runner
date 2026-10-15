VIDEOGID=$(getent group video | cut -d \: -f 3)
RENDERGID=$(getent group render | cut -d \: -f 3)
docker build --build-arg VIDEOGID=${VIDEOGID} --build-arg RENDERGID=${RENDERGID} . -t rocm-xrt-gh:latest

