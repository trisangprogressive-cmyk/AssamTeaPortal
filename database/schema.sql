-- =====================================================
-- Assam Tea Traders Portal Database Schema
-- Final Version 1.0
-- =====================================================

PRAGMA foreign_keys = ON;

-- ==========================================
-- Main Traders Table
-- ==========================================

CREATE TABLE IF NOT EXISTS traders (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_name TEXT NOT NULL,

    contact_person TEXT,

    phone TEXT,

    alternate_phone TEXT,

    email TEXT,

    website TEXT,

    address TEXT,

    district TEXT,

    state TEXT DEFAULT 'Assam',

    pincode TEXT,

    gst TEXT,

    business_type TEXT,

    tea_category TEXT,

    description TEXT,

    latitude REAL,

    longitude REAL,

    source_url TEXT NOT NULL,

    source_name TEXT,

    confidence REAL DEFAULT 0.0,

    last_verified DATE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Prevent Duplicate Records
-- ==========================================

CREATE UNIQUE INDEX IF NOT EXISTS idx_company_phone
ON traders(company_name, phone);

CREATE UNIQUE INDEX IF NOT EXISTS idx_company_website
ON traders(company_name, website);

CREATE UNIQUE INDEX IF NOT EXISTS idx_company_address
ON traders(company_name, address);

-- ==========================================
-- Search Indexes
-- ==========================================

CREATE INDEX IF NOT EXISTS idx_company
ON traders(company_name);

CREATE INDEX IF NOT EXISTS idx_district
ON traders(district);

CREATE INDEX IF NOT EXISTS idx_business
ON traders(business_type);

CREATE INDEX IF NOT EXISTS idx_email
ON traders(email);

-- ==========================================
-- Full Text Search (FTS5)
-- ==========================================

CREATE VIRTUAL TABLE IF NOT EXISTS traders_fts
USING fts5(

    company_name,

    address,

    district,

    business_type,

    tea_category,

    description,

    content='traders',

    content_rowid='id'
);

-- ==========================================
-- FTS Triggers
-- ==========================================

CREATE TRIGGER IF NOT EXISTS traders_ai
AFTER INSERT ON traders
BEGIN

INSERT INTO traders_fts(

rowid,

company_name,

address,

district,

business_type,

tea_category,

description

)

VALUES(

new.id,

new.company_name,

new.address,

new.district,

new.business_type,

new.tea_category,

new.description

);

END;

CREATE TRIGGER IF NOT EXISTS traders_ad
AFTER DELETE ON traders
BEGIN

INSERT INTO traders_fts(

traders_fts,

rowid,

company_name,

address,

district,

business_type,

tea_category,

description

)

VALUES(

'delete',

old.id,

old.company_name,

old.address,

old.district,

old.business_type,

old.tea_category,

old.description

);

END;

CREATE TRIGGER IF NOT EXISTS traders_au
AFTER UPDATE ON traders
BEGIN

INSERT INTO traders_fts(

traders_fts,

rowid,

company_name,

address,

district,

business_type,

tea_category,

description

)

VALUES(

'delete',

old.id,

old.company_name,

old.address,

old.district,

old.business_type,

old.tea_category,

old.description

);

INSERT INTO traders_fts(

rowid,

company_name,

address,

district,

business_type,

tea_category,

description

)

VALUES(

new.id,

new.company_name,

new.address,

new.district,

new.business_type,

new.tea_category,

new.description

);

END;