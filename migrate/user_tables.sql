CREATE TABLE IF NOT EXISTS service_alerts(
    id INTEGER,
    raw_text text,
    summary_en text,
    embedding_vector vector(768),
    created_at DATE,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS preferences(
    id INTEGER,
    lines TEXT[],
    stops INTEGER[],
    updated_at DATE,

    PRIMARY KEY (id)
);
