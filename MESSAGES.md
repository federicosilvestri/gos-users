# Go Out Safe - Messages

This table lists all messages sent to RabbitMQ broker. 

|Event                 | Key             | Body                  |
|:---------------------|:----------------|:----------------------|
|A customer is deleted |CUSTOMER_DELETION|`{user_id='<user_id>'}`|
|An operator is deleted|OPERATOR_DELETION|`{user_id='<user_id>'}`|