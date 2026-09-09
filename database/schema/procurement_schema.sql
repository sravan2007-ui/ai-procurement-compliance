--
-- PostgreSQL database dump
--

\restrict E2ysOTZ2GyY03qwNLvgaD8ayHvngm0pWz7bPxfr9bbBEOjVZBVROr5mJUY65EyW

-- Dumped from database version 18.6 (Homebrew)
-- Dumped by pg_dump version 18.6 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: bid_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bid_documents (
    id integer NOT NULL,
    bid_id integer NOT NULL,
    document_type character varying(100) NOT NULL,
    file_name character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    mime_type character varying(100) NOT NULL,
    status character varying(50) NOT NULL,
    uploaded_at timestamp without time zone NOT NULL
);


--
-- Name: bid_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bid_documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bid_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bid_documents_id_seq OWNED BY public.bid_documents.id;


--
-- Name: bidders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bidders (
    id integer NOT NULL,
    company_name character varying(255) NOT NULL,
    pan character varying(20),
    gstin character varying(20),
    udyam_number character varying(50),
    cin character varying(30),
    email character varying(255),
    phone character varying(20)
);


--
-- Name: bidders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bidders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bidders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bidders_id_seq OWNED BY public.bidders.id;


--
-- Name: document_extractions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_extractions (
    id integer NOT NULL,
    document_id integer NOT NULL,
    document_type character varying(100) NOT NULL,
    extracted_data json,
    extraction_status character varying(50) NOT NULL,
    model_name character varying(100),
    created_at timestamp without time zone NOT NULL
);


--
-- Name: document_extractions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_extractions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_extractions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_extractions_id_seq OWNED BY public.document_extractions.id;


