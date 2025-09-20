# Database Structure - VocabLoury Application

## Table of Contents
1. [Database Overview](#database-overview)
2. [Table Structures](#table-structures)
3. [Relationships](#relationships)
4. [Indexes and Constraints](#indexes-and-constraints)
5. [Data Types and Validation](#data-types-and-validation)
6. [Security Implementation](#security-implementation)
7. [Performance Optimization](#performance-optimization)
8. [Backup and Recovery](#backup-and-recovery)
9. [Migration Scripts](#migration-scripts)
10. [Sample Data](#sample-data)

---

## Database Overview

### Database Management System
- **Type**: SQLite 3.x
- **File**: `authentication.db`
- **Location**: Project root directory
- **Encoding**: UTF-8
- **ACID Compliance**: Full ACID support

### Database Characteristics
- **Size**: Lightweight, single-file database
- **Concurrency**: Multiple readers, single writer
- **Transactions**: Full transaction support
- **Foreign Keys**: Enabled with constraints
- **WAL Mode**: Write-Ahead Logging for better performance

---

## Table Structures

### 1. ACCOUNTS Table

#### Purpose
Stores user account information including authentication credentials and profile data.

#### Schema
```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    salt TEXT NOT NULL,
    profession TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Column Details

| Column | Data Type | Constraints | Description | Example |
|--------|-----------|-------------|-------------|---------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier | 1, 2, 3... |
| `username` | TEXT | UNIQUE, NOT NULL | User's chosen username | "john_doe" |
| `email` | TEXT | UNIQUE, NOT NULL | User's email address | "john@example.com" |
| `password` | TEXT | NOT NULL | PBKDF2 hashed password | "a1b2c3d4e5f6..." |
| `salt` | TEXT | NOT NULL | Random salt for hashing | "x9y8z7w6v5u4..." |
| `profession` | TEXT | NULL | User's profession | "Student", "Engineer" |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation time | "2024-12-01 10:30:00" |

#### Business Rules
- Username must be unique across all users
- Email must be unique and valid format
- Password must be hashed using PBKDF2
- Salt must be cryptographically secure random string
- Profession is optional but helps personalize learning

#### Sample Data
```sql
INSERT INTO accounts (username, email, password, salt, profession, created_at) VALUES
('alice_student', 'alice@university.edu', 'a1b2c3d4e5f6789...', 'x9y8z7w6v5u4t3s2...', 'Student', '2024-12-01 09:15:00'),
('bob_engineer', 'bob@techcorp.com', 'b2c3d4e5f6g7890...', 'y8z7w6v5u4t3s2r1...', 'Engineer', '2024-12-01 14:22:00'),
('carol_writer', 'carol@freelance.com', 'c3d4e5f6g7h8901...', 'z7w6v5u4t3s2r1q0...', 'Writer', '2024-12-01 16:45:00');
```

### 2. AUTH_TOKENS Table

#### Purpose
Manages "Remember Me" authentication tokens for persistent login sessions.

#### Schema
```sql
CREATE TABLE auth_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts (id) ON DELETE CASCADE
);
```

#### Column Details

| Column | Data Type | Constraints | Description | Example |
|--------|-----------|-------------|-------------|---------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique token identifier | 1, 2, 3... |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY | References accounts.id | 1, 2, 3... |
| `token` | TEXT | NOT NULL | Secure random token | "a1b2c3d4e5f6g7h8..." |
| `expires_at` | TIMESTAMP | NOT NULL | Token expiration time | "2024-12-31 23:59:59" |

#### Business Rules
- Each token is unique and cryptographically secure
- Tokens expire after 30 days
- Only one active token per user (old tokens are deleted)
- Tokens are automatically cleaned up when expired

#### Sample Data
```sql
INSERT INTO auth_tokens (user_id, token, expires_at) VALUES
(1, 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6', '2024-12-31 23:59:59'),
(2, 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7', '2024-12-31 23:59:59');
```

### 3. WORD_HISTORY Table

#### Purpose
Tracks user's dictionary search history and learned vocabulary.

#### Schema
```sql
CREATE TABLE word_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    word TEXT NOT NULL,
    meaning TEXT,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Column Details

| Column | Data Type | Constraints | Description | Example |
|--------|-----------|-------------|-------------|---------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique search identifier | 1, 2, 3... |
| `username` | TEXT | NOT NULL | Username (references accounts.username) | "alice_student" |
| `word` | TEXT | NOT NULL | The searched word | "serendipity" |
| `meaning` | TEXT | NULL | Word definition/meaning | "The occurrence of happy events by chance" |
| `searched_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Search timestamp | "2024-12-01 10:30:00" |

#### Business Rules
- Username must exist in accounts table
- Word searches are logged for learning analytics
- Meaning can be null if API call fails
- Timestamps are automatically recorded

#### Sample Data
```sql
INSERT INTO word_history (username, word, meaning, searched_at) VALUES
('alice_student', 'serendipity', 'The occurrence of happy events by chance', '2024-12-01 10:30:00'),
('alice_student', 'ephemeral', 'Lasting for a very short time', '2024-12-01 11:15:00'),
('bob_engineer', 'algorithm', 'A set of rules for solving a problem', '2024-12-01 14:22:00'),
('carol_writer', 'eloquent', 'Fluent and persuasive in speaking or writing', '2024-12-01 16:45:00');
```

---

## Relationships

### 1. ACCOUNTS → AUTH_TOKENS
- **Type**: One-to-Many
- **Foreign Key**: `auth_tokens.user_id` → `accounts.id`
- **Cascade**: ON DELETE CASCADE
- **Business Logic**: One user can have multiple tokens (different devices)

### 2. ACCOUNTS → WORD_HISTORY
- **Type**: One-to-Many
- **Reference**: `word_history.username` → `accounts.username`
- **Cascade**: No cascade (preserve history)
- **Business Logic**: One user can have multiple word searches

### Relationship Diagram
```
ACCOUNTS (1) ────── (M) AUTH_TOKENS
    │
    │ (1)
    │
    │ (M)
    │
WORD_HISTORY
```

---

## Indexes and Constraints

### Primary Keys
- `accounts.id` - Clustered index for fast user lookup
- `auth_tokens.id` - Clustered index for token management
- `word_history.id` - Clustered index for search history

### Unique Constraints
- `accounts.username` - Ensures unique usernames
- `accounts.email` - Ensures unique email addresses
- `auth_tokens.token` - Ensures unique tokens

### Foreign Key Constraints
- `auth_tokens.user_id` → `accounts.id` with CASCADE DELETE
- `word_history.username` → `accounts.username` (referential integrity)

### Performance Indexes
```sql
-- Index for fast username lookups in word_history
CREATE INDEX idx_word_history_username ON word_history(username);

-- Index for chronological sorting of word searches
CREATE INDEX idx_word_history_searched_at ON word_history(searched_at);

-- Index for token expiration cleanup
CREATE INDEX idx_auth_tokens_expires_at ON auth_tokens(expires_at);

-- Composite index for user-specific word searches
CREATE INDEX idx_word_history_user_word ON word_history(username, word);
```

---

## Data Types and Validation

### TEXT Fields
- **Username**: 3-50 characters, alphanumeric and underscores only
- **Email**: Valid email format, max 255 characters
- **Password**: PBKDF2 hash, 64 characters (hex)
- **Salt**: Cryptographically secure random, 32 characters (hex)
- **Profession**: Free text, max 100 characters
- **Token**: Cryptographically secure random, 64 characters (hex)
- **Word**: Dictionary word, max 100 characters
- **Meaning**: Word definition, max 1000 characters

### TIMESTAMP Fields
- **created_at**: Account creation timestamp
- **expires_at**: Token expiration timestamp
- **searched_at**: Word search timestamp
- **Format**: ISO 8601 (YYYY-MM-DD HH:MM:SS)

### Validation Rules
```python
# Username validation
def validate_username(username):
    if not username or len(username) < 3 or len(username) > 50:
        return False
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    return True

# Email validation
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Password validation
def validate_password(password):
    if not password or len(password) < 8:
        return False
    return True
```

---

## Security Implementation

### Password Security
```python
def hash_password(password, salt=None):
    """Hash password using PBKDF2 with SHA-256"""
    if salt is None:
        salt = secrets.token_hex(16)  # 32 character salt
    
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # 100,000 iterations
    ).hex()
    
    return password_hash, salt
```

### Token Security
```python
def generate_secure_token():
    """Generate cryptographically secure token"""
    return secrets.token_hex(32)  # 64 character token

def create_remember_token(user_id):
    """Create remember me token with expiration"""
    token = generate_secure_token()
    expires_at = datetime.now() + timedelta(days=30)
    
    # Delete existing tokens for user
    cursor.execute('DELETE FROM auth_tokens WHERE user_id = ?', (user_id,))
    
    # Insert new token
    cursor.execute('''
        INSERT INTO auth_tokens (user_id, token, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, token, expires_at))
    
    return token
```

### SQL Injection Prevention
```python
# Use parameterized queries
cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
cursor.execute('INSERT INTO word_history (username, word, meaning) VALUES (?, ?, ?)', 
               (username, word, meaning))
```

---

## Performance Optimization

### Query Optimization
```sql
-- Optimized user authentication query
SELECT id, password, salt FROM accounts WHERE username = ? LIMIT 1;

-- Optimized word history retrieval
SELECT word, meaning, searched_at 
FROM word_history 
WHERE username = ? 
ORDER BY searched_at DESC 
LIMIT 50;

-- Optimized token validation
SELECT a.id, a.username, t.expires_at 
FROM auth_tokens t
JOIN accounts a ON t.user_id = a.id
WHERE t.token = ? AND t.expires_at > ?;
```

### Connection Management
```python
class DatabaseManager:
    def __init__(self):
        self.db_file = "authentication.db"
        self.connection_pool = []
    
    def get_connection(self):
        """Get database connection with connection pooling"""
        if self.connection_pool:
            return self.connection_pool.pop()
        return sqlite3.connect(self.db_file)
    
    def return_connection(self, conn):
        """Return connection to pool"""
        self.connection_pool.append(conn)
```

### Caching Strategy
```python
# In-memory cache for frequently accessed data
class CacheManager:
    def __init__(self):
        self.user_cache = {}
        self.word_cache = {}
        self.cache_ttl = 300  # 5 minutes
    
    def get_cached_user(self, username):
        """Get user from cache if available"""
        if username in self.user_cache:
            user_data, timestamp = self.user_cache[username]
            if time.time() - timestamp < self.cache_ttl:
                return user_data
        return None
```

---

## Backup and Recovery

### Backup Script
```python
import shutil
import datetime
import os

def backup_database():
    """Create timestamped backup of database"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"authentication_backup_{timestamp}.db"
    backup_path = os.path.join("backups", backup_name)
    
    # Create backups directory if it doesn't exist
    os.makedirs("backups", exist_ok=True)
    
    # Copy database file
    shutil.copy2("authentication.db", backup_path)
    
    print(f"Database backed up to: {backup_path}")
    return backup_path
```

### Recovery Script
```python
def restore_database(backup_path):
    """Restore database from backup"""
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup file not found: {backup_path}")
    
    # Create backup of current database
    current_backup = f"authentication_current_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2("authentication.db", current_backup)
    
    # Restore from backup
    shutil.copy2(backup_path, "authentication.db")
    
    print(f"Database restored from: {backup_path}")
    print(f"Current database backed up to: {current_backup}")
```

---

## Migration Scripts

### Database Initialization
```python
def initialize_database():
    """Initialize database with all tables and indexes"""
    conn = sqlite3.connect("authentication.db")
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            profession TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES accounts (id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            word TEXT NOT NULL,
            meaning TEXT,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_word_history_username ON word_history(username)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_word_history_searched_at ON word_history(searched_at)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_auth_tokens_expires_at ON auth_tokens(expires_at)")
    
    conn.commit()
    conn.close()
```

### Data Migration
```python
def migrate_data():
    """Migrate data from old schema to new schema"""
    conn = sqlite3.connect("authentication.db")
    cursor = conn.cursor()
    
    # Add new columns if they don't exist
    try:
        cursor.execute("ALTER TABLE accounts ADD COLUMN profession TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Update existing data
    cursor.execute("UPDATE accounts SET profession = 'Student' WHERE profession IS NULL")
    
    conn.commit()
    conn.close()
```

---

## Sample Data

### Test Users
```sql
-- Insert test users for development
INSERT INTO accounts (username, email, password, salt, profession, created_at) VALUES
('test_student', 'student@test.com', 'a1b2c3d4e5f6789abcdef0123456789abcdef0123456789abcdef0123456789', 'x9y8z7w6v5u4t3s2r1q0p9o8n7m6l5k4j3i2h1g0f9e8d7c6b5a4', 'Student', '2024-12-01 09:00:00'),
('test_engineer', 'engineer@test.com', 'b2c3d4e5f6g7890bcdef0123456789abcdef0123456789abcdef0123456789a', 'y8z7w6v5u4t3s2r1q0p9o8n7m6l5k4j3i2h1g0f9e8d7c6b5a4z', 'Engineer', '2024-12-01 10:00:00'),
('test_writer', 'writer@test.com', 'c3d4e5f6g7h8901cdef0123456789abcdef0123456789abcdef0123456789ab', 'z7w6v5u4t3s2r1q0p9o8n7m6l5k4j3i2h1g0f9e8d7c6b5a4zy', 'Writer', '2024-12-01 11:00:00');
```

### Sample Word History
```sql
-- Insert sample word searches
INSERT INTO word_history (username, word, meaning, searched_at) VALUES
('test_student', 'serendipity', 'The occurrence of happy events by chance', '2024-12-01 09:15:00'),
('test_student', 'ephemeral', 'Lasting for a very short time', '2024-12-01 09:30:00'),
('test_student', 'ubiquitous', 'Present everywhere at the same time', '2024-12-01 09:45:00'),
('test_engineer', 'algorithm', 'A set of rules for solving a problem', '2024-12-01 10:15:00'),
('test_engineer', 'optimization', 'The process of making something as good as possible', '2024-12-01 10:30:00'),
('test_writer', 'eloquent', 'Fluent and persuasive in speaking or writing', '2024-12-01 11:15:00'),
('test_writer', 'narrative', 'A spoken or written account of connected events', '2024-12-01 11:30:00');
```

### Sample Auth Tokens
```sql
-- Insert sample auth tokens
INSERT INTO auth_tokens (user_id, token, expires_at) VALUES
(1, 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2', '2024-12-31 23:59:59'),
(2, 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3', '2024-12-31 23:59:59');
```

---

## Database Maintenance

### Cleanup Scripts
```python
def cleanup_expired_tokens():
    """Remove expired authentication tokens"""
    conn = sqlite3.connect("authentication.db")
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM auth_tokens WHERE expires_at < ?", (datetime.now(),))
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"Cleaned up {deleted_count} expired tokens")

def cleanup_old_word_history():
    """Remove word history older than 1 year"""
    conn = sqlite3.connect("authentication.db")
    cursor = conn.cursor()
    
    one_year_ago = datetime.now() - timedelta(days=365)
    cursor.execute("DELETE FROM word_history WHERE searched_at < ?", (one_year_ago,))
    deleted_count = cursor.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"Cleaned up {deleted_count} old word history entries")
```

### Database Statistics
```python
def get_database_stats():
    """Get database statistics"""
    conn = sqlite3.connect("authentication.db")
    cursor = conn.cursor()
    
    # Get table sizes
    cursor.execute("SELECT COUNT(*) FROM accounts")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM auth_tokens")
    token_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM word_history")
    word_count = cursor.fetchone()[0]
    
    # Get database file size
    db_size = os.path.getsize("authentication.db")
    
    conn.close()
    
    return {
        'users': user_count,
        'tokens': token_count,
        'word_searches': word_count,
        'database_size_mb': round(db_size / (1024 * 1024), 2)
    }
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Database Version**: SQLite 3.x
