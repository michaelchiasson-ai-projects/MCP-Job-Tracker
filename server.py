from mcp.server.mcpserver import MCPServer
import storage

# This is the MCP server. The name is how Claude Desktop will identify it.
mcp = MCPServer("job-tracker")

# Each @mcp.tool() decorator turns a function into a tool Claude can call.
# The docstring is important: Claude reads it to understand WHEN and HOW
# to use the tool, so it doubles as instructions to the model.

@mcp.tool()
def add_application(
    company: str,
    role: str,
    status: str = "applied",
    work_arrangement: str = "",
    notes: str = "",
) -> dict:
    """Add a new job application to the tracker.

    Use this when the user says they applied to a job or wants to record one.

    Args:
        company: The hiring company's name.
        role: The job title.
        status: Application status (applied, interviewing, rejected, offer). Defaults to applied.
        work_arrangement: Remote, hybrid, onsite, or unspecified.
        notes: Any extra notes about the application.
    """
    return storage.add_application(company, role, status, work_arrangement, notes)

@mcp.tool()
def list_applications() -> list:
    """List all job applications currently in the tracker.

    Use this when the user wants to see their applications, check their
    job search status, or asks what they've applied to.
    """
    return storage.list_applications()

@mcp.tool()
def update_status(app_id: int, new_status: str) -> dict:
    """Update the status of an existing job application.

    Use this when the user reports progress on an application, such as getting
    an interview, an offer, or a rejection.

    Args:
        app_id: The id of the application to update.
        new_status: The new status (applied, interviewing, rejected, offer).
    """
    result = storage.update_status(app_id, new_status)
    if result is None:
        return {"error": f"No application found with id {app_id}."}
    return result

@mcp.tool()
def delete_application(app_id: int) -> dict:
    """Delete a job application from the tracker.

    Use this when the user wants to remove an application, for example a
    duplicate or one they no longer want to track.

    Args:
        app_id: The id of the application to remove.
    """
    result = storage.delete_application(app_id)
    if result is None:
        return {"error": f"No application found with id {app_id}."}
    return {"deleted": result}

@mcp.prompt(title="Weekly application review")
def weekly_review() -> str:
    """Review all job applications: surface action items, follow up on top prospects, and flag applications with no update in over a week."""
    return (
        "Please give me a weekly review of my job applications. "
        "First, call list_applications to get the current state. Then produce a short, "
        "organized review covering:\n\n"
        "1. Action items: any applications whose notes or status indicate something I need "
        "to do (a flag to clarify, a follow-up owed, a pending task). List each with the "
        "company, the action, and the application id.\n\n"
        "2. Top prospects: the applications that look strongest based on their notes (strong "
        "fit, high compensation, roles I seem excited about), each with a one-line suggested "
        "follow-up.\n\n"
        "3. Stale applications: any application whose most recent activity (its last_updated "
        "date if present, otherwise its date_applied) is more than 7 days before today. For "
        "each, note how long it has been and suggest I check its status or send a follow-up.\n\n"
        "Keep it concise and scannable. If the tracker is empty, say so."
    )
# Start the server when this file is run.
if __name__ == "__main__":
        mcp.run(transport="stdio")