CREATE TABLE processed_data (
    id bigserial primary key,
    data jsonb,
    result_id varchar(36)
);

CREATE INDEX request_idx ON processed_data(result_id)
