docker build -t crg-comics .
docker save crg-comics:latest | gzip > crg-comics.tar.gz