-- public.comics definition

-- Drop table

-- DROP TABLE public.comics;

CREATE TABLE public.comics (
    ed2k_md4 varchar NOT NULL,
    ed2k_file_name varchar NOT NULL,
    ed2k_link varchar NOT NULL,
	topic_id int4 NOT NULL,
	topic_link varchar NOT NULL,
	audit_created timestamp NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
	audit_updated timestamp NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
	audit_hash varchar NOT NULL,
	CONSTRAINT comics_pkey PRIMARY KEY (ed2k_md4)
);