drop table if exists raw.stg_statuses;
create table raw.stg_statuses as (
    with raw_status as (
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
    ) select * from latest_status
);