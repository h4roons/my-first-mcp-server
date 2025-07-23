from mcp.server.fastmcp import FastMCP
from typing import List, Literal
from datetime import datetime, timedelta
from collections import defaultdict

# In-memory mock database
employee_leaves = {
    "E001": {
        "balance": {"casual": 10, "sick": 5, "earned": 3},
        "history": [{"date": "2024-12-25", "type": "casual"}]
    },
    "E002": {
        "balance": {"casual": 12, "sick": 4, "earned": 4},
        "history": []
    }
}

# Mock public holidays
public_holidays = ["2025-01-01", "2025-03-23", "2025-05-01", "2025-08-14"]

# Pending leave requests for manager approval
pending_requests = []

# Create MCP server
mcp = FastMCP("SmartHR")

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        balance_report = ', '.join([f"{k}: {v}" for k, v in data['balance'].items()])
        return f"📟 {employee_id} has the following leave balances: {balance_report}"
    return "🚫 Employee ID not found."

@mcp.tool()
def request_leave(employee_id: str, leave_dates: List[str], leave_type: Literal['casual', 'sick', 'earned']) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    requested_days = len(leave_dates)
    if employee_leaves[employee_id]['balance'].get(leave_type, 0) < requested_days:
        return f"⚠️ Not enough {leave_type} leaves available."

    if any(date in public_holidays for date in leave_dates):
        return f"🗕️ Some requested dates are public holidays. Try other dates."

    pending_requests.append({"id": employee_id, "dates": leave_dates, "type": leave_type})
    return f"📨 Leave request for {requested_days} {leave_type} day(s) sent for approval."

@mcp.tool()
def approve_leave(manager_id: str, employee_id: str) -> str:
    approved = [r for r in pending_requests if r["id"] == employee_id]
    if not approved:
        return "📭 No pending requests."

    response_msgs = []
    for req in approved:
        leave_type = req['type']
        dates = req['dates']
        employee_leaves[employee_id]['balance'][leave_type] -= len(dates)
        for d in dates:
            employee_leaves[employee_id]['history'].append({"date": d, "type": leave_type})
        pending_requests.remove(req)
        response_msgs.append(f"✅ Approved {len(dates)} {leave_type} day(s) for {employee_id}.")

    return '\n'.join(response_msgs)

@mcp.tool()
def cancel_leave(employee_id: str, cancel_dates: List[str]) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    history = employee_leaves[employee_id]["history"]
    cancelled = [entry for entry in history if entry["date"] in cancel_dates]

    if not cancelled:
        return "⚠️ None of the provided dates were found in leave history."

    for entry in cancelled:
        history.remove(entry)
        employee_leaves[employee_id]['balance'][entry["type"]] += 1

    return f"✅ {len(cancelled)} leave(s) cancelled. Updated balances applied."

@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    data = employee_leaves.get(employee_id)
    if data:
        if not data["history"]:
            return f"📜 {employee_id} has not taken any leave yet."
        sorted_history = sorted(data["history"], key=lambda x: x["date"])
        return "\n".join([f"🗕️ {entry['date']} ({entry['type']})" for entry in sorted_history])
    return "🚫 Employee ID not found."

@mcp.tool()
def suggest_next_leave_date(employee_id: str) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    taken = set(entry["date"] for entry in employee_leaves[employee_id]["history"] + [{"date": d} for d in public_holidays])
    next_date = datetime.today()

    while True:
        next_date += timedelta(days=1)
        date_str = next_date.strftime("%Y-%m-%d")
        if date_str not in taken and next_date.weekday() < 5:
            return f"📆 Next available leave day for {employee_id} could be: {date_str}"

@mcp.tool()
def monthly_leave_summary(employee_id: str) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."

    summary = defaultdict(int)
    for entry in employee_leaves[employee_id]["history"]:
        month = datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%B %Y")
        summary[month] += 1

    if not summary:
        return f"📊 No leave summary for {employee_id}."

    return "\n".join([f"📌 {month}: {count} day(s)" for month, count in summary.items()])

@mcp.tool()
def upcoming_leaves(employee_id: str) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."
    today = datetime.today().strftime("%Y-%m-%d")
    upcoming = [e["date"] for e in employee_leaves[employee_id]["history"] if e["date"] > today]
    return f"⏰ Upcoming leaves: {', '.join(upcoming)}" if upcoming else "📭 No upcoming leaves."

@mcp.tool()
def leave_utilization(employee_id: str) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."
    taken = len(employee_leaves[employee_id]["history"])
    total_allocated = sum(employee_leaves[employee_id]["balance"].values()) + taken
    return f"📊 {employee_id} used {taken} out of {total_allocated} total leave(s) this year."

@mcp.tool()
def slack_leave_summary(employee_id: str) -> str:
    if employee_id not in employee_leaves:
        return "🚫 Employee ID not found."
    history = employee_leaves[employee_id]["history"]
    if not history:
        return f"📒 No leave history for {employee_id}."
    return f"*{employee_id}'s Leave History:*\n• " + "\n• ".join([f"{e['date']} ({e['type']})" for e in history])

@mcp.tool()
def suggest_long_weekend() -> str:
    suggestions = []
    for holiday in public_holidays:
        dt = datetime.strptime(holiday, "%Y-%m-%d")
        if dt.weekday() == 1:  # Tuesday
            suggestions.append(f"Take Monday off before {holiday}.")
        elif dt.weekday() == 3:  # Thursday
            suggestions.append(f"Take Friday off after {holiday}.")
    return "📌 Long weekend suggestions:\n" + "\n".join(suggestions) if suggestions else "ℹ️ No long weekend opportunities found."

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"👋 Hello {name}, welcome to SmartHR! Let me know how I can help with your leave requests today."

if __name__ == "__main__":
    mcp.run()
