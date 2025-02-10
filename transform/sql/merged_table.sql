drop table if exists raw.merged_table;
create table raw.merged_table as (
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
    raw_status as (
        select
            uuid,
            id,
            message_uuid,
            message_id,
            status,
            number_id,
            TO_TIMESTAMP(inserted_at, 'MM/DD/YYYY HH24:MI:SS')::timestamp as inserted_at,
            TO_TIMESTAMP(updated_at, 'MM/DD/YYYY HH24:MI:SS')::timestamp as updated_at
        from raw.statuses s 
    ),
    latest_status as (
        select *,
            case 
                WHEN ROW_NUMBER() OVER (PARTITION BY message_uuid ORDER BY inserted_at DESC) = 1 THEN 1 
                ELSE 0 
            end as is_latest
        from raw_status
    ),
    latest_message as (
        select *,
            case 
                WHEN ROW_NUMBER() OVER (PARTITION BY uuid ORDER BY inserted_at DESC) = 1 THEN 1 
                ELSE 0 
            end as is_latest
        from raw_message
    ),
    final_message as (
        select * from latest_message where is_latest=1
    ),
    final_status as (
        select * from latest_status where is_latest=1
    ),
    main as (
        select 
            m.uuid,
            m.id,
            m.message_type,
            m.direction,
            m.masked_addressees,
            m.masked_author,
            m.content,
            m.author_type,
            m.external_id,
            m.external_timestamp,
            m.masked_from_addr,
            m.is_deleted,
            m.last_status,
            m.last_status_timestamp,
            m.rendered_content,
            m.source_type,
            m.inserted_at,
            m.updated_at,
            s.uuid as status_uuid,
            s.id as status_id,
            s.status as merged_last_status,
            s.number_id as status_number_id,
            s.inserted_at as status_inserted_at,
            s.updated_at as status_updated_at
        from final_message m 
        left join final_status s on m.uuid=s.message_uuid
    ) select * from main
);


