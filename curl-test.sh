#!/bin/bash

post_name="hi"
post_email="example@gmail.com"
post_content="$RANDOM"

post=$(curl --request POST http://127.0.0.1:5000/api/timeline_post -d "name=$post_name&email=$post_email&content=$post_content")

posts=$(curl --request GET http://127.0.0.1:5000/api/timeline_post)

if echo "$posts" | grep -Fq "$post"; then
    echo "Post successfully added"
else
    echo "Post was not added"
fi

