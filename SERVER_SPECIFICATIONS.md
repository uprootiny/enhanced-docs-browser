# Enhanced Documentation Browser - Server Specifications

## System Overview

A dual-server documentation system providing complementary experiences for exploring and consuming markdown documents through modern web interfaces.

## Architecture Specification

### Primary Server (Python) - Port 44500
**Intent**: Interactive document discovery and analysis platform  
**Scope**: Comprehensive document browsing with search, clustering, and similarity analysis  
**Paradigm**: Stateful, feature-rich web application with client-side intelligence

#### Technical Stack
- **Runtime**: Python 3.8+
- **HTTP Server**: Built-in `http.server.HTTPServer`
- **Search Engine**: ripgrep (`rg`) subprocess integration
- **Document Processing**: `markdown` library with extensions
- **Frontend**: Vanilla JavaScript with CSS Grid/Flexbox

#### API Endpoints

| Endpoint | Method | Purpose | Parameters | Response |
|----------|--------|---------|------------|----------|
| `/` | GET | Main application interface | - | HTML Document |
| `/api/files` | GET | List all markdown documents | - | JSON Array of file objects |
| `/api/search` | GET | Full-text search across documents | `q` (query string) | JSON Array of search results |
| `/api/content-analysis` | GET | Document clustering analysis | - | JSON Object with cluster data |
| `/file/{path}` | GET | Rendered markdown document | `path` (URL-encoded) | HTML Document |
| `/raw/{path}` | GET | Raw markdown content | `path` (URL-encoded) | Plain text |

#### Features Implementation

1. **Semantic Document Classification**
   - Filename-based heuristics
   - Six categories: roadmap, technical, essay, analysis, project, memo
   - Color-coded visual indicators

2. **Client-Side Similarity Engine**
   - TF-IDF vectorization in JavaScript
   - Cosine similarity computation
   - Real-time related document suggestions

3. **Fluid UI System**
   - CSS custom properties for theming
   - Staggered animations with `setTimeout` delays
   - Responsive grid layout adapting to screen size
   - Micro-interactions on hover and focus states

4. **Search Integration**
   - Debounced search with 300ms delay
   - Visual typing indicators and result counts
   - Context snippet highlighting
   - Error handling for timeouts and edge cases

### Secondary Server (Racket) - Port 44501  
**Intent**: Contemplative document reading experience  
**Scope**: Minimal, poetry-focused essay consumption  
**Paradigm**: Functional, stateless document garden

#### Technical Stack
- **Runtime**: Racket 8.2+
- **Web Framework**: `web-server/servlet-env`
- **Document Discovery**: Unix `find` command integration
- **Frontend**: Server-side HTML generation with embedded CSS

#### Routes

| Route | Purpose | Response |
|-------|---------|----------|
| `/` | Essay garden overview | HTML grid of all documents |
| `/essay/{path}` | Individual essay reading view | HTML formatted document |

#### Features Implementation

1. **Essay Garden Metaphor**
   - Grid layout with document "seeds"
   - Hover animations and visual feedback
   - Unified dark gradient aesthetic

2. **Minimal Content Processing**
   - Basic markdown header recognition
   - Paragraph-based content flow
   - Simple similarity clustering

3. **Typography-First Design**
   - Vollkorn serif for body text
   - Inter Tight sans for UI elements
   - Fira Code monospace for code

## System Requirements

### Server Requirements
- **OS**: Linux (Ubuntu 22.04 LTS tested)
- **Python**: 3.8+ with `markdown` package
- **Racket**: 8.2+ with web server libraries
- **System Tools**: `ripgrep`, `find`, `netstat`

### Network Requirements
- **Firewall**: Ports 44500 and 44501 open for external access
- **Interface Binding**: Both servers listen on `0.0.0.0` (all interfaces)
- **DNS/IP**: Accessible via server IP or domain name

### Resource Requirements
- **Memory**: ~50MB per server (100MB total)
- **CPU**: Minimal (I/O bound operations)
- **Storage**: Read access to markdown files across filesystem
- **Network**: Moderate bandwidth for font loading and API responses

## Configuration Specification

