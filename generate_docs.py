import os
import sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# -------------------------------------------------------------
# 1. GENERATE HANDWRITTEN PAGES (PNG + PDF)
# -------------------------------------------------------------

base_dir = r"C:\Users\N\Downloads\New folder (4)\superrdev-patch-exercise1"
handwritten_dir = os.path.join(base_dir, "handwritten")
os.makedirs(handwritten_dir, exist_ok=True)

font_regular = r"C:\Windows\Fonts\segoepr.ttf"
font_bold = r"C:\Windows\Fonts\segoeprb.ttf"

PAGE_WIDTH = 2480   # A4 at 300 DPI
PAGE_HEIGHT = 3508
MARGIN_LEFT = 200
MARGIN_RIGHT = 180
MARGIN_TOP = 220
MARGIN_BOTTOM = 200
LINE_SPACING = 68

INK_BLUE = (15, 35, 95)
INK_BLUE_DARK = (10, 25, 75)
INK_RED = (160, 25, 25)
INK_GREEN = (20, 110, 45)
INK_BLACK = (35, 35, 40)
INK_PURPLE = (80, 25, 105)

def draw_lined_background():
    img = Image.new("RGB", (PAGE_WIDTH, PAGE_HEIGHT), (253, 251, 246))
    draw = ImageDraw.Draw(img)
    
    # Left margin double red line
    margin_x = MARGIN_LEFT - 35
    draw.line([(margin_x, 0), (margin_x, PAGE_HEIGHT)], fill=(240, 180, 180), width=3)
    draw.line([(margin_x + 6, 0), (margin_x + 6, PAGE_HEIGHT)], fill=(248, 210, 210), width=2)
    
    # Horizontal ruled lines
    y = MARGIN_TOP
    while y < PAGE_HEIGHT - MARGIN_BOTTOM:
        draw.line([(0, y), (PAGE_WIDTH, y)], fill=(215, 230, 245), width=2)
        y += LINE_SPACING
        
    return img, draw

def get_fonts():
    f_title = ImageFont.truetype(font_bold, 54)
    f_h1 = ImageFont.truetype(font_bold, 42)
    f_h2 = ImageFont.truetype(font_bold, 36)
    f_body = ImageFont.truetype(font_regular, 32)
    f_body_b = ImageFont.truetype(font_bold, 32)
    f_code = ImageFont.truetype(font_bold, 28)
    f_small = ImageFont.truetype(font_regular, 26)
    return f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small

def draw_header(draw, title, bug_num, fonts):
    f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small = fonts
    draw.text((MARGIN_LEFT, 110), "Full-Stack Patch Exercise — Debugging & Root Cause Analysis", font=f_small, fill=INK_BLACK)
    draw.text((PAGE_WIDTH - MARGIN_RIGHT - 350, 110), "Date: 2026-10-07", font=f_small, fill=INK_BLACK)
    draw.text((MARGIN_LEFT, 150), f"BUG #{bug_num}: {title}", font=f_title, fill=INK_BLUE_DARK)
    draw.line([(MARGIN_LEFT, 215), (PAGE_WIDTH - MARGIN_RIGHT, 215)], fill=INK_BLUE_DARK, width=3)

