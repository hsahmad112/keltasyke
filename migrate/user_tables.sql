CREATE TABLE IF NOT EXISTS service_alerts(
    id SERIAL,
    raw_text text,
    summary_en text,
    embedding_vector vector(768),
    created_at TIMESTAMPTZ,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS preferences(
    id SERIAL,
    lines TEXT[],
    stops TEXT[],
    updated_at TIMESTAMPTZ,

    PRIMARY KEY (id)
);