### Environment Variables
```bash
# Optional: Customize document root path
DOCS_ROOT=/home/uprootiny

# Optional: Adjust server ports
PYTHON_PORT=44500
RACKET_PORT=44501
```

### File System Structure
```
enhanced-docs-browser/
├── enhanced_docs_server.py      # Main Python server
├── silver-simple.rkt            # Racket poetry server
├── test_servers.py              # Comprehensive test suite
├── README.md                    # Project documentation
├── FLUID_UI_ROADMAP.md         # Future enhancement plans
└── SERVER_SPECIFICATIONS.md     # This document
```

## Performance Characteristics

### Python Server Performance
- **Document Discovery**: O(n) filesystem scan via ripgrep
- **Search**: O(m) where m = matching document count (ripgrep optimization)
- **Similarity Computation**: O(k²) where k = documents with content loaded
- **Memory Usage**: Linear with number of cached document vectors

### Racket Server Performance
- **Document Loading**: O(n) with file I/O caching
- **Route Dispatch**: O(1) pattern matching
- **HTML Generation**: O(doc_length) template processing
- **Memory Usage**: Constant + document content in hash tables

## Security Model

### Access Control
- **Network Level**: Firewall-controlled port access
- **Application Level**: No authentication (read-only document access)
- **File System**: Server process permissions determine document access

### Input Validation
- **Path Traversal**: URL encoding/decoding with validation
- **Query Injection**: Limited subprocess exposure via ripgrep
- **XSS Prevention**: HTML escaping in search results and user content

### Resource Protection
- **Request Timeouts**: 10-second limits on subprocess operations
- **Result Limiting**: Maximum 50 search results per query
- **Rate Limiting**: None (suitable for internal/trusted networks)

## Monitoring and Observability

### Health Check Endpoints
- **Python**: `GET /api/files` (should return 200 with JSON array)
- **Racket**: `GET /` (should return 200 with HTML content)

### Log Output
- **Python**: Console output for HTTP requests and errors
- **Racket**: Console output with essay discovery and server status

### Process Monitoring
```bash
# Check server processes
pgrep -f enhanced_docs_server.py
pgrep -f silver-simple.rkt

# Check port bindings
netstat -tlnp | grep -E ":(44500|44501)"
```

## Testing Strategy

### Unit Tests
- API endpoint response validation
- Document classification accuracy
- Search functionality correctness
- Typography and styling verification

### Integration Tests
- Cross-server compatibility
- Concurrent access handling
- Error condition responses
- Performance under load

### User Acceptance Tests
- Browser compatibility across modern browsers
- Mobile responsiveness verification
- Accessibility compliance (WCAG 2.1 AA)
- Typography rendering across operating systems

## Deployment Checklist

1. **Prerequisites**
   - [ ] Python 3.8+ installed
   - [ ] Racket 8.2+ installed
   - [ ] ripgrep available in PATH
   - [ ] Firewall configured for ports 44500, 44501

2. **Server Startup**
   - [ ] Start Python server: `python3 enhanced_docs_server.py`
   - [ ] Start Racket server: `racket silver-simple.rkt`
   - [ ] Verify both servers respond to health checks

3. **Validation**
   - [ ] Run test suite: `python3 test_servers.py`
   - [ ] Manual browser testing on both ports
   - [ ] Document search functionality verification
   - [ ] Typography rendering confirmation

## Maintenance Procedures

### Regular Maintenance
- Monitor log output for errors
- Verify document discovery is finding new files
- Check memory usage for vector cache growth
- Validate search index accuracy

### Troubleshooting
- **Server won't start**: Check port conflicts, permissions
- **Search not working**: Verify ripgrep installation and PATH
- **Fonts not loading**: Check Google Fonts CDN accessibility
- **Performance issues**: Monitor document vector cache size

## Future Enhancement Considerations

### Scalability Improvements
- Document indexing with SQLite for large collections
- Caching layer for frequently accessed documents
- Load balancing for multiple server instances

### Feature Extensions
- User authentication and document access control
- Real-time collaboration features
- Advanced search with filters and facets
- Export functionality (PDF, EPUB generation)

This specification defines the complete technical architecture and operational requirements for the Enhanced Documentation Browser dual-server system.