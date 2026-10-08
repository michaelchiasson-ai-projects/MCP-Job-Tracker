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

# Start the server when this file is run.
if __name__ == "__main__":
        mcp.run(transport="stdio")