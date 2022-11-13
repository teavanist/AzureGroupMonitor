--
-- PostgreSQL database dump
--

-- Dumped from database version 12.12 (Ubuntu 12.12-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.12 (Ubuntu 12.12-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: get_actionrecords(integer); Type: FUNCTION; Schema: public;
--

CREATE FUNCTION public.get_actionrecords(idparam integer) RETURNS TABLE(id integer, activitydatetime date, initiatingprincipal character varying, actionactivitydisplayname character varying, targettype character varying, initiator character varying, targetdisplayname character varying, targetprincipal character varying, property character varying, oldvalue character varying, newvalue character varying, actionresult character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
 RETURN QUERY

	select
		a.id ,
		a.activitydatetime,
		i.userprincipalname as "InitiatingPrincipal",
		a.activitydisplayname,
		t."type" as "TargetType",
		i.userprincipalname as "Initiator",
		t.displayname ,
		t.userprincipalname as "TargetPrincipal",
		m.displayname "Property",
		m.oldvalue "Old value",
		m.newvalue "New value",
		a."result"
	FROM actions a
	left outer join initiators i on a.id=i.top_parent_id 
	LEFT OUTER JOIN targets t ON a.id = t.top_parent_id 
	left outer join modifications m  on t.top_parent_id = m.top_parent_id 
	where a.id=idparam and 
	t.modified_items_count != 0;

END; $$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: actions; Type: TABLE; Schema: public;
--

CREATE TABLE public.actions (
    id integer NOT NULL,
    source_system character varying(100) NOT NULL,
    source_id character varying(100) NOT NULL,
    category character varying(100) NOT NULL,
    correlationid character varying(100),
    result character varying(100),
    resultreason character varying(100),
    activitydisplayname character varying(500),
    activitydatetime date,
    loggedbyservice character varying(100),
    operationtype character varying(100)
);



--
-- Name: initiators; Type: TABLE; Schema: public;
--

CREATE TABLE public.initiators (
    id integer NOT NULL,
    top_parent_id integer,
    parent_action_id character varying(100),
    source_id character varying(100),
    displayname character varying(100),
    userprincipalname character varying(1000),
    ipaddress character varying(15),
    usertype character varying(100),
    hometenantid character varying(100),
    hometenantname character varying(100)
);



--
-- Name: modifications; Type: TABLE; Schema: public;
--

CREATE TABLE public.modifications (
    id integer NOT NULL,
    parent_target_id character varying(100),
    displayname character varying(100),
    oldvalue character varying(100),
    newvalue character varying(100),
    top_parent_id integer
);



--
-- Name: targets; Type: TABLE; Schema: public;
--

CREATE TABLE public.targets (
    id integer NOT NULL,
    parent_action_id character varying(100),
    source_id character varying(100),
    displayname character varying(100),
    type character varying(100),
    result character varying(100),
    userprincipalname character varying(1000),
    grouptype character varying(100),
    modified_items_count integer,
    top_parent_id integer
);



--
-- Name: action_initiator_target_modifications; Type: VIEW; Schema: public;
--

CREATE VIEW public.action_initiator_target_modifications AS
 SELECT a.id AS actionid,
    a.activitydatetime,
    a.activitydisplayname,
    i.userprincipalname AS "Initiator",
    m.displayname AS "Property",
    t.type AS "TargetType",
    t.source_id AS "TargetID",
    t.userprincipalname AS "TargetUPN",
    t.modified_items_count AS "ModifiedItemsCount",
    m.oldvalue AS "Oldvalue",
    m.newvalue AS "Newvalue",
    a.result,
    t.displayname AS "TargetDisplayName"
   FROM (((public.actions a
     LEFT JOIN public.initiators i ON ((a.id = i.top_parent_id)))
     LEFT JOIN public.targets t ON ((a.id = t.top_parent_id)))
     LEFT JOIN public.modifications m ON ((t.top_parent_id = m.top_parent_id)))
  WHERE (t.modified_items_count <> 0);



--
-- Name: actions_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.actions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: actions_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.actions_id_seq OWNED BY public.actions.id;


--
-- Name: objects; Type: TABLE; Schema: public;
--

CREATE TABLE public.objects (
    id integer NOT NULL,
    sourceobjectid character varying(1000),
    type character varying(15),
    name character varying(1000)
);



--
-- Name: objects_actions_mapping; Type: TABLE; Schema: public;
--

CREATE TABLE public.objects_actions_mapping (
    id integer NOT NULL,
    top_parent_id integer,
    sourceobjectid character varying(40)
);



--
-- Name: actions_with_affectedparties; Type: VIEW; Schema: public;
--

CREATE VIEW public.actions_with_affectedparties AS
 SELECT a.id,
    a.source_system,
    a.source_id,
    a.category,
    a.result,
    a.activitydisplayname,
    a.activitydatetime,
    o.sourceobjectid,
    o.type,
    o.name
   FROM ((public.actions a
     LEFT JOIN public.objects_actions_mapping oam ON ((a.id = oam.top_parent_id)))
     LEFT JOIN public.objects o ON (((oam.sourceobjectid)::text = (o.sourceobjectid)::text)));



--
-- Name: interpretations; Type: TABLE; Schema: public;
--

CREATE TABLE public.interpretations (
    id integer NOT NULL,
    top_parent_id integer,
    interpretation character varying(1000),
    isnotificationsent boolean DEFAULT false,
    notificationtime timestamp with time zone
);



--
-- Name: actions_with_interpretations; Type: VIEW; Schema: public;
--

CREATE VIEW public.actions_with_interpretations AS
 SELECT a.id,
    a.source_system,
    a.source_id,
    a.category,
    a.correlationid,
    a.result,
    a.resultreason,
    a.activitydisplayname,
    a.activitydatetime,
    a.loggedbyservice,
    a.operationtype,
    i.interpretation
   FROM (public.actions a
     LEFT JOIN public.interpretations i ON ((a.id = i.top_parent_id)));



--
-- Name: initiators_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.initiators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: initiators_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.initiators_id_seq OWNED BY public.initiators.id;


--
-- Name: interpretations_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.interpretations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: interpretations_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.interpretations_id_seq OWNED BY public.interpretations.id;


--
-- Name: modifications_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.modifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: modifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.modifications_id_seq OWNED BY public.modifications.id;


--
-- Name: objects_actions_mapping_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.objects_actions_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: objects_actions_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.objects_actions_mapping_id_seq OWNED BY public.objects_actions_mapping.id;


--
-- Name: objects_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.objects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: objects_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.objects_id_seq OWNED BY public.objects.id;


--
-- Name: targets_id_seq; Type: SEQUENCE; Schema: public;
--

CREATE SEQUENCE public.targets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: targets_id_seq; Type: SEQUENCE OWNED BY; Schema: public;
--

ALTER SEQUENCE public.targets_id_seq OWNED BY public.targets.id;


--
-- Name: view_for_actionoverview; Type: VIEW; Schema: public;
--

CREATE VIEW public.view_for_actionoverview AS
 SELECT a.id,
    a.source_system,
    a.source_id,
    a.category,
    a.result,
    a.activitydisplayname,
    a.activitydatetime,
    o.sourceobjectid,
    o.type,
    o.name,
    i.interpretation
   FROM (((public.actions a
     LEFT JOIN public.objects_actions_mapping oam ON ((a.id = oam.top_parent_id)))
     LEFT JOIN public.objects o ON (((oam.sourceobjectid)::text = (o.sourceobjectid)::text)))
     LEFT JOIN public.interpretations i ON ((a.id = i.top_parent_id)))
  ORDER BY a.id;


--
-- Name: view_for_pendingnotifications; Type: VIEW; Schema: public;
--

CREATE VIEW public.view_for_pendingnotifications AS
 SELECT a.activitydatetime,
    a.activitydisplayname,
    a.result,
    a.resultreason,
    i.id,
    i.interpretation,
    i.isnotificationsent,
    i.notificationtime
   FROM (public.interpretations i
     JOIN public.actions a ON ((a.id = i.top_parent_id)))
  WHERE (i.isnotificationsent = false)
  ORDER BY a.activitydatetime;


--
-- Name: actions id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.actions ALTER COLUMN id SET DEFAULT nextval('public.actions_id_seq'::regclass);


--
-- Name: initiators id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.initiators ALTER COLUMN id SET DEFAULT nextval('public.initiators_id_seq'::regclass);


--
-- Name: interpretations id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.interpretations ALTER COLUMN id SET DEFAULT nextval('public.interpretations_id_seq'::regclass);


--
-- Name: modifications id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.modifications ALTER COLUMN id SET DEFAULT nextval('public.modifications_id_seq'::regclass);


--
-- Name: objects id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.objects ALTER COLUMN id SET DEFAULT nextval('public.objects_id_seq'::regclass);


--
-- Name: objects_actions_mapping id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.objects_actions_mapping ALTER COLUMN id SET DEFAULT nextval('public.objects_actions_mapping_id_seq'::regclass);


--
-- Name: targets id; Type: DEFAULT; Schema: public;
--

ALTER TABLE ONLY public.targets ALTER COLUMN id SET DEFAULT nextval('public.targets_id_seq'::regclass);


--
-- Name: actions actions_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_pkey PRIMARY KEY (id);


--
-- Name: initiators initiators_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.initiators
    ADD CONSTRAINT initiators_pkey PRIMARY KEY (id);


--
-- Name: interpretations interpretations_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.interpretations
    ADD CONSTRAINT interpretations_pkey PRIMARY KEY (id);


--
-- Name: modifications modifications_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.modifications
    ADD CONSTRAINT modifications_pkey PRIMARY KEY (id);


--
-- Name: objects_actions_mapping objects_actions_mapping_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.objects_actions_mapping
    ADD CONSTRAINT objects_actions_mapping_pkey PRIMARY KEY (id);


--
-- Name: objects objects_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.objects
    ADD CONSTRAINT objects_pkey PRIMARY KEY (id);


--
-- Name: targets targets_pkey; Type: CONSTRAINT; Schema: public;
--

ALTER TABLE ONLY public.targets
    ADD CONSTRAINT targets_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--