--
-- Name: knowledge_chunks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.knowledge_chunks (
    id integer NOT NULL,
    document_id integer NOT NULL,
    content text NOT NULL,
    chunk_index integer NOT NULL,
    embedding public.vector(384) NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: knowledge_chunks_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.knowledge_chunks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: knowledge_chunks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.knowledge_chunks_id_seq OWNED BY public.knowledge_chunks.id;


--
-- Name: knowledge_documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.knowledge_documents (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    source character varying(500) NOT NULL,
    document_type character varying(100) NOT NULL,
    content text NOT NULL,
    created_at timestamp without time zone NOT NULL
);


--
-- Name: knowledge_documents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.knowledge_documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: knowledge_documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.knowledge_documents_id_seq OWNED BY public.knowledge_documents.id;


--
-- Name: registry_blacklist; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_blacklist (
    pan_number character varying(10) NOT NULL,
    gstin character varying(15),
    entity_name character varying(255) NOT NULL,
    blacklisted boolean,
    reason character varying,
    valid_until character varying(20)
);


--
-- Name: registry_epfo; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_epfo (
    establishment_id character varying(50) NOT NULL,
    establishment_name character varying(255) NOT NULL,
    contribution_status character varying(50) NOT NULL,
    status character varying(50) NOT NULL,
    last_compliant_period character varying(20)
);


--
-- Name: registry_esic; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_esic (
    employer_code character varying(50) NOT NULL,
    establishment_name character varying(255) NOT NULL,
    employer_name character varying(255),
    registration_date character varying(20),
    registration_status character varying(50) NOT NULL,
    contribution_status character varying(50) NOT NULL,
    last_compliant_period character varying(20)
);


--
-- Name: registry_gst; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_gst (
    gstin character varying(15) NOT NULL,
    legal_name character varying(255) NOT NULL,
    trade_name character varying(255),
    status character varying(50) NOT NULL,
    registration_date character varying(20),
    business_type character varying(100),
    return_filing_status character varying(50),
    principal_place_of_business character varying
);


--
-- Name: registry_income_tax; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_income_tax (
    pan_number character varying(10) NOT NULL,
    taxpayer_name character varying(255) NOT NULL,
    assessment_year character varying(20) NOT NULL,
    filing_status character varying(50) NOT NULL,
    return_filing_date character varying(20),
    gross_total_income character varying(50),
    taxable_income character varying(50)
);


--
-- Name: registry_pan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_pan (
    pan_number character varying(10) NOT NULL,
    legal_name character varying(255) NOT NULL,
    status character varying(50) NOT NULL
);


--
-- Name: registry_startup_india; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_startup_india (
    certificate_number character varying(50) NOT NULL,
    startup_name character varying(255) NOT NULL,
    recognition_date character varying(20),
    entity_type character varying(100),
    pan_number character varying(10) NOT NULL,
    validity_status character varying(50) NOT NULL
);


--
-- Name: registry_udyam; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.registry_udyam (
    udyam_number character varying(30) NOT NULL,
    enterprise_name character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    classification character varying(50)
);


--
-- Name: tender_bids; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tender_bids (
    id integer NOT NULL,
    tender_id integer NOT NULL,
    bidder_id integer NOT NULL,
    status character varying(50) NOT NULL,
    submitted_at timestamp without time zone NOT NULL
);


--
-- Name: tender_bids_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tender_bids_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tender_bids_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tender_bids_id_seq OWNED BY public.tender_bids.id;


--
-- Name: tenders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tenders (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    organization character varying(255) NOT NULL,
    description text,
    submission_deadline timestamp without time zone,
    status character varying(50) NOT NULL
);


--
-- Name: tenders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tenders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tenders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tenders_id_seq OWNED BY public.tenders.id;


--
-- Name: bid_documents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bid_documents ALTER COLUMN id SET DEFAULT nextval('public.bid_documents_id_seq'::regclass);


--
-- Name: bidders id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bidders ALTER COLUMN id SET DEFAULT nextval('public.bidders_id_seq'::regclass);


--
-- Name: document_extractions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_extractions ALTER COLUMN id SET DEFAULT nextval('public.document_extractions_id_seq'::regclass);


--
-- Name: knowledge_chunks id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_chunks ALTER COLUMN id SET DEFAULT nextval('public.knowledge_chunks_id_seq'::regclass);


--
-- Name: knowledge_documents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_documents ALTER COLUMN id SET DEFAULT nextval('public.knowledge_documents_id_seq'::regclass);


--
-- Name: tender_bids id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tender_bids ALTER COLUMN id SET DEFAULT nextval('public.tender_bids_id_seq'::regclass);


--
-- Name: tenders id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenders ALTER COLUMN id SET DEFAULT nextval('public.tenders_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: bid_documents bid_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bid_documents
    ADD CONSTRAINT bid_documents_pkey PRIMARY KEY (id);


--
-- Name: bidders bidders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bidders
    ADD CONSTRAINT bidders_pkey PRIMARY KEY (id);


--
-- Name: document_extractions document_extractions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_extractions
    ADD CONSTRAINT document_extractions_pkey PRIMARY KEY (id);


--
-- Name: knowledge_chunks knowledge_chunks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_chunks
    ADD CONSTRAINT knowledge_chunks_pkey PRIMARY KEY (id);


--
-- Name: knowledge_documents knowledge_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_documents
    ADD CONSTRAINT knowledge_documents_pkey PRIMARY KEY (id);


--
-- Name: registry_blacklist registry_blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_blacklist
    ADD CONSTRAINT registry_blacklist_pkey PRIMARY KEY (pan_number);


--
-- Name: registry_epfo registry_epfo_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_epfo
    ADD CONSTRAINT registry_epfo_pkey PRIMARY KEY (establishment_id);


--
-- Name: registry_esic registry_esic_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_esic
    ADD CONSTRAINT registry_esic_pkey PRIMARY KEY (employer_code);


--
-- Name: registry_gst registry_gst_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_gst
    ADD CONSTRAINT registry_gst_pkey PRIMARY KEY (gstin);


--
-- Name: registry_income_tax registry_income_tax_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_income_tax
    ADD CONSTRAINT registry_income_tax_pkey PRIMARY KEY (pan_number);


--
-- Name: registry_pan registry_pan_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_pan
    ADD CONSTRAINT registry_pan_pkey PRIMARY KEY (pan_number);


--
-- Name: registry_startup_india registry_startup_india_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_startup_india
    ADD CONSTRAINT registry_startup_india_pkey PRIMARY KEY (certificate_number);


--
-- Name: registry_udyam registry_udyam_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.registry_udyam
    ADD CONSTRAINT registry_udyam_pkey PRIMARY KEY (udyam_number);


--
-- Name: tender_bids tender_bids_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tender_bids
    ADD CONSTRAINT tender_bids_pkey PRIMARY KEY (id);


--
-- Name: tenders tenders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tenders
    ADD CONSTRAINT tenders_pkey PRIMARY KEY (id);


--
-- Name: ix_bid_documents_bid_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bid_documents_bid_id ON public.bid_documents USING btree (bid_id);


--
-- Name: ix_bidders_cin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bidders_cin ON public.bidders USING btree (cin);


--
-- Name: ix_bidders_gstin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bidders_gstin ON public.bidders USING btree (gstin);


--
-- Name: ix_bidders_pan; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bidders_pan ON public.bidders USING btree (pan);


--
-- Name: ix_bidders_udyam_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_bidders_udyam_number ON public.bidders USING btree (udyam_number);


--
-- Name: ix_document_extractions_document_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_document_extractions_document_id ON public.document_extractions USING btree (document_id);


--
-- Name: ix_knowledge_chunks_document_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_knowledge_chunks_document_id ON public.knowledge_chunks USING btree (document_id);


--
-- Name: ix_registry_blacklist_gstin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_blacklist_gstin ON public.registry_blacklist USING btree (gstin);


--
-- Name: ix_registry_blacklist_pan_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_blacklist_pan_number ON public.registry_blacklist USING btree (pan_number);


--
-- Name: ix_registry_epfo_establishment_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_epfo_establishment_id ON public.registry_epfo USING btree (establishment_id);


--
-- Name: ix_registry_esic_employer_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_esic_employer_code ON public.registry_esic USING btree (employer_code);


--
-- Name: ix_registry_gst_gstin; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_gst_gstin ON public.registry_gst USING btree (gstin);


--
-- Name: ix_registry_income_tax_pan_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_income_tax_pan_number ON public.registry_income_tax USING btree (pan_number);


--
-- Name: ix_registry_pan_pan_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_pan_pan_number ON public.registry_pan USING btree (pan_number);


--
-- Name: ix_registry_startup_india_certificate_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_startup_india_certificate_number ON public.registry_startup_india USING btree (certificate_number);


--
-- Name: ix_registry_startup_india_pan_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_startup_india_pan_number ON public.registry_startup_india USING btree (pan_number);


--
-- Name: ix_registry_udyam_udyam_number; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_registry_udyam_udyam_number ON public.registry_udyam USING btree (udyam_number);


--
-- Name: ix_tender_bids_bidder_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tender_bids_bidder_id ON public.tender_bids USING btree (bidder_id);


--
-- Name: ix_tender_bids_tender_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_tender_bids_tender_id ON public.tender_bids USING btree (tender_id);


--
-- Name: bid_documents bid_documents_bid_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bid_documents
    ADD CONSTRAINT bid_documents_bid_id_fkey FOREIGN KEY (bid_id) REFERENCES public.tender_bids(id);


--
-- Name: document_extractions document_extractions_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_extractions
    ADD CONSTRAINT document_extractions_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.bid_documents(id);


--
-- Name: knowledge_chunks knowledge_chunks_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.knowledge_chunks
    ADD CONSTRAINT knowledge_chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.knowledge_documents(id);


--
-- Name: tender_bids tender_bids_bidder_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tender_bids
    ADD CONSTRAINT tender_bids_bidder_id_fkey FOREIGN KEY (bidder_id) REFERENCES public.bidders(id);


--
-- Name: tender_bids tender_bids_tender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tender_bids
    ADD CONSTRAINT tender_bids_tender_id_fkey FOREIGN KEY (tender_id) REFERENCES public.tenders(id);


--
-- PostgreSQL database dump complete
--

\unrestrict E2ysOTZ2GyY03qwNLvgaD8ayHvngm0pWz7bPxfr9bbBEOjVZBVROr5mJUY65EyW

