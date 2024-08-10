# External Permission System Example

This Code Example shows how one could implement a secondary permission system decoupled from discord roles.

## Functionality

- 4 Internal Roles (User, Moderator, Administrator, Owner)
- Assignable through command
  - Hierarchy is in place, for example: Only Owner can assign Admin, but Admin cannot assign Owner or Admin.
  - The assigning hierarchy is dynamic.
- Decorator checks (see check.py)
- Automatically setting the Owner of each Guild the Bot is in
- A basic-moderation cog to showcase the system in action
