drop table if exists raw.stg_messages;
create table raw.stg_messages as (
    with raw_message as (
        select
            uuid,
            id,
            message_type,
            direction,
            masked_addressees,
            masked_author,
            content,
            author_type,
            external_id,
            external_timestamp,
            masked_from_addr,
            is_deleted,
            last_status,
            TO_TIMESTAMP(last_status_timestamp, 'MM/DD/YYYY HH24:MI:SS')::timestamp as last_status_timestamp,
            rendered_content,
            source_type,
            TO_TIMESTAMP(inserted_at, 'MM/DD/YYYY HH24:MI:SS')::timestamp as inserted_at,
            TO_TIMESTAMP(updated_at, 'MM/DD/YYYY HH24:MI:SS')::timestamp as updated_at
        from raw.messages m 
    ),
    latest_message as (
        select *,
            case 
                WHEN ROW_NUMBER() OVER (PARTITION BY uuid ORDER BY inserted_at DESC) = 1 THEN 1 
                ELSE 0 
            end as is_latest
        from raw_message
    )select * from latest_message
);

ALTER TABLE raw.stg_messages ADD COLUMN is_duplicate BOOLEAN;

UPDATE raw.stg_messages
SET is_duplicate = CASE 
                       WHEN EXISTS (
                           SELECT 1 FROM raw.stg_messages t2
                           WHERE t2.masked_addressees = raw.stg_messages.masked_addressees
                             AND t2.masked_from_addr = raw.stg_messages.masked_from_addr
                             AND t2.content = raw.stg_messages.content
                             AND t2.rendered_content = raw.stg_messages.rendered_content
                             AND t2.direction = raw.stg_messages.direction
                             AND t2.inserted_at < raw.stg_messages.inserted_at
                       ) 
                       THEN TRUE ELSE FALSE 
                   END;