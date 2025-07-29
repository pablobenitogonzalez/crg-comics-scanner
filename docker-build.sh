docker build -t crg-comics-scanner .
docker save crg-comics-scanner:latest | gzip > crg-comics-scanner.tar.gz