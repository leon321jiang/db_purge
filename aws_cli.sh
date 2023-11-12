aws lambda invoke \
--function-name item_purge_lambda \
--payload '{"db_name": "id3"}' \
response.json