# Page 1: SQL Precedence
def create_page_1():
    img, draw = draw_lined_background()
    fonts = get_fonts()
    f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small = fonts
    draw_header(draw, "SQL Boolean Operator Precedence Bug", 1, fonts)
    
    y = 250
    # 1. Location
    draw.text((MARGIN_LEFT, y), "1. WHERE THE BUG IS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• File: backend/src/main/java/com/internal/tasktracker/TaskRepository.java (Lines 14-16)", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Also in: db/queries/search_tasks.sql (Lines 10-13) & db/oracle/task_search_package.sql", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Layer: Database / Persistence / SQL Query Layer", font=f_body_b, fill=INK_BLUE)
    y += 70
    
    # 2. Discovery
    draw.text((MARGIN_LEFT, y), "2. HOW I DISCOVERED IT", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Step 1: Searched term 'api' in UI. Expected 6 active tasks, but saw 8 tasks returned.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 2: Found archived tasks #20 ('Decommission legacy...') & #21 ('Legacy API...') present!", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 3: Filtered by Status='DONE' with search 'Fix' -> OPEN/IN_PROGRESS tasks still showed up!", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 3. Root Cause
    draw.text((MARGIN_LEFT, y), "3. ROOT CAUSE ANALYSIS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• In SQL Standard, AND operator has higher precedence than OR operator.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Original unparenthesized query:", font=f_body, fill=INK_BLACK)
    y += 40
    
    # Box for original SQL
    draw.rectangle([(MARGIN_LEFT + 30, y), (PAGE_WIDTH - MARGIN_RIGHT - 20, y + 120)], fill=(255, 240, 240), outline=(220, 100, 100), width=2)
    draw.text((MARGIN_LEFT + 50, y + 15), "WHERE archived = FALSE AND LOWER(title) LIKE :term", font=f_code, fill=INK_RED)
    draw.text((MARGIN_LEFT + 50, y + 60), "   OR LOWER(description) LIKE :term AND (:status IS NULL OR status = :status)", font=f_code, fill=INK_RED)
    y += 140
    
    draw.text((MARGIN_LEFT + 30, y), "• SQL parser evaluates this as TWO separate branches:", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 60, y), "Branch A: (archived = FALSE AND LOWER(title) LIKE :term)", font=f_body_b, fill=INK_PURPLE)
    y += 40
    draw.text((MARGIN_LEFT + 60, y), "   -> If title matches, the status filter is completely BYPASSED!", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 60, y), "Branch B: (LOWER(description) LIKE :term AND (:status IS NULL OR status = :status))", font=f_body_b, fill=INK_PURPLE)
    y += 40
    draw.text((MARGIN_LEFT + 60, y), "   -> If description matches, archived = FALSE check is BYPASSED (leaks archived data)!", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 4. How Fixed & Approach
    draw.text((MARGIN_LEFT, y), "4. HOW I FIXED IT & WHY", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Added explicit parentheses around the OR search criteria:", font=f_body, fill=INK_BLACK)
    y += 40
    
    # Box for fixed SQL
    draw.rectangle([(MARGIN_LEFT + 30, y), (PAGE_WIDTH - MARGIN_RIGHT - 20, y + 160)], fill=(240, 255, 240), outline=(80, 180, 100), width=2)
    draw.text((MARGIN_LEFT + 50, y + 15), "SELECT * FROM tasks", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 50), "WHERE archived = FALSE", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 85), "  AND (LOWER(title) LIKE :term OR LOWER(description) LIKE :term)", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 120), "  AND (:status IS NULL OR status = :status) ORDER BY created_at DESC", font=f_code, fill=INK_GREEN)
    y += 180
    
    draw.text((MARGIN_LEFT + 30, y), "• Why this approach: It strictly enforces both archived=FALSE and status filter", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  across all text matches with zero overhead and no breaking schema changes.", font=f_body, fill=INK_BLACK)
    
    draw.text((PAGE_WIDTH - MARGIN_RIGHT - 420, PAGE_HEIGHT - 120), "Page 1 of 5  |  Verified with JUnit Tests", font=f_small, fill=INK_BLUE_DARK)
    return img

# Page 2: Backend Controller
def create_page_2():
    img, draw = draw_lined_background()
    fonts = get_fonts()
    f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small = fonts
    draw_header(draw, "Backend Latency, Enum Crash & Pagination Bounds", 2, fonts)
    
    y = 250
    # 1. Location
    draw.text((MARGIN_LEFT, y), "1. WHERE THE BUG IS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• File: backend/src/main/java/com/internal/tasktracker/TaskController.java", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Lines: 31-33 (enum parsing), 36-42 (Thread.sleep), 50-54 (subList pagination)", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Layer: Backend REST Controller / API Request Handling Layer", font=f_body_b, fill=INK_BLUE)
    y += 70
    
    # 2. Discovery
    draw.text((MARGIN_LEFT, y), "2. HOW I DISCOVERED IT", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Step 1: Noticed extreme 1000ms sluggishness in UI whenever typing 1-2 character search terms.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 2: Tested invalid status parameter curl /api/tasks?status=FOO -> crashed with HTTP 500.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 3: Tested negative/zero page curl /api/tasks?page=0 -> threw IndexOutOfBoundsException.", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 3. Root Cause
    draw.text((MARGIN_LEFT, y), "3. ROOT CAUSE ANALYSIS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Root Cause A: Thread.sleep(Math.max(0, 10 - query.length()) * 100L) blocked worker threads.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  Shorter queries waited 1000ms while longer queries finished in 0ms, causing race conditions.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Root Cause B: TaskStatus.valueOf(status.toUpperCase()) throws IllegalArgumentException", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  when given invalid status, uncaught -> Spring returns unhandled 500 Internal Server Error.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Root Cause C: int start = (page - 1) * pageSize -> for page=0, start = -10 (invalid index).", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 4. How Fixed & Approach
    draw.text((MARGIN_LEFT, y), "4. HOW I FIXED IT & WHY", font=f_h1, fill=INK_RED)
    y += 50
    
    draw.rectangle([(MARGIN_LEFT + 30, y), (PAGE_WIDTH - MARGIN_RIGHT - 20, y + 260)], fill=(240, 255, 240), outline=(80, 180, 100), width=2)
    draw.text((MARGIN_LEFT + 50, y + 15), "// 1. Safe Enum Parsing -> returns 400 Bad Request on invalid input", font=f_code, fill=INK_PURPLE)
    draw.text((MARGIN_LEFT + 50, y + 50), "if (status != null && !status.trim().isEmpty()) {", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 85), "    try { normalizedStatus = TaskStatus.valueOf(status.trim().toUpperCase()).name(); }", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 120), "    catch (IllegalArgumentException e) { return ResponseEntity.badRequest()...; } }", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 155), "// 2. Removed Thread.sleep completely", font=f_code, fill=INK_PURPLE)
    draw.text((MARGIN_LEFT + 50, y + 190), "// 3. Bounds Guard: int validPage = Math.max(1, page); int validSize = Math.max(1, pageSize);", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 225), "int start = (validPage - 1) * validSize; int end = Math.min(start + validSize, allResults.size());", font=f_code, fill=INK_GREEN)
    y += 280
    
    draw.text((MARGIN_LEFT + 30, y), "• Rationale: Eliminated artificial latency, hardened API against malformed inputs,", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  prevented 500 server crashes, and guaranteed non-negative subList offsets.", font=f_body, fill=INK_BLACK)
    
    draw.text((PAGE_WIDTH - MARGIN_RIGHT - 420, PAGE_HEIGHT - 120), "Page 2 of 5  |  Verified with JUnit Tests", font=f_small, fill=INK_BLUE_DARK)
    return img

# Page 3: Frontend Race Condition
def create_page_3():
    img, draw = draw_lined_background()
    fonts = get_fonts()
    f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small = fonts
    draw_header(draw, "Frontend Race Conditions & Stuck Loading State", 3, fonts)
    
    y = 250
    # 1. Location
    draw.text((MARGIN_LEFT, y), "1. WHERE THE BUG IS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• File: frontend/src/hooks/useTasks.js (Lines 10-22) & frontend/src/api.js", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Layer: Frontend Asynchronous State Management / React Hooks Layer", font=f_body_b, fill=INK_BLUE)
    y += 70
    
    # 2. Discovery
    draw.text((MARGIN_LEFT, y), "2. HOW I DISCOVERED IT", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Step 1: Typed fast into search bar (e.g. 'rate'). Results flickered erratically.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 2: Observed network tab: Request 1 ('r') returned AFTER Request 4 ('rate').", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 3: Stale 'r' results overwrote 'rate' results in state! Final UI showed wrong data.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 4: When API threw 400/500 error, UI was stuck in 'Loading tasks...' permanently.", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 3. Root Cause
    draw.text((MARGIN_LEFT, y), "3. ROOT CAUSE ANALYSIS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Out-of-order execution: In async JS, promise resolution order != dispatch order.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• useTasks had no AbortController or ignore flag to cancel/ignore stale requests.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Error handling flaw: .catch((err) => setError(err.message)) omitted setLoading(false).", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 4. How Fixed & Approach
    draw.text((MARGIN_LEFT, y), "4. HOW I FIXED IT & WHY", font=f_h1, fill=INK_RED)
    y += 50
    
    draw.rectangle([(MARGIN_LEFT + 30, y), (PAGE_WIDTH - MARGIN_RIGHT - 20, y + 330)], fill=(240, 255, 240), outline=(80, 180, 100), width=2)
    draw.text((MARGIN_LEFT + 50, y + 15), "useEffect(() => {", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 50), "  let ignore = false; const controller = new AbortController();", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 85), "  setLoading(true); setError(null);", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 120), "  fetchTasks({ query, status, page, pageSize, signal: controller.signal })", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 155), "    .then(data => { if (!ignore) { setTasks(data.items); setTotal(data.total); setLoading(false); }})", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 190), "    .catch(err => {", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 225), "      if (err.name === 'AbortError') return;", font=f_code, fill=INK_PURPLE)
    draw.text((MARGIN_LEFT + 50, y + 260), "      if (!ignore) { setError(err.message); setLoading(false); }});", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 295), "  return () => { ignore = true; controller.abort(); };", font=f_code, fill=INK_GREEN)
    y += 350
    
    draw.text((MARGIN_LEFT + 30, y), "• Rationale: Cancels in-flight stale network requests, prevents unmounted state updates,", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  resets errors cleanly on retry, and ensures loading spinner always terminates.", font=f_body, fill=INK_BLACK)
    
    draw.text((PAGE_WIDTH - MARGIN_RIGHT - 420, PAGE_HEIGHT - 120), "Page 3 of 5  |  Verified in Browser & Tests", font=f_small, fill=INK_BLUE_DARK)
    return img

# Page 4: Frontend Pagination Reset
def create_page_4():
    img, draw = draw_lined_background()
    fonts = get_fonts()
    f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small = fonts
    draw_header(draw, "Frontend Pagination Desynchronization on Filter", 4, fonts)
    
    y = 250
    # 1. Location
    draw.text((MARGIN_LEFT, y), "1. WHERE THE BUG IS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• File: frontend/src/App.jsx (Lines 8-26)", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Layer: Frontend Application State / UI Component Layer", font=f_body_b, fill=INK_BLUE)
    y += 70
    
    # 2. Discovery
    draw.text((MARGIN_LEFT, y), "2. HOW I DISCOVERED IT", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Step 1: Navigated to Page 3 of all tasks (tasks #21-30).", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 2: Typed 'rate limiting' into the search input (matching only 1 total task).", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 3: UI showed 'No tasks found.' with pagination label 'Page 3 of 1'!", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 4: Same issue occurred when changing StatusFilter dropdown on high page numbers.", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 3. Root Cause
    draw.text((MARGIN_LEFT, y), "3. ROOT CAUSE ANALYSIS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• The 'page' state was independent of 'query' and 'status' state.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• When query or status changed, page remained at its old value (e.g. 3).", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• The backend calculated start = (3 - 1) * 10 = 20. Since total results = 1,", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  subList returned empty items [], leading to a phantom empty state.", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 4. How Fixed & Approach
    draw.text((MARGIN_LEFT, y), "4. HOW I FIXED IT & WHY", font=f_h1, fill=INK_RED)
    y += 50
    
    draw.rectangle([(MARGIN_LEFT + 30, y), (PAGE_WIDTH - MARGIN_RIGHT - 20, y + 200)], fill=(240, 255, 240), outline=(80, 180, 100), width=2)
    draw.text((MARGIN_LEFT + 50, y + 15), "const handleQueryChange = (newQuery) => {", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 50), "  setQuery(newQuery);", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 85), "  setPage(1); // Reset to page 1 on new search", font=f_code, fill=INK_PURPLE)
    draw.text((MARGIN_LEFT + 50, y + 120), "};", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 155), "const handleStatusChange = (newStatus) => { setStatus(newStatus); setPage(1); };", font=f_code, fill=INK_GREEN)
    y += 220
    
    draw.text((MARGIN_LEFT + 30, y), "• Created dedicated handleQueryChange & handleStatusChange event handlers in App.jsx.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Rationale: Immediate, explicit reset on user interaction; zero side effects, no extra useEffects.", font=f_body, fill=INK_BLACK)
    
    draw.text((PAGE_WIDTH - MARGIN_RIGHT - 420, PAGE_HEIGHT - 120), "Page 4 of 5  |  Verified in Browser UI", font=f_small, fill=INK_BLUE_DARK)
    return img

# Page 5: Oracle PL/SQL Package Precedence & Offset
def create_page_5():
    img, draw = draw_lined_background()
    fonts = get_fonts()
    f_title, f_h1, f_h2, f_body, f_body_b, f_code, f_small = fonts
    draw_header(draw, "Oracle PL/SQL Package Precedence & Offset Validation", 5, fonts)
    
    y = 250
    # 1. Location
    draw.text((MARGIN_LEFT, y), "1. WHERE THE BUG IS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• File: db/oracle/task_search_package.sql (Lines 45-75)", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Layer: Oracle Database / Stored Procedure (PL/SQL Reference Artifact)", font=f_body_b, fill=INK_BLUE)
    y += 70
    
    # 2. Discovery
    draw.text((MARGIN_LEFT, y), "2. HOW I DISCOVERED IT", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• Step 1: Conducted full architectural audit of SQL artifacts across repository.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 2: Examined task_search_pkg body in task_search_package.sql.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 3: Spotted identical operator precedence flaw in both COUNT(*) and OPEN p_results cursor.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• Step 4: Spotted unprotected v_offset calculation when p_page < 1 or NULL.", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 3. Root Cause
    draw.text((MARGIN_LEFT, y), "3. ROOT CAUSE ANALYSIS", font=f_h1, fill=INK_RED)
    y += 50
    draw.text((MARGIN_LEFT + 30, y), "• In Oracle SQL, unparenthesized OR conditions cause archived tasks (archived = 1) to leak", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "  whenever description matches v_term, and bypasses p_status when title matches.", font=f_body, fill=INK_BLACK)
    y += 45
    draw.text((MARGIN_LEFT + 30, y), "• v_offset := (p_page - 1) * p_page_size yields negative numbers for page <= 0.", font=f_body, fill=INK_BLACK)
    y += 70
    
    # 4. How Fixed & Approach
    draw.text((MARGIN_LEFT, y), "4. HOW I FIXED IT & WHY", font=f_h1, fill=INK_RED)
    y += 50
    
    draw.rectangle([(MARGIN_LEFT + 30, y), (PAGE_WIDTH - MARGIN_RIGHT - 20, y + 250)], fill=(240, 255, 240), outline=(80, 180, 100), width=2)
    draw.text((MARGIN_LEFT + 50, y + 15), "-- 1. Safe Offset with GREATEST / NVL", font=f_code, fill=INK_PURPLE)
    draw.text((MARGIN_LEFT + 50, y + 50), "v_offset := (GREATEST(NVL(p_page, 1), 1) - 1) * GREATEST(NVL(p_page_size, 10), 1);", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 90), "-- 2. Enforce Operator Precedence in COUNT and Cursor", font=f_code, fill=INK_PURPLE)
    draw.text((MARGIN_LEFT + 50, y + 125), "WHERE archived = 0", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 160), "  AND (LOWER(title) LIKE v_term OR LOWER(description) LIKE v_term)", font=f_code, fill=INK_GREEN)
    draw.text((MARGIN_LEFT + 50, y + 195), "  AND (p_status IS NULL OR status = p_status)", font=f_code, fill=INK_GREEN)
    y += 270
    
    draw.text((MARGIN_LEFT + 30, y), "• Rationale: Ensures production parity between H2 Spring Data query and Oracle PL/SQL.", font=f_body, fill=INK_BLACK)
    
    draw.text((PAGE_WIDTH - MARGIN_RIGHT - 420, PAGE_HEIGHT - 120), "Page 5 of 5  |  Complete Architecture Parity", font=f_small, fill=INK_BLUE_DARK)
    return img

print("Generating refined handwritten pages...")
pages = [
    ("bug1_sql_operator_precedence.png", create_page_1()),
    ("bug2_backend_controller_fixes.png", create_page_2()),
    ("bug3_frontend_race_conditions.png", create_page_3()),
    ("bug4_frontend_pagination_reset.png", create_page_4()),
    ("bug5_oracle_plsql_precedence.png", create_page_5()),
]

image_paths = []
for filename, img in pages:
    filepath = os.path.join(handwritten_dir, filename)
    img.save(filepath, "PNG", dpi=(300, 300))
    image_paths.append(img)
    print(f"Saved: {filepath}")

# Save combined Handwritten PDF
pdf_path_hw = os.path.join(base_dir, "Handwritten_Bug_Explanations.pdf")
pdf_path_hw2 = os.path.join(handwritten_dir, "all_handwritten_notes.pdf")
image_paths[0].save(pdf_path_hw, "PDF", resolution=300.0, save_all=True, append_images=image_paths[1:])
image_paths[0].save(pdf_path_hw2, "PDF", resolution=300.0, save_all=True, append_images=image_paths[1:])
print(f"Saved combined handwritten PDF: {pdf_path_hw}")

# -------------------------------------------------------------
# 2. GENERATE COMPREHENSIVE INTERVIEW FOLLOW-UP GUIDE PDF
# -------------------------------------------------------------

interview_pdf_path = os.path.join(base_dir, "Interview_Followup_Guide.pdf")

doc = SimpleDocTemplate(
    interview_pdf_path,
    pagesize=letter,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#1E3A8A'),
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#4B5563'),
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'SectionH1',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=12,
    leading=15,
    textColor=colors.HexColor('#1E3A8A'),
    spaceBefore=10,
    spaceAfter=4,
    keepWithNext=True
)

h2_style = ParagraphStyle(
    'SectionH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=13,
    textColor=colors.HexColor('#1F2937'),
    spaceBefore=6,
    spaceAfter=3,
    keepWithNext=True
)

body_style = ParagraphStyle(
    'BodyDark',
    parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=12,
    textColor=colors.HexColor('#1F2937'),
    spaceAfter=4
)

bullet_style = ParagraphStyle(
    'BulletText',
    parent=body_style,
    leftIndent=12,
    firstLineIndent=-8,
    spaceAfter=3
)

code_style = ParagraphStyle(
    'CodeSnippet',
    parent=styles['Code'],
    fontName='Courier',
    fontSize=8,
    leading=10,
    textColor=colors.HexColor('#111827'),
    backColor=colors.HexColor('#F3F4F6'),
    borderPadding=4,
    spaceBefore=3,
    spaceAfter=4
)

table_header_style = ParagraphStyle(
    'TableHeader',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.white
)

table_cell_style = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor('#1F2937')
)

story = []

# Title & Metadata Banner
story.append(Paragraph("Full-Stack Patch Exercise — Interview Preparation & Architecture Guide", title_style))
story.append(Paragraph("Complete Technical Walkthrough, Tradeoff Analysis, Bug Explanations & Strategic Defense", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=8))

# Summary Table of Patched Issues
summary_data = [
    [Paragraph("Bug / Issue", table_header_style), Paragraph("Layer & File", table_header_style), Paragraph("Root Cause", table_header_style), Paragraph("Applied Patch Rationale", table_header_style)],
    [Paragraph("1. SQL Boolean Precedence", table_cell_style), Paragraph("Persistence / SQL<br/><code>TaskRepository.java</code><br/><code>search_tasks.sql</code>", table_cell_style), Paragraph("Unparenthesized <code>OR</code> caused <code>AND</code> to bind tighter, leaking archived items & ignoring status filter.", table_cell_style), Paragraph("Added parentheses around title/description conditions. Enforces strict filtering with 0 overhead.", table_cell_style)],
    [Paragraph("2. Artificial Latency & Crashes", table_cell_style), Paragraph("Backend Controller<br/><code>TaskController.java</code>", table_cell_style), Paragraph("<code>Thread.sleep</code> (up to 1s), uncaught enum <code>IllegalArgumentException</code>, negative page index.", table_cell_style), Paragraph("Removed sleep; caught enum exception returning 400 Bad Request; bounded page & pageSize >= 1.", table_cell_style)],
    [Paragraph("3. Race Conditions & Error Lock", table_cell_style), Paragraph("Frontend Hook<br/><code>useTasks.js</code> / <code>api.js</code>", table_cell_style), Paragraph("Async requests resolved out-of-order, overwriting UI with stale data. Error catch lacked <code>setLoading(false)</code>.", table_cell_style), Paragraph("Added <code>AbortController</code> and ignore flag to cancel stale fetches; reset error/loading states properly.", table_cell_style)],
    [Paragraph("4. Pagination Desync", table_cell_style), Paragraph("Frontend UI State<br/><code>App.jsx</code>", table_cell_style), Paragraph("Filtering or searching while on high page numbers (e.g. Page 3) retained stale <code>page</code> state.", table_cell_style), Paragraph("Reset <code>page = 1</code> in <code>handleQueryChange</code> and <code>handleStatusChange</code> handlers.", table_cell_style)],
    [Paragraph("5. Oracle PL/SQL Artifact", table_cell_style), Paragraph("SQL Reference<br/><code>task_search_pkg</code>", table_cell_style), Paragraph("Identical operator precedence bug in <code>COUNT</code> & cursor queries; unvalidated offset on <code>p_page &lt; 1</code>.", table_cell_style), Paragraph("Added parentheses to queries; protected offset with <code>GREATEST(NVL(p_page, 1), 1)</code>.", table_cell_style)],
]

t = Table(summary_data, colWidths=[1.3*inch, 1.4*inch, 2.3*inch, 2.4*inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(t)
story.append(Spacer(1, 8))

# Section 1: Prioritization
story.append(Paragraph("1. What You Fixed First and Why You Prioritized It", h1_style))
story.append(Paragraph(
    "<b>Priority 1 — Data Integrity & Query Correctness (SQL Operator Precedence):</b><br/>"
    "In any multi-tier architecture, data correctness at the persistence boundary is paramount. The unparenthesized SQL query in <code>TaskRepository.java</code> was a critical functional bug: "
    "archived tasks leaked into search results when description matched, and status filters were completely bypassed when title matched. Fixing this first was essential because all upstream layers depend on accurate data.",
    body_style
))
story.append(Paragraph(
    "<b>Priority 2 — Backend Robustness & Performance (Artificial Sleep & 500 Crashes):</b><br/>"
    "Next, I targeted <code>TaskController.java</code> to remove the artificial 1000ms <code>Thread.sleep</code> (which degraded throughput and amplified UI race conditions) "
    "and hardened input handling (preventing 500 server crashes on invalid enum status by returning 400 Bad Request, and preventing <code>IndexOutOfBoundsException</code> on page &lt;= 0).",
    body_style
))
story.append(Paragraph(
    "<b>Priority 3 — Frontend Asynchronous Reliability (Race Conditions & Pagination Sync):</b><br/>"
    "Finally, I resolved frontend race conditions in <code>useTasks.js</code> using <code>AbortController</code> to prevent stale responses from overriding newer search results, "
    "fixed the stuck loading spinner bug on error, and ensured <code>App.jsx</code> resets pagination to page 1 whenever filters change.",
    body_style
))

# Section 2: Tradeoffs & What Was Not Changed
story.append(Paragraph("2. What You Chose Not to Change and Why", h1_style))
story.append(Paragraph("Adhering strictly to the assignment's rule ('a small, high-quality diff beats a large rewrite'), I deliberately avoided the following:", body_style))
story.append(Paragraph("• <b>In-Memory Slicing vs Spring Data Pageable:</b> Transitioning to database-level pagination (<code>Pageable</code>) would require altering repository method signatures and query interfaces across the backend. For the current dataset, keeping <code>subList</code> with strict bounds checking was a safe, surgical fix.", bullet_style))
story.append(Paragraph("• <b>External Debounce Libraries:</b> Rather than adding Lodash (increasing bundle size and introducing typing lag), pairing native input events with React <code>AbortController</code> cleanly and instantly cancels obsolete in-flight requests.", bullet_style))
story.append(Paragraph("• <b>UI/CSS Framework Redesign:</b> The table and filter controls fulfill all functional requirements. Adding styling frameworks or rewriting layout would add noise without engineering value.", bullet_style))

# Section 3: Subtle Issues
story.append(Paragraph("3. Subtle Issues Found or Suspected", h1_style))
story.append(Paragraph("• <b>LIKE Wildcard Escaping:</b> Special characters like <code>%</code> and <code>_</code> in user input are passed unescaped into SQL <code>LIKE :term</code>, which can trigger broad pattern matches.", bullet_style))
story.append(Paragraph("• <b>Status Enum Sensitivity:</b> Calling <code>valueOf</code> directly without case-normalization or error handling produced unhandled 500 errors instead of client-friendly 400 responses.", bullet_style))
story.append(Paragraph("• <b>Silent Error Lock:</b> In <code>useTasks.js</code>, omitting <code>setLoading(false)</code> in <code>.catch()</code> caused the loading message to persist permanently on network failures.", bullet_style))
story.append(Paragraph("• <b>Phantom Empty Tables:</b> Entering a narrow search term while on Page 3 produced an empty table ('Page 3 of 1') because pagination state was not reset on filter changes.", bullet_style))

# Section 4: Future Risks
story.append(Paragraph("4. Future Risks Noticed in the Codebase", h1_style))
story.append(Paragraph("• <b>Database Full-Table Scans:</b> Wildcard queries (<code>LIKE %term%</code>) bypass standard B-Tree indexes, requiring full sequential scans that will degrade as rows reach 100k+.", bullet_style))
story.append(Paragraph("• <b>JVM Heap Pressure:</b> Loading entire datasets into memory before calling <code>subList</code> will cause garbage collection spikes and eventual <code>OutOfMemoryError</code> under high concurrency.", bullet_style))
story.append(Paragraph("• <b>Security & CORS Policy:</b> <code>@CrossOrigin(origins = 'http://localhost:5173')</code> lacks CSRF tokens, rate limiting, and authentication/authorization controls.", bullet_style))
story.append(Paragraph("• <b>Unstructured Logging:</b> Reliance on <code>System.out.println</code> rather than SLF4J structured logging hinders production telemetry and log aggregation.", bullet_style))

# Section 5: AI Tools Usage
story.append(Paragraph("5. AI/Tools Usage — Where Suggestions Were Accepted vs Overridden", h1_style))
story.append(Paragraph(
    "• <b>Where Accepted:</b> Used AI assistant to quickly trace multi-layer interactions, verify SQL operator precedence semantics across database dialects, draft <code>AbortController</code> cleanup boilerplate, and generate comprehensive JUnit 5 / MockMvc integration tests.<br/>"
    "• <b>Where Overridden:</b> Rejected AI proposals to completely rewrite the JPA repository with Spring Data <code>Pageable</code> and install third-party npm packages (e.g. <code>lodash.debounce</code>). Maintained strict focus on a minimal, zero-dependency patch.",
    body_style
))

# Section 6: Future Approaches With More Time
story.append(Paragraph("6. How You Would Approach the Issues Differently With More Time", h1_style))
story.append(Paragraph("1. <b>Database-Level Pagination & Full-Text Search:</b> Implement Spring Data <code>Pageable</code> (<code>LIMIT / OFFSET</code>) and integrate PostgreSQL <code>pg_trgm</code> or Elasticsearch for sub-millisecond fuzzy search.", bullet_style))
story.append(Paragraph("2. <b>Security & Multi-Tenancy:</b> Add Spring Security with JWT/OAuth2 authentication, RBAC authorization, and user-level rate limiting.", bullet_style))
story.append(Paragraph("3. <b>Frontend UX & Routing:</b> Add URL query parameter synchronization (e.g. <code>/tasks?q=api&page=2</code> for deep linking) and React 18 <code>useDeferredValue</code>.", bullet_style))
story.append(Paragraph("4. <b>Automated End-to-End Testing & CI/CD:</b> Implement Playwright E2E suites and Flyway database migrations.", bullet_style))

# Build PDF
doc.build(story)
print(f"Saved Interview Follow-up Guide PDF: {interview_pdf_path}")

