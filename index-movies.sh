#!/bin/bash -eux

curl -O https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/samples/sample-movies.zip
rm -rf sample-movies.bulk __MACOSX
unzip sample-movies.zip
echo "" >> sample-movies.bulk
curl -XPOST -k -u admin:admin "https://localhost:9200/_bulk" --data-binary @sample-movies.bulk -H 'Content-Type: application/x-ndjson'
