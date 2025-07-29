-- public.scans definition

-- Drop table

-- DROP TABLE public.scans;

CREATE TABLE public.scans (
	id bigserial NOT NULL,
	type varchar NOT NULL,
	"result" varchar NOT NULL,
	started timestamp NOT NULL,
	finished timestamp NOT NULL,
	elapsed varchar NOT NULL,
	scanned int4 NOT NULL,
	skipped int4 NOT NULL,
	added int4 NOT NULL,
	updated int4 NOT NULL,
	details json NOT NULL,
	exception_type varchar NULL,
	exception_message text NULL,
	exception_stacktrace text NULL,
	audit_created timestamp NULL DEFAULT (now() AT TIME ZONE 'utc'::text),
	CONSTRAINT scans_pkey PRIMARY KEY (id)
);