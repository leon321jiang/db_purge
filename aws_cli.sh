aws lambda invoke \
--function-name item_purge_lambda \
--payload '{"DB_ID": "id3"}' \
response.json
