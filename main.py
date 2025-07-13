from mcp.server.fastmcp import FastMCP
from typing import List
from datetime import datetime
from collections import defaultdict

# In-memory mock database
employee_leaves = {
    "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
    "E002": {"balance": 20, "history": []}
}

# Mock public holidays
public_holidays = ["2025-01-01", "2025-03-23", "2025-05-01", "2025-08-14"]

# Create MCP server
mcp = FastMCP("SmartHR")

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        return f"🧾 {employee_id} has {data['balance']} leave day(s) left."
    return "🚫 Employee ID not found."

# Tool: Apply for Leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return f"⚠️ You requested {requested_days} day(s), but only {available_balance} are available."

    # Check for holidays
    holidays = [date for date in leave_dates if date in public_holidays]
    if holidays:
        return f"📅 Some requested dates are public holidays: {', '.join(holidays)}. Try other dates."

    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    return f"✅ {requested_days} day(s) leave approved for {employee_id}. New balance: {employee_leaves[employee_id]['balance']}."

# Tool: Cancel Leave
@mcp.tool()
def cancel_leave(employee_id: str, cancel_dates: List[str]) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    history = employee_leaves[employee_id]["history"]
    cancelled = [date for date in cancel_dates if date in history]

    if not cancelled:
        return "⚠️ None of the provided dates were found in leave history."

    for date in cancelled:
        history.remove(date)
        employee_leaves[employee_id]["balance"] += 1

    return f"✅ {len(cancelled)} leave(s) cancelled. Updated balance: {employee_leaves[employee_id]['balance']}."

# Tool: Get Leave History
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        if not data["history"]:
            return f"📜 {employee_id} has not taken any leave yet."
        return f"📅 Leave history for {employee_id}: {', '.join(sorted(data['history']))}"
    return "🚫 Employee ID not found."

# Tool: Suggest Next Available Leave Date
@mcp.tool()
def suggest_next_leave_date(employee_id: str) -> str:
    from datetime import timedelta
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    taken = set(employee_leaves[employee_id]["history"] + public_holidays)
    next_date = datetime.today()

    while True:
        next_date += timedelta(days=1)
        date_str = next_date.strftime("%Y-%m-%d")
        if date_str not in taken and next_date.weekday() < 5:  # Avoid weekends
            return f"📆 Next available leave day for {employee_id} could be: {date_str}"

# Tool: Monthly Leave Summary
@mcp.tool()
def monthly_leave_summary(employee_id: str) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    summary = defaultdict(int)
    for date in employee_leaves[employee_id]["history"]:
        month = datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")
        summary[month] += 1

    if not summary:
        return f"📊 No leave summary for {employee_id}."

    return "\n".join([f"📌 {month}: {count} day(s)" for month, count in summary.items()])

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"👋 Hello {name}, welcome to SmartHR! Let me know how I can help with your leave requests today."

if __name__ == "__main__":
    mcp.run()
